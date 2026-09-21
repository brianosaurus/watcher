# Change test report

## Changed requirement/behavior IDs

BX-1, BX-2 (CHANGE_SPEC.md §6); AC-1..AC-8 (CHANGE_SPEC.md §5).

## Baseline result

`python3 -m py_compile app/main.py` — exit 0 (unaffected, not re-run; no code changed).
`python3 -c "import html.parser,pathlib; ...feed(...)"` on pre-edit tree — exit 0 (BASELINE_REPORT.md §9).

## Targeted tests

- `grep -n '<h3><a' frontend/public/home.html` → order vLLM, Uncle, H100 Roofline Study, Pydantic AI, ... (AC-1).
- `git diff frontend/public/home.html | grep -E '^[+-]'` → only the moved Uncle `<article>` block's add/remove lines; em-dash clause is the only textual difference between old/new copies (AC-2).
- `sed -n '462,475p' frontend/public/home.html | grep -c "—"` → 0 (AC-3).
- Manual read of frontend/public/home.html:466: "...coordinates the coding agents you already use (Claude, Codex, and others, not a fixed pairing)..." — meaning preserved (AC-4).
- `git diff frontend/public/home.html | grep -E '^[+-]'` → no +/- lines inside vLLM (440-460), H100 (477-490 new), Pydantic AI (492-503 new) blocks (AC-5).
- `grep -c "—" frontend/public/home.html` → 0, baseline was 1 (BASELINE_REPORT.md did not count this char directly but CHANGE_SPEC.md §3 confirms exactly one em dash existed); differs by exactly 1 (AC-6).
- `python3 -c "import html.parser, pathlib; p = html.parser.HTMLParser(); p.feed(pathlib.Path('frontend/public/home.html').read_text()); print('parsed ok')"` → exit 0, `parsed ok` (AC-7).
- `git diff frontend/public/home.html | grep -E '^@@'` → hunks `@@ -459,6 +459,20 @@`, `@@ -486,20 +500,6 @@`, both within old lines ≤506; nothing at/below live-systems-heading (old line 507+) touched (AC-8).

## Regression tests

None exist (BASELINE_REPORT.md §7). `git diff --stat` — only `frontend/public/home.html` changed (14 insertions, 14 deletions), matching frozen scope.

## Full test suite

DRIVER PENDING

## Formatting

N/A (no formatter configured for static HTML — BASELINE_REPORT.md §7)

## Compiler or type checker

N/A (no code changed; app/main.py untouched)

## Linting

N/A (no linter configured — BASELINE_REPORT.md §7)

## Integration tests

N/A (none exist)

## Frontend build

NOT RUN (frontend/node_modules absent per BASELINE_REPORT.md §9; not needed to verify static-HTML edit, same as baseline)

## Migration tests

N/A (no schema/data change)

## Rollback test

N/A (CHANGE_SPEC.md §10: revert via git; not exercised)

## Performance checks

N/A (static markup only)

## Security checks

N/A (no new links/attributes; only existing github.com/unclehq/uncle links repositioned)

## Newly introduced warnings

None observed.

## Pre-existing failures

None (BASELINE_REPORT.md §10: no pre-existing failures).

## Untested areas

Rendered visual layout of the reordered card grid (CSS grid reflow) not checked in a browser.
