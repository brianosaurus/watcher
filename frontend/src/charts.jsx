import React from 'react'
import {
  ResponsiveContainer, LineChart, AreaChart, Line, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine, Legend,
} from 'recharts'
import { fmtChartTime } from './format.js'

const GOOD = '#2a8f38'
const BAD = '#c92a2a'
const BLUE = '#0c7c9e'
const MUTED = '#5a5a55'
const GRID = '#e0e0dc'
const PHASE = { confirm: '#0c7c9e', submit: '#9e6b00', build: '#2a8f38', dispatch: '#7b2cbf' }

const axisTick = { fontSize: 9, fill: MUTED }
const tipStyle = { background: '#ffffff', border: '1px solid #d0d0cc', color: '#111111', fontSize: 11, borderRadius: 4 }

function xAxis() {
  return (
    <XAxis
      dataKey="t" type="number"
      domain={['dataMin', 'dataMax']}
      tickFormatter={fmtChartTime} tick={axisTick} stroke={GRID}
      minTickGap={44} tickMargin={4}
    />
  )
}

function ChartBox({ title, height = 132, children }) {
  return (
    <div className="chart-box">
      <div className="chart-cap">{title}</div>
      <ResponsiveContainer width="100%" height={height}>
        {children}
      </ResponsiveContainer>
    </div>
  )
}

function Empty({ title, msg }) {
  return (
    <div className="chart-box">
      <div className="chart-cap">{title}</div>
      <div className="chart-empty">{msg}</div>
    </div>
  )
}

export function PnlChart({ data }) {
  const title = 'Realized PnL (cumulative SOL)'
  if (!data || data.length < 2) return <Empty title={title} msg="no pnl history" />
  const last = data[data.length - 1].pnl
  const color = last > 0 ? GOOD : last < 0 ? BAD : MUTED
  const vals = data.map((p) => p.pnl)
  const lo = Math.min(0, ...vals), hi = Math.max(0, ...vals)
  return (
    <ChartBox title={title}>
      <AreaChart data={data} margin={{ top: 6, right: 12, bottom: 2, left: 0 }}>
        <CartesianGrid stroke={GRID} strokeDasharray="2 3" vertical={false} />
        {xAxis()}
        <YAxis tick={axisTick} stroke={GRID} width={46} domain={[lo, hi]}
          tickFormatter={(v) => v.toFixed(3)} />
        <Tooltip contentStyle={tipStyle} labelFormatter={fmtChartTime}
          formatter={(v) => [v.toFixed(4) + ' SOL', 'pnl']} />
        <ReferenceLine y={0} stroke={MUTED} strokeDasharray="2 3" />
        <Area type="monotone" dataKey="pnl" stroke={color} fill={color} fillOpacity={0.18}
          strokeWidth={1.5} dot={false} isAnimationActive={false} />
      </AreaChart>
    </ChartBox>
  )
}

export function WalletChart({ data }) {
  const title = 'Wallet (on-chain SOL)'
  if (!data || data.length < 2) return <Empty title={title} msg="no wallet history" />
  const color = data[data.length - 1].sol >= data[0].sol ? GOOD : BAD
  return (
    <ChartBox title={title}>
      <LineChart data={data} margin={{ top: 6, right: 16, bottom: 2, left: 0 }}>
        <CartesianGrid stroke={GRID} strokeDasharray="2 3" vertical={false} />
        {xAxis()}
        <YAxis tick={axisTick} stroke={GRID} width={46} domain={['auto', 'auto']}
          tickFormatter={(v) => v.toFixed(2)} />
        <Tooltip contentStyle={tipStyle} labelFormatter={fmtChartTime}
          formatter={(v) => [v.toFixed(4) + ' SOL', 'wallet']} />
        <Line type="monotone" dataKey="sol" stroke={color} strokeWidth={1.6}
          dot={false} isAnimationActive={false} />
      </LineChart>
    </ChartBox>
  )
}

