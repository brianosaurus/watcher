# Combined baseline, change specification, and planning

In this single stage and the same model and context, first establish the baseline by running verification commands and write BASELINE_REPORT.md, then write CHANGE_SPEC.md, then use it to write CHANGE_PLAN.md. These are drafts for the existing approval gates. Do not implement source changes.

Write each document to disk the moment its inputs are in hand -- BASELINE_REPORT.md before any reading for the specification, CHANGE_SPEC.md before any reading for the plan. A document on disk survives a context that runs out; work still in progress does not. Grep for the symbols CHANGE_REQUEST.md names and read the surrounding lines; never read a large file end to end.

You are the primary existing-code analyst.

Read:

- README.md
- CHANGE_REQUEST.md
- repository documentation
- build and dependency files
- relevant source code
- existing tests

Inspect the current repository before changing anything.

Create BASELINE_REPORT.md containing:

1. Change-request summary
2. Repository architecture
3. Relevant code paths
4. Current observable behavior
5. Existing invariants
6. Current API, schema, and interface contracts
7. Existing automated-test coverage
8. Exact build and test commands executed
9. Baseline test results
10. Existing failures, warnings, and flaky behavior
11. Reproduction result for the reported bug, if applicable
12. Likely change surface
13. Regression-sensitive components
14. Areas explicitly outside the change
15. Unknowns and assumptions
16. Initial risk assessment

For each existing behavior include:

| ID | Trigger | Current result | Evidence | Must preserve? |
|---|---|---|---|---|

For each existing invariant include:

| ID | Invariant | Current enforcement | Existing test | Confidence |
|---|---|---|---|---|

Do not modify source code.
Do not fix the issue.
Do not create an implementation plan.

## Context economy

Everything a tool returns stays in context and is re-sent on every later turn
of this stage. A large command output read early is paid for many times over.
This stage reads more of the repository than any other, so the discipline
matters most here.

- Run test suites with the quietest flag that still reports failures. Record
  the summary line and the names of failures; never paste passing output.
- Pipe commands whose output is unbounded through `tail`, `wc -l`, or a
  summary flag. `find`, `ls -R`, and full-tree greps need a bound.
- Use Grep with a targeted pattern in preference to reading a large file end
  to end. Never read a file longer than about 300 lines end to end: grep for
  the symbols CHANGE_REQUEST.md names and read the surrounding lines. One
  whole large module is a third of this stage's context.
- Write BASELINE_REPORT.md as soon as sections 8 and 9 have their evidence,
  before any reading for later documents. A report on disk survives a context
  that runs out; one still in your head does not.
- Cite code by path and line rather than quoting it. The report is read by
  five later stages; quoted source is paid for in each of them.
- Do not re-read a file you have already read in this stage.

## Output economy

Length is a cost. Write the shortest report a reviewer can act on. Six later
stages read this report, and each of them re-sends it on every turn, so a word
here is paid for six times over.

- Use the appended budget and enforcement mode; no separate word limit.
- Omit any numbered section with no substantive content for this change.
- Directly under the title write one line:
  `Omitted sections: <name> (<reason>); <name> (<reason>)`
  or `Omitted sections: none`.
- Do not restate CHANGE_REQUEST.md. Cite it and move on.
- Prefer tables and short declarative clauses over prose.
- Never omit a section to avoid resolving something. If a section applies but
  you cannot complete it, keep it and mark it UNRESOLVED with the reason.

Section 8 and section 9 are never omitted: the exact commands you ran and their
results are the evidence the rest of the workflow depends on.

## Section 8 is executed, not just read

The driver re-runs section 8 itself — once now, against the unmodified tree,
and once after the change — and compares the two. That is how the workflow
knows a check passed, rather than taking the implementation stage's word for
it. So write section 8 as a command list a shell can run:

- one fenced block, immediately under the heading, and nothing else in it;
- one command per line, exactly as you ran it, from the repository root;
- no prompt prefixes, no comments, no prose, no placeholders;
- no command that needs a human, a password, an interactive browser, or a network service
  you cannot reach here — leave those to the manual checklist instead;
- no command that changes the repository. These run twice, and the first run
  must leave the tree exactly as it found it.

A check that is already failing is still listed. The driver records that it
failed before the change, so it will not be blamed on the change; omitting it
only hides it.

Prefer the project's documented test runner over constructing shell loops.
When analyzing Uncle itself, if `scripts/run-shell-tests.sh` exists, use
`bash scripts/run-shell-tests.sh` for its shell regression suites and record
that exact command. It already parallelizes suites and aggregates failures;
do not also run those suites individually or wrap them in a serial loop.

