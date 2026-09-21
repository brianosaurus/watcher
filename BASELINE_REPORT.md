# Baseline report

Omitted sections: Reproduction result for the reported bug (not a bug fix; copy/link rewrite)

## 1. Change-request summary

See CHANGE_REQUEST.md. Rewrite the "Agentic Workflow" card on the portfolio home page and
`AGENTIC_WORKFLOW_STRATEGY.md` to describe the real project `unclehq/uncle` instead of a
fictional Claude/Codex pairing.

## 2. Repository architecture

- FastAPI backend `app/main.py` (1882 lines) serves static/portfolio content and a trading-bot
  dashboard API.
- Portfolio home page source lives at `frontend/public/home.html` (599 lines), plain HTML/CSS,
  no templating engine, no JS framework dependency for this page.
- `frontend/vite.config.js:9-11` sets `base: '/static/'`, `outDir: '../static'`. Vite's `public/`
  convention copies `frontend/public/*` verbatim into the build output, so `static/home.html`
  (served path) is a build artifact of `frontend/public/home.html` (source of truth). `static/`
  is not checked in and does not exist in this worktree (unbuilt).
- `app/main.py:1785-1786` — route handler returns `FileResponse(STATIC_DIR / "home.html")`
  where `STATIC_DIR = REPO_ROOT / "static"`.
- `AGENTIC_WORKFLOW_STRATEGY.md` (85 lines) is a standalone positioning-notes doc, not rendered
  by the app.

## 3. Relevant code paths

- `frontend/public/home.html:490-500` — the "Agentic Workflow" `<article class="card">` block:
  heading link (line 491), URL label (line 491), body `<p>` (492-495), `Code` link (497), `tag`
  span (498).
- `AGENTIC_WORKFLOW_STRATEGY.md:1-85` — entire file frames the project as "Claude builds, Codex
  audits" and proposes renaming away from "Agentic Workflow"; needs to match uncle's actual
  agent-agnostic framing.
- `app/main.py:1785-1786` — unaffected; serves the file unchanged.

## 4. Current observable behavior

| ID | Trigger | Current result | Evidence | Must preserve? |
|---|---|---|---|---|
| B-1 | GET `/` on the running app | Returns `frontend/public/home.html` (once built to `static/home.html`) unmodified | app/main.py:1785-1786 | Yes — route and serving mechanism |
| B-2 | View "Agentic Workflow" card heading/URL/Code link | All three point to `https://github.com/brianosaurus/agentic-workflow` | frontend/public/home.html:491,497 | No — CR requires these to point to `https://github.com/unclehq/uncle` |
| B-3 | View card body copy | Describes "Claude builds, Codex audits in a read-only sandbox" and SHA-256-pinned approvals only | frontend/public/home.html:492-495 | No — must be rewritten per CR acceptance criteria |
| B-4 | View card `tag` line | Reads "LLM agents · pipeline tooling · open source" | frontend/public/home.html:498 | No — must be updated to match new scope |
| B-5 | Read AGENTIC_WORKFLOW_STRATEGY.md | Frames product as "Claude builds, Codex audits", proposes renaming, lists HN-launch tactics | AGENTIC_WORKFLOW_STRATEGY.md:1-85 | No — positioning language must match uncle |

Note: CHANGE_REQUEST.md states the card links to `github.com/unclehq/stagegate`; the actual
current link is `github.com/brianosaurus/agentic-workflow` (frontend/public/home.html:491,497).
No reference to `unclehq/stagegate` or `unclehq` exists anywhere in the tree (verified by
repo-wide grep). Treated as a stale premise in the change request, not a baseline defect;
flagged in Unknowns (section 15) for the spec stage to resolve.

## 5. Existing invariants

| ID | Invariant | Current enforcement | Existing test | Confidence |
|---|---|---|---|---|
| I-1 | `/` route serves the built `static/home.html` byte-for-byte via `FileResponse` | app/main.py:1785-1786 | None | High |
| I-2 | Card markup follows sibling-card structure: `article.card > h3(a + span.url), p, div.links(a..., span.tag)` | frontend/public/home.html:463-500 (adjacent cards use identical structure) | None | High |
| I-3 | `frontend/public/home.html` is plain static HTML with no build-time templating for card content | Whole-file structure (599 lines, no `{{`/templating syntax found) | None | High |

## 6. Current API, schema, and interface contracts

Not applicable — no API/schema touches text/markup content only. The `/` route contract
(`FileResponse` of a static file) is unaffected by this change.

