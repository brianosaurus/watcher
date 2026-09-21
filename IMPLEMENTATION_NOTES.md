# Implementation notes

## Completed changes

| File | Change | Plan step |
|---|---|---|
| frontend/public/home.html | Moved Uncle `article.card` (formerly lines 490-502) to directly after vLLM (before H100 Roofline Study); rephrased line 493's em dash clause to "...and others, not a fixed pairing)..." | CHANGE_PLAN.md §1, §4 |

No other files changed.

## Traceability

- AC-1: Card order now vLLM, Uncle, H100 Roofline Study, Pydantic AI.
- AC-2: Uncle card h3/p/div.links text unchanged except the AC-3 rephrase (diff shows only the em-dash clause differs; see `git diff`).
- AC-3/AC-6: Em dash removed via comma substitution; `grep -c "—" frontend/public/home.html` = 0 (was 1 in baseline, differs by exactly 1, matches AC-6).
- AC-4: "coordinates the coding agents you already use (Claude, Codex, and others, not a fixed pairing)" preserves the original meaning (coordination of already-in-use agents, not a fixed pairing).
- AC-5: `git diff` shows vLLM/H100/Pydantic AI blocks appear only as unchanged context lines, no `+`/`-` inside them.
- AC-7: HTML parses cleanly (`html.parser`, exit 0, `parsed ok`).
- AC-8: Both diff hunks (`@@ -459,6 +459,20 @@`, `@@ -486,20 +500,6 @@`) fall entirely within the "Open source" section (old lines ≤506); nothing below `live-systems-heading` touched.

## Deviations

None from CHANGE_PLAN.md scope.

## Unresolved concerns

None.

## Acceptance delivery

| ID | Status | Changed code | Observed targeted verification |
|---|---|---|---|
| AC-1 | IMPLEMENTED | frontend/public/home.html:463 (Uncle h3 moved after vLLM) | `grep -n '<h3><a' frontend/public/home.html` → order vLLM, Uncle, H100 Roofline Study, Pydantic AI |
| AC-2 | IMPLEMENTED | frontend/public/home.html:463-473 (Uncle card block) | `git diff` shows only em-dash clause differs between old/new Uncle card text |
| AC-3 | IMPLEMENTED | frontend/public/home.html:466 (rephrased clause) | `sed -n '462,475p' frontend/public/home.html \| grep -c "—"` → 0 |
| AC-4 | IMPLEMENTED | frontend/public/home.html:466 | Manual read: "...coordinates the coding agents you already use (Claude, Codex, and others, not a fixed pairing)..." preserves original meaning |
| AC-5 | IMPLEMENTED | n/a (no change to these cards) | `git diff frontend/public/home.html \| grep -E '^[+-]'` shows no +/- lines inside vLLM, H100, or Pydantic AI blocks |
| AC-6 | IMPLEMENTED | frontend/public/home.html (whole file) | `grep -c "—" frontend/public/home.html` → 0 (baseline was 1; differs by exactly 1) |
| AC-7 | IMPLEMENTED | frontend/public/home.html | `python3 -c "import html.parser, pathlib; ...feed(...)"` → exit 0, `parsed ok` |
| AC-8 | IMPLEMENTED | n/a (no change below line 504) | `git diff frontend/public/home.html \| grep -E '^@@'` → hunks `@@ -459,6 +459,20 @@` and `@@ -486,20 +500,6 @@`, both entirely within old lines ≤506 (Open source section) |
