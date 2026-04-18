"""Leeroy Chainkins — bot status dashboard + start/stop control."""
from __future__ import annotations

import json
import logging
import os
import re
import shlex
import signal
import sqlite3
import subprocess
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import psutil
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

log = logging.getLogger("watcher")

REPO_ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = REPO_ROOT / "static"
CONFIG_PATH = REPO_ROOT / "deploy" / "bot_commands.json"
ACTION_LOG = REPO_ROOT / "actions.log"

HOME = Path(os.path.expanduser("~"))

# --- Detection ---------------------------------------------------------------

SCRIPT_PATTERNS: dict[str, re.Pattern[str]] = {
    "memeorator.py": re.compile(r"\bmemeorator\.py\b"),
    "wallet_follower.py": re.compile(r"\bwallet_follower\.py\b"),
    "graduator.py": re.compile(r"\bgraduator\.py\b"),
    "sniper.py": re.compile(r"\bsniper\.py\b"),
    "statalyzer.py": re.compile(r"\bstatalyzer\.py\b"),
}

PROJECT_BY_SCRIPT = {
    "memeorator.py": "memeorator",
    "wallet_follower.py": "memeorator",
    "graduator.py": "memeorator",
    "sniper.py": "memeorator",
    "statalyzer.py": "statalyzer",
}


@dataclass
class BotRole:
    """A registered bot (from bot_commands.json) that we know how to start/stop."""
    key: str
    display_name: str
    project: str
    script: str
    name_pattern: re.Pattern[str]
    cwd: Path
    start_command: str
    start_log: Path | None


def _load_roles() -> list[BotRole]:
    if not CONFIG_PATH.exists():
        return []
    try:
        data = json.loads(CONFIG_PATH.read_text())
    except json.JSONDecodeError as e:
        log.error("bad bot_commands.json: %s", e)
        return []
    roles: list[BotRole] = []
    for entry in data:
        try:
            roles.append(BotRole(
                key=entry["key"],
                display_name=entry.get("display_name", entry["key"]),
                project=entry["project"],
                script=entry["script"],
                name_pattern=re.compile(entry["name_pattern"]),
                cwd=Path(entry["cwd"]),
                start_command=entry["start_command"],
                start_log=Path(entry["start_log"]) if entry.get("start_log") else None,
            ))
        except (KeyError, re.error) as e:
            log.error("skipping bad role entry %s: %s", entry, e)
    return roles


# --- Cmdline parsing ---------------------------------------------------------

def _parse_flag(tokens: list[str], flag: str) -> str | None:
    for i, tok in enumerate(tokens):
        if tok == flag and i + 1 < len(tokens):
            return tokens[i + 1]
        if tok.startswith(flag + "="):
            return tok.split("=", 1)[1]
    return None


def _infer_mode(tokens: list[str]) -> str:
    if "--live" in tokens and "--confirm-live" in tokens:
        return "LIVE"
    if "--dry-run" in tokens:
        return "DRY-RUN"
    if "-e" in tokens:
        idx = tokens.index("-e")
        if idx + 1 < len(tokens) and tokens[idx + 1] == "live":
            return "LIVE"
    return "UNKNOWN"


# --- DB + log reading (always read-only) ------------------------------------

def _safe_open_db(db_path: Path) -> sqlite3.Connection | None:
    if not db_path.exists():
        return None
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=2.0)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error:
        return None


def _positions_summary(db_path: Path) -> dict[str, Any] | None:
    conn = _safe_open_db(db_path)
    if conn is None:
        return None
    try:
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        if "positions" not in tables:
            return None
        open_n = conn.execute(
            "SELECT COUNT(*) FROM positions WHERE status='open'"
        ).fetchone()[0]
        closed_n = conn.execute(
            "SELECT COUNT(*) FROM positions WHERE status!='open'"
        ).fetchone()[0]
        pnl = conn.execute(
            "SELECT COALESCE(SUM(realized_pnl), 0) FROM positions "
            "WHERE realized_pnl IS NOT NULL"
        ).fetchone()[0]
        last_entry = conn.execute("SELECT MAX(entry_time) FROM positions").fetchone()[0]
        return {
            "open": int(open_n),
            "closed": int(closed_n),
            "realized_pnl": round(float(pnl), 6),
            "last_entry_time": last_entry,
        }
    except sqlite3.Error as e:
        return {"error": str(e)}
    finally:
        conn.close()


