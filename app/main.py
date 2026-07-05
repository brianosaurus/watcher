"""Leeroy Chainkins — read-only bot status dashboard."""
from __future__ import annotations

import json
import logging
import os
import re
import shlex
import sqlite3
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import psutil
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

log = logging.getLogger("watcher")

REPO_ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = REPO_ROOT / "static"
# Global reset marker: all cards (bots + sections) only count data with ts >= this epoch.
# `echo $(date +%s) > ~/watcher/reset.epoch` on Frankfurt; delete the file to clear.
_RESET_FILE = REPO_ROOT / "reset.epoch"

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

# Projects with a single on-chain wallet we can hit for real balance.
# The memeorator DB's `snapshots.portfolio_value_sol` is the bot's allocated
# capital parameter, not the on-chain balance — so for these projects we
# prefer getBalance from Solana RPC.
PROJECT_WALLETS: dict[str, str] = {
    # memeorator trades from memeorator-key.json (WALLET_KEYPAIR_PATH in its .env),
    # NOT leeroy-mainnet.json. statalyzer trades from statalyzer-key.json.
    "memeorator": "FyXKk2Bs4Du82Lw3nE2g2ifQ2rL7ZoRzJdCBVZddH5si",
    "statalyzer": "3rXDjvUpqgiSQqh86StDqwczMtiKS8BA1pJvVyzf7P81",
}
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"

# Upper sanity bound on a trade's slot delta (confirm_slot - signal_slot). Real confirmed
# trades land within a handful of slots; values beyond this come from a stale captured slot
# (a bot bug) and are dropped rather than displayed. ~100k slots ≈ 11h — far above any real.
_SLOT_DELTA_MAX = 100_000


# --- Cmdline parsing ---------------------------------------------------------

def _parse_flag(tokens: list[str], flag: str) -> str | None:
    for i, tok in enumerate(tokens):
        if tok == flag and i + 1 < len(tokens):
            return tokens[i + 1]
        if tok.startswith(flag + "="):
            return tok.split("=", 1)[1]
    return None


def _infer_mode(tokens: list[str], script: str) -> str:
    if "--live" in tokens and "--confirm-live" in tokens:
        return "LIVE"
    if "--dry-run" in tokens:
        return "DRY-RUN"
    if "-e" in tokens:
        idx = tokens.index("-e")
        if idx + 1 < len(tokens) and tokens[idx + 1] == "live":
            return "LIVE"
    # Memeorator-family convention: absence of --dry-run means real trades.
    if PROJECT_BY_SCRIPT.get(script) == "memeorator":
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


def _load_true_pnl(db_path: Path) -> dict:
    """tx-level reconstructed REAL on-chain PnL per position id, written by
    true_pnl_reconciler.py next to the statalyzer DB. {pid_str: {pnl, won, ts}}.
    This is the ground truth — positions.realized_pnl is the deceptive price-based
    value (shows positive while the wallet bleeds)."""
    try:
        import json as _json
        d = _json.loads((db_path.parent / "true_pnl.json").read_text())
        return {k: v for k, v in d.items() if not k.startswith("_")}
    except Exception:
        return {}


def _balance_series(db_path: Path, max_points: int = 80,
                    since_ts: float | None = None) -> list[dict[str, float]]:
    """native SOL vs total wallet value (SOL) over time, from balance_series.json
    (written by true_pnl_reconciler). Makes the 'cash rising / net worth falling'
    split visible: native climbs as the bot liquidates LSTs, total drifts down.
    `since_ts` scopes to a reset window (points with t >= since_ts)."""
    try:
        import json as _json
        s = _json.loads((db_path.parent / "balance_series.json").read_text())
    except Exception:
        return []
    if since_ts is not None:
        s = [x for x in s if x.get("t", 0) >= since_ts]
    if len(s) > max_points:
        stride = len(s) / max_points
        s = [s[min(len(s) - 1, int(i * stride))] for i in range(max_points)]
    return [{"t": x["t"], "native": x["native"], "total": x["total"]} for x in s]


def _realized_pnl_sol(conn: sqlite3.Connection, true_pnl: dict, since_ts: float | None = None) -> float:
    """REAL on-chain SOL PnL across closed positions, summed from the tx-level
    `true_pnl` map (NOT the deceptive positions.realized_pnl). `since_ts` scopes to
    the current run via COALESCE(exit_time, entry_time)."""
    scope = " AND COALESCE(exit_time, entry_time) >= ?" if since_ts is not None else ""
    args = (since_ts,) if since_ts is not None else ()
    ids = [str(r[0]) for r in conn.execute(
        f"SELECT id FROM positions WHERE status!='open'{scope}", args)]
    return float(sum(true_pnl[i]["pnl"] for i in ids if i in true_pnl))


def _positions_summary(db_path: Path, since_ts: float | None = None) -> dict[str, Any] | None:
    conn = _safe_open_db(db_path)
    if conn is None:
        return None
    try:
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        if "positions" not in tables:
            return None
        cols = {r[1] for r in conn.execute("PRAGMA table_info(positions)")}
        # OPEN positions are live state — always count ALL of them, even ones carried
        # over from a previous run (entered before this process started).
        open_n = conn.execute(
            "SELECT COUNT(*) FROM positions WHERE status='open'"
        ).fetchone()[0]
        # CLOSED count + realized PnL are scoped to closes during THIS run since
        # statalyzer's DB persists across restarts. Use COALESCE(exit_time, entry_time)
        # so a just-closed position (exit_time not written until reconciliation, ~seconds
        # later) still counts immediately instead of lagging the display by one.
        scope = " AND COALESCE(exit_time, entry_time) >= ?" if (
            since_ts is not None and "exit_time" in cols) else ""
        args = (since_ts,) if scope else ()
        closed_n = conn.execute(
            f"SELECT COUNT(*) FROM positions WHERE status!='open'{scope}", args
        ).fetchone()[0]
        _sts = since_ts if "exit_time" in cols else None
        _tp = _load_true_pnl(db_path)
        pnl_sol = _realized_pnl_sol(conn, _tp, _sts)
        # REAL win rate from tx-level reconstructed on-chain PnL (true_pnl.json)
        _cids = [str(r[0]) for r in conn.execute(
            f"SELECT id FROM positions WHERE status!='open'{scope}", args)]
        _rec = [_tp[i] for i in _cids if i in _tp]
        win_rate = (sum(x["won"] for x in _rec) / len(_rec)) if _rec else None
        last_entry = conn.execute("SELECT MAX(entry_time) FROM positions").fetchone()[0]
        return {
            "open": int(open_n),
            "closed": int(closed_n),
            "realized_pnl_sol": round(pnl_sol, 6),
            "win_rate": round(win_rate, 4) if win_rate is not None else None,
            "reconciled": len(_rec),
            "last_entry_time": last_entry,
        }
    except sqlite3.Error as e:
        return {"error": str(e)}
    finally:
        conn.close()


def _tail_log(path: Path, n_lines: int = 100, max_bytes: int = 131_072) -> list[str]:
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


def _grep_log_lines(path: Path, needle: str, max_lines: int = 4000) -> list[str]:
    """Return the last `max_lines` lines of `path` containing `needle` (fixed string).

    Uses `grep` so sparse markers (e.g. per-trade "swap OK" / "TIMING" lines) are found
    no matter how large the log grows — a byte-tail would miss them once enough other
    log volume scrolls past. The log is recreated per run, so this stays current-run scoped.
    """
    if not path.exists() or not path.is_file():
        return []
    try:
        out = subprocess.run(
            ["grep", "-aF", needle, str(path)],
            capture_output=True, text=True, timeout=10, check=False,
        )
        return out.stdout.splitlines()[-max_lines:]
    except (OSError, subprocess.SubprocessError):
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


