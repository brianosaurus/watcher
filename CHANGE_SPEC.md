# Change specification

Omitted sections: Performance requirements (static markup reorder, no perf implication); Security requirements (no new links/attributes); Migration requirements (no data/schema); Prototype-isolation requirements (not a prototype)

NOTE: BASELINE_REPORT.md documents a prior change (rewriting the Agentic Workflow card into
the Uncle card) that is already applied in the working tree (frontend/public/home.html:490-502
already links `unclehq/uncle`). CHANGE_REQUEST.md (Issue 3) is a distinct, later request:
reorder the already-rewritten Uncle card and remove its em dash. Baseline's sections 1-4 describe
the superseded change; this spec relies instead on direct inspection of
frontend/public/home.html:439-503 (current state), cited below by line number.

## 1. Change type

Refactor (markup reorder) + copy fix (em dash removal). No route, schema, or logic change.

## 2. Problem statement

The Uncle card is the 4th card in the "Open source" `.projects` list (home.html:490-502),
after vLLM, H100 Roofline Study, and Pydantic AI. CHANGE_REQUEST.md asks it to appear above the
H100 Roofline Study card. The card body also contains one em dash (home.html:493, "others — not
a fixed pairing") that CHANGE_REQUEST.md asks to be removed.

## 3. Current behavior

- Card order in `.projects` (home.html:439-503): vLLM (440-460), H100 Roofline Study (462-475),
  Pydantic AI (477-488), Uncle (490-502).
- Uncle card body (home.html:493) reads "...coordinates the coding agents you already use
  (Claude, Codex, and others — not a fixed pairing)..." — one em dash character (`—`).

## 4. Desired behavior

- Card order becomes: vLLM, Uncle, H100 Roofline Study, Pydantic AI — i.e. the Uncle card
  (lines 490-502) moves to directly after the vLLM card (after line 460) and before the H100
  Roofline Study card.
- Uncle card body no longer contains an em dash; the clause is rephrased using a comma, period,
  or parentheses so the sentence reads naturally without `—`.
- Uncle card's own content (links, tag, wording other than the em dash) is otherwise unchanged.

## 5. Acceptance criteria

| ID | Criterion | Verification |
|---|---|---|
| AC-1 | In `frontend/public/home.html`, the Uncle `article.card` block appears immediately after the vLLM card and immediately before the H100 Roofline Study card, within the same `.projects` div | Read file: order of `<h3>` link texts under `open-source-heading` is vLLM, Uncle, H100 Roofline Study, Pydantic AI |
| AC-2 | The Uncle card block (all of h3/p/div.links) is textually identical to its pre-move content except for the em-dash rephrase in AC-3 | `git diff` shows the Uncle `<article>` block moved with no unrelated wording changes |
| AC-3 | No em dash character (`—`) remains anywhere in the Uncle card | `grep -c "—" ` restricted to the Uncle card's line range returns 0 |
| AC-4 | The rephrased sentence at former home.html:493 preserves its meaning: coding agents already in use (e.g. Claude, Codex, others) are coordinated, not a fixed pairing | Manual read of the rewritten clause |
| AC-5 | vLLM, H100 Roofline Study, and Pydantic AI cards are byte-identical to baseline except for surrounding whitespace from the move | `git diff` shows no content hunks inside those three `<article>` blocks |
| AC-6 | No other `—` characters in `frontend/public/home.html` are touched (only the one in the Uncle card is in scope) | `grep -c "—" frontend/public/home.html` before/after differs by exactly 1 (or 0 if other em dashes coincidentally exist elsewhere and are left untouched — count outside the Uncle card is unchanged) |
| AC-7 | HTML remains well-formed after edit | `python3 -c "import html.parser,pathlib; p=html.parser.HTMLParser(); p.feed(pathlib.Path('frontend/public/home.html').read_text())"` exits 0 |
| AC-8 | Sections other than "Open source" (`live-systems-heading` and beyond, home.html:506+) are unchanged | `git diff` shows no hunks below line 504 |

## 6. Observable behavior table

| ID | Class | Trigger | Current behavior | Expected behavior | Verification |
|---|---|---|---|---|---|
| BX-1 | MODIFY | View "Open source" card order | vLLM, H100 Roofline Study, Pydantic AI, Uncle | vLLM, Uncle, H100 Roofline Study, Pydantic AI | AC-1 |
| BX-2 | MODIFY | Read Uncle card body clause at former line 493 | "...you already use (Claude, Codex, and others — not a fixed pairing)..." | Same meaning, no em dash | AC-3, AC-4 |
| BX-3 | PRESERVE | View vLLM, H100 Roofline Study, Pydantic AI card content | Unchanged text | Unchanged text | AC-5 |
| BX-4 | PRESERVE | View any card outside "Open source" section | Unchanged | Unchanged | AC-8 |
| BX-5 | PRESERVE | GET `/` route (app/main.py:1785-1786) | Serves built `static/home.html` via `FileResponse` | Unchanged | Not re-tested; no code change |

## 7. Invariant table

| ID | Status | Invariant | Scope | Enforcement point | Verification |
|---|---|---|---|---|---|
| IX-1 | EXISTING | Card markup follows sibling structure `article.card > h3(a+span.url), p, div.links(a...,span.tag)` | frontend/public/home.html:439-503 | Manual/HTML parse | AC-7 |
| IX-2 | EXISTING | `.projects` div contains exactly 4 `article.card` children in "Open source" section (only order changes, not count) | frontend/public/home.html:439-503 | Manual count | AC-1, AC-5 |
| IX-3 | EXISTING | `frontend/public/home.html` stays static HTML, no templating introduced | Whole file | Manual read | AC-7 |

## 8. Compatibility requirements

Route `/` and `FileResponse` mechanism (app/main.py:1785-1786) unchanged. No build config,
schema, or API surface touched.

## 9. Error and failure behavior

Not applicable — static markup reorder and text edit, no error paths introduced.

## 10. Rollback expectations

Revert `frontend/public/home.html` via git; no other rollback surface (no schema/migration/
build-artifact state).

## 11. Explicit non-goals

- Do not reorder or edit vLLM, H100 Roofline Study, or Pydantic AI card content.
- Do not touch sections below "Open source" (Live systems and beyond, home.html:506+).
- Do not modify `app/main.py`, routing, or build config.
- Do not remove em dashes anywhere outside the Uncle card.
- Do not re-litigate the prior Uncle-card content rewrite (already applied; out of scope here).

## 12. Assumptions and unresolved questions

- ASSUMPTION: "this card" in CHANGE_REQUEST.md ("move the uncle card... above this card") refers
  to the H100 Roofline Study card, matched via the CR's own excerpt ("Latest study / What is an
  H100 actually doing?" mirrors home.html:464-465's "Roofline study of five open models on an
  H100"). Unverified: no other card in the home page matches that excerpt as closely.
  Settled by: AC-1 fixes the target position explicitly; a reviewer can reject at the spec gate
  if a different target was intended.
- ASSUMPTION: "remove the em dashes" (plural in CR) refers to the single em dash found in the
  Uncle card (home.html:493); no other em dash exists in that card block.
  Settled by: AC-3/AC-6 grep-verify the count within the card is 0 after the change.
