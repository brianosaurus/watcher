# Change test report

## Changed requirement/behavior IDs

BX-1..BX-4 (CHANGE_SPEC.md §6), AC-1..AC-9 (CHANGE_SPEC.md §5).

## Baseline result

`python3 -m py_compile app/main.py` — exit 0 (BASELINE_REPORT.md §9, re-run post-change, unchanged: app/main.py not touched).

## Targeted tests

- `grep -o "unclehq/uncle" frontend/public/home.html | wc -l` → 3 (AC-1).
- `grep -c "brianosaurus/agentic-workflow\|unclehq/stagegate" frontend/public/home.html` → 0 (AC-1).
- Manual read of `<p>` block (home.html:492-497) against AC-2's six points → all present (AC-2).
- `grep -ic "claude builds\|codex audits\|claude/codex" AGENTIC_WORKFLOW_STRATEGY.md frontend/public/home.html` → 0, 0 (AC-3, AC-6).
- `grep -rl "stagegate" --exclude-dir=.git --exclude-dir=.uncle -- app frontend AGENTIC_WORKFLOW_STRATEGY.md | wc -l` → 0 (AC-4; repo-wide count including `.uncle/` workflow logs is 99, all in generated reports/logs, not source — pre-existing per BASELINE_REPORT.md §15).
- `grep -n "LLM agents · pipeline tooling · open source" frontend/public/home.html` → no match (AC-5).
- `gh api repos/unclehq/uncle` + `gh api repos/unclehq/uncle/readme` read before writing copy, cited in IMPLEMENTATION_NOTES.md (AC-7).
- `git diff frontend/public/home.html | grep -E '^@@'` → one hunk `@@ -488,14 +488,16 @@`, no hunks outside the 490-500 card block; adjacent cards (463-489, 507+) untouched (AC-8).
- `python3 -c "import html.parser, pathlib; p = html.parser.HTMLParser(); p.feed(pathlib.Path('frontend/public/home.html').read_text()); print('parsed ok')"` → exit 0, `parsed ok` (AC-9).

## Regression tests

None exist (BASELINE_REPORT.md §7). `git diff --stat` — only `AGENTIC_WORKFLOW_STRATEGY.md` and `frontend/public/home.html` changed, matching the frozen scope; adjacent cards confirmed byte-identical by AC-8 hunk check above.

## Full test suite

DRIVER PENDING.

## Formatting

N/A (no formatter configured for this repo; plain HTML/Markdown edit).

## Compiler or type checker

`python3 -m py_compile app/main.py` — exit 0, no output.

## Linting

N/A (no linter configured — BASELINE_REPORT.md §7 found no lint/test tooling).

## Integration tests

N/A (no API/schema surface touched — CHANGE_SPEC.md §6 BX-6 preserved untested per spec).

## Frontend build

NOT RUN (`frontend/node_modules` absent, requires network `npm install` — BASELINE_REPORT.md §9; not needed to verify a static-HTML source edit, per baseline's own conclusion). Source-level HTML-parse check (AC-9) substitutes.

## Migration tests

N/A (no schema/data change).

## Rollback test

NOT RUN. Rollback expectation (CHANGE_SPEC.md §13) is a plain `git checkout` of the two files; not exercised since no commit was made this stage.

## Performance checks

N/A (static text/link edit, no performance-sensitive path — CHANGE_SPEC.md omits performance requirements).

## Security checks

`rel="noopener noreferrer"` preserved on both rewritten `unclehq/uncle` links (home.html:491,497), matching sibling-card convention (CHANGE_SPEC.md §11).

## Newly introduced warnings

None observed in any command above.

## Pre-existing failures

None (BASELINE_REPORT.md §10: none observed at baseline).

## Untested areas

AC-2 and AC-7 verified by manual read/citation only, not by an automated assertion (CHANGE_SPEC.md specifies manual verification for both). Frontend build (Vite) not exercised — see Frontend build row.
