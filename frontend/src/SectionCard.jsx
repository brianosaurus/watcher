import React, { useEffect, useRef } from 'react'
import { fmtMs } from './format.js'
import { WalletChart, TradePhaseChart, SlotDeltaChart, BuySwapChart, SellTimingChart } from './charts.jsx'

function KV({ k, v, cls = '' }) {
  return (
    <div className="kv">
      <div className="k">{k}</div>
      <div className={'v ' + cls}>{v}</div>
    </div>
  )
}

// A standalone card summarising a trade-log .jsonl (see backend `_trades_section`).
export default function SectionCard({ section: s }) {
  const logLines = s.log_tail || []
  const logRef = useRef(null)
  useEffect(() => {
    if (logRef.current) logRef.current.scrollTop = logRef.current.scrollHeight
  }, [logLines])

  const tag = s.tag || 'trades'
  const tagClass = s.tag_class || 'project'

  return (
    <div className="bot">
      <div className="head">
        <div className="title">
          <div className="name">{s.title}</div>
          <div className="sub">{s.source} · {tag}</div>
        </div>
        <div className="tags">
          <span className={'tag ' + tagClass}>{tag}</span>
        </div>
      </div>

      <div className="body">
        <KV k="trades" v={String(s.entered)} />
        {s.open_trades != null && (
          <KV k="open / closed" v={`${s.open_trades} open / ${s.closed_trades} closed`} />
        )}
        {s.grad_count != null && (
          <KV k="graduated" v={`${s.grad_count} / ${s.bought_count} bought` +
            (s.grad_rate != null ? ` (${(s.grad_rate * 100).toFixed(1)}%)` : '')} />
        )}
        {s.grad_captured != null && s.grad_captured > 0 && (
          <KV k="grad captured" v={String(s.grad_captured)} />
        )}
        {s.observed != null && s.observed !== s.entered && (
          <KV k="observed" v={String(s.observed)} />
        )}
        {s.rugs != null && <KV k="rugs" v={String(s.rugs)} />}

        {s.mean_trade_time_ms != null && <KV k="mean trade time" v={fmtMs(s.mean_trade_time_ms)} />}
        {s.mean_trade_time_ms != null && s.trade_phases &&
          [['dispatch', '· dispatch'], ['build', '· build'], ['submit', '· submit'], ['confirm', '· confirm']]
            .filter(([key]) => s.trade_phases[key] != null)
            .map(([key, label]) => <KV key={key} k={label} v={fmtMs(s.trade_phases[key])} />)}

        {s.mean_sell_time_ms != null && <KV k="mean sell time"
          v={fmtMs(s.mean_sell_time_ms) + (s.median_sell_time_ms != null ? ` (med ${fmtMs(s.median_sell_time_ms)})` : '')} />}
        {s.mean_sell_time_ms != null && s.sell_detect_feeds &&
          <KV k="· detect feed" v={Object.entries(s.sell_detect_feeds).map(([k, v]) => `${k} ${v}`).join(' · ') || '–'} />}

        {(s.build_slot != null || s.confirm_slot != null) && <>
          <KV k="build slot" v={s.build_slot != null ? String(s.build_slot) : '–'} />
          <KV k="confirm slot" v={s.confirm_slot != null ? String(s.confirm_slot) : '–'} />
          <KV k="buy slot Δ" v={(s.slot_delta != null ? String(s.slot_delta) : '–') +
            (s.median_slot_delta != null ? ` (med ${s.median_slot_delta} · ~${Math.round(s.median_slot_delta * 400)}ms)` : '')} />
        </>}
        {(s.grad_slot != null || s.sell_slot != null) && <>
          <KV k="sell slot" v={s.sell_slot != null ? String(s.sell_slot) : '–'} />
          <KV k="sell slot Δ" v={(s.sell_slot_delta != null ? String(s.sell_slot_delta) : '–') +
            (s.median_sell_slot_delta != null ? ` (med ${s.median_sell_slot_delta} · ~${Math.round(s.median_sell_slot_delta * 400)}ms)` : '')} />
        </>}
        {s.buy_swap != null && (
          <KV k="buy swap #" v={String(s.buy_swap) +
            (s.median_buy_swap != null ? ` (med ${s.median_buy_swap})` : '')} />
        )}
      </div>

      <div className="chart-status">Gathering data for retrain</div>
      <div className="chart-wrap">
        {(s.wallet_series || []).length >= 2 && <WalletChart data={s.wallet_series} />}
        {(s.trade_phase_series || []).length >= 2 && <TradePhaseChart data={s.trade_phase_series} />}
        {(s.slot_delta_series || []).length >= 2 && <SlotDeltaChart data={s.slot_delta_series} title="Buy slot Δ per trade (slots to confirm · lower=faster)" />}
        {(s.sell_slot_delta_series || []).length >= 2 && <SlotDeltaChart data={s.sell_slot_delta_series} title="Sell slot Δ (graduation → sell landed · 0 = in-slot)" />}
        {(s.sell_timing_series || []).length >= 2 && <SellTimingChart data={s.sell_timing_series} />}
        {(s.buy_swap_series || []).length >= 2 && <BuySwapChart data={s.buy_swap_series} />}
      </div>

      {logLines.length
        ? <pre className="log" ref={logRef}>{logLines.join('\n')}</pre>
        : <pre className="log empty">(no records yet)</pre>}
    </div>
  )
}