It takes about three minutes at the default four jobs; allow ten before
treating it as hung. Two things make that worse rather than better: cutting it
off early and retrying, and lowering `--jobs`, which only makes the same work
take longer. Run it with `bash` -- the suites are shell scripts, and `python3`
on one fails with a parse error that reads like a broken test rather than the
wrong interpreter.
For other projects, inspect their runner and fixture isolation before choosing
parallelism; do not assume this Uncle-specific script exists.

Automated browsers and local test servers are permitted when required for
acceptance. Run independent test suites in parallel by default. Append
`## Parallel verification groups` for independent suites, holding one
fenced block and nothing else — bare rows of consecutive, one-based command
positions, one group per line:

```text
2 3
5 6
```

Rows must be ordered and disjoint; no bullets, labels, backticked numbers, or
prose in the block. Group only commands with independent ports, outputs,
fixtures, and state, and explain their independence in the test coverage
section.
The driver uses the approved groups for both baseline and post-change checks;
do not regroup commands after approval.

Write BASELINE_REPORT.md and stop.

## Bounded baseline and compact first draft

Start with CHANGE_REQUEST.md and the repository's documented verification entry
points. Build a short map of affected symbols, their callers and relevant tests.
Read only documentation and code needed to establish current behavior, invariants
and regression risks for this change. Expand discovery only to answer a concrete
unresolved question; do not read remaining large-file sections for completeness.
Batch independent reads. Existing reports are navigation hints, not fresh PASS
evidence, and reports from other issues must not become this baseline.

Choose the documented relevant checks once, including any repository-mandated
full suite. Execute each selected command once and capture full stdout/stderr
and its real exit status in workflow logs. For Uncle use run-shell-tests.sh;
do not run its selected suites again individually. Group other independent
commands only when their fixtures, ports and outputs are isolated. Do not overlap
a full suite with its constituent tests. Poll an active command rather than
launching it again. Inspect a failing check's saved log before considering a
rerun; rerun only for a specific reproduction or flakiness question and record why.
Do not pipe a check through tail in a way that loses its failure exit status.

Compose the report after collecting evidence: one canonical row per behavior,
invariant and executed result, referenced elsewhere by ID. Preserve exact commands,
exit codes, failures, evidence paths and unknowns. Reconcile sections 8/9 and
parallel groups once. No repeated narrated format sweeps or whole-report rereads
without a specific discrepancy. In advisory-budget mode perform ZERO size-only
compaction passes; mandatory evidence survives above the guide. The driver
measures the report. Enforced budgets retain the two-pass limit.

Return/write the complete BASELINE_REPORT.md under the runner contract. Steering
questions do not replace the task: answer them, then finish the baseline. Never
substitute a conversation summary, filename or progress note for the report.
Do not modify source code or create project commits.


# Then specify the change

You are the primary requirements analyst for a change to an existing system.

Read:

- CHANGE_REQUEST.md
- BASELINE_REPORT.md

BASELINE_REPORT.md already summarizes the repository and its documentation.
Do not re-read README.md or the source tree; if the baseline is missing
something you need, say so rather than rediscovering it here.

Create CHANGE_SPEC.md.

Use a `## Acceptance criteria` section with a table headed
`| ID | Criterion | Verification |`. Give every required criterion a unique
stable AC-number ID (AC-1, AC-2, ...). Include all required behavior; these IDs
are the driver's implementation handoff contract, not optional examples.

Include:

1. Change type
2. Problem statement
3. Current behavior
4. Desired behavior
5. Acceptance criteria
6. Observable behavior table
7. Invariant table
8. Compatibility requirements
9. Error and failure behavior
10. Performance requirements
11. Security requirements
12. Migration requirements
13. Rollback expectations
14. Prototype-isolation requirements, if applicable
15. Explicit non-goals
16. Assumptions and unresolved questions

Behavior table:

| ID | Class | Trigger | Current behavior | Expected behavior | Verification |
|---|---|---|---|---|---|

Class must be one of:

- PRESERVE
- MODIFY
- ADD
- REMOVE
- EXPERIMENTAL

Invariant table:

| ID | Status | Invariant | Scope | Enforcement point | Verification |
|---|---|---|---|---|---|

Status must be one of:

- EXISTING
- NEW
- STRENGTHENED
- RELAXED
- REMOVED
- EXPERIMENTAL

Highlight every RELAXED or REMOVED invariant.

Do not design implementation details.
Do not modify source code.

## Output economy

Length is a cost. Write the shortest specification a reviewer can act on.

- Omit any numbered section with no substantive content for this change.
- Directly under the title write one line:
  `Omitted sections: <name> (<reason>); <name> (<reason>)`
  or `Omitted sections: none`.
- Do not restate BASELINE_REPORT.md. Reference its IDs instead of copying rows.
- Prefer tables and short declarative clauses over prose.
- Never omit a section to avoid resolving something. If a section applies but
  you cannot complete it, keep it and mark it UNRESOLVED with the reason.

