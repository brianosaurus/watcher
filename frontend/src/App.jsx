import React, { useEffect, useState } from 'react'
import BotCard from './BotCard.jsx'
import SectionCard from './SectionCard.jsx'
import OptimumCard from './OptimumCard.jsx'
import { fmtUsd, fmtPnlSol, fmtClock } from './format.js'

const REFRESH_MS = 10_000

function useStatus() {
  const [data, setData] = useState(null)
  const [status, setStatus] = useState({ text: 'idle', ok: true })

  useEffect(() => {
    let alive = true
    async function refresh() {
      try {
        const r = await fetch('/api/status', { cache: 'no-store' })
        if (!r.ok) throw new Error(`HTTP ${r.status}`)
        const json = await r.json()
        if (!alive) return
        setData(json)
        setStatus({ text: 'ok', ok: true })
      } catch (e) {
        if (!alive) return
        setStatus({ text: `error: ${e.message}`, ok: false })
      }
    }
    refresh()
    const id = setInterval(refresh, REFRESH_MS)
    return () => { alive = false; clearInterval(id) }
  }, [])

  return { data, status }
}

function SummaryBar({ bots, sections }) {
  const running = bots.filter((b) => b.running)
  const live = running.filter((b) => b.mode === 'LIVE').length
  const dry = running.filter((b) => b.mode === 'DRY-RUN').length
  let openPos = 0
  for (const b of running) {
    openPos += b.positions?.open || 0
  }
  // "total realized pnl" = the visible gains: statalyzer's cash-line increase (native
  // now − start) + each trade section's wallet-chart increase (sol now − start).
  let pnl = 0
  for (const b of bots) {
    const bal = b.balance_series || []
    if (b.project === 'statalyzer' && bal.length >= 2) {
      pnl += bal[bal.length - 1].native - bal[0].native
    }
  }
  for (const s of sections) {
    const ws = s.wallet_series || []
    if (ws.length >= 2) pnl += ws[ws.length - 1].sol - ws[0].sol
  }
  const cards = [
    ['running', String(running.length), ''],
    ['live', String(live), ''],
    ['dry-run', String(dry), ''],
    ['open positions', String(openPos), ''],
    ['total realized pnl', fmtPnlSol(pnl), pnl > 0 ? 'good' : pnl < 0 ? 'bad' : ''],
  ]
  return (
    <section className="summary">
      {cards.map(([label, value, cls]) => (
        <div className="card" key={label}>
          <div className="label">{label}</div>
          <div className={'value ' + cls}>{value}</div>
        </div>
      ))}
    </section>
  )
}

export default function App() {
  const { data, status } = useStatus()
  const bots = data?.bots || []
  const sections = data?.sections || []

  return (
    <>
      <header>
        <div className="brand">
          <img src="/static/leeroy_chainkins.png" alt="Leeroy Chainkins" className="logo" />
          <h1>Leeroy Chainkins</h1>
        </div>
        <div className="meta">
          <span>{data?.host ?? '–'}</span>
          <span>{data?.sol_usd_price ? `SOL ${fmtUsd(data.sol_usd_price)}` : 'SOL –'}</span>
          <span>{data ? fmtClock(data.now) : '–'}</span>
          <span className={status.ok ? 'ok' : 'err'}>{status.text}</span>
        </div>
      </header>

      <main>
        <SummaryBar bots={bots} sections={sections} />
        <OptimumCard />
        <section className="bots">
          {bots.length === 0 && sections.length === 0
            ? <div className="empty-state">no bots running</div>
            : bots.map((b) => <BotCard key={`${b.project}:${b.name}:${b.pid ?? 'x'}`} bot={b} />)}
          {sections.map((s) => <SectionCard key={s.source} section={s} />)}
        </section>
      </main>

      <footer>
        <span>auto-refresh every 10s · <a href="/api/status">raw json</a></span>
      </footer>
    </>
  )
}
