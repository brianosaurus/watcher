## AR-001: Verification command undercounts occurrences on shared lines
- Severity: High
- References: CHANGE_PLAN.md:78 (section 10), CHANGE_SPEC.md AC-1; frontend/public/home.html:491,499
- Failure: `grep -c "unclehq/uncle"` counts matching *lines*, not occurrences; line 491 contains the string twice (href + url span), so a fully compliant file returns 2, not the expected 3 — verified by running the command (`grep -c` → 2, `grep -o | wc -l` → 3). The check fails correct code.
- Fix: replace with `grep -o "unclehq/uncle" frontend/public/home.html | wc -l` (expect 3), or restate the check per-line.
- Verify: run both grep forms against the current file and confirm the corrected form is used before treating the check as passing evidence.

## AR-002: Rollback plan is broader than "this plan's edit" and has no pre-adoption snapshot
- Severity: High
- References: CHANGE_PLAN.md:70-74 (section 9), CHANGE_PLAN.md:9-13 (D-1)
- Failure: D-1 states the working-tree draft predates and is not authored by this plan, yet the only rollback (`git checkout -- home.html AGENTIC_WORKFLOW_STRATEGY.md`) restores HEAD, discarding the pre-existing draft along with any plan edits. If steps 2/3 are no-ops (fetch unavailable), invoking rollback destroys uncommitted prior work with no saved copy.
- Fix: snapshot the pre-plan working tree (e.g. `git stash` to a tagged ref or `cp` backups) before step 1, and define rollback as restoring that snapshot, not `HEAD`.
- Verify: confirm a backup of the D-1 draft exists and that rollback restores draft state, not committed state, when no plan edits were made.

## AR-003: AC-7 gate is undefined on fetch failure, and network capability is understated
- Severity: Medium
- References: CHANGE_PLAN.md:103-110 (section 13), CHANGE_PLAN.md:125-136 (R-2)
- Failure: plan says a failed fetch must be "reported, not silently passed," but never states whether the change can still be merged with AC-7 unmet — leaving the human approval gate undefined. R-2 also claims network/fetch capability is "not probed," but this runner exposes a `WebFetch` tool, so the uncertainty is avoidable, not an inherent constraint.
- Fix: probe/use `WebFetch` for step 1; if genuinely unavailable, state explicitly that AC-7 failure blocks merge pending manual fetch, not that steps 2/3 silently become no-ops.
- Verify: confirm WebFetch (or equivalent) is invoked and succeeds before accepting the draft; absent that, the PR must be marked blocked, not "confirmed."

## AR-004: Draft provenance accepted as ground truth without evidence it derives from the real repo
- Severity: Medium
- References: CHANGE_PLAN.md:9-13,26-27 (D-1, section 3); CR AC-7
- Failure: the plan treats the pre-existing uncommitted draft as authoritative "current ground truth" even though no citation exists yet that it was derived from `github.com/unclehq/uncle` — the exact failure mode (invented project description) the CR exists to fix. Steps 2/3 only revise on "inaccuracy found," biasing toward accepting unverified prose.
- Fix: require step 1's fetch to produce an explicit point-by-point comparison against draft text before any "confirmed accurate" conclusion is recorded, not just a pass/fail gut check.
- Verify: PR description must quote/cite specific README lines matched against each of AC-2's six required points.

## Overall assessment

Blocking: AR-001 (broken verification command), AR-002 (destructive rollback with no backup). AR-003 and AR-004 must be resolved before execution to avoid silently accepting unverified copy. Plan's scope, invariants, and behavior classification (D-1, CI-1/CI-2) are otherwise sound.