def _tail_log(path: Path, n_lines: int = 25, max_bytes: int = 32_768) -> list[str]:
    if not path.exists() or not path.is_file():
        return []
    try:
        size = path.stat().st_size
        with path.open("rb") as f:
            if size > max_bytes:
                f.seek(-max_bytes, os.SEEK_END)
                f.readline()
            data = f.read()
        return data.decode("utf-8", errors="replace").splitlines()[-n_lines:]
    except OSError:
        return []


def _guess_log(cwd: Path, db_path: Path | None, experiment: str | None) -> Path | None:
    candidates: list[Path] = []
    if db_path is not None:
        candidates += [
            db_path.with_suffix(".log"),
            cwd / f"{db_path.stem}.log",
            cwd / "logs" / f"{db_path.stem}.log",
        ]
    if experiment:
        candidates += [cwd / f"{experiment}.log", cwd / "logs" / f"{experiment}.log"]
    candidates.append(cwd / "live.log")
    for c in candidates:
        if c.exists() and c.is_file():
            return c
    return None


def _process_cwd(proc: psutil.Process) -> Path:
    try:
        return Path(proc.cwd())
    except (psutil.Error, OSError):
        return HOME


# --- SOL price (cached, free CoinGecko endpoint) ----------------------------

_SOL_PRICE_CACHE: dict[str, float] = {"ts": 0.0, "usd": 0.0}
_SOL_PRICE_TTL_S = 60.0

def _sol_usd_price() -> float | None:
    now = time.time()
    if _SOL_PRICE_CACHE["usd"] > 0 and (now - _SOL_PRICE_CACHE["ts"]) < _SOL_PRICE_TTL_S:
        return _SOL_PRICE_CACHE["usd"]
    url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "leeroy-chainkins/1.0"})
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        usd = float(data["solana"]["usd"])
        if usd <= 0:
            raise ValueError("non-positive price")
        _SOL_PRICE_CACHE["usd"] = usd
        _SOL_PRICE_CACHE["ts"] = now
        return usd
    except (urllib.error.URLError, OSError, ValueError, KeyError, json.JSONDecodeError) as e:
        log.warning("sol price fetch failed: %s", e)
        # Fall back to last known price if we have one, otherwise None.
        return _SOL_PRICE_CACHE["usd"] or None


def _wallet_summary(db_path: Path, sol_price: float | None) -> dict[str, Any] | None:
    """Return {sol, usd, source, ts} from whichever snapshot table the DB has."""
    conn = _safe_open_db(db_path)
    if conn is None:
        return None
    try:
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        # Memeorator-style: native SOL balance
        if "snapshots" in tables:
            row = conn.execute(
                "SELECT timestamp, portfolio_value_sol FROM snapshots "
                "WHERE portfolio_value_sol IS NOT NULL "
                "ORDER BY timestamp DESC LIMIT 1"
            ).fetchone()
            if row and row["portfolio_value_sol"] is not None:
                sol = float(row["portfolio_value_sol"])
                usd = sol * sol_price if sol_price else None
                return {"sol": sol, "usd": usd, "source": "sol", "ts": float(row["timestamp"])}
        # Statalyzer-style: native USD value
        if "portfolio_snapshots" in tables:
            row = conn.execute(
                "SELECT timestamp, total_value FROM portfolio_snapshots "
                "ORDER BY timestamp DESC LIMIT 1"
            ).fetchone()
            if row and row["total_value"] is not None:
                usd = float(row["total_value"])
                sol = usd / sol_price if sol_price else None
                return {"sol": sol, "usd": usd, "source": "usd", "ts": float(row["timestamp"])}
        return None
    except sqlite3.Error as e:
        return {"error": str(e)}
    finally:
        conn.close()


# --- Building bot rows -------------------------------------------------------