_CHAIN_BAL_CACHE: dict[str, tuple[float, float]] = {}  # pubkey -> (ts, sol)
_CHAIN_BAL_TTL_S = 30.0
# In-memory on-chain balance history per pubkey (the wallet isn't logged over time
# anywhere, so the watcher samples it via getBalance ~every TTL and keeps a rolling
# series for the wallet chart). Resets on watcher restart.
_CHAIN_BAL_HISTORY: dict[str, list[tuple[float, float]]] = {}
_CHAIN_BAL_HISTORY_MAX = 3000

def _chain_sol_balance(pubkey: str) -> dict[str, Any] | None:
    now = time.time()
    cached = _CHAIN_BAL_CACHE.get(pubkey)
    if cached and (now - cached[0]) < _CHAIN_BAL_TTL_S:
        return {"sol": cached[1], "source": f"rpc:getBalance({pubkey[:6]}…)", "ts": cached[0]}
    body = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "getBalance", "params": [pubkey],
    }).encode("utf-8")
    try:
        req = urllib.request.Request(
            SOLANA_RPC_URL, data=body,
            headers={"Content-Type": "application/json", "User-Agent": "leeroy-chainkins/1.0"},
        )
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        lamports = int(data["result"]["value"])
        sol = lamports / 1_000_000_000
        _CHAIN_BAL_CACHE[pubkey] = (now, sol)
        hist = _CHAIN_BAL_HISTORY.setdefault(pubkey, [])
        hist.append((now, sol))
        if len(hist) > _CHAIN_BAL_HISTORY_MAX:
            del hist[:len(hist) - _CHAIN_BAL_HISTORY_MAX]
        return {"sol": sol, "source": f"rpc:getBalance({pubkey[:6]}…)", "ts": now}
    except (urllib.error.URLError, OSError, ValueError, KeyError, json.JSONDecodeError) as e:
        log.warning("chain balance fetch failed for %s: %s", pubkey, e)
        if cached:
            return {"sol": cached[1], "source": f"rpc:getBalance({pubkey[:6]}…) stale", "ts": cached[0]}
        return None


def _chain_balance_series(pubkey: str, max_points: int = 120) -> list[dict[str, float]]:
    """Rolling on-chain SOL series for a wallet, from samples the watcher has taken."""
    hist = _CHAIN_BAL_HISTORY.get(pubkey) or []
    if len(hist) < 2:
        return []
    raw = list(hist)
    if len(raw) > max_points:
        stride = len(raw) / max_points
        raw = [raw[min(len(raw) - 1, int(i * stride))] for i in range(max_points)] + [raw[-1]]
    return [{"t": t, "sol": round(s, 6)} for t, s in raw]


def _wallet_summary(db_path: Path, sol_price: float | None) -> dict[str, Any] | None:
    """Return {sol, source, ts} — always native SOL. Memeorator stores SOL directly;
    statalyzer's actual wallet balance lives in `sol_balance_log.sol_after`, with a
    USD/price fallback via `portfolio_snapshots.total_value`."""
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
                return {
                    "sol": float(row["portfolio_value_sol"]),
                    "source": "snapshots.portfolio_value_sol",
                    "ts": float(row["timestamp"]),
                }
        # Statalyzer-style: latest observed wallet SOL balance
        if "sol_balance_log" in tables:
            row = conn.execute(
                "SELECT timestamp, sol_after FROM sol_balance_log "
                "WHERE sol_after IS NOT NULL "
                "ORDER BY timestamp DESC LIMIT 1"
            ).fetchone()
            if row and row["sol_after"] is not None:
                return {
                    "sol": float(row["sol_after"]),
                    "source": "sol_balance_log.sol_after",
                    "ts": float(row["timestamp"]),
                }
        # Statalyzer fallback: convert USD portfolio_snapshots → SOL via live price
        if "portfolio_snapshots" in tables and sol_price:
            row = conn.execute(
                "SELECT timestamp, total_value FROM portfolio_snapshots "
                "ORDER BY timestamp DESC LIMIT 1"
            ).fetchone()
            if row and row["total_value"] is not None:
                return {
                    "sol": float(row["total_value"]) / sol_price,
                    "source": "portfolio_snapshots.total_value/usd",
                    "ts": float(row["timestamp"]),
                }
        return None
    except sqlite3.Error as e:
        return {"error": str(e)}
    finally:
        conn.close()


def _pnl_series(db_path: Path, max_points: int = 80, since_ts: float | None = None) -> list[dict[str, float]]:
    """Cumulative realized PnL (SOL) time series for sparklines (statalyzer). Empty if no data.

    memeorator's series is built from the log STATS block instead (see `_parse_memeorator_stats`).
    `since_ts` scopes to the current run (entry_time >= process start).
    """
    conn = _safe_open_db(db_path)
    if conn is None:
        return []
    try:
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        raw: list[tuple[float, float]] = []
        if "positions" in tables:
            cols = {r[1] for r in conn.execute("PRAGMA table_info(positions)")}
            order_col = next(
                (c for c in ("exit_time", "close_time", "closed_at", "close_timestamp", "entry_time") if c in cols),
                None,
            )
            scope = f" AND {order_col} >= ?" if since_ts is not None and order_col else ""
            args = (since_ts,) if scope else ()
            if order_col:
                true_pnl = _load_true_pnl(db_path)
                rows = conn.execute(
                    f"SELECT id, {order_col} AS ts FROM positions "
                    f"WHERE status != 'open' "
                    f"AND {order_col} IS NOT NULL{scope} ORDER BY {order_col}", args
                ).fetchall()
                cum = 0.0
                for r in rows:                       # REAL on-chain cumulative PnL
                    tp = true_pnl.get(str(r["id"]))
                    if tp is None:
                        continue                     # not yet reconciled
                    cum += float(tp["pnl"])
                    raw.append((float(r["ts"]), cum))
        if not raw and "snapshots" in tables:
            rows = conn.execute(
                "SELECT timestamp, total_pnl_sol FROM snapshots "
                "WHERE total_pnl_sol IS NOT NULL "
                "ORDER BY timestamp"
            ).fetchall()
            raw = [(float(r["timestamp"]), float(r["total_pnl_sol"])) for r in rows]
        if not raw:
            return []
        if len(raw) > max_points:
            stride = len(raw) / max_points
            picked = [raw[min(len(raw) - 1, int(i * stride))] for i in range(max_points)]
            if picked[-1] != raw[-1]:
                picked[-1] = raw[-1]
            raw = picked
        return [{"t": t, "pnl": round(p, 6)} for t, p in raw]
    except sqlite3.Error:
        return []
    finally:
        conn.close()


