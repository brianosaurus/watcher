import React, { useEffect, useMemo, useRef, useState } from 'react'

/**
 * Optimum — Ethereum block-propagation latency counterfactual.
 *
 * A live ticker of the profit a staking operator WOULD gain from a propagation
 * accelerator, priced slot-by-slot off the real mainnet beacon head.
 *
 * DESIGN CONSTRAINT, and it is not negotiable: this is NOT revenue. mump2p is not
 * deployed on Ethereum mainnet, so nobody is earning a cent of this. A number that
 * climbs on a public page reads as money by default, so the counterfactual framing
 * is baked into the component itself — the banner is not dismissible, the word
 * "would" is in the headline, and the channel breakdown carries the caveat that
 * ~93% of the value only materialises if the operator ALSO re-tunes its timing
 * games. Do not "clean up" the disclaimer.
 *
 * The smooth increment is an expected-value accrual over observed slots, not a
 * realised cashflow. Real gains are lumpy (an operator proposes a block every few
 * hours); the ticker interpolates so the eye can read a rate.
 */

const SPEEDUPS = ['6x', '3x', '2x']

const CHANNELS = [
  { key: 'a', label: 'Attester head votes', hint: 'receive-side: my nodes see blocks sooner' },
  { key: 'b', label: 'Proposer reorgs avoided', hint: 'my late blocks not orphaned' },
  { key: 'c', label: 'MEV: delay budget', hint: 'publish later, catch a better bid' },
]