def _describe_running(proc: psutil.Process, script: str, sol_price: float | None = None) -> dict[str, Any] | None:
    try:
        cmdline = proc.cmdline()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None
    if not cmdline:
        return None

    first = os.path.basename(cmdline[0])
    if not first.startswith("python"):
        return None
    if any(tok.endswith("pgrep") or tok == "grep" for tok in cmdline):
        return None

    cwd = _process_cwd(proc)
    db_value = _parse_flag(cmdline, "--db")
    db_path = (cwd / db_value) if db_value and not os.path.isabs(db_value) else (Path(db_value) if db_value else None)
    experiment = _parse_flag(cmdline, "--experiment")
    name = experiment or (db_path.stem if db_path else script)
    mode = _infer_mode(cmdline)

    try:
        with proc.oneshot():
            cpu = proc.cpu_percent(interval=None)
            mem_mb = proc.memory_info().rss / (1024 * 1024)
            create_time = proc.create_time()
    except psutil.Error:
        return None

    positions = _positions_summary(db_path) if db_path else None
    wallet = _wallet_summary(db_path, sol_price) if db_path else None
    log_path = _guess_log(cwd, db_path, experiment)
    log_tail = _tail_log(log_path) if log_path else []

    return {
        "pid": proc.pid,
        "running": True,
        "project": PROJECT_BY_SCRIPT.get(script, "?"),
        "script": script,
        "name": name,
        "experiment": experiment,
        "mode": mode,
        "cmdline": shlex.join(cmdline),
        "cwd": str(cwd),
        "db_path": str(db_path) if db_path else None,
        "log_path": str(log_path) if log_path else None,
        "log_tail": log_tail,
        "uptime_s": int(max(0.0, time.time() - create_time)),
        "cpu_pct": round(cpu, 1),
        "mem_mb": round(mem_mb, 1),
        "positions": positions,
        "wallet": wallet,
    }


def _scan_running(sol_price: float | None = None) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for proc in psutil.process_iter(["pid"]):
        try:
            joined = " ".join(proc.cmdline())
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        script = next((s for s, p in SCRIPT_PATTERNS.items() if p.search(joined)), None)
        if script is None:
            continue
        row = _describe_running(proc, script, sol_price)
        if row is not None:
            out.append(row)
    return out


def _match_role(row: dict[str, Any], roles: list[BotRole]) -> BotRole | None:
    for r in roles:
        if r.project == row["project"] and r.script == row["script"] and r.name_pattern.search(row["name"]):
            return r
    return None


def _role_stub(role: BotRole) -> dict[str, Any]:
    """Render a registered-but-not-running bot as an entry."""
    log_tail = _tail_log(role.start_log) if role.start_log else []
    return {
        "pid": None,
        "running": False,
        "project": role.project,
        "script": role.script,
        "name": role.display_name,
        "experiment": None,
        "mode": "STOPPED",
        "cmdline": role.start_command,
        "cwd": str(role.cwd),
        "db_path": None,
        "log_path": str(role.start_log) if role.start_log else None,
        "log_tail": log_tail,
        "uptime_s": 0,
        "cpu_pct": 0.0,
        "mem_mb": 0.0,
        "positions": None,
        "wallet": None,
        "role_key": role.key,
        "can_start": True,
        "can_stop": False,
    }


def _build_bots(sol_price: float | None = None) -> list[dict[str, Any]]:
    roles = _load_roles()
    running = _scan_running(sol_price)

    matched_role_keys: set[str] = set()
    bots: list[dict[str, Any]] = []
    for row in running:
        role = _match_role(row, roles)
        row["role_key"] = role.key if role else None
        row["can_start"] = False  # already running
        row["can_stop"] = True
        if role is not None:
            matched_role_keys.add(role.key)
            row["name"] = row["name"]  # keep specific experiment name
        bots.append(row)

    for role in roles:
        if role.key in matched_role_keys:
            continue
        bots.append(_role_stub(role))

    bots.sort(key=lambda b: (not b["running"], b["project"], b["script"], b["name"]))
    return bots


# --- Actions -----------------------------------------------------------------

def _audit(action: str, key: str, **extra: Any) -> None:
    line = json.dumps({"ts": time.time(), "action": action, "key": key, **extra})
    try:
        with ACTION_LOG.open("a") as f:
            f.write(line + "\n")
    except OSError:
        pass
    log.info("action %s", line)


