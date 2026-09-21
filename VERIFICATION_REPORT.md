# Verification report

## MC-1 Card order after move
- Action: `grep -o '<h3><a[^>]*>[^<]*</a>' frontend/public/home.html | sed -n '1,4p'` (worker MC-1.md)
- Expected: order vLLM, Uncle, H100 Roofline Study, Pydantic AI
- Actual: order matches exactly
- Status: PASS
- Defect: none

## MC-2 Uncle card content unchanged except em-dash clause
- Action: `git diff frontend/public/home.html`, added vs removed Uncle block compared line-by-line (worker MC-2.md)
- Expected: only the em-dash clause differs
- Actual: h3, links, tag identical; `<p>` differs only in "— not a" vs ", not a"
- Status: PASS
- Defect: none

## MC-3 No em dash remains in Uncle card
- Action: `sed -n '462,474p' frontend/public/home.html | grep -c "—"` (worker MC-3.md)
- Expected: 0
- Actual: 0
- Status: PASS
- Defect: none

## MC-4 Rephrased clause preserves meaning
- Action: read frontend/public/home.html:462-474 (worker MC-4.md)
- Expected: coordination of already-in-use agents, not a fixed pairing; no em dash
- Actual: "coordinates the coding agents you already use (Claude, Codex, and others, not a fixed pairing)" — meaning preserved, no em dash
- Status: PASS
- Defect: none

## MC-5 vLLM, H100 Roofline Study, Pydantic AI cards byte-identical
- Action: `diff <(git show HEAD:frontend/public/home.html | sed -n '<baseline range>p') <(sed -n '<current range>p')` for each of the 3 cards (worker MC-5.md)
- Expected: byte-identical content, position may shift
- Actual: all three diffs empty; only position changed for H100/Pydantic AI
- Status: PASS
- Defect: none

## MC-6 No other em dashes touched
- Action: `git show HEAD:frontend/public/home.html | grep -c "—"` vs `grep -c "—" frontend/public/home.html` (worker MC-6.md)
- Expected: post-edit count is baseline minus 1
- Actual: baseline 1, post-edit 0
- Status: PASS
- Defect: none

## MC-7 HTML well-formed after edit
- Action: `python3 -c "import html.parser,pathlib; p=html.parser.HTMLParser(); p.feed(pathlib.Path('frontend/public/home.html').read_text())"` (worker MC-7.md)
- Expected: exit 0, no exception
- Actual: exit 0, no exception
- Status: PASS
- Defect: none

## MC-8 Sections below Open source unchanged
- Action: `git diff frontend/public/home.html`, hunk range inspection (worker MC-8.md)
- Expected: no changes at/below `live-systems-heading` (home.html:506)
- Actual: hunks `@@ -459,6 +459,20 @@` and `@@ -486,20 +500,6 @@`, both old-range ≤506; no hunk below that line
- Status: PASS
- Defect: none

## MC-9 Route serving mechanism unaffected
- Action: `git diff --stat` (worker MC-9.md)
- Expected: `app/main.py` not listed
- Actual: not listed; changed files are docs + frontend/public/home.html
- Status: PASS
- Defect: none

## MC-10 Change scope limited to home.html
- Action: `git diff --stat` (worker MC-10.md)
- Expected: only `frontend/public/home.html` listed as changed
- Actual: 8 files changed — ADVERSARIAL_REVIEW.md, CHANGE_PLAN.md, CHANGE_REQUEST.md, CHANGE_SPEC.md, CHANGE_TEST_REPORT.md, IMPLEMENTATION_NOTES.md, MANUAL_CHECKLIST.md, frontend/public/home.html
- Status: FAIL
- Evidence: `git diff --stat` output quoted in worker MC-10.md
- Defect: D-1

## Acceptance criteria summary
AC-1..AC-8 map to MC-1..MC-8 respectively (MANUAL_CHECKLIST.md traceability table); all PASS.

## Preserved-behavior summary
BX-3 (MC-5), BX-4 (MC-8), BX-5 (MC-9) all PASS: adjacent cards, other sections, and backend route untouched.

## Changed-behavior summary
BX-1 (MC-1, MC-2) and BX-2 (MC-2, MC-3, MC-4) PASS: card relocated, em dash removed, meaning preserved.

## Invariant summary
IX-1 (MC-7) PASS. IX-2 (MC-1, MC-5) PASS. IX-3 (MC-7) PASS.

## Regression summary
MC-5, MC-8, MC-9 PASS (no regression in adjacent cards, other sections, backend route). MC-10 FAIL: workflow-document churn (7 non-home.html files) is outside CHANGE_SPEC.md's stated scope of `frontend/public/home.html` only, though these are the workflow's own generated artifacts, not application source/product files.

## Unresolved defects
D-1 (MC-10, open).

## Recommendation
Application-facing change (home.html) satisfies all AC/BX/IX checks. MC-10's literal criterion fails only against non-product workflow-artifact files (ADVERSARIAL_REVIEW.md, CHANGE_PLAN.md, CHANGE_REQUEST.md, CHANGE_SPEC.md, CHANGE_TEST_REPORT.md, IMPLEMENTATION_NOTES.md, MANUAL_CHECKLIST.md); no evidence these files affect runtime behavior. Do not mark MC-10 PASS despite that: the checklist's exact wording was not met, and reconciling scope wording is a plan/spec decision, not this stage's to make.

## Acceptance gate

| ID | Required | Status | Evidence |
|---|---|---|---|
| MC-1 | YES | PASS | grep output order matches vLLM, Uncle, H100 Roofline Study, Pydantic AI |
| MC-2 | YES | PASS | git diff shows only em-dash clause differs in Uncle block |
| MC-3 | YES | PASS | grep -c em dash in Uncle range returns 0 |
| MC-4 | YES | PASS | rewritten clause preserves meaning, no em dash |
| MC-5 | YES | PASS | diff of 3 card blocks vs baseline empty |
| MC-6 | YES | PASS | em-dash count baseline 1, post-edit 0 |
| MC-7 | YES | PASS | html.parser exit 0 |
| MC-8 | YES | PASS | diff hunks confined to old lines <=506 |
| MC-9 | NO | PASS | app/main.py absent from git diff --stat |
| MC-10 | YES | FAIL | git diff --stat lists 7 non-home.html files changed |
