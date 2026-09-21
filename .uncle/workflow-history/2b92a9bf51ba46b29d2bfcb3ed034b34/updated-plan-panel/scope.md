# Scope-lens evidence packet

## AR-001 — Green-check baseline-probe vs. post-change gate ambiguity
- Gap: CHANGE_PLAN.md §"Verification commands" (lines 105-112) lists correct post-change assertions (`grep -c "unclehq/uncle"`, absence checks), but `.uncle/workflow/green-check.commands` cmd3/cmd4 still encode the *pre-change* baseline greps (`unclehq/stagegate\|brianosaurus/agentic-workflow`, `Claude builds, Codex audits`) that BASELINE_REPORT.md §9 shows currently return nonzero counts and are expected to hit 0 only after the edit.
- Evidence: `.uncle/workflow/green-check.commands` lines 3-4 vs. BASELINE_REPORT.md lines 85-89 vs. CHANGE_PLAN.md line 106-108.
- Risk: If the driver's runner treats these two commands as pass/fail gates without inverted expectation, a correct implementation produces count=0 (a change from baseline nonzero), which is the desired outcome — but if the runner instead expects the baseline's original nonzero exit/count semantics unchanged, the gate misfires. This is unresolved: the plan doesn't explicitly state whether green-check cmd3/cmd4 are being reinterpreted as post-change assertions or need driver-config exemption.
- Required correction: Revised plan must explicitly state the post-change expected exit/count for green-check cmd3 and cmd4 (both should be 0 after the edit), and confirm/update the driver config or gate interpretation so it isn't scored against baseline expectations. This is AR-001, still open — not resolved by CHANGE_PLAN.md as written.

## Scope boundary check (no new findings beyond AR-001)
- CHANGE_PLAN.md §4-5 (lines 28-37) correctly scopes to `frontend/public/home.html:490-500` and `AGENTIC_WORKFLOW_STRATEGY.md`, explicitly excluding sibling cards, `app/main.py`, and build config — matches CHANGE_SPEC.md AC-8/BX-5/BX-6 and BASELINE_REPORT.md §12/§14. No scope creep found.
- AC-9 (html.parser) and diff-scoped regression check (§17) are appropriately proportional to a static-copy change; no over- or under-engineering identified.

## Acceptance-provenance check
- CHANGE_PLAN.md §18 (lines 69-73) explicitly declines to add a separate human sign-off gate for AC-2/AC-6 wording quality, reasoning "CHANGE_REQUEST.md names no additional reviewer" and relying on existing plan-approval/final-approval gates. This is a defensible non-automatable-judgment call (prose quality) correctly left to the existing approval gates rather than inventing a new mandatory human sign-off — no source requires an additional gate, so none should be added. No conflict found here.

## Disposition
- 1 open gap (AR-001), scope lens only. No new scope-boundary or unauthorized-sign-off issues found. Canonical resolution owned by the plan writer.