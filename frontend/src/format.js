// Formatting helpers — ported 1:1 from the vanilla app.

export function fmtUptime(s) {
  if (!s) return '–'
  if (s < 60) return `${s}s`
  const m = Math.floor(s / 60)
  if (m < 60) return `${m}m`
  const h = Math.floor(m / 60)
  const rm = m % 60
  if (h < 48) return `${h}h ${rm}m`
  const d = Math.floor(h / 24)
  const rh = h % 24
  return `${d}d ${rh}h`
}

export function fmtPnlSol(v) {
  if (v === null || v === undefined) return '–'
  const sign = v > 0 ? '+' : ''
  return `${sign}${v.toFixed(4)} SOL`
}

export function fmtSol(v) {
  if (v === null || v === undefined) return '–'
  return `${v.toFixed(3)} SOL`
}

export function fmtUsd(v) {
  if (v === null || v === undefined) return '–'
  return `$${v.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
}

export function fmtMs(v) {
  if (v === null || v === undefined) return '–'
  if (v >= 1000) return `${(v / 1000).toFixed(2)} s`
  if (v < 10) return `${v.toFixed(1)} ms`
  return `${Math.round(v)} ms`
}

// Epoch seconds -> "MM-DD HH:MM" (UTC), used on chart axes/tooltips.
export function fmtChartTime(t) {
  const d = new Date(t * 1000)
  const p = (n) => String(n).padStart(2, '0')
  return `${p(d.getUTCMonth() + 1)}-${p(d.getUTCDate())} ${p(d.getUTCHours())}:${p(d.getUTCMinutes())}`
}

// Signed plain number (e.g. paper-trade net return / cumulative return — unitless).
export function fmtNet(v) {
  if (v === null || v === undefined) return '–'
  return `${v > 0 ? '+' : ''}${v.toFixed(3)}`
}

export function fmtClock(nowSec) {
  return new Date(nowSec * 1000).toISOString().replace('T', ' ').slice(0, 19) + 'Z'
}
