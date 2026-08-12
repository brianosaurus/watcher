# Optimum / mump2p — Results Summary

*Companion document for the watcher dashboard (`/` OptimumCard, `/optimum` report,
`/api/optimum`). Full pipeline, data and tests live in `../optimum`; deployed on
frankfurt at `~/optimum`. All data public (ethPandaOps Xatu + MEV relay traces).
Last updated 2026-07-14.*

---

## The one-paragraph version

mump2p has exactly one deployed network — the Hoodi testnet — and **five
independent identification designs find no trace of it carrying blocks there**,
while the one non-null result shows the deployment window *adding* propagation
load, not removing it. On mainnet (where it has never run), the measured physics
say the product's real value is **MEV delay budget** (~92% of a modelled
~$32–35/validator/yr at the vendor's 6× claim), it is worth most at **40–55%
adoption** and self-cannibalises at saturation, and the "6×" headline was won
against a testnet baseline twice as slow as mainnet's.

---

## Mainnet physics (216,000 slots, 2025-06)

- **Latency is free until it isn't.** Correct-head votes: 99.96% → 95.9% →
  **67.4%** → 22.4% → 0.1% across the 4,000 ms attestation deadline. Mean
  latency is the wrong KPI; the tail is everything.
- **61% of head-vote misses happen on blocks that arrived on time** — they are
  nodes in the propagation tail. The attester benefit of a faster transport is
  leaving the tail on every block, not rescuing rare late ones.
- **Late blocks are published late, not transported slowly** (median publication
  3,656 ms vs 1,811 ms). An infinitely fast network rescues only ~80% of them;
  2× rescues 1.5%.
- **Orphans are timing-game losers**: 188/214,712 blocks (0.088%); hazard is a
  cliff (0.04% → 1.6% → 9.9% → 28.5% across 4.0–6.0 s). Orphaned blocks carry
  exactly average MEV (1.02× — validated against relay delivered payloads).
- **Only 5.8% of proposals capture max block value safely**; the average
  proposer leaves ~25% of block value (0.013 ETH) on the table. Attesters are
  near-saturated (99.06% of the possible 99.96%).

## The counterfactual (modelled, NOT revenue — mump2p is not on mainnet)

Per validator/yr at the vendor's 6× (ETH @ $1,805.50, post-Pectra set):

| channel | mechanism | $/val/yr |
|---|---|---|
| A — attester head votes | my nodes leave the propagation tail | 2.48 |
| B — reorgs avoided | my late blocks survive fork choice | 0.14 |
| **C — MEV delay budget** | publish later at same arrival → better bid | **32.76** |
| D — bandwidth | RLNC kills redundant gossip (~3.8 TB/node/yr) | 0.68 cloud / ~0 metal |

Total = A + max(B,C) + D (B and C are exclusive uses of the same saved ms).
**All seven named partners: ~$4.8M/yr** (Kiln $1.55M, P2P $1.04M, Everstake
$0.96M, …). Channel C pays **only if the operator re-tunes publication timing**
— install-and-change-nothing earns ~$2–3.

**Hoodi→mainnet floor extrapolation** (overlay = absolute floor, not a
multiplier; `transit = min(observed, floor)`): the vendor's 150 ms floor is
6.7× on Hoodi but only **2.2× for mainnet's median node** (331 ms) — and 0.8×
(a *downgrade*) if the realised floor is 400 ms. What transfers is tail
compression (p90 976 ms → floor), i.e. the MEV channel. Totals: $32.06 /
$28.46 / $22.81 per val/yr at floors 150/250/400 ms.

**Adoption sweep** (C needs ≥~40% of attesters receiving fast — proposer-boost
threshold — and decays 1−α as adopting predecessors steal the same flow):
per-adopter peak at **40% adoption ($20.82/val/yr)**, total-value peak at
**55% ($7.95M/yr)**, collapse to $3.30 at 100%. The seven partners (16.8% of
the network) sit **below** the sweet spot. The adopt-vs-not spread saturates at
~$32/val and never decays — late adoption is bought to stop bleeding.