def _winrate_series(db_path: Path, max_points: int = 80, since_ts: float | None = None) -> list[dict[str, float]]:
    """Cumulative winrate (wins / closed trades so far) over time (statalyzer). Empty if no data.

    memeorator keeps no clean per-trade win/loss series in its DB, so it has no winrate chart.
    `since_ts` scopes to the current run (entry_time >= process start).
    """
    conn = _safe_open_db(db_path)
    if conn is None:
        return []
    try:
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        if "positions" not in tables:
            return []
        cols = {r[1] for r in conn.execute("PRAGMA table_info(positions)")}
        order_col = next(
            (c for c in ("close_time", "exit_time", "closed_at", "close_timestamp", "entry_time") if c in cols),
            None,
        )
        if order_col is None:
            return []
        scope = f" AND {order_col} >= ?" if since_ts is not None and order_col else ""
        args = (since_ts,) if scope else ()
        rows = conn.execute(
            f"SELECT id, {order_col} AS ts FROM positions "
            f"WHERE status!='open' "
            f"AND {order_col} IS NOT NULL{scope} ORDER BY {order_col}", args
        ).fetchall()
        true_pnl = _load_true_pnl(db_path)
        rows = [r for r in rows if str(r["id"]) in true_pnl]  # only reconciled (real on-chain) trades
        if not rows:
            return []
        wins = 0
        raw: list[tuple[float, float]] = []
        for i, r in enumerate(rows, 1):
            if true_pnl[str(r["id"])]["won"]:
                wins += 1
            raw.append((float(r["ts"]), wins / i))
        if len(raw) > max_points:
            stride = len(raw) / max_points
            picked = [raw[min(len(raw) - 1, int(i * stride))] for i in range(max_points)]
            if picked[-1] != raw[-1]:
                picked[-1] = raw[-1]
            raw = picked
        return [{"t": t, "wr": round(wr, 4)} for t, wr in raw]
    except sqlite3.Error:
        return []
    finally:
        conn.close()


def _median(values: list[float]) -> float:
    s = sorted(values)
    m = len(s) // 2
    return float(s[m]) if len(s) % 2 else round((s[m - 1] + s[m]) / 2, 2)


def _downsample(raw: list[tuple[float, float]], max_points: int) -> list[tuple[float, float]]:
    """Evenly thin a (ts, value) series to <= max_points, always keeping the last point."""
    if len(raw) <= max_points:
        return raw
    stride = len(raw) / max_points
    picked = [raw[min(len(raw) - 1, int(i * stride))] for i in range(max_points)]
    if picked[-1] != raw[-1]:
        picked[-1] = raw[-1]
    return picked


def _statalyzer_execlog_stats(
    db_path: Path, since_ts: float | None = None, max_points: int = 80
) -> tuple[dict[str, Any], list[dict[str, float]], list[dict[str, float]]] | None:
    """Rebalance-mode statalyzer stats from `execution_log.captured_sol`.

    In `--rebalance-mode` statalyzer never writes the `positions` table (so the bot's own
    "RUNNING PnL: realized=..." log line, which SUMs that table, is stuck at 0). Each
    rebalance swap is one `execution_log` row whose `captured_sol` is its realized PnL (±).
    So realized PnL = SUM(captured_sol), each row is a win (>0) or loss (<0), and the
    cumulative series feed the PnL + win-rate charts. (Per-swap latency phases come from
    the log instead — see `_statalyzer_trade_phases`.) `since_ts` limits to the current
    session (rows with timestamp >= the process start). Returns None if there are no rows.
    """
    conn = _safe_open_db(db_path)
    if conn is None:
        return None
    try:
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        if "execution_log" not in tables:
            return None
        cols = {r[1] for r in conn.execute("PRAGMA table_info(execution_log)")}
        if "captured_sol" not in cols or "timestamp" not in cols:
            return None
        params: list[Any] = []
        since_clause = ""
        if since_ts is not None:
            since_clause = "AND timestamp >= ? "
            params.append(since_ts)
        rows = conn.execute(
            "SELECT timestamp, captured_sol FROM execution_log "
            "WHERE side='rebalance' AND captured_sol IS NOT NULL AND timestamp IS NOT NULL "
            f"{since_clause}ORDER BY timestamp",
            params,
        ).fetchall()
        if not rows:
            return None
        cum = 0.0
        wins = losses = 0
        pnl_raw: list[tuple[float, float]] = []
        wr_raw: list[tuple[float, float]] = []
        for r in rows:
            v = float(r["captured_sol"])
            ts = float(r["timestamp"])
            cum += v
            pnl_raw.append((ts, cum))
            if v > 0:
                wins += 1
            elif v < 0:
                losses += 1
            decided = wins + losses
            if decided:
                wr_raw.append((ts, wins / decided))
        summary = {
            "open": 0,
            "closed": len(rows),
            "wins": wins,
            "losses": losses,
            "realized_pnl_sol": round(cum, 6),
            "last_entry_time": pnl_raw[-1][0] if pnl_raw else None,
        }
        pnl_series = [{"t": t, "pnl": round(p, 6)} for t, p in _downsample(pnl_raw, max_points)]
        wr_series = [{"t": t, "wr": round(w, 4)} for t, w in _downsample(wr_raw, max_points)]
        return summary, pnl_series, wr_series
    except sqlite3.Error:
        return None
    finally:
        conn.close()


# --- statalyzer rebalancer log PnL parsing ----------------------------------
# statalyzer's realized PnL (per the user) is the portfolio-value change printed on its
# rebalancer status line, which has NO inline timestamp:
#   Rebalancer: 2 swaps | edge 14.8bps | captured +0.000098SOL | portfolio 4.3200 SOL (+0.0129)
# The "(+0.0129)" is `portfolio_value - session_start_value` (resets each restart). We read
# the latest one for the number and chart all of them for the PnL sparkline; each delta is
# anchored in time to the nearest timestamped log line so the series ends at "now".

_REBAL_PNL_RE = re.compile(r"portfolio\s+[\d.]+\s+SOL\s+\(([+-][\d.]+)\)")
_LOG_TS_RE = re.compile(r"^(\d{2}):(\d{2}):(\d{2})\b")


def _statalyzer_log_pnl(
    lines: list[str], now: float, max_points: int = 80
) -> tuple[float | None, list[dict[str, float]]]:
    """Parse 'portfolio X SOL (+Y)' deltas from statalyzer's rebalancer log tail.

    Returns (latest_delta, pnl_series). Log timestamps are HH:MM:SS only, so we track
    seconds-of-day with midnight rollover and anchor the newest point to `now` — only
    relative spacing matters for the chart. (None, []) if no delta line is found.
    """
    # Map line index -> absolute seconds for timestamped lines (with day rollover).
    ts_by_idx: dict[int, int] = {}
    day = 0
    prev_sod: int | None = None
    for i, ln in enumerate(lines):
        m = _LOG_TS_RE.match(ln)
        if m:
            sod = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
            if prev_sod is not None and sod < prev_sod - 3600:  # large backward jump => next day
                day += 1
            prev_sod = sod
            ts_by_idx[i] = day * 86400 + sod

    pts: list[tuple[int, float]] = []  # (abs_seconds, delta)
    for i, ln in enumerate(lines):
        m = _REBAL_PNL_RE.search(ln)
        if not m:
            continue
        delta = float(m.group(1))
        t = next((ts_by_idx[j] for j in range(i, len(lines)) if j in ts_by_idx), None)
        if t is None:
            t = next((ts_by_idx[j] for j in range(i, -1, -1) if j in ts_by_idx), None)
        if t is not None:
            pts.append((t, delta))

    if not pts:
        return None, []
    last_t = pts[-1][0]
    raw = [(now - (last_t - t), d) for t, d in pts]
    series = [{"t": t, "pnl": round(d, 6)} for t, d in _downsample(raw, max_points)]
    return pts[-1][1], series


