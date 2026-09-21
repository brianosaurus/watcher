# Change plan

Issue 1

Omitted sections: Data-flow changes (none — static text); State-transition changes (none); Interface and API changes (none); Schema or persistence changes (none); Migration plan (none); Feature-flag or containment strategy (static copy, no flag needed); Observability changes (none)

## 1. Selected technical approach

Fetch `github.com/unclehq/uncle`'s README/source once, then hand-edit two files directly:
`frontend/public/home.html:490-500` (the card) and `AGENTIC_WORKFLOW_STRATEGY.md` (positioning
prose). No tooling, template, or script is introduced — both are plain-text edits consistent
with BASELINE_REPORT.md I-2/I-3.

## 2. Alternative approaches considered

- Generate the card body via a script/templating layer reading uncle's README at build time —
  rejected: no templating exists (I-3), and the CR asks for a one-time accurate rewrite, not a
  live sync mechanism (D-1).
- Delete `AGENTIC_WORKFLOW_STRATEGY.md` instead of updating it — rejected: CR explicitly asks to
  bring it "in line," not remove it (CHANGE_REQUEST.md line 31) (D-2).

## 3. Why the selected approach is preferred

Smallest change that satisfies CHANGE_SPEC.md AC-1..AC-9 without introducing new tooling,
matching the "proportional implementation" guidance and BASELINE_REPORT.md's risk assessment
(section 16: low risk, confined to two files).

## 4. Exact components to modify

- `frontend/public/home.html` (lines 490-500 only).
- `AGENTIC_WORKFLOW_STRATEGY.md` (whole file: reframe sections that assert Claude/Codex pairing).

## 5. Components explicitly not to modify

- Sibling cards in `frontend/public/home.html` (lines 463-489, 507+) — CHANGE_SPEC.md BX-5, AC-8.
- `app/main.py` route/serving logic (BASELINE_REPORT.md I-1) — CHANGE_SPEC.md BX-6.
- `frontend/vite.config.js`, `frontend/package.json`, any build config.

## 6. Compatibility strategy

`/` route and `FileResponse` mechanism untouched (CHANGE_SPEC.md section 8); no compatibility
risk beyond correct HTML.

## 12. Error and recovery behavior

Not applicable — no runtime error paths are introduced by a static-copy edit.

## 14. Rollback plan

`git checkout -- frontend/public/home.html AGENTIC_WORKFLOW_STRATEGY.md` restores prior content;
no other state to roll back (no schema, no build artifacts committed).

## 16. Automated-test strategy

No test suite exists (BASELINE_REPORT.md section 7). Verification is grep/parse-based per
CHANGE_SPEC.md's Verification column. No new automated tests are added — a copy/link correction
has no testable logic to regress-guard beyond content assertions already specified.

## 17. Regression-test strategy

Diff-scoped check: confirm no hunches outside `frontend/public/home.html:490-500` (AC-8) via
`git diff --stat` and `git diff -- frontend/public/home.html` line-range inspection.

## 18. Manual-verification strategy

- Read `AC-2`'s six required points against the drafted `<p>` copy by eye.
- Confirm `AGENTIC_WORKFLOW_STRATEGY.md` no longer proposes a Claude/Codex-specific rename or
  "Claude builds, Codex audits" framing (AC-6), by eye.
- These are content-accuracy judgments that automated grep alone cannot fully confirm (wording
  quality); grep confirms the banned/required phrases (AC-1, AC-3, AC-4, AC-5), a human or the
  implementing agent's own re-read confirms the prose reads coherently. No separate human
  sign-off gate is required beyond the workflow's existing plan-approval and final-approval gates
  — CHANGE_REQUEST.md names no additional reviewer.

## 20. Implementation sequence

