const REFRESH_MS = 10_000;
let currentInflight = new Set();

function fmtUptime(s) {
  if (!s) return "–";
  if (s < 60) return `${s}s`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m}m`;
  const h = Math.floor(m / 60);
  const rm = m % 60;
  if (h < 48) return `${h}h ${rm}m`;
  const d = Math.floor(h / 24);
  const rh = h % 24;
  return `${d}d ${rh}h`;
}

function fmtPnl(v) {
  if (v === null || v === undefined) return "–";
  const sign = v > 0 ? "+" : "";
  return `${sign}${v.toFixed(4)}`;
}

function el(tag, attrs = {}, children = []) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") e.className = v;
    else if (k === "html") e.innerHTML = v;
    else if (k.startsWith("on") && typeof v === "function") e.addEventListener(k.slice(2), v);
    else e.setAttribute(k, v);
  }
  for (const c of [].concat(children)) {
    if (c == null) continue;
    e.append(c.nodeType ? c : document.createTextNode(c));
  }
  return e;
}

async function act(kind, bot, btn) {
  const key = bot.role_key;
  if (!key) {
    alert("this bot has no registered role — can't " + kind);
    return;
  }
  const verb = kind === "stop" ? "STOP" : "START";
  const label = bot.name + (bot.mode === "LIVE" ? " (LIVE!)" : "");
  if (!confirm(`${verb} ${label}?\n\nkey: ${key}`)) return;
  if (bot.mode === "LIVE" && kind === "stop") {
    if (!confirm(`This bot is LIVE. Really stop it? Open positions may remain unmanaged.`)) return;
  }

  const inflightKey = `${kind}:${key}`;
  if (currentInflight.has(inflightKey)) return;
  currentInflight.add(inflightKey);
  btn.disabled = true;
  btn.textContent = kind === "stop" ? "stopping…" : "starting…";

  try {
    const r = await fetch(`/api/${kind}/${encodeURIComponent(key)}`, { method: "POST" });
    const j = await r.json();
    if (!r.ok || j.ok === false) {
      alert(`${kind} failed: ${JSON.stringify(j)}`);
    } else {
      btn.textContent = kind === "stop" ? "stopped" : "started";
    }
  } catch (e) {
    alert(`${kind} error: ${e.message}`);
  } finally {
    currentInflight.delete(inflightKey);
    setTimeout(refresh, 500);
  }
}

function renderBot(bot) {
  const running = bot.running;
  const modeClass = bot.mode === "LIVE" ? "live"
                  : bot.mode === "DRY-RUN" ? "dry"
                  : bot.mode === "STOPPED" ? "stopped"
                  : "dry";
  const modeTag = el("span", { class: "tag " + modeClass }, bot.mode);
  const projTag = el("span", { class: "tag project" }, bot.project);

  const head = el("div", { class: "head" }, [
    el("div", { class: "title" }, [
      el("div", { class: "name" }, bot.name),
      el("div", { class: "sub" }, running ? `${bot.script} · pid ${bot.pid}` : `${bot.script} · not running`),
    ]),
    el("div", { class: "tags" }, [projTag, modeTag]),
  ]);

  const pos = bot.positions || {};
  const pnl = pos.realized_pnl;
  const pnlClass = pnl == null ? "" : pnl > 0 ? "good" : pnl < 0 ? "bad" : "";

  const body = el("div", { class: "body" }, [
    el("div", { class: "kv" }, [
      el("div", { class: "k" }, "uptime"),
      el("div", { class: "v" }, running ? fmtUptime(bot.uptime_s) : "–"),
    ]),
    el("div", { class: "kv" }, [
      el("div", { class: "k" }, "cpu / mem"),
      el("div", { class: "v" }, running ? `${bot.cpu_pct}% · ${bot.mem_mb.toFixed(0)}MB` : "–"),
    ]),
    el("div", { class: "kv" }, [
      el("div", { class: "k" }, "positions"),
      el("div", { class: "v" },
        pos.open != null ? `${pos.open} open / ${pos.closed} closed` : "–"),
    ]),
    el("div", { class: "kv" }, [
      el("div", { class: "k" }, "realized pnl"),
      el("div", { class: "v " + pnlClass }, fmtPnl(pnl)),
    ]),
  ]);

  const logLines = bot.log_tail || [];
  const logPane = logLines.length
    ? el("pre", { class: "log" }, logLines.join("\n"))
    : el("pre", { class: "log empty" }, "(no log file found)");

  // ACTIONS
  const canStart = bot.can_start;
  const canStop = bot.can_stop;
  const actions = el("div", { class: "actions" }, []);
  const startBtn = el("button", {
    class: "btn start" + (bot.mode === "LIVE" ? " live" : ""),
    disabled: !canStart || !bot.role_key ? "disabled" : null,
    title: bot.role_key ? "" : "no role mapping — add to deploy/bot_commands.json",
  }, "▶ start");
  const stopBtn = el("button", {
    class: "btn stop" + (bot.mode === "LIVE" ? " live" : ""),
    disabled: !canStop || !bot.role_key ? "disabled" : null,
    title: bot.role_key ? "" : "no role mapping — add to deploy/bot_commands.json",
  }, "■ stop");
  if (canStart && bot.role_key) {
    startBtn.addEventListener("click", () => act("start", bot, startBtn));
  }
  if (canStop && bot.role_key) {
    stopBtn.addEventListener("click", () => act("stop", bot, stopBtn));
  }
  actions.append(startBtn, stopBtn);

  const cmd = el("div", { class: "cmd", title: bot.cmdline }, bot.cmdline);

  return el("div", { class: "bot" + (running ? "" : " not-running") }, [head, body, actions, logPane, cmd]);
}

function renderSummary(bots) {
  const running = bots.filter(b => b.running);
  const live = running.filter(b => b.mode === "LIVE").length;
  const dry = running.filter(b => b.mode === "DRY-RUN").length;
  const stopped = bots.filter(b => !b.running).length;
  let openPos = 0, closedPos = 0, pnl = 0;
  for (const b of running) {
    const p = b.positions;
    if (!p) continue;
    openPos += p.open || 0;
    closedPos += p.closed || 0;
    pnl += p.realized_pnl || 0;
  }
  const pnlClass = pnl > 0 ? "good" : pnl < 0 ? "bad" : "";
  const root = document.getElementById("summary");
  root.replaceChildren(
    el("div", { class: "card" }, [el("div", { class: "label" }, "running"), el("div", { class: "value" }, String(running.length))]),
    el("div", { class: "card" }, [el("div", { class: "label" }, "live"), el("div", { class: "value" }, String(live))]),
    el("div", { class: "card" }, [el("div", { class: "label" }, "dry-run"), el("div", { class: "value" }, String(dry))]),
    el("div", { class: "card" }, [el("div", { class: "label" }, "stopped"), el("div", { class: "value" }, String(stopped))]),
    el("div", { class: "card" }, [el("div", { class: "label" }, "open positions"), el("div", { class: "value" }, String(openPos))]),
    el("div", { class: "card" }, [el("div", { class: "label" }, "total realized pnl"), el("div", { class: "value " + pnlClass }, fmtPnl(pnl))]),
  );
}

async function refresh() {
  const statusEl = document.getElementById("refresh-status");
  try {
    const r = await fetch("/api/status", { cache: "no-store" });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const data = await r.json();
    document.getElementById("host").textContent = data.host;
    document.getElementById("clock").textContent = new Date(data.now * 1000).toISOString().replace("T", " ").slice(0, 19) + "Z";
    renderSummary(data.bots);
    const root = document.getElementById("bots");
    if (!data.bots.length) {
      root.replaceChildren(el("div", { class: "empty-state" }, "no bots detected or registered"));
    } else {
      root.replaceChildren(...data.bots.map(renderBot));
    }
    statusEl.textContent = "ok";
    statusEl.className = "ok";
  } catch (e) {
    statusEl.textContent = `error: ${e.message}`;
    statusEl.className = "err";
  }
}

refresh();
setInterval(refresh, REFRESH_MS);
