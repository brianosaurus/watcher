# Change plan

Issue 1

| Finding | Disposition | Reason | Exact plan change |
|---|---|---|---|
| AR-001 | Accepted | `grep -c` counts matching lines, not occurrences; line 491 holds `unclehq/uncle` twice, so a compliant file returns 2, not 3 | Section 10, AC-1 check |
| AR-002 | Accepted | Rollback restoring `HEAD` would discard the pre-existing D-1 draft even when this plan made no edits | Section 9, new step 0 |
| AR-003 | Accepted | Fetch-failure outcome for AC-7 was stated as "reported" without saying whether merge is blocked | Section 13, step 1 |

Omitted sections: Data-flow changes (static markup, no data flow); State-transition changes (none); Schema or persistence changes (none); Concurrency implications (none); Migration plan (none); Feature-flag or containment strategy (single static file, no flag needed); Automated-test strategy (no test framework exists per BASELINE_REPORT.md section 7; not introduced — non-goal in CHANGE_SPEC.md section 15); Observability changes (none)

## 1. Selected technical approach

Working-tree state already contains most of the required edit (see D-1 below, discovered
during planning, not applied by this plan). Plan verifies that draft against CHANGE_SPEC.md
acceptance criteria, fetches uncle's actual README/source to confirm accuracy (CR checklist
item 1, AC-7), corrects any divergence in `frontend/public/home.html:490-500` and
`AGENTIC_WORKFLOW_STRATEGY.md:14`, then reconciles.

## 2. Alternative approaches considered

- Rewrite the card from scratch, discarding the current working-tree draft. Rejected: the
  draft already satisfies AC-1, AC-3, AC-4, AC-5, AC-8 (git diff below); discarding it is pure
  rework with no requirement gain.
- Skip the README fetch and accept the draft as-is. Rejected: AC-7 requires copy derived from
  the actual repo, and the draft's accuracy against uncle's real feature set has not been
  checked against source; this step is a verification/fetch, not a scope expansion.

## 3. Why the selected approach is preferred

Confirms AC-7 without discarding already-correct work; the working-tree content becomes an
input to check, not a foregone conclusion, so revision is targeted and small.

## D-1: Working-tree state (discovered, not this plan's edit)

`git diff frontend/public/home.html` and `git diff AGENTIC_WORKFLOW_STRATEGY.md` (both
checked at planning time) show the working tree already differs from `HEAD` in exactly the
card region (`frontend/public/home.html:490-500`) and one bullet
(`AGENTIC_WORKFLOW_STRATEGY.md:14`), matching BX-1..BX-4 target state: links point to
`https://github.com/unclehq/uncle`, body/tag copy drop the Claude/Codex-pairing framing, no
`stagegate` string exists anywhere in the tree (`grep -rn stagegate .` outside `.git`: no
matches). This contradicts BASELINE_REPORT.md section 4's "current behavior" snapshot, which
was taken against `HEAD`/committed content, not the live working tree. Treated as current
ground truth for this plan; BASELINE_REPORT.md is not re-run.

## 4. Exact components to modify

- `frontend/public/home.html:490-500` — only if step 2's README check finds the existing draft
  body/tag copy (BX-2, BX-3) inaccurate against uncle's real feature set.
- `AGENTIC_WORKFLOW_STRATEGY.md:11-19` (Positioning pivot section) — only if step 3 finds
  remaining stale framing inconsistent with agent-agnostic positioning (BX-4).

## 5. Components explicitly not to modify

- `frontend/public/home.html:463-489,507+` (sibling cards, IX-1, AC-8).
- `AGENTIC_WORKFLOW_STRATEGY.md` "Name alternatives", "How to get contributors", "Advertising",
  "Immediate next steps", "Related project recommendations" sections — unrelated backlog, CR
  out-of-scope, CHANGE_SPEC.md section 15.
- `app/main.py`, `frontend/vite.config.js` — CHANGE_SPEC.md section 8, IX-2.

## 6. Interface and API changes

