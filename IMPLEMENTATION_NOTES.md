# Implementation notes

## Completed changes by file

| File | Change |
|---|---|
| `frontend/public/home.html:490-500` | Agentic Workflow card rewritten: heading/URL/Code link now `https://github.com/unclehq/uncle`; body copy (2 sentences) covers terminal-native, issue/requirements-in verified-PR-out, works with existing coding agents (not a fixed pairing), independent review, human approval gates, cryptographic pinning; `tag` line changed to `agentic coding · independent review · human approval gates`. Copy derived from `gh api repos/unclehq/uncle` description/homepage and `gh api repos/unclehq/uncle/readme` (README sections: intro tagline, "Why Uncle?" bullet list, "The change is the unit of trust") — satisfies AC-7. |
| `AGENTIC_WORKFLOW_STRATEGY.md:14` | Replaced "Adversarial review by a second model (Claude builds, Codex audits)" with agent-agnostic wording naming Claude/Codex only as examples of swappable implementing agents, decoupled from the independent reviewer. |

## Requirement/plan-step traceability

- CHANGE_PLAN.md §4 (exact components to modify) → both files above, no others touched.
- CHANGE_SPEC.md AC-1, AC-2, AC-3, AC-5, AC-7, AC-8, AC-9 → `frontend/public/home.html` card edit.
- CHANGE_SPEC.md AC-3, AC-6 → `AGENTIC_WORKFLOW_STRATEGY.md` line 14 edit.
- CHANGE_SPEC.md AC-4 → no edit required; verified still zero in source (see CHANGE_TEST_REPORT.md).

## Intentional deviations

None. Change surface matches CHANGE_PLAN.md's frozen file list (`AGENTIC_WORKFLOW_STRATEGY.md`, `frontend/public/home.html`) exactly.

Left `AGENTIC_WORKFLOW_STRATEGY.md:3` ("Saved from Claude Code session...") and the "Name alternatives" / "Immediate next steps" backlog sections unchanged — CHANGE_SPEC.md §15 (non-goals) explicitly excludes acting on the rename decision and backlog items; line 3 is session metadata, not a fixed-pairing positioning claim, and does not match the AC-3 grep pattern.

## Unresolved blockers

None. All nine acceptance criteria have passing targeted checks (CHANGE_TEST_REPORT.md).

## Acceptance delivery

| ID | Status | Changed code | Observed targeted verification |
|---|---|---|---|
| AC-1 | IMPLEMENTED | frontend/public/home.html:491,497 links → `unclehq/uncle` | `grep -o "unclehq/uncle" frontend/public/home.html \| wc -l` → 3; `grep -c "brianosaurus/agentic-workflow\|unclehq/stagegate" frontend/public/home.html` → 0 |
| AC-2 | IMPLEMENTED | frontend/public/home.html:492-497 body `<p>` | Manual read: covers terminal-native, issue/requirements-in verified-PR-out, existing agents not fixed pairing, independent review, human approval gates, crypto pinning |
| AC-3 | IMPLEMENTED | home.html card + AGENTIC_WORKFLOW_STRATEGY.md:14 | `grep -ic "claude builds\|codex audits\|claude/codex" AGENTIC_WORKFLOW_STRATEGY.md frontend/public/home.html` → 0,0 |
| AC-4 | IMPLEMENTED | No code change required; card link rewrite (AC-1) removed the only prior `brianosaurus/agentic-workflow` references and no `stagegate` reference was ever present in home.html or AGENTIC_WORKFLOW_STRATEGY.md | `grep -rl "stagegate" --exclude-dir=.git --exclude-dir=.uncle -- app frontend AGENTIC_WORKFLOW_STRATEGY.md \| wc -l` → 0 |
| AC-5 | IMPLEMENTED | frontend/public/home.html:498 `tag` line | `grep -n "LLM agents · pipeline tooling · open source" frontend/public/home.html` → no match |
| AC-6 | IMPLEMENTED | AGENTIC_WORKFLOW_STRATEGY.md:14 | AC-3 grep (above) covers banned phrase; manual read confirms agent-agnostic framing |
| AC-7 | IMPLEMENTED | frontend/public/home.html:492-497 | Copy cites `gh api repos/unclehq/uncle` description/homepage and README sections (intro tagline, "Why Uncle?", "The change is the unit of trust") |
| AC-8 | IMPLEMENTED | n/a (preserve) | `git diff frontend/public/home.html \| grep -E '^@@'` → single hunk `@@ -488,14 +488,16 @@`, contained within card block (490-500) |
| AC-9 | IMPLEMENTED | frontend/public/home.html | `python3 -c "import html.parser,pathlib; ...feed(...)"` → exit 0, `parsed ok` |

## Handoff notes

`static/home.html` is a Vite build artifact (BASELINE_REPORT.md §2) and does not exist in this worktree; no rebuild was run or required to verify the source change.
