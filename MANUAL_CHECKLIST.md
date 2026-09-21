# Manual checklist

Base checks: 11; resolved: 1; added: 3; removed: 0

### MC-1 Card link targets
- Priority: P0
- Behavior classification: MODIFY
- Related behavior: B-2
- Related invariant: none
- Preconditions: none
- Exclusive resources: none
- Depends on: none
- Exact action: `grep -o "unclehq/uncle" frontend/public/home.html | wc -l`; then `grep -c "brianosaurus/agentic-workflow\|unclehq/stagegate" frontend/public/home.html`
- Expected result: first command outputs 3; second outputs 0
- Evidence to capture: both command outputs
- Actual result:
- Status: NOT RUN

### MC-2 Body copy content
- Priority: P0
- Behavior classification: MODIFY
- Related behavior: B-3
- Related invariant: none
- Preconditions: none
- Exclusive resources: none
- Depends on: none
- Exact action: read `<p>` at frontend/public/home.html:492-497
- Expected result: states terminal-native; issue/requirements in, verified PR out; existing coding agents not a fixed pairing; independent review; human approval gates; cryptographically pinned plans/artifacts — all six present
- Evidence to capture: quoted paragraph text
- Actual result:
- Status: NOT RUN — CHANGE_TEST_REPORT.md:15 claims PASS but delivery-summary.tsv:2 marks AC-2 INCOMPLETE against IMPLEMENTATION_NOTES.md; conflict unresolved, run independently

### MC-3 No fixed Claude/Codex pairing language
- Priority: P0
- Behavior classification: REMOVE
- Related behavior: B-3, B-5
- Related invariant: none
- Preconditions: none
- Exclusive resources: none
- Depends on: none
- Exact action: `grep -in "claude builds\|codex audits\|claude/codex" frontend/public/home.html AGENTIC_WORKFLOW_STRATEGY.md`
- Expected result: no matches in either file
- Evidence to capture: command output
- Actual result:
- Status: NOT RUN

### MC-4 stagegate absent
- Priority: P1
- Behavior classification: PRESERVE
- Related behavior: AC-4
- Related invariant: none
- Preconditions: none
- Exclusive resources: none
- Depends on: none
- Exact action: `grep -rli "stagegate" --exclude-dir=.git --exclude-dir=.uncle -- app frontend AGENTIC_WORKFLOW_STRATEGY.md`
- Expected result: no matches, or a match accompanied by a documented justification in the PR description
- Evidence to capture: grep output; PR description text if matches found
- Actual result:
- Status: NOT RUN — CHANGE_TEST_REPORT.md:17 reports 0 in source paths but 99 repo-wide (all in `.uncle/` generated logs, pre-existing); run against source paths only

### MC-5 Tag line updated
- Priority: P1
- Behavior classification: MODIFY
- Related behavior: B-4
- Related invariant: none
- Preconditions: none
- Exclusive resources: none
- Depends on: none
- Exact action: `grep -n "LLM agents · pipeline tooling · open source" frontend/public/home.html`
- Expected result: no match; current tag reads "agentic coding · independent review · human approval gates" per cached read of home.html:500
- Evidence to capture: grep output and current tag text
- Actual result:
- Status: NOT RUN — delivery-summary.tsv:3 marks AC-5 INCOMPLETE against CHANGE_TEST_REPORT.md:18 PASS claim; reconcile via MC-12 before accepting

### MC-6 Strategy doc positioning
- Priority: P1
- Behavior classification: MODIFY
- Related behavior: B-5
- Related invariant: none
- Preconditions: none
- Exclusive resources: none
- Depends on: none
- Exact action: read AGENTIC_WORKFLOW_STRATEGY.md in full
- Expected result: no agent-agnostic violation; no "Claude builds, Codex audits" framing (MC-3 covers phrase). Current cached copy (AGENTIC_WORKFLOW_STRATEGY.md:14) still names "Claude, Codex, or others" as example agents in a review-decoupling sentence — verify this reads as illustrative, not a fixed pairing, per AC-6
- Evidence to capture: quoted lines
- Actual result:
- Status: NOT RUN — delivery-summary.tsv:4 marks AC-6 INCOMPLETE; reconcile via MC-12

### MC-7 Copy derived from uncle source
- Priority: P0
- Behavior classification: ADD
- Related behavior: AC-7
- Related invariant: none
- Preconditions: network access to github.com
- Exclusive resources: none
- Depends on: MC-13
- Exact action: fetch `https://github.com/unclehq/uncle` README (`gh api repos/unclehq/uncle/readme` or web fetch); compare against home.html:492-497 body copy and against IMPLEMENTATION_NOTES.md's cited fetch output (CHANGE_TEST_REPORT.md:19)
- Expected result: card copy traces to README content, not to the old card's Claude/Codex/SHA-256-only framing; IMPLEMENTATION_NOTES.md's citation matches an actual successful fetch, not an assumed one
- Evidence to capture: fetched README excerpt; IMPLEMENTATION_NOTES.md citation text
- Actual result:
- Status: NOT RUN — resolved from NEEDS-DETAIL; delivery-summary.tsv:5 marks AC-7 INCOMPLETE despite CHANGE_TEST_REPORT.md:19 PASS claim, run MC-13 first

### MC-8 Adjacent cards untouched
- Priority: P0
- Behavior classification: PRESERVE
- Related behavior: AC-8
- Related invariant: I-2
- Preconditions: none
- Exclusive resources: none
- Depends on: none
- Exact action: `git diff -- frontend/public/home.html | grep -E "^@@"`
- Expected result: only the hunk at the Agentic Workflow card block (CHANGE_TEST_REPORT.md:20 records `@@ -488,14 +488,16 @@`); no hunks in lines 463-489 or 507+
- Evidence to capture: diff hunk headers
- Actual result:
- Status: NOT RUN

