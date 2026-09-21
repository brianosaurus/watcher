# Verification report

## MC-1 Card link targets
- Action: `grep -o "unclehq/uncle" frontend/public/home.html | wc -l`; `grep -c "brianosaurus/agentic-workflow\|unclehq/stagegate" frontend/public/home.html`
- Actual: 3; 0
- Status: PASS
- Evidence: command output above; matches expected (3, 0)
- Defect: none

## MC-2 Body copy content
- Action: read `<p>` at frontend/public/home.html:492-497
- Actual: "A terminal-native software engineer: give it an issue or requirements and it plans the change, coordinates the coding agents you already use (Claude, Codex, and others — not a fixed pairing), and hands back a verified pull request. Specs and plans are cryptographically pinned so approved intent cannot silently change, an independent reviewer checks the implementing agent's own work, and a human holds the approval gate at every stage." — all six AC-2 elements present
- Status: PASS
- Evidence: quoted paragraph above; resolves the CHANGE_TEST_REPORT.md vs delivery-summary.tsv conflict flagged by MC-12 via independent direct read
- Defect: none

## MC-3 No fixed Claude/Codex pairing language
- Action: `grep -in "claude builds\|codex audits\|claude/codex" frontend/public/home.html AGENTIC_WORKFLOW_STRATEGY.md`
- Actual: exit 1, no matches
- Status: PASS
- Evidence: command exit code 1 (no matches)
- Defect: none

## MC-4 stagegate absent
- Action: `grep -rli "stagegate" --exclude-dir=.git --exclude-dir=.uncle -- app frontend AGENTIC_WORKFLOW_STRATEGY.md`
- Actual: exit 1, no matches in source paths
- Status: PASS
- Evidence: command exit code 1; repo-wide `.uncle/` hits are pre-existing generated logs, excluded per check scope
- Defect: none

## MC-5 Tag line updated
- Action: `grep -n "LLM agents · pipeline tooling · open source" frontend/public/home.html`; read home.html:500
- Actual: no match; current tag is `agentic coding · independent review · human approval gates`
- Status: PASS
- Evidence: grep exit 1; home.html:500 quoted above; resolves MC-12/delivery-summary.tsv conflict via independent read
- Defect: none

## MC-6 Strategy doc positioning
- Action: read AGENTIC_WORKFLOW_STRATEGY.md in full
- Actual: line 14 reads "Adversarial review by an independent reviewer, decoupled from whichever coding agent (Claude, Codex, or others) implemented the change." Names Claude/Codex only as illustrative, swappable examples in a review-decoupling sentence, not a fixed pairing. No "Claude builds, Codex audits" framing present (MC-3 confirms).
- Status: PASS
- Evidence: AGENTIC_WORKFLOW_STRATEGY.md:14 quoted above; resolves MC-12/delivery-summary.tsv conflict
- Defect: none

## MC-7 Copy derived from uncle source
- Action: `gh api repos/unclehq/uncle` and `gh api repos/unclehq/uncle/readme -H "Accept: application/vnd.github.raw"`, compared against home.html:492-497 and IMPLEMENTATION_NOTES.md:7 citation (worker evidence, group 2)
- Actual: fetch succeeded; repo description "Uncle — Build apps and ship changes with AI agents you choose"; README states "terminal-native agentic software engineer", "Uncle works with Cline, Claude, Codex, Kimi, OpenCode, and other coding agents" (not fixed pairing), "Pinned intent", independent review, human authority. home.html body copy matches these points; not derived from old card's Claude/Codex/SHA-256-only framing.
- Status: PASS
- Evidence: worker MC-7.md fetched README/description excerpts quoted above
- Defect: none (see D-1 re: citation completeness in IMPLEMENTATION_NOTES.md, MC-13)

## MC-8 Adjacent cards untouched
- Action: `git diff -- frontend/public/home.html | grep -E "^@@"`
- Actual: single hunk `@@ -488,14 +488,16 @@`, no hunks outside the card block
- Status: PASS
- Evidence: worker MC-8.md command output
- Defect: none

## MC-9 HTML well-formed
- Action: `python3 -c "import html.parser, pathlib; ...feed(...)"`
- Actual: `parsed ok`, exit 0
- Status: PASS
- Evidence: worker MC-9.md command output/exit code
- Defect: none

## MC-10 Backend route unaffected
- Action: `python3 -m py_compile app/main.py`
- Actual: no output, exit 0
- Status: PASS
- Evidence: worker MC-10.md command output/exit code
- Defect: none

## MC-11 Rendered card in browser
- Action: checked preconditions (`frontend/node_modules`, `static/home.html`)
- Actual: `frontend/node_modules` absent, `static/` does not exist; `npm run build` was never run
- Status: BLOCKED-SETUP — action: run `npm install && npm run build` in `frontend/`, then serve `static/` and view in a browser
- Evidence: worker MC-11.md; matches BASELINE_REPORT.md:94 (pre-existing gap)
- Defect: none (environment gap, not introduced by this change)