None. `/` route and `FileResponse` mechanism (I-1) untouched.

## 7. Compatibility strategy

No compatibility surface exists for static card copy; `rel="noopener noreferrer"` already
present on both rewritten links (frontend/public/home.html:491,499) and must be kept if the
lines are re-edited in step 2/3.

## 8. Error and recovery behavior

Not applicable — static text, no runtime error path (CHANGE_SPEC.md section 9).

## 9. Rollback plan

Step 0 (below) snapshots the D-1 draft (`git diff HEAD > /tmp/d1-draft.patch`) before any
plan edit runs. Rollback:
- If steps 2/3 made no edit (draft confirmed accurate): no rollback action needed — tree is
  already at the snapshotted state.
- If steps 2/3 edited either file: `git checkout -- frontend/public/home.html
  AGENTIC_WORKFLOW_STRATEGY.md` (restores `HEAD`), then `git apply /tmp/d1-draft.patch`
  (restores the pre-existing D-1 draft). This undoes only this plan's edits, not D-1.
No other rollback surface: no schema, migration, or build artifact holds state from this
change.

## 10. Manual-verification strategy

- `grep -o "unclehq/uncle" frontend/public/home.html | wc -l` → expect 3 (heading href, url
  span, Code href) — AC-1. (`grep -c` undercounts when a match appears twice on one line, per
  AR-001; do not use `-c` for this check.)
- `grep -c "brianosaurus/agentic-workflow\|unclehq/stagegate" frontend/public/home.html` →
  expect 0 — AC-1, AC-4.
- `grep -rn "stagegate" . --exclude-dir=.git` → expect 0 matches repo-wide — AC-4.
- `grep -in "claude builds\|codex audits\|claude/codex" frontend/public/home.html
  AGENTIC_WORKFLOW_STRATEGY.md` → expect 0 — AC-3.
- `python3 -c "import html.parser, pathlib; p=html.parser.HTMLParser();
  p.feed(pathlib.Path('frontend/public/home.html').read_text())"` → exit 0 — AC-9.
- `git diff HEAD -- frontend/public/home.html` → hunks confined to lines 490-500 — AC-8.
- Manual read of `frontend/public/home.html:492-497` against AC-2's six required points, and
  of `AGENTIC_WORKFLOW_STRATEGY.md:11-19` against AC-6, after step 1's README fetch — AC-2,
  AC-6, AC-7.

## 11. Regression-test strategy

No automated suite exists (BASELINE_REPORT.md section 7); manual checks above are the full
regression net for this change. `python3 -m py_compile app/main.py` re-run only if step 2/3
edits are made near unrelated code, which they are not — skipped.

## 12. Scope cuts under time pressure

None available: all nine acceptance criteria are required by CHANGE_REQUEST.md's checklist
and are individually cheap (grep/manual read). No criterion is a candidate for deferral.

## 13. Risks and unresolved questions

- Risk: `https://github.com/unclehq/uncle` fetch (step 1) fails or is unreachable. Resolution:
  if the fetch cannot complete, steps 2/3 make no edit, step 4 reports AC-7 as unmet, and this
  change does not merge until step 1 is re-run successfully — AC-7 failure is a merge blocker,
  not a silently passed check or a no-op treated as success (AR-003).
- Risk: re-editing `frontend/public/home.html:490-500` after step 1 could reintroduce an HTML
  well-formedness break. Mitigated by the AC-9 `html.parser` check in step 4.

## R-1: Restriction — no automated test framework introduced