### MC-9 HTML well-formed
- Priority: P1
- Behavior classification: PRESERVE
- Related behavior: AC-9
- Related invariant: I-3
- Preconditions: none
- Exclusive resources: none
- Depends on: none
- Exact action: `python3 -c "import html.parser, pathlib; p = html.parser.HTMLParser(); p.feed(pathlib.Path('frontend/public/home.html').read_text()); print('parsed ok')"`
- Expected result: exit 0, prints `parsed ok`
- Evidence to capture: command output and exit code
- Actual result:
- Status: NOT RUN — green-check.tsv:2 and CHANGE_TEST_REPORT.md:21 both record PASS but delivery-summary.tsv:6 marks AC-9 INCOMPLETE; rerun to settle

### MC-10 Backend route unaffected
- Priority: P2
- Behavior classification: PRESERVE
- Related behavior: B-1
- Related invariant: I-1
- Preconditions: none
- Exclusive resources: none
- Depends on: none
- Exact action: `python3 -m py_compile app/main.py`
- Expected result: exit 0, no output
- Evidence to capture: command output
- Actual result:
- Status: NOT RUN

### MC-11 Rendered card in browser
- Priority: P2
- Behavior classification: MODIFY
- Related behavior: B-2, B-3, B-4
- Related invariant: I-2
- Preconditions: `npm run build` completed in `frontend/`, producing `static/home.html`
- Exclusive resources: port:8000
- Depends on: MC-1, MC-2, MC-5
- Exact action: serve `static/` (`python3 -m http.server 8000 --directory static`), open `http://127.0.0.1:8000/home.html` via the system default browser (`open` on macOS)
- Expected result: card renders "Uncle" heading, unclehq/uncle link, updated body/tag, layout matches sibling cards
- Evidence to capture: screenshot; browser used
- Actual result:
- Status: BLOCKED-SETUP — `frontend/node_modules` absent (BASELINE_REPORT.md:94); `npm install && npm run build` would make this runnable

### MC-12 Reconcile INCOMPLETE vs PASS conflict
- Priority: P0
- Behavior classification: ADD
- Related behavior: AC-2, AC-5, AC-6, AC-7, AC-9
- Related invariant: none
- Preconditions: IMPLEMENTATION_NOTES.md exists
- Exclusive resources: none
- Depends on: none
- Exact action: read IMPLEMENTATION_NOTES.md in full; compare its stated status for AC-2/5/6/7/9 against delivery-summary.tsv (all five rows INCOMPLETE) and CHANGE_TEST_REPORT.md §Targeted tests (all five claim PASS, lines 15-19,21)
- Expected result: IMPLEMENTATION_NOTES.md explains the discrepancy (e.g. a later revision not reflected in CHANGE_TEST_REPORT.md); if it does not, treat all five ACs as unresolved regardless of CHANGE_TEST_REPORT.md's claims
- Evidence to capture: quoted IMPLEMENTATION_NOTES.md status lines for each AC
- Actual result:
- Status: NOT RUN — this check gates MC-2, MC-5, MC-6, MC-7, MC-9 acceptance

### MC-13 IMPLEMENTATION_NOTES.md AC-7 citation
- Priority: P0
- Behavior classification: ADD
- Related behavior: AC-7
- Related invariant: none
- Preconditions: IMPLEMENTATION_NOTES.md exists
- Exclusive resources: none
- Depends on: none
- Exact action: read IMPLEMENTATION_NOTES.md for its citation of `gh api repos/unclehq/uncle` / `.../readme` output (referenced by CHANGE_TEST_REPORT.md:19)
- Expected result: citation includes actual fetched content (not just "fetch attempted"), sufficient to compare against home.html body copy
- Evidence to capture: cited excerpt
- Actual result:
- Status: NOT RUN

### MC-14 Untested report sections
- Priority: P2
- Behavior classification: ADD
- Related behavior: none (process gap)
- Related invariant: none
- Preconditions: none
- Exclusive resources: none
- Depends on: none
- Exact action: inspect CHANGE_TEST_REPORT.md §Regression tests, §Full test suite, §Formatting, §Compiler or type checker (lines 23-35, largely empty/no-suite-exists)
- Expected result: confirm no test suite, formatter, or type checker is configured (BASELINE_REPORT.md:65-68) so these sections' emptiness is expected, not an omission
- Evidence to capture: confirmation that no config files exist for these tools
- Actual result:
- Status: NOT RUN

## Acceptance-criteria traceability
AC-1: MC-1. AC-2: MC-2, MC-12. AC-3: MC-3. AC-4: MC-4. AC-5: MC-5, MC-11, MC-12. AC-6: MC-6, MC-3, MC-12. AC-7: MC-7, MC-13, MC-12. AC-8: MC-8. AC-9: MC-9, MC-12.

## Preserved-behavior coverage
B-1: MC-10. I-1: MC-10. I-2: MC-8, MC-11. I-3: MC-9.

## Changed-behavior coverage
B-2: MC-1, MC-11. B-3: MC-2, MC-3, MC-11. B-4: MC-5, MC-11. B-5: MC-3, MC-6.

## Invariant coverage
I-1: MC-10. I-2: MC-8, MC-11. I-3: MC-9.

## Regression coverage
MC-8, MC-10, MC-9, MC-14.

## Removed checks
None.