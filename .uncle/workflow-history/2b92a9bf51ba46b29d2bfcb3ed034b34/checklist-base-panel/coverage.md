# Coverage Evidence Packet — Base Pass Manual Checklist

## Required checks (per AC, coverage status)

| AC | Automatable? | Coverage gap |
|---|---|---|
| AC-1 | Yes — grep count | None; must also assert count = 3 (not just >0) — CHANGE_SPEC.md:33 |
| AC-2 | No — 6-point semantic content | Manual check required: verify `<p>` states all 6 points (terminal-native, issue-in/PR-out, agent-agnostic, independent review, human approval gates, crypto pinning). No automated proxy exists. |
| AC-3 | Yes — grep -i, but AR-004 (CHANGE_PLAN.md:11) flags literal-phrase grep can miss reworded fixed-pairing claim | Checklist must add a manual read step pairing with the grep, not grep alone |
| AC-4 | Yes — repo-wide grep | None |
| AC-5 | Yes — grep absence of old text, but AR-003 (CHANGE_PLAN.md:10) flags this only proves *difference*, not *accuracy* | Checklist must add manual read: new tag reflects uncle's actual scope, not just "any edit" |
| AC-6 | Partially — AC-3 grep covers banned phrase; positioning-match is subjective | Manual read required, no automated proxy for "framing matches uncle" |
| AC-7 | No — provenance check | Requires implementer's plan/PR notes citing what was read from github.com/unclehq/uncle; checklist must verify such notes exist, not just trust a claim |
| AC-8 | Yes — `git diff --stat` / line-range check | None |
| AC-9 | Yes — html.parser exit 0 | None; note html.parser is lenient (BASELINE_REPORT.md:84), doesn't validate nesting/attrs — checklist should not overstate this as full HTML validation |

## Dependencies
- AC-7's manual verification depends on step 1 of CHANGE_PLAN.md (fetch uncle README) actually having occurred — checklist needs a check that this occurred (e.g., citation present) not just that copy "looks plausible."
- AC-2/AC-6 manual reads depend on AC-1/AC-3/AC-5 edits landing first (same file, home.html:490-500 and AGENTIC_WORKFLOW_STRATEGY.md).

## Exclusive resources
None — single-file static edits, no shared mutable state, no exclusive locks needed for verification.

## Acceptance provenance
No mandatory human sign-off beyond existing plan/final-approval gates is sourced anywhere in CHANGE_REQUEST.md, CHANGE_SPEC.md, or CHANGE_PLAN.md. AC-2, AC-6, AC-7 are genuinely non-automatable (semantic accuracy / provenance judgments) — CHANGE_SPEC.md itself designates these "Manual read" (§29-40), not grep-verifiable. This is a specific, sourced judgment (content-quality assessment automated grep cannot establish), not an invented approval gate. Checklist should mark these three items as required manual checks, not require a distinct "human sign-off" gate beyond the standard workflow approval points.

## Coverage gap summary
1. **AC-2/AC-6 manual read checks** are required and correctly non-automatable — must be explicit checklist items, not folded into grep-only verification.
2. **AC-3/AC-5 grep-only coverage is insufficient per AR-003/AR-004** — checklist must pair each with a manual read (reworded-claim detection, tag accuracy), not rely on grep as sole evidence.
3. **AC-7 provenance check has no automated proxy** — checklist must verify a citation/note exists showing the uncle README was actually read, not accept unverified implementer claims.
4. **AC-1 count assertion** — checklist should specify exact count (=3), not just non-zero, to avoid a partial-fix false pass.