- source_kind: REPOSITORY (BASELINE_REPORT.md section 7: no test config found).
- Requirement: CHANGE_SPEC.md section 15 non-goal ("do not add test infrastructure").
- Required property: verification must use only tools already present (`python3`, `grep`,
  `git`) — CAP-1 (ambient `python3` interpreter with stdlib `html.parser`, confirmed present
  at BASELINE_REPORT.md section 8's executed commands).
- Selected mechanism: shell `grep`/`git diff`/`python3 -c` one-liners (section 10).
- Rationale: matches repo convention (static site, no CI) and CR scope.
- Phase: CODING and LIVE_VERIFICATION both use the same commands; no separate live-only step.

## R-2: Restriction — copy must originate from uncle's real repository

- source_kind: USER (CHANGE_REQUEST.md acceptance criterion 1: "Read the uncle README and
  source before writing copy").
- Requirement: AC-7.
- Required property: implementer states, with citation, what was read from
  `github.com/unclehq/uncle` before finalizing or confirming copy.
- Selected mechanism: step 1 fetch (LIVE_VERIFICATION phase — needs network; CAP-2, network
  fetch capability, not probed in this planning session, no sandboxed network access
  confirmed available here). If unavailable, AC-7 blocks merge per section 13.
- Rationale: CR explicitly bans deriving copy from the old card's assumptions.
- Non-secret prerequisite evidence: none required beyond public GitHub URL; no auth needed.

## R-3: Restriction — rollback must not discard the pre-existing D-1 draft

- source_kind: DESIGN (AR-002).
- Requirement: rollback undoes only this plan's own edits.
- Required property: a snapshot of D-1 exists before any plan edit, and rollback restores that
  snapshot rather than `HEAD`, when no plan edit was made.
- Selected mechanism: `git diff HEAD > /tmp/d1-draft.patch` in step 0, applied on rollback
  (section 9).
- Rationale: `HEAD` predates D-1; restoring it silently loses uncommitted work not authored by
  this plan.
- Phase: CODING (step 0 runs before step 1).

## Change-impact table

| ID | Component | Planned change | Reason | Regression risk | Test coverage |
|---|---|---|---|---|---|
| CI-1 | `frontend/public/home.html` | Verify existing uncommitted draft (lines 490-500) against AC-1,3,4,5,8,9; revise body/tag only if step 1 finds inaccuracy | AC-2, AC-7, R-2 | Low — confined region, checked by AC-8/AC-9 | Manual grep + html.parser (section 10) |
| CI-2 | `AGENTIC_WORKFLOW_STRATEGY.md` | Verify line 14 draft against AC-3, AC-6; revise Positioning pivot section only if step 1 finds inaccuracy | AC-6, R-2 | Low — single-file prose, no code path | Manual grep + read (section 10) |

## Implementation sequence

0. Snapshot current working tree: `git diff HEAD > /tmp/d1-draft.patch` (R-3). Owns: none.
   Depends on: none.
1. Fetch and read `https://github.com/unclehq/uncle` README and top-level source structure;
   record findings against AC-2, AC-6, AC-7 and R-2. Compare to current draft text at
   `frontend/public/home.html:492-497,500` and `AGENTIC_WORKFLOW_STRATEGY.md:14`. If the fetch
   fails, stop and report per section 13 — do not proceed to steps 2-4 as if AC-7 were met.
   Phase: LIVE_VERIFICATION. Owns: none. Depends on: 0.
2. If step 1 finds the draft body copy or tag inaccurate against uncle's real scope, edit
   `frontend/public/home.html:492-497,500` to correct it; keep `rel="noopener noreferrer"` on
   both links (section 7); otherwise make no edit and record "draft confirmed accurate."
   Owns: `frontend/public/home.html`. Depends on: 1.
3. If step 1 finds `AGENTIC_WORKFLOW_STRATEGY.md`'s Positioning pivot section (lines 11-19)
   still inconsistent with uncle's agent-agnostic framing beyond line 14, revise only that
   section; leave Name alternatives / Immediate next steps / Advertising sections untouched
   (section 5). Owns: `AGENTIC_WORKFLOW_STRATEGY.md`. Depends on: 1.
4. Run every command in section 10 against the post-step-2/3 tree; confirm AC-1 through AC-9
   all pass; confirm `git diff HEAD` touches only `frontend/public/home.html:490-500` and
   `AGENTIC_WORKFLOW_STRATEGY.md:11-19`; write the PR description citing what was read from
   `github.com/unclehq/uncle` in step 1 (AC-7 evidence). Owns: `*`. Depends on: 2, 3.

## Traceability

| Requirement | Behavior | Invariant | Component | Automated test | Manual check |
|---|---|---|---|---|---|
| AC-1 | BX-1 | — | CI-1 | none | section 10 grep #1 (`-o \| wc -l`, AR-001),#2 |
| AC-2 | BX-2 | — | CI-1 | none | section 10 manual read |
| AC-3 | BX-4 | IX-3 | CI-1, CI-2 | none | section 10 grep #4 |
| AC-4 | — | — | CI-1 | none | section 10 grep #3 |
| AC-5 | BX-3 | — | CI-1 | none | section 10 grep #1 (tag text) |
| AC-6 | BX-4 | IX-3 | CI-2 | none | section 10 manual read |
| AC-7 | — | R-2 | CI-1, CI-2 | none | step 1 fetch + PR citation; merge-blocking per section 13 |
| AC-8 | BX-5 | IX-1 | CI-1 | none | section 10 git diff scope check |
| AC-9 | — | IX-1, IX-2 | CI-1 | none | section 10 html.parser check |

## Frozen change scope

Rewrite the Agentic Workflow card (`frontend/public/home.html:490-500`) and
`AGENTIC_WORKFLOW_STRATEGY.md`'s Positioning pivot section to describe `unclehq/uncle`
accurately, per CHANGE_REQUEST.md and CHANGE_SPEC.md AC-1..AC-9. No other file, route, or
sibling card changes.

## Files expected to change

- `frontend/public/home.html` (lines 490-500 only) — conditional on step 1 findings (CI-1).
- `AGENTIC_WORKFLOW_STRATEGY.md` (lines 11-19 only) — conditional on step 1 findings (CI-2).

## Files that must not change

- `frontend/public/home.html:463-489,507+` (sibling cards).
- `AGENTIC_WORKFLOW_STRATEGY.md` sections other than "Positioning pivot".
- `app/main.py`, `frontend/vite.config.js`.

## Expected behavioral differences

- Card heading link, URL label, and Code link resolve to `https://github.com/unclehq/uncle`
  instead of `unclehq/stagegate` (AC-1).
- Card body and tag describe uncle's actual scope instead of the old Claude/Codex framing
  (AC-2, AC-3, AC-5).
- `AGENTIC_WORKFLOW_STRATEGY.md` Positioning pivot section no longer implies a fixed
  Claude/Codex pairing (AC-6).

## Expected unchanged behavior

- `/` route and `FileResponse` serving mechanism (section 6).
- All sibling cards on the portfolio home page, byte-identical (AC-8).
- HTML document structure and parseability (AC-9).

## Exact acceptance criteria

AC-1 through AC-9 as defined in CHANGE_SPEC.md section 5, verified by the commands in
section 10 of this plan (AC-1 count check corrected per AR-001).

## Pre-implementation checks

- Step 0 snapshot taken (`/tmp/d1-draft.patch` exists) before any edit — R-3.
- D-1 state confirmed current: re-run `git diff frontend/public/home.html
  AGENTIC_WORKFLOW_STRATEGY.md` and compare against the D-1 description; report divergence if
  found.

## Post-implementation checks

All checks in section 10, run against the final tree, plus the `git diff HEAD` scope check in
step 4. All nine must pass before the PR is written.

## First features to cut if time expires

None (section 12): every acceptance criterion is required and individually cheap to verify.

## Conditions that require stopping implementation

- Step 1's fetch of `https://github.com/unclehq/uncle` fails or is unreachable — stop, report
  AC-7 as unmet and merge-blocked (section 13), do not proceed to steps 2-4.
- `git diff HEAD` at step 4 touches any file or line range outside section 4's exact
  components — stop, do not write the PR description, investigate the extra diff.
- Step 0's snapshot is missing or unreadable when rollback is needed — stop and report before
  running `git checkout --`, to avoid discarding D-1 without a way back (R-3).