function usd(n, dp = 2) {
  if (n == null || !isFinite(n)) return '–'
  return n.toLocaleString('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: dp, maximumFractionDigits: dp })
}

/**
 * The ticker. We take the server's cumulative total plus its per-second rate and
 * interpolate locally at 10Hz, so the number visibly climbs between the 10s API
 * polls instead of stepping.
 *
 * Anchored to the server value on every refresh — it never free-runs, so it
 * cannot drift away from the truth.
 */
function useTicker(baseUsd, ratePerSec) {
  const [val, setVal] = useState(baseUsd || 0)
  const anchor = useRef({ base: baseUsd || 0, at: Date.now() })

  useEffect(() => {
    anchor.current = { base: baseUsd || 0, at: Date.now() }
    setVal(baseUsd || 0)
  }, [baseUsd])

  useEffect(() => {
    if (!ratePerSec) return
    const id = setInterval(() => {
      const dt = (Date.now() - anchor.current.at) / 1000
      setVal(anchor.current.base + ratePerSec * dt)
    }, 100)
    return () => clearInterval(id)
  }, [ratePerSec])

  return val
}

function ArrivalSparkline({ recent, deadlineMs }) {
  if (!recent?.length) return null
  const W = 260, H = 44
  const max = Math.max(6000, ...recent.map((r) => r.arrival_ms))
  const step = W / Math.max(1, recent.length - 1)
  const y = (ms) => H - (ms / max) * H
  const pts = recent.map((r, i) => `${i * step},${y(r.arrival_ms)}`).join(' ')

  return (
    <svg className="opt-spark" width={W} height={H} viewBox={`0 0 ${W} ${H}`} role="img"
         aria-label="recent block arrival times">
      {/* The 4s attestation deadline — the line the whole model turns on. */}
      <line x1="0" x2={W} y1={y(deadlineMs)} y2={y(deadlineMs)}
            stroke="#d95f0e" strokeWidth="1" strokeDasharray="3 3" />
      <polyline points={pts} fill="none" stroke="#2c7fb8" strokeWidth="1.5" />
      {recent.map((r, i) => r.late ? (
        <circle key={r.slot} cx={i * step} cy={y(r.arrival_ms)} r="2.5" fill="#d95f0e" />
      ) : null)}
    </svg>
  )
}

function OperatorRow({ op, speedup, ethPrice }) {
  const sc = op.scenarios?.[speedup]
  const live = useTicker(sc?.usd_total, sc?.usd_per_sec)
  if (!sc) return null

  const total = sc.usd_a + sc.usd_b + sc.usd_c || 1
  // Channel widths show WHERE the value is. In practice C dominates so hard that
  // the bar is the argument: this product is an MEV timing play, not a
  // reliability play.
  const pct = (v) => `${Math.max(0, (v / total) * 100)}%`

  return (
    <div className="opt-row">
      <div className="opt-row-head">
        <span className="opt-op">{op.operator}</span>
        <span className="opt-val">{op.validators.toLocaleString()} val</span>
        <span className="opt-ticker">{usd(live, 4)}</span>
        <span className="opt-rate">{usd(sc.usd_per_year, 0)}/yr run-rate</span>
      </div>
      <div className="opt-bar" title="A / B / C share of modelled uplift">
        <span className="opt-seg opt-a" style={{ width: pct(sc.usd_a) }} />
        <span className="opt-seg opt-b" style={{ width: pct(sc.usd_b) }} />
        <span className="opt-seg opt-c" style={{ width: pct(sc.usd_c) }} />
      </div>
    </div>
  )
}

export default function OptimumCard() {
  const [data, setData] = useState(null)
  const [err, setErr] = useState(null)
  const [speedup, setSpeedup] = useState('6x')

  useEffect(() => {
    let alive = true
    async function refresh() {
      try {
        const r = await fetch('/api/optimum', { cache: 'no-store' })
        if (!r.ok) throw new Error(`HTTP ${r.status}`)
        const j = await r.json()
        if (alive) { setData(j); setErr(null) }
      } catch (e) {
        if (alive) setErr(e.message)
      }
    }
    refresh()
    const id = setInterval(refresh, 10_000)
    return () => { alive = false; clearInterval(id) }
  }, [])

  const totals = useMemo(() => {
    const all = data?.operators?.find((o) => o.operator === 'ALL SEVEN')
    return all?.scenarios?.[speedup]
  }, [data, speedup])

  if (err) return <div className="card opt-card"><h2>Optimum</h2><div className="err">error: {err}</div></div>
  if (!data) return <div className="card opt-card"><h2>Optimum</h2><div className="muted">loading…</div></div>

  if (!data.available) {
    return (
      <div className="card opt-card">
        <h2>Optimum: Ethereum propagation latency</h2>
        <div className="opt-warn">{data.disclaimer}</div>
        <div className="muted">tracker not running yet ({data.reason})</div>
      </div>
    )
  }

  return (
    <div className="card opt-card">
      <h2>Optimum: what faster block propagation would be worth</h2>

      {/* Not dismissible, not collapsible, not small print. A climbing number on a
          public page is read as revenue unless you say otherwise, loudly. */}
      <div className="opt-warn">
        <strong>Modelled counterfactual: nobody is earning this.</strong>{' '}
        {data.disclaimer}
      </div>

      <div className="opt-controls">
        {SPEEDUPS.map((s) => (
          <button key={s}
                  className={s === speedup ? 'on' : ''}
                  onClick={() => setSpeedup(s)}>
            {s}{s === '6x' ? ' (vendor claim)' : ''}
          </button>
        ))}
      </div>

      <div className="opt-live">
        <div className="opt-stat">
          <span className="k">slots observed</span>
          <span className="v">{data.slots_observed.toLocaleString()}</span>
        </div>
        <div className="opt-stat">
          <span className="k">mean arrival</span>
          <span className="v">{Math.round(data.avg_arrival_ms)} ms</span>
        </div>
        <div className="opt-stat">
          <span className="k">past 4s deadline</span>
          <span className="v">{data.late_pct.toFixed(2)}%</span>
        </div>
        <div className="opt-stat">
          <span className="k">ETH</span>
          <span className="v">{usd(data.eth_usd_price, 0)}</span>
        </div>
      </div>

      <ArrivalSparkline recent={data.recent} deadlineMs={data.deadline_ms} />

      <div className="opt-legend">
        {CHANNELS.map((c) => (
          <span key={c.key} className="opt-leg" title={c.hint}>
            <i className={`sw opt-${c.key}`} /> {c.label}
            {totals ? `: ${usd(totals[`usd_${c.key}`], 4)}` : ''}
          </span>
        ))}
      </div>

      <div className="opt-rows">
        {data.operators
          .filter((o) => o.operator !== 'per validator')
          .map((o) => (
            <OperatorRow key={o.operator} op={o} speedup={speedup}
                         ethPrice={data.eth_usd_price} />
          ))}
      </div>

      <div className="opt-foot">
        Priced per real mainnet slot off the beacon head. Total ={' '}
        <code>A + max(B, C)</code>; B and C are mutually exclusive uses of the same
        saved milliseconds, so they are never summed. ~93% of the value is channel C,
        which pays only if the operator re-tunes its publication timing.
        Late blocks are mostly late because they were published late, which
        no transport can fix: even an infinitely fast network rescues only ~80% of them.
      </div>
    </div>
  )
}