The behavior table, the invariant table, and the acceptance criteria are never
omitted. Everything downstream is traced against them.

Write CHANGE_SPEC.md and stop.


# Then plan the specified change

You are the primary change architect.

Produce an executable plan, not a list of decisions for the implementation
agent to make before it can start. Apply these rules before finalizing:

- Resolve routine engineering choices within the authorized scope now. Use the
  existing code and the user's requested behavior to choose defaults; record
  each as a decision with a short reason, not an unresolved approval request.
  Examples include internal event transport, cached display state, identifier
  selection, and layout at narrow widths.
- Check the selected approach against every requirement and scope constraint.
  If your approach conflicts with one, revise the approach within scope. Do
  not leave a required implementation step conditional on an unapproved
  exception, or silently weaken acceptance criteria to fit your design.
- Treat approval of this plan as approval of its clearly stated, in-scope
  design decisions. Do not require the user to approve those same decisions
  again before coding. Never claim that a separate, genuinely required scope
  or product decision has already been approved.
- If a decision truly cannot be resolved within the user's authority and
  requirements, ask the precise question during planning when interaction is
  available. Otherwise identify it prominently as a blocking planning decision,
  explain the conflict and alternatives, and state that the plan is not ready
  for implementation. Do not bury it in an assumptions table or present it as
  an executable plan that will stop immediately.
- Reserve implementation stop conditions for newly discovered contradictions,
  missing external prerequisites, or changes requiring new authority. Resolve
  known design questions here instead of copying them into stop conditions.
- Perform a final consistency pass across decisions, steps, scope, acceptance
  criteria, prerequisites, and stop conditions. Every required step must be
  actionable on the current evidence. Remove stale UNRESOLVED labels and
  approval prerequisites after settling the corresponding decision.
- Check proposed behavior changes against existing tests, including protected
  verification paths. Resolve conflicting expectations within scope before
  approval; explicitly identify any test change requiring renewed authority.
  Separate prerequisites for coding from prerequisites for live verification.
  Missing credentials for one runner must not halt independent implementation.

Read:

- CHANGE_REQUEST.md
- BASELINE_REPORT.md
- CHANGE_SPEC.md
- the source and tests named in the baseline's change surface

BASELINE_REPORT.md lists the relevant code paths by file and line. Go straight
to those. Do not re-explore the repository or re-read README.md.

BASELINE_REPORT.md and CHANGE_SPEC.md have just passed a human approval gate
and may have been edited during that review. Re-read both from disk. Do not
rely on remembered content for either one.

Create CHANGE_PLAN.md.

Carry issue identity from CHANGE_REQUEST.md into CHANGE_PLAN.md:

- Inspect only metadata before the first `##` in CHANGE_REQUEST.md. Use the
  first top-level `Seeded from` link (optionally prefixed with `> `); extract
  the issue number from its GitHub issue URL. Preserve that source seed URL
  verbatim in the plan.
- If that URL supplies no issue number, use the first standalone `Issue N`
  line in the same metadata, where N is a decimal issue number. The URL number wins
  if it conflicts with the standalone line; this also supports legacy requests
  containing only the seed link.
- Write exactly one standalone `Issue <number>` line after title metadata
  (including any omission or review-disposition metadata), before the first `##`.
  Ignore issue identities in body sections, examples, and other documents.
- If neither source supplies an issue number, omit the identity line without
  failing. Preserve any available source seed URL verbatim; never invent a URL.

Include:

1. Selected technical approach
2. Alternative approaches considered
3. Why the selected approach is preferred
4. Exact components to modify
5. Components explicitly not to modify
6. Data-flow changes
7. State-transition changes
8. Interface and API changes
9. Schema or persistence changes
10. Compatibility strategy
11. Concurrency implications
12. Error and recovery behavior
13. Migration plan
14. Rollback plan
15. Feature-flag or containment strategy
16. Automated-test strategy
17. Regression-test strategy
18. Manual-verification strategy
19. Observability changes
20. Implementation sequence

21. Scope cuts under time pressure
22. Risks and unresolved questions

Include a change-impact table:

| Component | Planned change | Reason | Regression risk | Test coverage |
|---|---|---|---|---|

Include traceability:

| Requirement | Behavior | Invariant | Component | Automated test | Manual check |
|---|---|---|---|---|---|

For bug fixes, identify the regression test that should fail before the fix and
pass afterward.

For prototypes, explain how the experiment will be isolated from production
behavior.

Do not implement code.

## Output economy

Length is a cost. Write the shortest plan an implementer can execute and a
reviewer can attack.