## Hoodi: five designs, no treatment found

mump2p's only deployment (announced 2025-06-24; first vendor results
2025-09-23). Xatu's Hoodi attestation coverage only begins ~2025-10-26, after
the deployment window, so there is no pre-adoption baseline for attestation
outcomes and the designs use propagation physics instead. (Attestation data
from Nov 2025 onward exists and is usable, but it post-dates the treatment.)

| # | design | second difference | verdict |
|---|---|---|---|
| 1 | ITS + comparison series (vs Sepolia, 487 net-days) | network | null — the never-treated control owns every clean break (−72% vs −56%, r² 0.84 vs 0.34, Fusaka-era common shock) |
| 2 | Per-operator send-side stepping (1.6M proposals, 14 fee-recipient clusters) | operator × time | null — **zero staggering**: all 14 clusters break the same day (2025-09-29), same day-zero as the control |
| 3 | Peer-level gateway hunt (libp2p first-delivery races) | sending peer × time | null — no speed edge (young peers win at 1.3–1.5 s, not overlay speeds), no persistent deployment-window cohort |
| 4 | Size-penalty DiD (Q4 vs Q1 block size, label-free) | block difficulty × time | **inverted** — penalty tripled (225→1,346 ms) in the deployment window: a congestion signature, the opposite of constant-time offloading |
| 5 | Mixture emergence (2-comp EM on log-transit, label-free) | distribution shape × time | null — bimodality pre-exists deployment; no overlay-like (~150–300 ms) component ever appears |

Supporting facts: during the deployment window Hoodi's transit **tripled** in a
clean Aug-1→Oct-1 square pulse while Sepolia stayed flat (stable sentries — not
an observation artifact); the vendor's "6× vs gossipsub" benchmark was captured
**inside that degraded window**, on a network whose baseline gossipsub is
already ~2× slower than mainnet's. Shadow-mode duplication (blocks through
*both* stacks, per their own methodology) both predicts the nulls and is
consistent with the size-dependent congestion.

**Answer to "can we date validator adoption from Xatu?": no — because nothing
load-bearing was ever adopted, as far as public data can see.** The detection
machinery (`adoption_scan.py`, `peer_scan.py`, `within_did.py`) is built and
reusable on mainnet the day a real rollout happens — that's the staggered DiD,
pre-built and waiting for its treatment.

## What runs where

- **frankfurt `~/optimum`** — full pipeline (59+ tests), 30-day mainnet panel,
  Hoodi/Sepolia panels, all scan tooling.
- **`optimum-tracker.service`** — live mainnet slot pricer (beacon-head poll,
  NTP-corrected in-process: the host clock is ~94 s behind with NTP disabled —
  still unfixed at OS level; fixing it may affect the Solana bots, user's call).
- **watcher `/api/optimum`** — live counterfactual accruals (SQLite WAL reader).
- **`/` OptimumCard** — live ticker, A/B/C channel bars, arrival sparkline.
- **`/optimum`** — the public report (this content, with figures); the earlier
  five-step notebook is preserved at `/optimum/notebook.html`.

## Standing caveats (keep these attached to any number quoted)

1. Every dollar figure is a **modelled counterfactual** — nobody earns this
   today; the dashboard must keep saying so.
2. The 6× input is the **vendor's testnet gateway measurement**, unverified at
   validator clients; hence the 3×/2× and floor-model haircuts.
3. Arrival is a sentry-median → measurement error smooths the deadline
   discontinuity → sharp-RD estimates are bandwidth-sensitive; lead with the
   dose-response.
4. Hoodi results are **no evidence of effect** under a shadow-mode deployment,
   not proof of none. Only 4 sentries feed the libp2p layer.
5. Post-PeerDAS (Fusaka), blob propagation is re-architected — Channel D and
   the blob share of transit need re-measuring.