# Per-swap latency breakdown + slots, logged by executor.py on every fill, e.g.:
#   23:42:58 INFO executor: LL direct swap OK: BonK1Yhk→5oVNBeEE build=9ms submit=9ms
#   confirm=440ms | signal_slot=426736396 processed_slot=426736398 slot_Δ=2 time_Δ=475ms
# build  = quote + tx build; submit = bundle/RPC send; confirm = submit→on-chain confirm.
# signal_slot = slot when the TX build started; processed_slot = slot it confirmed in.
_SWAP_PHASE_RE = re.compile(r"build=(\d+)ms\s+submit=(\d+)ms\s+confirm=(\d+)ms")
_SWAP_TOTAL_RE = re.compile(r"time_Δ=(\d+)\s*ms")
_SWAP_SLOT_RE = re.compile(r"signal_slot=(\d+)\s+processed_slot=(\d+)\s+slot_Δ=(-?\d+)")


def _statalyzer_trade_phases(
    lines: list[str], now: float, max_points: int = 80
) -> tuple[dict[str, Any] | None, list[dict[str, float]]]:
    """Parse per-swap latency phases + slots from statalyzer's 'swap OK: ...' log lines.

    Each such line is timestamped and self-contained. Returns (summary, series):
      summary = mean build/submit/confirm/dispatch/total (ms), mean_slot_delta, and the
                latest swap's build_slot / confirm_slot / slot_delta.
      series  = per-swap {t, build, submit, confirm, dispatch} for the stacked chart,
                anchored so the newest point == now.
    (None, []) if no swap-OK line is found. `dispatch` = total − build − submit − confirm
    (signal→build-start lag).
    """
    day = 0
    prev_sod: int | None = None
    # (abs_sec, build, submit, confirm, dispatch, total, build_slot, confirm_slot, slot_delta)
    raw: list[tuple[int, int, int, int, int, int, int | None, int | None, int | None]] = []
    for ln in lines:
        mp = _SWAP_PHASE_RE.search(ln)
        mt = _LOG_TS_RE.match(ln)
        if not mp or not mt:
            continue
        sod = int(mt.group(1)) * 3600 + int(mt.group(2)) * 60 + int(mt.group(3))
        if prev_sod is not None and sod < prev_sod - 3600:
            day += 1
        prev_sod = sod
        b, s, c = int(mp.group(1)), int(mp.group(2)), int(mp.group(3))
        mtot = _SWAP_TOTAL_RE.search(ln)
        total = int(mtot.group(1)) if mtot else b + s + c
        dispatch = max(0, total - b - s - c)
        msl = _SWAP_SLOT_RE.search(ln)
        bslot = int(msl.group(1)) if msl else None
        cslot = int(msl.group(2)) if msl else None
        sdelta = int(msl.group(3)) if msl else None
        raw.append((day * 86400 + sod, b, s, c, dispatch, total, bslot, cslot, sdelta))

    if not raw:
        return None, []
    n = len(raw)
    deltas = [r[8] for r in raw if r[8] is not None]
    last = raw[-1]
    summary = {
        "mean_trade_time_ms": round(sum(r[5] for r in raw) / n, 1),
        "phases": {
            "build": round(sum(r[1] for r in raw) / n, 1),
            "submit": round(sum(r[2] for r in raw) / n, 1),
            "confirm": round(sum(r[3] for r in raw) / n, 1),
            "dispatch": round(sum(r[4] for r in raw) / n, 1),
        },
        # slot delta is the low-noise latency signal; report median (robust to a few
        # stale-signal_slot outliers) alongside mean.
        "mean_slot_delta": round(sum(deltas) / len(deltas), 2) if deltas else None,
        "median_slot_delta": _median(deltas) if deltas else None,
        "build_slot": last[6],
        "confirm_slot": last[7],
        "slot_delta": last[8],
    }
    last_t = raw[-1][0]
    anchored = [(now - (last_t - r[0]), r) for r in raw]
    series = [
        {"t": t, "build": r[1], "submit": r[2], "confirm": r[3], "dispatch": r[4],
         "slot_delta": r[8]}
        for t, r in _downsample(anchored, max_points)
    ]
    return summary, series


# Per-close slot data for statalyzer's inventory (token<->token) arb swaps, which do NOT
# emit a "swap OK" phase line. Every close logs a reconciliation pair:
#   …Exit reconciliation #162: sol_before=… slot=427748382 expected_pnl=… SOL sigs=2
#   …Reconciliation #162: finalized at slot 427748384, sol_after=…
# slot Δ = finalized − start. (No build/submit/confirm ms is recorded for these — the only
# per-close timing signal is the slot delta.)
_RECON_START_RE = re.compile(r"Exit reconciliation #(\d+):.*?\bslot=(\d+)")
_RECON_FINAL_RE = re.compile(r"\bReconciliation #(\d+): finalized at slot (\d+)")


def _statalyzer_recon_slots(
    lines: list[str], now: float, max_points: int = 80
) -> tuple[dict[str, Any] | None, list[dict[str, float]]]:
    """Per-close slot deltas from statalyzer's exit-reconciliation log lines.

    Pairs 'Exit reconciliation #N … slot=START' with 'Reconciliation #N: finalized at
    slot END' to get slot_delta=END-START per close. Returns (summary, series) with the
    latest build/confirm slots, mean/median slot delta, and the per-close slot-Δ series;
    (None, []) if none found. This updates on every close (unlike the sparse swap-OK lines).
    """
    day = 0
    prev_sod: int | None = None
    starts: dict[int, int] = {}
    finals: list[tuple[int, int, int]] = []  # (abs_sec, n, finalized_slot)
    for ln in lines:
        m = _LOG_TS_RE.match(ln)
        abs_t: int | None = None
        if m:
            sod = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
            if prev_sod is not None and sod < prev_sod - 3600:
                day += 1
            prev_sod = sod
            abs_t = day * 86400 + sod
        ms = _RECON_START_RE.search(ln)
        if ms:
            starts[int(ms.group(1))] = int(ms.group(2))
            continue
        mf = _RECON_FINAL_RE.search(ln)
        if mf and abs_t is not None:
            finals.append((abs_t, int(mf.group(1)), int(mf.group(2))))

    raw: list[tuple[int, int, int, int]] = []  # (abs_sec, slot_delta, start_slot, final_slot)
    for abs_t, n, fslot in finals:
        if n in starts:
            raw.append((abs_t, fslot - starts[n], starts[n], fslot))
    if not raw:
        return None, []
    raw.sort()
    deltas = [r[1] for r in raw]
    last = raw[-1]
    last_t = last[0]
    summary = {
        "build_slot": last[2],
        "confirm_slot": last[3],
        "slot_delta": last[1],
        "mean_slot_delta": round(sum(deltas) / len(deltas), 2),
        "median_slot_delta": _median(deltas),
    }
    anchored = [(now - (last_t - r[0]), float(r[1])) for r in raw]
    series = [{"t": t, "slot_delta": sd} for t, sd in _downsample(anchored, max_points)]
    return summary, series


# --- memeorator log STATS parsing -------------------------------------------
# memeorator does NOT persist positions/PnL to its DB (the positions table stays
# empty across runs). Its authoritative position/PnL accounting only appears in the
# periodic STATS block it prints to its log, e.g.:
#   STATS (720s elapsed) — c4plus_drainml_...
#   Portfolio: 0 open, 0 closed, PnL=+0.0000 SOL, WR=0% | Rugs: 0 (-0.00 SOL)
#   BC_OBS [pos=0.01 SOL]: 177 decided, 23 admitted, 0 open, 22 closed (WR=31.8%, ..., PnL=-0.0783 SOL)
#   GRAD [pos=0.100 SOL]: 149 decided, 1 admitted, 1 open, 0 closed (WR=—, ..., PnL=+0.0000 SOL)
# We track ONLY the GRAD strategy line (the graduation trader) — BC_OBS and the
# Portfolio line are deliberately ignored.

