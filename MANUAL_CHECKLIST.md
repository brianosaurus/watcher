# Manual checklist

Base checks: 9; resolved: 1; added: 1; removed: 0

### MC-1 Card order after move

- Priority: P0
- Behavior classification: MODIFY
- Related behavior: BX-1
- Related invariant: IX-2
- Preconditions: implementation edit applied to frontend/public/home.html
- Exclusive resources: none
- Depends on: none
- Exact action: `grep -o '<h3><a[^>]*>[^<]*</a>' frontend/public/home.html | sed -n '1,4p'` within the Open source `.projects` div (home.html:439-503 range)
- Expected result: order is vLLM, Uncle, H100 Roofline Study, Pydantic AI
- Evidence to capture: command output
- Actual result:
- Status: NOT RUN

### MC-2 Uncle card content unchanged except em-dash clause

- Priority: P0
- Behavior classification: MODIFY
- Related behavior: BX-1, BX-2
- Related invariant: none
- Preconditions: implementation edit applied
- Exclusive resources: none
- Depends on: none
- Exact action: `git diff frontend/public/home.html` — inspect the Uncle `<article>` block's h3/p/div.links content
- Expected result: only textual difference inside the Uncle block is the em-dash clause rewrite; no other wording, link, or tag change
- Evidence to capture: diff excerpt for the Uncle block
- Actual result:
- Status: NOT RUN

### MC-3 No em dash remains in Uncle card

- Priority: P0
- Behavior classification: MODIFY
- Related behavior: BX-2
- Related invariant: none
- Preconditions: implementation edit applied
- Exclusive resources: none
- Depends on: none
- Exact action: `sed -n '462,474p' frontend/public/home.html | grep -c "—"` (Uncle card's post-move range per change.diff:9-21)
- Expected result: 0
- Evidence to capture: command output
- Actual result:
- Status: NOT RUN

### MC-4 Rephrased clause preserves meaning

- Priority: P1
- Behavior classification: MODIFY
- Related behavior: BX-2
- Related invariant: none
- Preconditions: implementation edit applied
- Exclusive resources: none
- Depends on: none
- Exact action: read the rewritten clause at frontend/public/home.html:465
- Expected result: sentence still conveys that coding agents already in use (e.g. Claude, Codex, others) are coordinated, not a fixed pairing; no em dash
- Evidence to capture: quoted rewritten sentence
- Actual result:
- Status: NOT RUN

### MC-5 vLLM, H100 Roofline Study, Pydantic AI cards byte-identical

- Priority: P0
- Behavior classification: PRESERVE
- Related behavior: BX-3
- Related invariant: IX-2
- Preconditions: pre-edit baseline snapshot of the three `<article>` blocks captured before implementation began
- Exclusive resources: none
- Depends on: none
- Exact action: extract each of the three `<article class="card">` blocks (vLLM: home.html:440-460, H100: 476-489, Pydantic AI: 491-502) from current home.html and diff/hash against the pre-edit baseline snapshot
- Expected result: byte-identical content (whitespace from relocation excepted)
- Evidence to capture: hash or diff output per block
- Actual result:
- Status: NOT RUN

### MC-6 No other em dashes touched

- Priority: P1
- Behavior classification: PRESERVE
- Related behavior: none
- Related invariant: none
- Preconditions: pre-edit baseline count of `grep -c "—" frontend/public/home.html` captured before implementation began
- Exclusive resources: none
- Depends on: none
- Exact action: `grep -c "—" frontend/public/home.html` post-edit; compare to pre-edit baseline count
- Expected result: post-edit count is exactly one less than baseline (or unchanged if em dashes exist elsewhere and are untouched)
- Evidence to capture: before/after counts
- Actual result:
- Status: NOT RUN

### MC-7 HTML well-formed after edit

- Priority: P0
- Behavior classification: MODIFY
- Related behavior: none
- Related invariant: IX-1, IX-3
- Preconditions: implementation edit applied
- Exclusive resources: none
- Depends on: none
- Exact action: `python3 -c "import html.parser,pathlib; p=html.parser.HTMLParser(); p.feed(pathlib.Path('frontend/public/home.html').read_text())"`
- Expected result: exits 0, no exception
- Evidence to capture: exit code, stdout/stderr
- Actual result:
- Status: NOT RUN

### MC-8 Sections below Open source unchanged

- Priority: P0
- Behavior classification: PRESERVE
- Related behavior: BX-4
- Related invariant: none
- Preconditions: implementation edit applied
- Exclusive resources: none
- Depends on: none
- Exact action: `git diff frontend/public/home.html` — confirm both hunks (change.diff:5, change.diff:26) fall entirely within old lines ≤506; inspect for any hunk at or below the `live-systems-heading` line (home.html:506)
- Expected result: no content changes at or below that section
- Evidence to capture: diff output
- Actual result:
- Status: NOT RUN

### MC-9 Route serving mechanism unaffected

- Priority: P2
- Behavior classification: PRESERVE
- Related behavior: BX-5
- Related invariant: I-1 (BASELINE_REPORT.md)
- Preconditions: none
- Exclusive resources: none
- Depends on: none
- Exact action: confirm `app/main.py` is absent from `git diff --stat` output
- Expected result: `app/main.py` not listed as changed
- Evidence to capture: diff --stat output
- Actual result:
- Status: NOT RUN

### MC-10 Change scope limited to home.html

- Priority: P1
- Behavior classification: PRESERVE
- Related behavior: none
- Related invariant: none
- Preconditions: implementation edit applied
- Exclusive resources: none
- Depends on: none
- Exact action: `git diff --stat` — full file list, independent of IMPLEMENTATION_NOTES.md:9's "No other files changed" claim
- Expected result: only `frontend/public/home.html` listed as changed
- Evidence to capture: diff --stat output
- Actual result:
- Status: NOT RUN

## Acceptance-criteria traceability

AC-1: MC-1. AC-2: MC-2. AC-3: MC-3. AC-4: MC-4. AC-5: MC-5. AC-6: MC-6. AC-7: MC-7. AC-8: MC-8.

## Preserved-behavior coverage

BX-3: MC-5. BX-4: MC-8. BX-5: MC-9.

## Changed-behavior coverage

BX-1: MC-1, MC-2. BX-2: MC-2, MC-3, MC-4.

## Invariant coverage

IX-1: MC-7. IX-2: MC-1, MC-5. IX-3: MC-7.

## Regression coverage

MC-5 (adjacent cards), MC-8 (other sections), MC-9 (backend route), MC-10 (full change scope) cover BASELINE_REPORT.md §13 regression-sensitive components.

## Removed checks

None. No base check is provably inapplicable to change.diff.