## 7. Existing automated-test coverage

None found. `find . -iname "*test*"` (excluding `.git`, `node_modules`) returns no results.
No pytest/vitest/jest config, no CI workflow files discovered in the repo tree.

## 8. Exact build and test commands executed

```
python3 -m py_compile app/main.py
python3 -c "import html.parser, pathlib; p = html.parser.HTMLParser(); p.feed(pathlib.Path('frontend/public/home.html').read_text()); print('parsed ok')"
grep -c "unclehq/stagegate\|brianosaurus/agentic-workflow" frontend/public/home.html
grep -c "Claude builds, Codex audits" AGENTIC_WORKFLOW_STRATEGY.md frontend/public/home.html
```

## 9. Baseline test results

- `python3 -m py_compile app/main.py` — exit 0, no output (compiles cleanly; file is unaffected
  by the planned change and this only confirms the app still imports/parses before and after).
- HTML parse of `frontend/public/home.html` via `html.parser` — exit 0, printed `parsed ok`
  (no parser exceptions; note `html.parser` is lenient and does not validate nesting/attributes).
- `grep -c "unclehq/stagegate\|brianosaurus/agentic-workflow"` on `frontend/public/home.html` —
  count 2 (both current occurrences are `brianosaurus/agentic-workflow`; `unclehq/stagegate`
  does not appear, consistent with section 4's note).
- `grep -c "Claude builds, Codex audits"` — 1 in `frontend/public/home.html` (line 492), 1 in
  `AGENTIC_WORKFLOW_STRATEGY.md` (line 14).

No test suite exists to run (`pytest`, `npm test` are not configured — section 7). `fastapi` is
not installed in the ambient `python3` (`ModuleNotFoundError: No module named 'fastapi'`);
`app/main.py` was checked with `py_compile` only (syntax/compile check), not executed.
`frontend/node_modules` is absent, so `npm run build` (vite) was not run — it would require a
network-dependent `npm install` first and is not needed to verify a static-HTML/Markdown edit.

## 10. Existing failures, warnings, and flaky behavior

None observed in the commands run. No pre-existing failures to attribute pre/post-change.

## 12. Likely change surface

- `frontend/public/home.html:490-500` (the Agentic Workflow card only — do not touch sibling
  cards at lines 463-489 or 507+).
- `AGENTIC_WORKFLOW_STRATEGY.md` (positioning language throughout; CR does not require deleting
  the file, only aligning its framing).

## 13. Regression-sensitive components

- Adjacent cards in the same `<div class="projects">` list (`frontend/public/home.html:463-489`,
  `507+`) — must remain byte-identical; shared CSS classes (`card`, `url`, `links`, `tag`) mean a
  malformed edit could visually break the whole grid.
- `app/main.py:1785-1786` and the `/static` mount (`app/main.py:1852`) — not touched, but any
  accidental rename/move of `home.html` would break the route.

## 14. Areas explicitly outside the change

- Backend routes, `/leeroy`, `/optimum`, `/h100`, `/blog` handlers (app/main.py) — untouched.
- All other cards on the home page.
- Build tooling (`vite.config.js`, `package.json`).

## 15. Unknowns and assumptions

- ASSUMPTION: CHANGE_REQUEST.md's claim that the card links to `github.com/unclehq/stagegate`
  does not match the current repo state (actual link is `github.com/brianosaurus/agentic-workflow`,
  section 4 note). Unverified: whether `unclehq/stagegate` exists as a real GitHub repo, or was
  already fixed/never existed in this tree.
  Settled by: CHANGE_SPEC.md should treat "current behavior" as the actual observed link
  (`brianosaurus/agentic-workflow`), and the desired behavior as `unclehq/uncle`, without
  depending on the stagegate premise.
- ASSUMPTION: the content of `https://github.com/unclehq/uncle` (README, source) was not fetched
  in this stage (no network access exercised here; baseline is repo-internal).
  Unverified: exact wording of uncle's README/feature set.
  Settled by: the implementation stage fetching/reading the uncle README before writing final
  copy, per CR acceptance criterion 1.

## 16. Initial risk assessment

Low risk. Change is confined to static markup text/links in one card and prose in one
standalone Markdown file; no code paths, schemas, or tests are affected. Main risk is copy
accuracy (requires reading the real uncle repo, not guessing) and accidentally breaking
adjacent-card HTML structure via a bad edit.

## Parallel verification groups

```text
1 2
3 4
```