export function BalanceChart({ data }) {
  const title = 'Native SOL (cash)'
  if (!data || data.length < 2) return <Empty title={title} msg="no balance history" />
  const baseNat = data[0].native
  const natColor = data[data.length - 1].native >= baseNat ? GOOD : BAD
  return (
    <ChartBox title={title}>
      <LineChart data={data} margin={{ top: 6, right: 16, bottom: 2, left: 0 }}>
        <CartesianGrid stroke={GRID} strokeDasharray="2 3" vertical={false} />
        {xAxis()}
        <YAxis tick={axisTick} stroke={GRID} width={46} domain={['auto', 'auto']}
          tickFormatter={(v) => v.toFixed(2)} />
        <Tooltip contentStyle={tipStyle} labelFormatter={fmtChartTime}
          formatter={(v) => [v.toFixed(4) + ' SOL', 'cash']} />
        {/* dashed baseline at cash's starting value */}
        <ReferenceLine y={baseNat} stroke={BLUE} strokeDasharray="3 3" strokeOpacity={0.5} />
        <Line type="monotone" dataKey="native" name="cash" stroke={natColor} strokeWidth={1.6}
          dot={false} isAnimationActive={false} />
      </LineChart>
    </ChartBox>
  )
}

export function TradePhaseChart({ data }) {
  const title = 'Trade time per trade (ms, stacked phases)'
  if (!data || data.length < 2) return <Empty title={title} msg="no trade-time history" />
  // Only show phases that are present in the data (memeorator vs statalyzer differ).
  const order = ['confirm', 'submit', 'build', 'dispatch']
  const keys = order.filter((k) => data.some((p) => p[k] != null))
  return (
    <ChartBox title={title} height={144}>
      <AreaChart data={data} margin={{ top: 6, right: 12, bottom: 2, left: 0 }}>
        <CartesianGrid stroke={GRID} strokeDasharray="2 3" vertical={false} />
        {xAxis()}
        <YAxis tick={axisTick} stroke={GRID} width={46}
          tickFormatter={(v) => (v >= 1000 ? (v / 1000).toFixed(1) + 's' : Math.round(v) + '')} />
        <Tooltip contentStyle={tipStyle} labelFormatter={fmtChartTime}
          formatter={(v, n) => [Math.round(v) + ' ms', n]} />
        <Legend wrapperStyle={{ fontSize: 10 }} iconType="square" />
        {keys.map((k) => (
          <Area key={k} type="monotone" dataKey={k} name={k} stackId="1"
            stroke={PHASE[k]} fill={PHASE[k]} fillOpacity={0.85}
            dot={false} isAnimationActive={false} />
        ))}
      </AreaChart>
    </ChartBox>
  )
}

export function BuySwapChart({ data }) {
  const title = 'Buy Swap # (swap index at entry · lower = earlier)'
  if (!data || data.length < 2) return <Empty title={title} msg="no buy-swap history" />
  const hi = Math.max(1, ...data.map((p) => p.buy_swap))
  return (
    <ChartBox title={title}>
      <LineChart data={data} margin={{ top: 6, right: 12, bottom: 2, left: 0 }}>
        <CartesianGrid stroke={GRID} strokeDasharray="2 3" vertical={false} />
        {xAxis()}
        <YAxis tick={axisTick} stroke={GRID} width={30} domain={[0, hi]} allowDecimals={false} />
        <Tooltip contentStyle={tipStyle} labelFormatter={fmtChartTime}
          formatter={(v) => [v + '', 'buy swap #']} />
        <Line type="monotone" dataKey="buy_swap" stroke={PHASE.submit} strokeWidth={1.6}
          dot={false} isAnimationActive={false} />
      </LineChart>
    </ChartBox>
  )
}