_STATS_ELAPSED_RE = re.compile(r"STATS\s*\((\d+)\s*s\s*elapsed\)")
_STATS_GRAD_RE = re.compile(r"\bGRAD\b.*?(\d+)\s*open,\s*(\d+)\s*closed.*?PnL=([+-]?[\d.]+)\s*SOL")
_STATS_GRAD_WR_RE = re.compile(r"\bGRAD\b.*?WR=([\d.]+)\s*%")


def _parse_memeorator_stats(
    lines: list[str], create_time: float
) -> tuple[dict[str, Any] | None, list[dict[str, float]], list[dict[str, float]]]:
    """Parse the GRAD line from memeorator STATS blocks in its log tail.

    Returns (summary, pnl_series, winrate_series). `summary` is the latest block's GRAD
    {open, closed, realized_pnl_sol}; the series are per block over time (block
    elapsed-seconds anchored to the process create_time). winrate_series uses the GRAD
    line's own `WR=...%` field (blocks with no WR — before any GRAD trade closes — are
    skipped). All empty if no STATS block is found.
    """
    blocks: list[dict[str, Any]] = []
    cur: dict[str, Any] | None = None
    for ln in lines:
        m = _STATS_ELAPSED_RE.search(ln)
        if m:
            if cur is not None:
                blocks.append(cur)
            cur = {"elapsed": float(m.group(1)), "open": 0.0, "closed": 0.0, "pnl": 0.0, "wr": None}
            continue
        if cur is None:
            continue
        mg = _STATS_GRAD_RE.search(ln)
        if mg:
            cur["open"] += int(mg.group(1))
            cur["closed"] += int(mg.group(2))
            cur["pnl"] += float(mg.group(3))
            mw = _STATS_GRAD_WR_RE.search(ln)
            if mw:
                cur["wr"] = float(mw.group(1)) / 100.0
    if cur is not None:
        blocks.append(cur)
    if not blocks:
        return None, [], []
    last = blocks[-1]
    summary = {
        "open": int(last["open"]),
        "closed": int(last["closed"]),
        "realized_pnl_sol": round(last["pnl"], 6),
        "last_entry_time": None,
    }
    pnl_series = [
        {"t": create_time + b["elapsed"], "pnl": round(b["pnl"], 6)}
        for b in blocks
    ]
    winrate_series = [
        {"t": create_time + b["elapsed"], "wr": round(b["wr"], 4)}
        for b in blocks if b["wr"] is not None
    ]
    return summary, pnl_series, winrate_series


# memeorator per-trade latency (TradeTimer.log_summary in timing.py), e.g.:
#   01:21:12.908 | INFO | TIMING DHbWEVj7.. | total=1.2ms | grpc_detected=+0.2ms →
#   signal_emitted=+-0.1ms → ... → tx_built=+0.2ms → bundle_submitted=+0.0ms → bundle_responded=+0.0ms
# Bucketed into the same shape as statalyzer (build / submit / dispatch) so the watcher
# can show one consistent trade-time view. memeorator has no on-chain confirm phase here
# (it ends at the Lunar Lander response), so `confirm` is omitted. Slots come from the DB.
_MEME_TIMING_RE = re.compile(r"\bTIMING\b.*?\btotal=([\d.]+)\s*ms")
_MEME_DELTA_RE = re.compile(r"(\w+)=\+?(-?[\d.]+)ms")
_MEME_BUILD_CKPTS = {"curve_fetched", "ix_built", "tx_signed", "tx_built"}
_MEME_SUBMIT_CKPTS = {"bundle_submitted", "bundle_responded"}
_MEME_CONFIRM_CKPTS = {"confirmed"}


def _parse_memeorator_timing(
    lines: list[str], now: float, max_points: int = 80
) -> tuple[dict[str, Any] | None, list[dict[str, float]]]:
    """Parse per-trade latency phases from memeorator's TIMING log lines.

    Each line is self-timestamped. Buckets the checkpoint deltas into build (tx
    construction), submit (bundle send), and dispatch (= total − build − submit, i.e. the
    detect→queue→checks lead-in). Returns (summary, series) mirroring
    `_statalyzer_trade_phases`; (None, []) if no TIMING line is found.
    """
    day = 0
    prev_sod: int | None = None
    # (abs_sec, dispatch, build, submit, confirm, total)
    raw: list[tuple[int, float, float, float, float, float]] = []
    for ln in lines:
        m0 = _MEME_TIMING_RE.search(ln)
        mts = _LOG_TS_RE.match(ln)
        if not m0 or not mts:
            continue
        sod = int(mts.group(1)) * 3600 + int(mts.group(2)) * 60 + int(mts.group(3))
        if prev_sod is not None and sod < prev_sod - 3600:
            day += 1
        prev_sod = sod
        total = float(m0.group(1))
        bld = sub = conf = 0.0
        for name, val in _MEME_DELTA_RE.findall(ln):
            if name == "total":
                continue
            d = max(0.0, float(val))
            if name in _MEME_BUILD_CKPTS:
                bld += d
            elif name in _MEME_SUBMIT_CKPTS:
                sub += d
            elif name in _MEME_CONFIRM_CKPTS:
                conf += d
        dispatch = max(0.0, total - bld - sub - conf)
        raw.append((day * 86400 + sod, dispatch, bld, sub, conf, total))

    if not raw:
        return None, []
    n = len(raw)
    summary = {
        "mean_trade_time_ms": round(sum(r[5] for r in raw) / n, 2),
        "phases": {
            "dispatch": round(sum(r[1] for r in raw) / n, 2),
            "build": round(sum(r[2] for r in raw) / n, 2),
            "submit": round(sum(r[3] for r in raw) / n, 2),
            "confirm": round(sum(r[4] for r in raw) / n, 2),
        },
    }
    last_t = raw[-1][0]
    anchored = [(now - (last_t - r[0]), r) for r in raw]
    series = [
        {"t": t, "dispatch": r[1], "build": r[2], "submit": r[3], "confirm": r[4]}
        for t, r in _downsample(anchored, max_points)
    ]
    return summary, series


def _memeorator_slots(
    db_path: Path, max_points: int = 80
) -> dict[str, Any] | None:
    """Per-trade slot data from memeorator's `live_trades` table (signal/confirmation slots).

    Returns {build_slot, confirm_slot, slot_delta (latest), mean/median_slot_delta, series}
    or None if the table is empty (e.g. nothing has landed live yet).

    Sanity-filters implausible slot deltas: memeorator's GRAD path sometimes captures a
    STALE `self.config.latest_slot` (~21.9M slots / ~100 days behind), yielding ±tens-of-
    millions deltas. A real confirmed trade lands within a handful of slots, so we drop any
    row outside 0..`_SLOT_DELTA_MAX` rather than display garbage."""
    conn = _safe_open_db(db_path)
    if conn is None:
        return None
    try:
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        if "live_trades" not in tables:
            return None
        rows = conn.execute(
            "SELECT timestamp, signal_slot, confirmation_slot, slot_delta FROM live_trades "
            "WHERE confirmation_slot > 0 AND slot_delta IS NOT NULL AND timestamp IS NOT NULL "
            "AND slot_delta >= 0 AND slot_delta <= ? "
            "ORDER BY timestamp",
            (_SLOT_DELTA_MAX,),
        ).fetchall()
        if not rows:
            return None
        deltas = [int(r["slot_delta"]) for r in rows]
        last = rows[-1]
        sd_raw = [(float(r["timestamp"]), float(r["slot_delta"])) for r in rows]
        return {
            "build_slot": int(last["signal_slot"]),
            "confirm_slot": int(last["confirmation_slot"]),
            "slot_delta": int(last["slot_delta"]),
            "mean_slot_delta": round(sum(deltas) / len(deltas), 2),
            "median_slot_delta": _median(deltas),
            "series": [{"t": t, "slot_delta": round(d, 1)} for t, d in _downsample(sd_raw, max_points)],
        }
    except sqlite3.Error:
        return None
    finally:
        conn.close()


