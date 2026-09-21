## AR-001: Stale AC-numbered artifacts collide with current spec
- Severity: High
- References: CHANGE_TEST_REPORT.md, VERIFICATION_REPORT.md, MANUAL_CHECKLIST.md, DEFECTS.md, IMPLEMENTATION_NOTES.md (repo root); CHANGE_SPEC.md AC-1..AC-8.
- Failure: these files test AC-1..AC-9 of the prior "rewrite Uncle card" change (checks for "unclehq/uncle" count, "Claude builds, Codex audits" phrase) — not this plan's AC-1..AC-8 (card move + em-dash removal). Live file state confirms this plan is unimplemented: `grep -n "<h3>" frontend/public/home.html` still shows order vLLM/H100/Pydantic/Uncle and line 493 still contains `—`. A later verification/audit stage reading PASS claims under matching AC-1..AC-3 IDs could wrongly treat this plan as already satisfied.
- Fix: plan's implementation sequence (section 12) must add a step to remove or clearly supersede the stale CHANGE_TEST_REPORT.md/VERIFICATION_REPORT.md/MANUAL_CHECKLIST.md/DEFECTS.md/IMPLEMENTATION_NOTES.md before or alongside producing new ones for this change, so AC IDs are unambiguous.
- Verify: after implementation, confirm CHANGE_TEST_REPORT.md's targeted-test list contains an em-dash grep and a card-order grep tied to *this* spec's AC-1/AC-3, not the prior spec's checks.

## AR-002: Move-detection verification method is ambiguous
- Severity: Medium
- References: CHANGE_PLAN.md §10 ("no hunks inside the vLLM, H100... blocks"); CHANGE_SPEC.md AC-5, AC-8.
- Failure: `git diff` on a block relocated across other unchanged blocks produces one large hunk spanning the deletion/insertion region, with the intervening cards appearing only as unchanged context lines inside that same hunk — "no hunks inside X" is not a well-defined pass/fail signal from raw `git diff` output and could hide a stray edit to context lines that a reviewer skims past.
- Fix: specify `git diff --color-moved` or a line-by-line diff of each of the three untouched `<article>` blocks against baseline (e.g. `diff <(sed -n '463,475p' baseline) <(sed -n 'new-range p' current)`), not hunk-counting.
- Verify: byte-for-byte diff of vLLM/H100/Pydantic AI block line ranges pre- and post-edit returns empty.

## AR-003: AC-4 has no objective verification
- Severity: Low
- References: CHANGE_SPEC.md AC-4; CHANGE_PLAN.md §1 (example rewrite "...others, not a fixed pairing...").
- Failure: AC-4's only check is "manual read," so any rephrasing — including the plan's own comma-spliced example — passes regardless of grammaticality; a defective rewrite could ship unnoticed.
- Fix: plan should commit to a specific rewrite text (e.g. "...others; not a fixed pairing...") rather than an illustrative example, removing wording discretion from implementation.
- Verify: reviewer reads the exact committed sentence in the plan, not a placeholder, before approval.

## Overall assessment
Plan is executable and narrowly scoped; no incorrect-behavior or invariant defects found in CHANGE_SPEC.md/CHANGE_PLAN.md themselves. AR-001 is blocking: stale same-numbered AC artifacts in the repo create a real risk of false PASS attribution and must be resolved before/alongside implementation. AR-002/AR-003 are non-blocking hardening items.