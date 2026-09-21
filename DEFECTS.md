# Defects

## D-1
- Severity: P1
- Reproduction/evidence: `git diff --stat` (worker MC-10.md) lists ADVERSARIAL_REVIEW.md, CHANGE_PLAN.md, CHANGE_REQUEST.md, CHANGE_SPEC.md, CHANGE_TEST_REPORT.md, IMPLEMENTATION_NOTES.md, MANUAL_CHECKLIST.md as changed in addition to frontend/public/home.html
- Affected requirement/check: MC-10, CHANGE_SPEC.md §4 (change scoped to home.html only)
- Current status: OPEN. The 7 additional files are the workflow's own generated documentation artifacts, not application source or product files, and are unrelated to any of the AC-1..AC-8 acceptance criteria, which all PASS.
- Owner/next action: reconcile CHANGE_SPEC.md/MANUAL_CHECKLIST.md scope wording (whether workflow-artifact updates count as in-scope) — a plan/spec decision, not resolvable by re-running the check.
- Disposition: does not block AC-1..AC-8; MC-10 remains FAIL as literally worded.