# memeorator logs its on-chain wallet balance whenever it changes, e.g.:
#   02:33:00.516 | INFO | WALLET: on_chain=0.4357 internal=0.0985 diff=+0.3372 SOL | open=0 ...
# Parsed into a per-run on-chain SOL time series for the wallet chart.
_MEME_WALLET_RE = re.compile(r"WALLET: on_chain=([\d.]+)")


def _memeorator_wallet_series(
    lines: list[str], now: float, max_points: int = 120
) -> list[dict[str, float]]:
    """On-chain wallet SOL over time from memeorator's 'WALLET: on_chain=' log lines.

    Each line is self-timestamped (HH:MM:SS); anchored so the newest point == now. Empty
    if none found. The log is per-run, so this is current-run scoped."""
    day = 0
    prev_sod: int | None = None
    raw: list[tuple[int, float]] = []
    for ln in lines:
        mw = _MEME_WALLET_RE.search(ln)
        mts = _LOG_TS_RE.match(ln)
        if not mw or not mts:
            continue
        sod = int(mts.group(1)) * 3600 + int(mts.group(2)) * 60 + int(mts.group(3))
        if prev_sod is not None and sod < prev_sod - 3600:
            day += 1
        prev_sod = sod
        raw.append((day * 86400 + sod, float(mw.group(1))))
    if not raw:
        return []
    last_t = raw[-1][0]
    anchored = [(now - (last_t - t), sol) for t, sol in raw]
    return [{"t": t, "sol": round(sol, 6)} for t, sol in _downsample(anchored, max_points)]


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
    mode = _infer_mode(cmdline, script)

    try:
        with proc.oneshot():
            cpu = proc.cpu_percent(interval=None)
            mem_mb = proc.memory_info().rss / (1024 * 1024)
            create_time = proc.create_time()
    except psutil.Error:
        return None

    project = PROJECT_BY_SCRIPT.get(script, "?")
    # statalyzer's DB persists across restarts, so scope its positions stats to the
    # current run (entry_time >= process start). memeorator's positions come from the
    # log, not the DB, so it isn't scoped here. A global reset marker (reset.epoch) can
    # further clamp the window to a manual "from N ago" time.
    reset_ts = _read_reset_ts(_RESET_FILE)
    stat_since = None
    if project == "statalyzer":
        stat_since = create_time if reset_ts is None else max(create_time, reset_ts)
    positions = _positions_summary(db_path, since_ts=stat_since) if db_path else None

    # Wallet SOL: for a LIVE bot with a known on-chain wallet, the real balance is
    # `getBalance` on that pubkey. Dry-run bots don't touch that wallet, so fall back
    # to the DB's simulated/observed balance to avoid showing a misleading number.
    chain_pubkey = PROJECT_WALLETS.get(project)
    if chain_pubkey and mode == "LIVE":
        wallet = _chain_sol_balance(chain_pubkey)
    elif db_path:
        wallet = _wallet_summary(db_path, sol_price)
    else:
        wallet = None

    log_path = _guess_log(cwd, db_path, experiment)
    trade_phase_series: list[dict[str, float]] = []
    slot_delta_series: list[dict[str, float]] = []
    wallet_series: list[dict[str, float]] = []

    if project == "memeorator":
        # memeorator never persists positions/PnL to its DB — read its STATS block from
        # the log. Use a wider window than the display tail to reliably catch a STATS block
        # (graduation logging is very noisy between them).
        stats_lines = _tail_log(log_path, n_lines=600, max_bytes=262_144) if log_path else []
        mstats, mseries, mwr = _parse_memeorator_stats(stats_lines, create_time)
        if mstats is not None:
            positions = mstats
        pnl_series = mseries
        winrate_series = mwr
        # Same TX-time view as statalyzer: phase breakdown from the TIMING log line,
        # slots from the live_trades DB. (Both empty until memeorator lands live trades.)
        timing_lines = _grep_log_lines(log_path, "TIMING ") if log_path else []
        tphase, trade_phase_series = _parse_memeorator_timing(timing_lines, time.time())
        # On-chain wallet SOL over time, from the bot's 'WALLET: on_chain=' log lines.
        wallet_series = _memeorator_wallet_series(
            _grep_log_lines(log_path, "WALLET: on_chain="), time.time()) if log_path else []
        if tphase is not None:
            if positions is None:
                positions = {"open": 0, "closed": 0, "last_entry_time": None}
            positions["mean_trade_time_ms"] = tphase["mean_trade_time_ms"]
            positions["trade_phases"] = tphase["phases"]
        slots = _memeorator_slots(db_path) if db_path else None
        if slots is not None:
            if positions is None:
                positions = {"open": 0, "closed": 0, "last_entry_time": None}
            positions.update({
                "build_slot": slots["build_slot"],
                "confirm_slot": slots["confirm_slot"],
                "slot_delta": slots["slot_delta"],
                "mean_slot_delta": slots["mean_slot_delta"],
                "median_slot_delta": slots["median_slot_delta"],
            })
            slot_delta_series = slots["series"]
    else:
        pnl_series = _pnl_series(db_path, since_ts=stat_since) if db_path else []
        winrate_series = _winrate_series(db_path, since_ts=stat_since) if db_path else []
        # statalyzer combines sources:
        #   - wins/losses + win-rate chart  <- execution_log.captured_sol (per-swap, DB)
        #   - realized PnL + PnL chart      <- rebalancer log "portfolio X SOL (+Y)" delta
        #   - trade-time phase breakdown + slots <- executor "swap OK: build= submit= ..." log
        if db_path and project == "statalyzer":
            # PnL/wins source: rebalance execlog + log delta — only when the positions
            # table has nothing closed (pure rebalance mode). When real arb positions
            # exist, keep the positions-table PnL/series computed above.
            if not (positions and positions.get("closed")):
                rb = _statalyzer_execlog_stats(db_path, since_ts=create_time)
                if rb is not None:
                    positions, _, winrate_series = rb
                pnl_lines = _tail_log(log_path, n_lines=40000, max_bytes=4_194_304) if log_path else []
                latest_delta, log_series = _statalyzer_log_pnl(pnl_lines, time.time())
                if latest_delta is not None:
                    if positions is None:
                        positions = {"open": 0, "closed": 0, "last_entry_time": None}
                    positions["realized_pnl_sol"] = round(latest_delta, 6)
                    pnl_series = log_series
            # Trade-time + slots come from two log sources (grep'd so sparse markers are
            # found in the large per-run log):
            #   - "swap OK" lines: full build/submit/confirm phases + slots (SOL-direct
            #     swaps: startup inventory-split, rebalances). Sparse — often only startup.
            #   - reconciliation lines: a slot-Δ on EVERY close (inventory token<->token
            #     arb swaps, which log no phase line). This is what keeps slot Δ live.
            now_ts = time.time()
            swapok_lines = _grep_log_lines(log_path, "swap OK") if log_path else []
            phase_summary, phase_series = _statalyzer_trade_phases(swapok_lines, now_ts)
            recon_summary, recon_series = _statalyzer_recon_slots(
                _grep_log_lines(log_path, "econciliation"), now_ts) if log_path else (None, [])
            swapok_latest = phase_series[-1]["t"] if phase_series else None
            recon_latest = recon_series[-1]["t"] if recon_series else None
            # Prefer reconciliation when it's the fresher source (current arb mode): per-close
            # slot Δ, with the trade-time estimated from slots (no per-trade phase ms exists).
            if recon_summary is not None and (swapok_latest is None or (recon_latest or 0) >= swapok_latest):
                if positions is None:
                    positions = {"open": 0, "closed": 0, "last_entry_time": None}
                positions.update({
                    "mean_trade_time_ms": round(recon_summary["median_slot_delta"] * 400, 1),
                    "trade_phases": None,  # not logged for inventory arb swaps
                    "mean_slot_delta": recon_summary["mean_slot_delta"],
                    "median_slot_delta": recon_summary["median_slot_delta"],
                    "build_slot": recon_summary["build_slot"],
                    "confirm_slot": recon_summary["confirm_slot"],
                    "slot_delta": recon_summary["slot_delta"],
                })
                trade_phase_series = []
                slot_delta_series = recon_series
            elif phase_summary is not None:
                if positions is None:
                    positions = {"open": 0, "closed": 0, "last_entry_time": None}
                positions.update({
                    "mean_trade_time_ms": phase_summary["mean_trade_time_ms"],
                    "trade_phases": phase_summary["phases"],
                    "mean_slot_delta": phase_summary["mean_slot_delta"],
                    "median_slot_delta": phase_summary["median_slot_delta"],
                    "build_slot": phase_summary["build_slot"],
                    "confirm_slot": phase_summary["confirm_slot"],
                    "slot_delta": phase_summary["slot_delta"],
                })
                trade_phase_series = phase_series
                slot_delta_series = [
                    {"t": p["t"], "slot_delta": p["slot_delta"]}
                    for p in phase_series if p.get("slot_delta") is not None
                ]

    # Live on-chain SOL wallet balance chart: for any LIVE bot with a known wallet, reuse
    # the getBalance samples the watcher already collects each poll (see _chain_sol_balance
    # / _CHAIN_BAL_HISTORY). This drives the statalyzer wallet chart. memeorator already
    # builds its own wallet_series from log lines above, so don't clobber it.
    if chain_pubkey and mode == "LIVE" and not wallet_series:
        wallet_series = _chain_balance_series(chain_pubkey)
        if reset_ts is not None:
            wallet_series = [p for p in wallet_series if p["t"] >= reset_ts]

    # Scope statalyzer's per-close slot-Δ series to the reset/run window so a long log tail
    # (which can span days of reconciliation lines) doesn't stretch the chart's x-axis.
    if project == "statalyzer" and stat_since is not None:
        slot_delta_series = [p for p in slot_delta_series if p["t"] >= stat_since]
        trade_phase_series = [p for p in trade_phase_series if p["t"] >= stat_since]

    log_tail = _tail_log(log_path) if log_path else []

    return {
        "pid": proc.pid,
        "running": True,
        "project": project,
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
        "pnl_series": pnl_series,
        "winrate_series": winrate_series,
        "balance_series": (_balance_series(db_path, since_ts=stat_since) if (db_path and project == "statalyzer") else []),
        "trade_phase_series": trade_phase_series,
        "slot_delta_series": slot_delta_series,
        "wallet_series": wallet_series,
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


def _build_bots(sol_price: float | None = None) -> list[dict[str, Any]]:
    """Only running bots are surfaced — non-running/registered roles are not displayed."""
    bots = _scan_running(sol_price)
    bots.sort(key=lambda b: (b["project"], b["script"], b["name"]))
    return bots


# --- Trade-log sections ------------------------------------------------------
# Standalone cards summarising a trade .jsonl (one JSON record per line). Config
# per section:
#   pnl_key       — the per-trade PnL field (e.g. est_pnl SOL, or realized_net fraction)
#   unit          — "SOL" (format as SOL) or "net" (plain signed number)
#   entered_key   — a truthiness gate field (e.g. "entered"); None = every record counts
#   dedupe_mint   — collapse to one record per mint (last wins); False = every line is a trade
#   tag/tag_class — badge shown on the card
_SECTION_CONFIGS = [
    {
        "title": "BC live",
        "path": HOME / "memeorator" / "bc_live_trades.jsonl",
        "pnl_key": "est_pnl",
        "unit": "SOL",
        "entered_key": None,
        "dedupe_mint": False,
        "tag": "live",
        "tag_class": "live",
        "wallet_pubkey": "FyXKk2Bs4Du82Lw3nE2g2ifQ2rL7ZoRzJdCBVZddH5si",
        "timing_log": Path("/home/ubuntu/memeorator/bc_staged.log"),
        "log_file": Path("/home/ubuntu/memeorator/bc_staged.log"),  # tail shown on the card
        # Per-trade "buy_swap" (swap index at entry) from bc_real_trades.jsonl.
        "buy_swap_file": HOME / "memeorator" / "bc_real_trades.jsonl",
        # Global reset marker shared with the bot cards (see _RESET_FILE).
        "reset_file": _RESET_FILE,
    },
]


def _read_reset_ts(path: Path | None) -> float | None:
    if path is None:
        return None
    try:
        return float(path.read_text().strip())
    except (OSError, ValueError):
        return None


def _buy_swap_stats(path: Path, reset_ts: float | None = None, max_points: int = 120) -> dict[str, Any]:
    """Per-trade `buy_swap` (swap index at entry) from a jsonl (each line has ts + buy_swap).
    Returns {buy_swap (latest), median_buy_swap, mean_buy_swap, buy_swap_series} or {}."""
    if not path.exists() or not path.is_file():
        return {}
    try:
        rows: list[tuple[float, float]] = []
        with path.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    x = json.loads(line)
                except json.JSONDecodeError:
                    continue
                bs, ts = x.get("buy_swap"), x.get("ts")
                if bs is None or ts is None:
                    continue
                if reset_ts is not None and float(ts) < reset_ts:
                    continue
                rows.append((float(ts), float(bs)))
        if not rows:
            return {}
        rows.sort()
        vals = [v for _, v in rows]
        return {
            "buy_swap": int(rows[-1][1]),
            "median_buy_swap": _median(vals),
            "mean_buy_swap": round(sum(vals) / len(vals), 2),
            "buy_swap_series": [{"t": t, "buy_swap": round(v, 2)} for t, v in _downsample(rows, max_points)],
        }
    except OSError:
        return {}

# bc_live.py per-trade timing, e.g.:
#   15:58:31 TIMING 6yft7ZE4 | signal->enter=5 enter->buildstart=0 build=0 sign=0
#   submit_post=3 ack=0 submit->fill=196 | TOTAL signal->fill=205ms
#   15:58:33 SLOTS 6yft7ZE4 decide_slot=430552386 landed_slot=430552387 diff=1
# Phases bucketed into the same dispatch/build/submit/confirm shape as the bot cards.
_BC_TIMING_RE = re.compile(r"\bTIMING\b.*?\|(.*?)\|\s*TOTAL\s+signal->fill=(\d+)\s*ms")
_BC_KV_RE = re.compile(r"([A-Za-z_>\-]+)=(\d+)")
_BC_SLOTS_RE = re.compile(r"\bSLOTS\b.*?decide_slot=(\d+)\s+landed_slot=(\d+)\s+diff=(-?\d+)")


def _bc_live_timings(log_path: Path, now: float, reset_ts: float | None = None,
                     max_points: int = 120) -> dict[str, Any]:
    out: dict[str, Any] = {"trade_phase_series": [], "slot_delta_series": []}

    def _parse(lines, matcher):
        # HH:MM:SS only → walk in file (chronological) order, bumping the day on each
        # rollover, then anchor the LAST line to `now`. Monotonic and correct across
        # multi-day spans (a plain today-midnight+sod mis-dates older lines).
        day = 0
        prev: int | None = None
        rel = []
        for ln in lines:
            mts = _LOG_TS_RE.match(ln)
            m = matcher(ln)
            if not mts or m is None:
                continue
            sod = int(mts.group(1)) * 3600 + int(mts.group(2)) * 60 + int(mts.group(3))
            if prev is not None and sod < prev - 3600:
                day += 1
            prev = sod
            rel.append((day * 86400 + sod, m))
        if not rel:
            return []
        last = rel[-1][0]
        rows = [(now - (last - r), m) for r, m in rel]
        if reset_ts is not None:
            rows = [(t, m) for t, m in rows if t >= reset_ts]
        return rows

    # --- TIMING → phase breakdown ---
    def _timing(ln):
        m = _BC_TIMING_RE.search(ln)
        if not m:
            return None
        total = int(m.group(2))
        kv = {k: int(v) for k, v in _BC_KV_RE.findall(m.group(1))}
        build = kv.get("enter->buildstart", 0) + kv.get("build", 0) + kv.get("sign", 0)
        submit = kv.get("submit_post", 0) + kv.get("ack", 0)
        confirm = kv.get("submit->fill", 0)
        dispatch = max(0, total - build - submit - confirm)
        return (dispatch, build, submit, confirm, total)

    traw = _parse(_grep_log_lines(log_path, " TIMING "), _timing)
    if traw:
        n = len(traw)
        out["mean_trade_time_ms"] = round(sum(p[4] for _, p in traw) / n, 1)
        out["trade_phases"] = {
            "dispatch": round(sum(p[0] for _, p in traw) / n, 1),
            "build": round(sum(p[1] for _, p in traw) / n, 1),
            "submit": round(sum(p[2] for _, p in traw) / n, 1),
            "confirm": round(sum(p[3] for _, p in traw) / n, 1),
        }
        out["trade_phase_series"] = [
            {"t": t, "dispatch": p[0], "build": p[1], "submit": p[2], "confirm": p[3]}
            for t, p in _downsample(traw, max_points)
        ]

    # --- SLOTS → slot deltas ---
    def _slots(ln):
        m = _BC_SLOTS_RE.search(ln)
        if not m:
            return None
        diff = int(m.group(3))
        if diff < 0 or diff > _SLOT_DELTA_MAX:
            return None
        return (int(m.group(1)), int(m.group(2)), diff)

    sraw = _parse(_grep_log_lines(log_path, " SLOTS "), _slots)
    if sraw:
        deltas = [p[2] for _, p in sraw]
        last = sraw[-1][1]
        out["build_slot"] = last[0]
        out["confirm_slot"] = last[1]
        out["slot_delta"] = last[2]
        out["mean_slot_delta"] = round(sum(deltas) / len(deltas), 2)
        out["median_slot_delta"] = _median(deltas)
        out["slot_delta_series"] = [
            {"t": t, "slot_delta": p[2]} for t, p in _downsample(sraw, max_points)
        ]
    return out


def _trades_section(cfg: dict[str, Any], max_points: int = 200, tail_lines: int = 40) -> dict[str, Any] | None:
    path: Path = cfg["path"]
    if not path.exists() or not path.is_file():
        return None
    pnl_key = cfg["pnl_key"]
    entered_key = cfg.get("entered_key")
    try:
        recs: list[dict[str, Any]] = []
        by_mint: dict[Any, dict[str, Any]] = {}
        with path.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if cfg.get("dedupe_mint"):
                    m = rec.get("mint")
                    if m is not None:
                        by_mint[m] = rec
                else:
                    recs.append(rec)
        if cfg.get("dedupe_mint"):
            recs = list(by_mint.values())
        reset_ts = _read_reset_ts(cfg.get("reset_file"))
        trades = [
            x for x in recs
            if (entered_key is None or x.get(entered_key)) and x.get(pnl_key) is not None
            and (reset_ts is None or (x.get("ts") or 0) >= reset_ts)
        ]
        trades.sort(key=lambda x: x.get("ts") or 0)
        n = len(trades)
        wins = sum(1 for x in trades if float(x[pnl_key]) > 0)
        cum = 0.0
        raw: list[tuple[float, float, float]] = []  # (ts, cum, running_mean)
        for i, x in enumerate(trades, 1):
            cum += float(x[pnl_key])
            ts = x.get("ts")
            if ts is not None:
                raw.append((float(ts), cum, cum / i))
        if len(raw) > max_points:
            stride = len(raw) / max_points
            raw = [raw[min(len(raw) - 1, int(i * stride))] for i in range(max_points)] + [raw[-1]]
        series = [{"t": t, "cum": round(c, 6), "mean": round(mn, 6)} for t, c, mn in raw]
        # On-chain wallet SOL over time (watcher-sampled history) for the wallet chart.
        wallet_series: list[dict[str, float]] = []
        wp = cfg.get("wallet_pubkey")
        if wp:
            _chain_sol_balance(wp)  # take/refresh a sample this request
            wallet_series = _chain_balance_series(wp)
            if reset_ts is not None:
                wallet_series = [p for p in wallet_series if p["t"] >= reset_ts]
        out = {
            "kind": "trades",
            "title": cfg["title"],
            "source": path.name,
            "unit": cfg.get("unit", "SOL"),
            "wallet_series": wallet_series,
            "tag": cfg.get("tag", "live"),
            "tag_class": cfg.get("tag_class", "live"),
            "observed": len(recs),
            "entered": n,
            "wins": wins,
            "losses": n - wins,
            "win_rate": round(wins / n, 4) if n else None,
            "mean_realized": round(cum / n, 6) if n else None,
            "cum_pnl": round(cum, 6),
            "series": series,
            "log_tail": _tail_log(cfg.get("log_file") or path, n_lines=tail_lines),
            "updated": trades[-1].get("ts") if trades else None,
        }
        # Per-trade timing (build/submit/confirm) + slot deltas from the bot's log.
        bsf = cfg.get("buy_swap_file")
        if bsf is not None:
            out.update(_buy_swap_stats(bsf, reset_ts))
        tlog = cfg.get("timing_log")
        if tlog is not None:
            out.update(_bc_live_timings(tlog, time.time(), reset_ts))
            # Currently-open positions = latest "open=N" the bot logged (live state, not
            # reset-scoped). Closed = post-reset completed trades (each jsonl line is a sell).
            for ln in reversed(_grep_log_lines(tlog, "open=")):
                mo = re.search(r"\bopen=(\d+)", ln)
                if mo:
                    out["open_trades"] = int(mo.group(1))
                    break
        out["closed_trades"] = n
        return out
    except OSError:
        return None


def _paper_sections() -> list[dict[str, Any]]:
    out = []
    for cfg in _SECTION_CONFIGS:
        s = _trades_section(cfg)
        if s is not None:
            out.append(s)
    return out


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
        "sections": _paper_sections(),
    }


@app.get("/api/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
