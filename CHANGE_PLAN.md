# Change plan

Issue 3

| Finding | Disposition | Reason | Exact plan change |
|---|---|---|---|
| AR-001 | Accepted | Stale AC-1..AC-9 artifacts (CHANGE_TEST_REPORT.md, VERIFICATION_REPORT.md, MANUAL_CHECKLIST.md, DEFECTS.md, IMPLEMENTATION_NOTES.md) describe the prior "rewrite Uncle card" change, not this move+em-dash change | Section 9 (test-report scoping rule added) |
| AR-002 | Accepted | `git diff` hunk boundaries on a relocated block can absorb unchanged intervening cards as context, making "no hunks inside X" unreliable | Section 10 (content-hash regression check replaces hunk-location check) |
| AR-003 | Partially accepted | AC-4 keeps a manual grammaticality read (irreducibly subjective) but gains an objective substring check | Section 11 step 2 (added grep assertions) |

Omitted sections: Data-flow changes (none — static markup); State-transition changes (none); Interface and API changes (none); Schema or persistence changes (none); Concurrency implications (none); Migration plan (none); Feature-flag or containment strategy (single static-file edit, no runtime toggle); Observability changes (none)

## 1. Selected technical approach

Single in-place edit to `frontend/public/home.html`: cut the Uncle `<article class="card">` block
(lines 490-502) and reinsert it immediately after the vLLM card (after line 460, before line 462's
H100 card open tag). Within the moved block, rewrite the em-dash clause at former line 493 to drop
`—` while preserving meaning (AC-4), e.g. "...coding agents you already use (Claude, Codex, and
others, not a fixed pairing)...".

## 2. Alternative approaches considered

- CSS `order` reorder: rejected — source order stays wrong; CHANGE_SPEC.md IX-2 requires document
  order.
- Templating for card order: rejected — IX-3 requires the file stay plain static HTML.

## 3. Why the selected approach is preferred

Matches IX-3, minimal diff scoped to AC-1/AC-3, keeps AC-5/AC-8 trivially satisfiable.

## 4. Exact components to modify

- `frontend/public/home.html:439-503` — "Open source" `.projects` div only.

## 5. Components explicitly not to modify

- `frontend/public/home.html:506+` (Live systems and later sections).
- `app/main.py`, `frontend/vite.config.js`, `package.json`.
- vLLM, H100 Roofline Study, Pydantic AI card content.

## 6. Compatibility strategy

No interface changes. `/` route continues serving `static/home.html` unchanged
(app/main.py:1785-1786, CHANGE_SPEC.md BX-5).

## 7. Error and recovery behavior

Not applicable. A malformed move (unbalanced tags) is caught by the HTML-parse check (AC-7).

## 8. Rollback plan

`git checkout -- frontend/public/home.html` restores prior state.

## 9. Automated-test strategy

No test suite exists (no pytest/vitest/jest config, no CI). None added (CHANGE_SPEC.md section
11). Verification uses the scripted checks below. Any test-report artifact this change produces
must target only this spec's AC-1..AC-8 (card order, em-dash removal); it must not reuse or
extend CHANGE_TEST_REPORT.md, VERIFICATION_REPORT.md, MANUAL_CHECKLIST.md, DEFECTS.md, or
IMPLEMENTATION_NOTES.md from the prior "rewrite Uncle card" change (AR-001) — those check for
`unclehq/uncle` link presence and the "Claude builds, Codex audits" phrase, which is out of scope
here.

## 10. Regression-test strategy

Content-identity check, not hunk-location: before editing, extract the vLLM, H100 Roofline
Study, and Pydantic AI `<article>` blocks (delimited by their `<h3>` anchor text) into three
strings; after editing, re-extract the same three blocks by anchor text and diff each string
pair directly. All three must be byte-identical (AC-5). Separately confirm no line at or below
current line 504 (`live-systems-heading` and beyond) changed, via `diff <(sed -n '504,$p' <old>)
<(sed -n '<new-504-equivalent>,$p' <new>)` after accounting for the block's line-count shift
(AC-8). This replaces the AR-002 hunk-location check.