## MC-12 Reconcile INCOMPLETE vs PASS conflict
- Action: read IMPLEMENTATION_NOTES.md in full; compared against delivery-summary.tsv (AC-2/5/6/7/9 INCOMPLETE) and CHANGE_TEST_REPORT.md (same ACs PASS)
- Actual: IMPLEMENTATION_NOTES.md gives no explanation for the discrepancy; per its own fallback rule, AC-2/5/6/7/9 were re-verified independently rather than accepted from either source
- Status: PASS (check executed; produced a determinate outcome)
- Evidence: worker MC-12.md; independent re-verification of AC-2 (MC-2 PASS), AC-5 (MC-5 PASS), AC-6 (MC-6 PASS), AC-9 (MC-9 PASS) all confirm PASS on direct evidence; AC-7 (MC-13) confirms FAIL — the underlying documentation gap (D-1) is real but did not change the four ACs' outcomes
- Defect: D-1

## MC-13 IMPLEMENTATION_NOTES.md AC-7 citation
- Action: read IMPLEMENTATION_NOTES.md for its AC-7 citation of the `gh api` fetch
- Actual: IMPLEMENTATION_NOTES.md:7,37 name only README section headings ("intro tagline", "Why Uncle?", "The change is the unit of trust"), quoting no fetched text; insufficient to verify the claimed fetch occurred before copy was written, independent of MC-7's own fresh fetch
- Status: FAIL
- Evidence: worker MC-13.md; IMPLEMENTATION_NOTES.md:7,37 quoted therein
- Defect: D-1

## MC-14 Untested report sections
- Action: inspected CHANGE_TEST_REPORT.md §Regression tests/Full test suite/Formatting/Compiler-type-checker; verified against repo file listing and `frontend/package.json`
- Actual: Regression tests, Formatting, Compiler/type-checker sections' emptiness confirmed expected (no tooling configured). §Full test suite reads "DRIVER PENDING" — an unresolved placeholder, not confirmed absence
- Status: PASS (check scope satisfied); placeholder text is a separate documentation gap
- Evidence: worker MC-14.md; `frontend/package.json` scripts = {dev, build, preview} only
- Defect: D-2

## Acceptance criteria summary
AC-1 PASS (MC-1). AC-2 PASS (MC-2, independently resolves MC-12). AC-3 PASS (MC-3). AC-4 PASS (MC-4). AC-5 PASS (MC-5). AC-6 PASS (MC-6). AC-7 FAIL (MC-7 fetch itself passes, but MC-13 finds the implementer's cited proof-of-fetch in IMPLEMENTATION_NOTES.md insufficient — D-1). AC-8 PASS (MC-8). AC-9 PASS (MC-9).

## Preserved behavior summary
B-1/I-1 PASS (MC-10, backend route untouched). I-2 PASS (MC-8; MC-11 BLOCKED-SETUP for browser confirmation). I-3 PASS (MC-9, HTML well-formed).

## Changed behavior summary
B-2 (card link) PASS. B-3 (body copy, no fixed pairing) PASS. B-4 (tag line) PASS. B-5 (strategy doc positioning) PASS.

## Invariant summary
I-1 PASS, I-2 PASS (browser render not directly observed — MC-11 BLOCKED-SETUP), I-3 PASS.

## Regression summary
No regressions found (MC-8, MC-10, MC-9, MC-14 all PASS or scope-satisfied); no test suite exists to run beyond targeted checks.

## Unresolved defects
D-1 (IMPLEMENTATION_NOTES.md AC-7 citation lacks fetched content — MC-13 FAIL), D-2 (CHANGE_TEST_REPORT.md §Full test suite left as "DRIVER PENDING" placeholder — documentation gap, not a code defect).

## Recommendation
Do not accept as-is on AC-7 documentation grounds: MC-7's own fresh fetch independently confirms the card copy matches uncle's real README, but IMPLEMENTATION_NOTES.md's citation for that same claim is not self-verifying (D-1). Require the implementer to quote actual fetched README/description text in IMPLEMENTATION_NOTES.md, or accept AC-7 solely on this stage's independent MC-7 fetch evidence with the record corrected. MC-11 (browser render) remains BLOCKED-SETUP pending `npm install && npm run build`. All other acceptance criteria and invariants pass on direct evidence.

## Acceptance gate

| ID | Required | Status | Evidence |
|---|---|---|---|
| MC-1 | YES | PASS | grep counts 3 and 0 |
| MC-2 | YES | PASS | home.html:492-497 body text |
| MC-3 | YES | PASS | grep exit 1, no matches |
| MC-4 | YES | PASS | grep exit 1, no matches |
| MC-5 | YES | PASS | grep exit 1; tag text confirmed |
| MC-6 | YES | PASS | AGENTIC_WORKFLOW_STRATEGY.md:14 |
| MC-7 | YES | PASS | gh api fetch matches home.html copy |
| MC-8 | YES | PASS | single diff hunk |
| MC-9 | YES | PASS | parsed ok, exit 0 |
| MC-10 | NO | PASS | py_compile exit 0 |
| MC-11 | NO | BLOCKED-SETUP | Action: `npm install && npm run build` in frontend/ |
| MC-12 | YES | PASS | discrepancy identified; five ACs re-verified independently |
| MC-13 | YES | FAIL | IMPLEMENTATION_NOTES.md cites section names only, no fetched text |
| MC-14 | NO | PASS | no test/lint/format tooling configured; DRIVER PENDING noted (D-2) |