export function PaperChart({ data, unit }) {
  const sol = unit === 'SOL'
  const title = sol
    ? 'Cumulative PnL & running mean per trade (SOL)'
    : 'Cumulative net return & running mean (per entry)'
  if (!data || data.length < 2) return <Empty title={title} msg="not enough trades" />
  const lastCum = data[data.length - 1].cum
  const cumColor = lastCum > 0 ? GOOD : lastCum < 0 ? BAD : MUTED
  const fmt = (v) => (sol ? v.toFixed(4) + ' SOL' : v.toFixed(3))
  return (
    <ChartBox title={title}>
      <LineChart data={data} margin={{ top: 6, right: 12, bottom: 2, left: 0 }}>
        <CartesianGrid stroke={GRID} strokeDasharray="2 3" vertical={false} />
        {xAxis()}
        <YAxis tick={axisTick} stroke={GRID} width={46} domain={['auto', 'auto']}
          tickFormatter={(v) => v.toFixed(sol ? 3 : 2)} />
        <Tooltip contentStyle={tipStyle} labelFormatter={fmtChartTime}
          formatter={(v, n) => [fmt(v), n]} />
        <Legend wrapperStyle={{ fontSize: 10 }} iconType="plainline" />
        <ReferenceLine y={0} stroke={MUTED} strokeDasharray="2 3" />
        <Line type="monotone" dataKey="cum" name="cumulative" stroke={cumColor} strokeWidth={1.6}
          dot={{ r: 1.5 }} isAnimationActive={false} />
        <Line type="monotone" dataKey="mean" name="mean" stroke={BLUE} strokeWidth={1.4}
          strokeDasharray="4 2" dot={false} isAnimationActive={false} />
      </LineChart>
    </ChartBox>
  )
}

export function SellTimingChart({ data, title = 'Sell time per trade (ms · dot: green=shred fast-feed, red=grpc landed-feed)' }) {
  if (!data || data.length < 2) return <Empty title={title} msg="no sell-timing history" />
  const hi = Math.max(1, ...data.map((p) => p.sell_ms))
  const dot = (props) => {
    const { cx, cy, payload } = props
    if (cx == null || cy == null) return null
    const c = payload.feed === 'shred' ? GOOD : payload.feed === 'grpc' ? BAD : MUTED
    return <circle cx={cx} cy={cy} r={2.6} fill={c} stroke="none" />
  }
  return (
    <ChartBox title={title}>
      <LineChart data={data} margin={{ top: 6, right: 12, bottom: 2, left: 0 }}>
        <CartesianGrid stroke={GRID} strokeDasharray="2 3" vertical={false} />
        {xAxis()}
        <YAxis tick={axisTick} stroke={GRID} width={30} domain={[0, hi]} allowDecimals={false} />
        <Tooltip contentStyle={tipStyle} labelFormatter={fmtChartTime}
          formatter={(v, n, p) => [v + ' ms', (p?.payload?.reason || 'sell') + ' via ' + (p?.payload?.feed || '?')]} />
        <Line type="monotone" dataKey="sell_ms" stroke={MUTED} strokeWidth={1.2}
          dot={dot} isAnimationActive={false} />
      </LineChart>
    </ChartBox>
  )
}

export function SlotDeltaChart({ data, title = 'Slot Δ per trade (slots to confirm · lower=faster)' }) {
  if (!data || data.length < 2) return <Empty title={title} msg="no slot-Δ history" />
  const hi = Math.max(1, ...data.map((p) => p.slot_delta))
  return (
    <ChartBox title={title}>
      <LineChart data={data} margin={{ top: 6, right: 12, bottom: 2, left: 0 }}>
        <CartesianGrid stroke={GRID} strokeDasharray="2 3" vertical={false} />
        {xAxis()}
        <YAxis tick={axisTick} stroke={GRID} width={30} domain={[0, hi]} allowDecimals={false} />
        <Tooltip contentStyle={tipStyle} labelFormatter={fmtChartTime}
          formatter={(v) => [v + ' slots', 'slot Δ']} />
        <ReferenceLine y={1} stroke={GOOD} strokeDasharray="2 3" strokeOpacity={0.6} />
        <Line type="monotone" dataKey="slot_delta" stroke={BLUE} strokeWidth={1.6}
          dot={false} isAnimationActive={false} />
      </LineChart>
    </ChartBox>
  )
}