This document is not superseded later: the adversarial review is answered by
editing this file in place, and every stage after that reads this file. Write
sections that can be edited surgically — one claim per line, tables over
paragraphs — rather than prose that has to be rewritten wholesale to change one
fact.

- Use the appended stage budget and enforcement mode; no separate word limit.
- Omit any numbered section with no substantive content for this change. A
  change that touches no schema, no migration, and no concurrency should not
  carry those headings at all.
- Directly under the title write one line:
  `Omitted sections: <name> (<reason>); <name> (<reason>)`
  or `Omitted sections: none`.
- Do not restate CHANGE_SPEC.md. Reference its behavior and invariant IDs.
- Prefer tables and short declarative clauses over prose.
- Never omit a section to avoid resolving something. If a section applies but
  you cannot complete it, keep it and mark it UNRESOLVED with the reason.

The change-impact table, the traceability table, the implementation sequence,
and the rollback plan are never omitted.

Write CHANGE_PLAN.md and stop.

Every restriction, including carried-forward review mitigations, needs an R- ID,
source_kind USER/REPOSITORY/PLATFORM/DESIGN, source location, requirement IDs,
required property, selected mechanism, rationale and CAP- capability IDs.
Record selected runner/config binding, observed feasibility evidence (path/hash,
probe command or inspected symbol/lines and result), and CODING versus LIVE_VERIFICATION
phase. A generated mechanism remains a revisable DESIGN choice after plan approval.
Preserve genuine constraints and required properties while selecting feasible alternatives.
Inventory steps with IDs, paths, requirements, dependencies, capability IDs and decision IDs.
Separate unavailable live authentication from coding prerequisites; include approved live
check IDs/commands and non-secret prerequisite evidence paths for verification resume.

## Proportional implementation and verification

Choose the smallest architecture and toolchain that meets the actual requested
behavior and the repository's conventions. For a static page, prefer plain HTML
and CSS unless a stated requirement needs more. Do not add a framework, linter,
formatter, build system, browser matrix, or test dependency solely to populate a
plan section. Reuse existing suitable tools. Retain required browser-grounded
checks, negative cases, and acceptance evidence; simplicity does not waive them.

Plan setup separately from verification. Allow reuse of dependencies and browser
binaries only after checking version/lockfile compatibility and actual usability.
Require fresh installation only when testing installation, when reuse is invalid,
or when explicitly requested. State cache invalidation inputs in the setup step.

Group independent file creation and verification work so the implementation model
can batch it. Name concrete reasons for serial dependencies. Arrange for each
required report to be written once after evidence is collected. On revision,
change only what findings or requirements require; do not expand scope or invent
additional tooling merely because another planning pass is occurring.

## Compact first draft

Build the required heading skeleton and canonical rows before drafting prose.
Each behavior, invariant, acceptance obligation, restriction and implementation
step has one complete location with a stable ID. Other sections reference that
ID instead of repeating its wording. Preserve exact assertions, thresholds,
failure behavior, dependencies, evidence requirements and restriction fields.
Use concise tables initially, not an expanded narrative to compress afterward.
Keep short None entries where appropriate; do not omit required sections.

Define each verification command and protected path once in its required
location. Strategy and step rows reference those commands and check IDs; avoid
second lists that can diverge. Before the single final write, reconcile coverage,
traceability, dependencies, commands and paths once. Resolve actual omissions or
contradictions without narrating repeated compliance checks. Return the complete
plan, with no preamble, work diary, filename-only answer or closing recap.

Do not repeatedly estimate byte counts or request unavailable tools to measure
size. The driver measures the artifact. In advisory-budget mode, do ZERO
size-only compaction passes after the complete draft. Mandatory content survives
even above the guide. Enforced budgets retain the preservation validator and
at most two passes total; retain an oversized complete artifact for driver
resolution if needed. Format, completeness and executability checks still apply.

Every step in the implementation sequence must end with `Owns:` — the
repository-relative files that step writes, backticked and comma-separated. A
step owns a file when it is the only step that writes it. Add
`Depends on: <step numbers>` when a step needs an earlier one finished first.
A step that touches everything declares `Owns: *`.

If a step's own description or title names a file it touches (a "scaffold", a ".gitignore update", a config it edits), that file must also appear in its `Owns:` list -- do not describe touching a file without declaring it. This is the single most common real gap: a step that legitimately runs a package manager also writes its lockfile, which needs its own `Owns:` entry beside the manifest.

  1. Arithmetic core — Owns: `src/calc.js`, `tests/calc.test.js`
  2. Keypad and display — Owns: `src/ui.js`, `index.html`
  3. Reconcile — Owns: `*` — Depends on: 1, 2

A step is not complete without it. Declare honestly rather than optimistically:
claiming a file the step does not write is worse than claiming none, and a step
whose files genuinely overlap another's should say so by naming the same file,
not by omitting the field.