def _find_running_for_role(role: BotRole) -> psutil.Process | None:
    for row in _scan_running():
        if (row["project"] == role.project
                and row["script"] == role.script
                and role.name_pattern.search(row["name"])):
            try:
                return psutil.Process(row["pid"])
            except psutil.NoSuchProcess:
                return None
    return None


def _stop_proc(proc: psutil.Process, grace_s: float = 10.0) -> dict[str, Any]:
    pid = proc.pid
    try:
        pgid = os.getpgid(pid)
    except OSError:
        pgid = None

    # SIGTERM first (prefer process group to catch wrappers)
    try:
        if pgid is not None and pgid != os.getpgid(os.getpid()):
            os.killpg(pgid, signal.SIGTERM)
        else:
            proc.terminate()
    except (ProcessLookupError, psutil.NoSuchProcess):
        return {"pid": pid, "terminated": True, "method": "already-dead"}

    # Wait up to grace_s for graceful exit
    try:
        proc.wait(timeout=grace_s)
        return {"pid": pid, "terminated": True, "method": "sigterm"}
    except psutil.TimeoutExpired:
        pass

    # Force kill
    try:
        if pgid is not None and pgid != os.getpgid(os.getpid()):
            os.killpg(pgid, signal.SIGKILL)
        else:
            proc.kill()
    except (ProcessLookupError, psutil.NoSuchProcess):
        pass
    try:
        proc.wait(timeout=3.0)
        return {"pid": pid, "terminated": True, "method": "sigkill"}
    except psutil.TimeoutExpired:
        return {"pid": pid, "terminated": False, "method": "sigkill-timeout"}


# --- FastAPI -----------------------------------------------------------------

app = FastAPI(title="Leeroy Chainkins")


@app.get("/api/status")
def status() -> dict[str, Any]:
    sol_price = _sol_usd_price()
    return {
        "host": os.uname().nodename,
        "now": int(time.time()),
        "sol_usd_price": sol_price,
        "bots": _build_bots(sol_price),
    }


@app.get("/api/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/stop/{key}")
def api_stop(key: str) -> dict[str, Any]:
    roles = {r.key: r for r in _load_roles()}
    role = roles.get(key)
    if role is None:
        raise HTTPException(status_code=404, detail=f"unknown role {key}")
    proc = _find_running_for_role(role)
    if proc is None:
        _audit("stop", key, result="not-running")
        return {"ok": True, "status": "not-running"}
    result = _stop_proc(proc)
    _audit("stop", key, **result)
    return {"ok": result["terminated"], **result}


@app.post("/api/start/{key}")
def api_start(key: str) -> dict[str, Any]:
    roles = {r.key: r for r in _load_roles()}
    role = roles.get(key)
    if role is None:
        raise HTTPException(status_code=404, detail=f"unknown role {key}")
    existing = _find_running_for_role(role)
    if existing is not None:
        _audit("start", key, result="already-running", pid=existing.pid)
        return {"ok": True, "status": "already-running", "pid": existing.pid}
    if not role.cwd.is_dir():
        raise HTTPException(status_code=500, detail=f"cwd {role.cwd} missing")

    log_path = role.start_log or role.cwd / f"{role.key.replace(':', '_')}.log"
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_fd = open(log_path, "ab", buffering=0)
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"open log failed: {e}")

    try:
        proc = subprocess.Popen(
            ["bash", "-lc", role.start_command],
            cwd=str(role.cwd),
            stdin=subprocess.DEVNULL,
            stdout=log_fd,
            stderr=log_fd,
            start_new_session=True,
            close_fds=True,
        )
    except OSError as e:
        log_fd.close()
        raise HTTPException(status_code=500, detail=f"Popen failed: {e}")
    finally:
        log_fd.close()  # child keeps its dup'd fd

    _audit("start", key, wrapper_pid=proc.pid, command=role.start_command)
    # Don't block — return immediately. The python bot will show up on next /api/status.
    return {"ok": True, "status": "starting", "wrapper_pid": proc.pid}


@app.get("/")
def root() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