1. Read `https://github.com/unclehq/uncle` README and top-level source to ground the rewrite (CHANGE_SPEC.md AC-7). No repo files written. Owns: none — Depends on: none
2. Rewrite `frontend/public/home.html:490-500`: update `href` on the heading `<a>` and the `Code` `<a>` to `https://github.com/unclehq/uncle`, update `<span class="url">` text to `github.com/unclehq/uncle`, rewrite the `<p>` body per AC-2, rewrite `<span class="tag">` per AC-5. Keep `rel="noopener noreferrer"` on both links and the existing `article.card` structure (IX-1). Owns: `frontend/public/home.html` — Depends on: 1
3. Rewrite `AGENTIC_WORKFLOW_STRATEGY.md` sections that assert "Claude builds, Codex audits" or a fixed pairing (lines 14, 25 and any other occurrence found by grep) to agent-agnostic framing consistent with the new card copy; leave unrelated backlog items (contributor/advertising plans) intact per CHANGE_SPEC.md section 15 non-goals. Owns: `AGENTIC_WORKFLOW_STRATEGY.md` — Depends on: 1
4. Run verification commands (section below) and confirm AC-1 through AC-9; fix any grep mismatch in the owning file from step 2 or 3. Owns: none — Depends on: 2, 3

## Change-impact table

| Component | Planned change | Reason | Regression risk | Test coverage |
|---|---|---|---|---|
| `frontend/public/home.html` | Rewrite lines 490-500 (Agentic Workflow card: links, body, tag) | CHANGE_SPEC.md BX-1..BX-3 | Low — scoped to one card; AC-8 checks no bleed into siblings | AC-1, AC-2, AC-5, AC-8, AC-9 (grep + html.parser, no automated test suite exists) |
| `AGENTIC_WORKFLOW_STRATEGY.md` | Reframe Claude/Codex-pairing language to agent-agnostic | CHANGE_SPEC.md BX-4 | Low — standalone doc, not rendered by app | AC-3, AC-6 (grep + manual read) |

## Traceability

| Requirement | Behavior | Invariant | Component | Automated test | Manual check |
|---|---|---|---|---|---|
| AC-1 | BX-1 | IX-1 | frontend/public/home.html | grep for `unclehq/uncle` / absence of old links | — |
| AC-2 | BX-2 | — | frontend/public/home.html | — | Read `<p>` against 6 required points |
| AC-3 | BX-4 | IX-3 | Both files | grep `-i "claude builds\|codex audits"` | — |
| AC-4 | BX-1 | — | frontend/public/home.html, repo-wide | grep `-r stagegate` | — |
| AC-5 | BX-3 | — | frontend/public/home.html | grep old tag text absent | — |
| AC-6 | BX-4 | IX-3 | AGENTIC_WORKFLOW_STRATEGY.md | AC-3 grep | Read framing |
| AC-7 | BX-2 | — | Implementation notes | — | Confirm README was read (step 1) |
| AC-8 | BX-5 | — | frontend/public/home.html | `git diff` line-range check | — |
| AC-9 | IX-1, IX-2 | frontend/public/home.html | `html.parser` parse (BASELINE_REPORT.md section 8 command) | — |

## Verification commands

```
grep -c "unclehq/uncle" frontend/public/home.html
grep -c "brianosaurus/agentic-workflow\|unclehq/stagegate" frontend/public/home.html
grep -ri "claude builds\|codex audits\|claude/codex" frontend/public/home.html AGENTIC_WORKFLOW_STRATEGY.md
grep -r "stagegate" --include=* . --exclude-dir=.git
python3 -c "import html.parser, pathlib; p = html.parser.HTMLParser(); p.feed(pathlib.Path('frontend/public/home.html').read_text()); print('parsed ok')"
git diff --stat -- frontend/public/home.html
```

## 21. Scope cuts under time pressure

None required — change is already minimal (two files, no tooling).

## 22. Risks and unresolved questions

- Risk: copy quality (AC-2 wording) is a judgment call, not fully grep-verifiable — mitigated by
  manual-verification step in section 18.
- No blocking planning decisions remain; D-1 and D-2 above are resolved, in-scope design choices
  covered by plan approval.