## 11. Manual-verification strategy

1. `grep -n "<h3>" frontend/public/home.html | sed -n '1,4p'` — confirm order is vLLM, Uncle,
   H100 Roofline Study, Pydantic AI (AC-1).
2. Em-dash and rewrite check: `grep -c "—" frontend/public/home.html` before/after differs by
   exactly 1, and 0 within the Uncle card's new line range (AC-3, AC-6). Then
   `grep -A5 "<h3>.*Uncle" frontend/public/home.html | grep -c "not a fixed pairing"` returns 1
   and the same span still contains "Claude" and "Codex" (objective proxy for AC-4's meaning
   preservation); follow with one manual read of the full rewritten clause for grammaticality
   (AC-4).
3. `python3 -c "import html.parser,pathlib; p=html.parser.HTMLParser(); p.feed(pathlib.Path('frontend/public/home.html').read_text())"` exits 0 (AC-7).
4. Run the section 10 content-identity diffs and confirm zero differences (AC-2, AC-5, AC-8).

## 12. Implementation sequence

1. Edit `frontend/public/home.html`: relocate the Uncle `<article class="card">` block (lines
   490-502) to directly after the vLLM `<article>`'s closing `</article>` (line 460) and before
   the H100 Roofline Study `<article>` (line 462); rewrite the clause at former line 493 to
   remove the em dash while preserving meaning.
   Owns: `frontend/public/home.html`
   Depends on: none

2. Run verification commands from section 11 against the edited file and record results.
   Owns: none (read-only verification; no file writes)
   Depends on: 1

## Change-impact table

| Component | Change | Test coverage |
|---|---|---|
| `frontend/public/home.html` | Move Uncle `<article>` block above H100 Roofline Study card; remove one em dash in its body copy | Section 10 content-identity diffs + section 11 manual checks |

## Traceability

| Requirement | Behavior | Invariant | Component | Automated test | Manual check |
|---|---|---|---|---|---|
| AC-1 | BX-1 | IX-2 | `frontend/public/home.html` | none | Step 1 of section 11 |
| AC-2 | BX-1 | IX-1 | `frontend/public/home.html` | none | Step 4 of section 11 |
| AC-3 | BX-2 | — | `frontend/public/home.html` | none | Step 2 of section 11 |
| AC-4 | BX-2 | — | `frontend/public/home.html` | none | Step 2 of section 11 |
| AC-5 | BX-3 | IX-2 | `frontend/public/home.html` | none | Step 4 of section 11 / section 10 |
| AC-6 | BX-2 | — | `frontend/public/home.html` | none | Step 2 of section 11 |
| AC-7 | BX-1, BX-2 | IX-1, IX-3 | `frontend/public/home.html` | none | Step 3 of section 11 |
| AC-8 | BX-4 | — | `frontend/public/home.html` | none | Step 4 of section 11 / section 10 |

## Scope cuts under time pressure

None — single-file, single-block move plus a one-clause rewrite; no reduced scope available
without failing AC-1 or AC-3.

## Risks and unresolved questions

- R-1 (source_kind: USER; source: CHANGE_REQUEST.md "above this card"; requirement: AC-1;
  required property: correct insertion point; selected mechanism: match CR's H100 excerpt to
  home.html:464-465 per CHANGE_SPEC.md section 12 assumption; rationale: closest and only textual
  match in the file; CAP: none needed, plain-text edit). Resolved by CHANGE_SPEC.md's stated
  assumption and AC-1's explicit target; not a blocking question.
- Build artifact `static/home.html` does not exist in this worktree; this plan edits the source
  `frontend/public/home.html` only (Vite copies `public/*` verbatim on build). No build step is
  part of this plan (CODING phase only; no LIVE_VERIFICATION step requires `npm run build`).
