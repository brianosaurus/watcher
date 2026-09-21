# Change specification

Omitted sections: Performance requirements (static text edit, no perf implication); Migration requirements (no data/schema); Prototype-isolation requirements (not a prototype)

## 1. Change type

Content/copy correction (portfolio card + positioning doc). Not a bug fix in code; no
behavioral/logic change to `app/main.py`.

## 2. Problem statement

The "Agentic Workflow" card on the portfolio home page (BASELINE_REPORT.md B-2..B-4) and
`AGENTIC_WORKFLOW_STRATEGY.md` (B-5) describe a fictional "Claude builds, Codex audits" pipeline
and link to a repo that is not the real project. The real project is `unclehq/uncle`.

## 3. Current behavior

Per BASELINE_REPORT.md B-2, B-3, B-4, B-5. Card links point to
`github.com/brianosaurus/agentic-workflow` (not `unclehq/stagegate` as CHANGE_REQUEST.md
assumed — BASELINE_REPORT.md section 4 note, treated as authoritative over the stale CR premise).

## 4. Desired behavior

Card heading, URL label, and Code link point to `https://github.com/unclehq/uncle`. Body copy
and tag describe uncle accurately: agent-agnostic, terminal-native, issue-in/verified-PR-out,
independent review, human approval gates, cryptographic pinning of plans/artifacts.
`AGENTIC_WORKFLOW_STRATEGY.md` framing updated to match (agent-agnostic, not Claude/Codex).

## 5. Acceptance criteria

| ID | Criterion | Verification |
|---|---|---|
| AC-1 | Card heading link, URL label, and `Code` link (frontend/public/home.html:491,497) all target `https://github.com/unclehq/uncle` | grep for `unclehq/uncle` count = 3 in the card block; grep for `brianosaurus/agentic-workflow` and `unclehq/stagegate` count = 0 file-wide |
| AC-2 | Body copy (2-4 sentences) states: terminal-native; issue/requirements in, verified PR out; works with existing coding agents (not a fixed pairing); independent review; human approval gates; cryptographically pinned plans/artifacts | Manual read of `<p>` block against these six points |
| AC-3 | No mention of "Claude" and "Codex" as a fixed pairing anywhere in the card or in AGENTIC_WORKFLOW_STRATEGY.md | grep `-i "claude builds\|codex audits\|claude/codex"` across both files returns 0 matches |
| AC-4 | `unclehq/stagegate` does not appear anywhere in the repo after the change (already true at baseline — must remain true) | grep `-r "stagegate"` repo-wide (excluding `.git`) returns 0 matches, or, if uncle's own repo shows stagegate as a distinct still-maintained component, a justified exception is documented in the PR description |
| AC-5 | `tag` line (frontend/public/home.html:498) reflects uncle's actual scope, not "LLM agents · pipeline tooling · open source" verbatim unless still accurate | grep confirms line no longer reads exactly the old B-4 text |
| AC-6 | `AGENTIC_WORKFLOW_STRATEGY.md` positioning language matches uncle (agent-agnostic; no "Claude builds, Codex audits") | Manual read; AC-3 grep covers the banned phrase |
| AC-7 | Copy is derived from uncle's actual README/source, not rewritten from the old card's assumptions | Implementer's plan/PR notes cite what was read from `github.com/unclehq/uncle` before writing copy |
| AC-8 | Adjacent cards (frontend/public/home.html:463-489, 507+) remain byte-identical | `git diff` shows no hunks outside lines 490-500 in home.html |
| AC-9 | HTML remains well-formed after edit | `python3 -c "import html.parser,pathlib; p=html.parser.HTMLParser(); p.feed(pathlib.Path('frontend/public/home.html').read_text())"` exits 0 |

## 6. Observable behavior table

| ID | Class | Trigger | Current behavior | Expected behavior | Verification |
|---|---|---|---|---|---|
| BX-1 | MODIFY | View card heading/URL/Code link | Points to `brianosaurus/agentic-workflow` (B-2) | Points to `https://github.com/unclehq/uncle` | AC-1 |
| BX-2 | MODIFY | Read card body copy | Describes Claude/Codex pairing (B-3) | Describes uncle per AC-2 | AC-2, AC-7 |
| BX-3 | MODIFY | Read card tag line | "LLM agents · pipeline tooling · open source" (B-4) | Reflects uncle's scope | AC-5 |
| BX-4 | MODIFY | Read AGENTIC_WORKFLOW_STRATEGY.md | Frames Claude/Codex pairing, proposes rename (B-5) | Agent-agnostic framing matching uncle | AC-3, AC-6 |
| BX-5 | PRESERVE | View any other card on the home page | Unchanged (B-1) | Unchanged | AC-8 |
| BX-6 | PRESERVE | GET `/` route | Serves `static/home.html` via FileResponse (I-1) | Unchanged | Not re-tested; no route/code change |

## 7. Invariant table

| ID | Status | Invariant | Scope | Enforcement point | Verification |
|---|---|---|---|---|---|
| IX-1 | EXISTING | Card markup follows sibling structure `article.card > h3(a+span.url), p, div.links(a...,span.tag)` (I-2) | frontend/public/home.html:490-500 | Manual/HTML parse | AC-9 |
| IX-2 | EXISTING | `frontend/public/home.html` stays static HTML, no templating introduced (I-3) | Whole file | Manual read | AC-9 |
| IX-3 | NEW | No fixed Claude/Codex pairing described anywhere in the two touched files | home.html card, AGENTIC_WORKFLOW_STRATEGY.md | grep | AC-3 |

## 8. Compatibility requirements

Route `/` and `FileResponse` mechanism (I-1) unchanged. No build config, no schema, no API
surface touched.

## 9. Error and failure behavior

Not applicable — static copy change, no error paths introduced.

## 11. Security requirements

None beyond existing: outbound links use `rel="noopener noreferrer"` already present on
sibling cards (frontend/public/home.html:472,478,483); the rewritten `unclehq/uncle` links must
keep this attribute.

## 13. Rollback expectations

Revert the two files (`frontend/public/home.html`, `AGENTIC_WORKFLOW_STRATEGY.md`) via git;
no other rollback surface exists (no schema/migration/build-artifact state).

## 15. Explicit non-goals

- Do not rename other cards, restructure the home page layout, or touch CSS.
- Do not modify `app/main.py`, routing, or build config.
- Do not add tests infrastructure (none exists; not required by the CR).
- Do not act on `AGENTIC_WORKFLOW_STRATEGY.md`'s own "Immediate next steps" (rename decision,
  CONTRIBUTING.md, demo video, HN post) — those are unrelated backlog items in that file, not
  part of this change.

## 16. Assumptions and unresolved questions

- ASSUMPTION (carried from BASELINE_REPORT.md section 15): current card link is
  `brianosaurus/agentic-workflow`, not `unclehq/stagegate` as CHANGE_REQUEST.md states. This spec
  treats the observed repo state as ground truth; AC-4's stagegate check is satisfied trivially
  at baseline and must remain satisfied.
  Settled by: no further action needed unless implementation discovers a stagegate reference
  elsewhere.
- UNRESOLVED: exact wording of uncle's README (BASELINE_REPORT.md section 15, second item) is
  not yet read. AC-7 requires the implementer to read `https://github.com/unclehq/uncle` before
  finalizing body copy; this spec does not pre-write the copy so it is not derived secondhand.
  Settled by: implementation stage fetching the README and citing it.
