import React, { useEffect, useRef } from 'react'
import { fmtUptime, fmtPnlSol, fmtSol, fmtMs } from './format.js'
import { PnlChart, WalletChart, BalanceChart, TradePhaseChart, SlotDeltaChart } from './charts.jsx'

function KV({ k, v, cls = '', sub = false }) {
  return (
    <div className={'kv' + (sub ? ' sub' : '')}>
      <div className="k">{k}</div>
      <div className={'v ' + cls}>{v}</div>
    </div>
  )
}

function pnlCls(v) {
  return v == null ? '' : v > 0 ? 'good' : v < 0 ? 'bad' : ''
}

export default function BotCard({ bot }) {
  const running = bot.running
  const isStat = bot.project === 'statalyzer'
  const pos = bot.positions || {}
  const wallet = bot.wallet && !bot.wallet.error ? bot.wallet : null
  const bal = bot.balance_series || []

  const modeClass =
    bot.mode === 'LIVE' ? 'live' : bot.mode === 'STOPPED' ? 'stopped' : 'dry'

  const rows = []
  rows.push(<KV key="uptime" k="uptime" v={running ? fmtUptime(bot.uptime_s) : '–'} />)

  rows.push(
    <KV key="cpumem" k="cpu / mem"
      v={running ? `${bot.cpu_pct}% · ${bot.mem_mb.toFixed(0)}MB` : '–'} />
  )

  // wins/losses (bots with per-trade outcomes) else positions
  if (pos.wins != null || pos.losses != null) {
    rows.push(<KV key="wins" k="wins" v={String(pos.wins || 0)} cls="good" />)
    rows.push(<KV key="losses" k="losses" v={String(pos.losses || 0)} cls="bad" />)
  } else {
    rows.push(
      <KV key="positions" k="positions"
        v={pos.open != null ? `${pos.open} open / ${pos.closed} closed` : '–'} />
    )
  }

  // realized pnl — hidden for statalyzer (noisy/price-based)
  if (!isStat) {
    rows.push(<KV key="realized" k="realized pnl" v={fmtPnlSol(pos.realized_pnl_sol)}
      cls={pnlCls(pos.realized_pnl_sol)} />)
  }

  // mean trade time + phase sub-rows
  if (pos.mean_trade_time_ms != null) {
    rows.push(<KV key="mtt" k="mean trade time" v={fmtMs(pos.mean_trade_time_ms)} />)
    const ph = pos.trade_phases || {}
    for (const [key, label] of [['dispatch', '· dispatch'], ['build', '· build'], ['submit', '· submit'], ['confirm', '· confirm']]) {
      if (ph[key] == null) continue
      rows.push(<KV key={'ph-' + key} k={label} v={fmtMs(ph[key])} sub />)
    }
  }

  // slots
  if (pos.build_slot != null || pos.confirm_slot != null) {
    rows.push(<KV key="bslot" k="build slot" v={pos.build_slot != null ? String(pos.build_slot) : '–'} />)
    rows.push(<KV key="cslot" k="confirm slot" v={pos.confirm_slot != null ? String(pos.confirm_slot) : '–'} />)
    const med = pos.median_slot_delta
    const slotMsEst = med != null ? ` · ~${Math.round(med * 400)}ms` : ''
    const medStr = med != null ? ` (med ${med}${slotMsEst})` : ''
    rows.push(<KV key="slotd" k="slot Δ"
      v={(pos.slot_delta != null ? String(pos.slot_delta) : '–') + medStr} />)
  }

  rows.push(<KV key="walletsol" k="wallet sol" v={wallet ? fmtSol(wallet.sol) : '–'} />)

  // charts (mirrors the vanilla conditional order)
  const charts = []
  if (!isStat) charts.push(<PnlChart key="pnl" data={bot.pnl_series || []} />)
  if (bal.length >= 2) charts.push(<BalanceChart key="bal" data={bal} />)
  if ((bot.wallet_series || []).length >= 2) charts.push(<WalletChart key="wal" data={bot.wallet_series} />)
  if ((bot.trade_phase_series || []).length) charts.push(<TradePhaseChart key="tp" data={bot.trade_phase_series} />)
  if ((bot.slot_delta_series || []).length >= 2) charts.push(<SlotDeltaChart key="sd" data={bot.slot_delta_series} />)

  // log tail — auto-scroll to bottom on update
  const logLines = bot.log_tail || []
  const logRef = useRef(null)
  useEffect(() => {
    if (logRef.current) logRef.current.scrollTop = logRef.current.scrollHeight
  }, [logLines])

  return (
    <div className={'bot' + (running ? '' : ' not-running')}>
      <div className="head">
        <div className="title">
          <div className="name">{bot.name}</div>
          <div className="sub">{running ? `${bot.script} · pid ${bot.pid}` : `${bot.script} · not running`}</div>
        </div>
        <div className="tags">
          <span className="tag project">{bot.project}</span>
          <span className={'tag ' + modeClass}>{bot.mode}</span>
        </div>
      </div>

      <div className="body">{rows}</div>

      {charts.length > 0 && <>
        <div className="chart-status">Gathering data for retrain</div>
        <div className="chart-wrap">{charts}</div>
      </>}

      {logLines.length
        ? <pre className="log" ref={logRef}>{logLines.join('\n')}</pre>
        : <pre className="log empty">(no log file found)</pre>}

      <div className="cmd" title={bot.cmdline}>{bot.cmdline}</div>
    </div>
  )
}
