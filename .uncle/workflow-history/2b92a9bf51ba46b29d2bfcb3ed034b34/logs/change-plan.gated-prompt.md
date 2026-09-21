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

## Acceptance provenance

A mandatory human sign-off needs an explicit user/source requirement, or a
specific judgment that available automated evidence cannot establish. Cite that
source or explain the non-automatable property. A generated plan or an earlier
model's assumption is not independent authority to add a human approval.
"Browser verification" does not itself require a person; automated browser
assertions can establish exactly what they measure. Do not invent a requirement
to approve an ordinary engineering choice such as an unspecified browser engine.
Never claim a human observation occurred. Keep genuinely subjective judgments
unverified until observed or explicitly waived. If a prior generated obligation
has no source, identify the conflict and resolve it in the report rather than
silently treating it as user intent or silently claiming PASS.

## Shared driver evidence index
Current files were rehashed. Cached excerpts are navigation only, never PASS or approval evidence.
Read omitted input and exact assertion evidence directly. Missing files do not imply satisfied requirements.
Changes since this stage last prepared inputs: CHANGE_SPEC.md, BASELINE_REPORT.md, package.json, pyproject.toml, requirements.txt, package-lock.json, @green-check.commands, @green-check.groups
Independent reviewers must challenge conclusions even when input hashes are unchanged.

CHANGE_SPEC.md: {"status": "missing or unreadable"}


BASELINE_REPORT.md: {"status": "missing or unreadable"}


package.json: {"status": "missing or unreadable"}


pyproject.toml: {"status": "missing or unreadable"}


requirements.txt: {"path": "/Users/brianwoods/src/watcher-issue-1/requirements.txt", "sha256": "be5277eb495d005d6613b3431c366773f902bc8acf8c466692bbb72720c54188", "bytes": 57}
fastapi==0.115.4
uvicorn[standard]==0.32.0
psutil==6.1.0


package-lock.json: {"status": "missing or unreadable"}


@green-check.commands: {"status": "missing or unreadable"}


@green-check.groups: {"status": "missing or unreadable"}

All excerpts are bounded; read source documents for complete requirements and command blocks.


## Git signing during automated work

For every project, building, testing, verification, approval, and completion
must work without creating a project commit. Do not require a baseline,
checkpoint, implementation, or final commit, or a clean working tree, as a
prerequisite for those stages. This also applies when resuming an older plan:
replace commit-dependent verification with equivalent file-based evidence;
do not ask the user to commit to unblock ordinary build work.

Use file hashes and path inventories that include
untracked files instead of requiring a clean Git status. Snapshot protected
inputs before changes and protected test paths immediately before checks;
compare afterward without refreshing the snapshot. Leave real project commits
to the final user-approved publishing flow unless the user explicitly requests
an intermediate commit. Publishing and PR creation are optional follow-up
actions; declining them does not invalidate completed build work. A generated
plan is not user authorization to commit. Tests of Git behavior may create
commits only in disposable fixtures under the signing rules below.

All automated tests and test fixtures MUST disable GPG/SSH commit and tag signing.
Never let a test use the user's signer, GPG agent, pinentry, or private keys.

- Run fixture Git commands with `git -c commit.gpgsign=false -c tag.gpgsign=false`.
- Every fixture `git commit` and `git commit-tree` must also include
  `--no-gpg-sign`; fixture tag creation must use `--no-sign`.
- Set repository-local `commit.gpgsign=false` and `tag.gpgsign=false` in each
  disposable test repository. Keep the explicit command flags as well.
- Ensure test subprocesses use those same settings; do not inherit the user's
  signing configuration. Never run tests against the user's real signing keys.
- Signing-specific tests must mock signing or use isolated disposable test keys.
- Never change the user's global Git configuration or disable signing in the
  actual project checkout to make an automated command succeed.

Real project commits are different from test-fixture commits. A plan that calls
for a baseline, checkpoint, implementation, or release commit does not authorize
the agent to invoke signing. If a real commit needs signing, present the exact
Git command for the user to run, then verify the resulting commit. Do not invoke
the signer, retry a signing failure, or launch pinentry automatically. Do not
replace a required signed project commit with an unsigned commit.

## Launching the finished application

For implementation stages, record the verified launch method in
`.uncle/launch.json` before completion. This is product launch metadata, not a
commit prerequisite. Use one of these JSON shapes:

- Command: `{"kind":"command","command":["python3","app.py"]}`
- Static webpage: `{"kind":"webpage","path":"index.html"}`
- Web server: `{"kind":"webpage","command":["npm","run","start"],"url":"http://127.0.0.1:3000"}`
- No runnable application (for example a library): `{"kind":"none"}`

Use the actual verified entry point and arguments; do not copy these examples
unless they match the project. Commands are argument arrays, not shell strings.
Choose a normal demo invocation, never installation, deployment, publishing,
committing, or a destructive operation. Refresh stale launch metadata when the
entry point changes. The TUI launches it after successful workflow completion,
streams command output in the build window, and opens webpages in the browser
before offering the optional GitHub star dialog.


---

# Output rules (binding)

The document you write must satisfy every rule below. They govern its shape;
this stage's instructions above govern its content. Where they disagree about
shape, these rules win.

# Output Rules

These rules apply to every markdown document a stage writes for a human to
read: the requirements interpretation, the baseline, the specs, the plans, the
notes, the test reports, the checklists, the verification reports, the audits.

They are appended to the prompt of every document-producing stage, so they
bind whatever agent runs it. They are about the shape of the document, not its
content: a stage's own prompt says what to write, and `lib/gates/GATES.md`
adds the quality gates a plan must pass.

If a rule fails, fix the document before writing it. Do not emit a document
that breaks one and note the breakage in the text.

## Rule 0 — Output target

- Write exactly the file the stage asked for, at exactly that path. Do not
  rename it, do not add a suffix, do not write a second copy elsewhere.
- When the stage explicitly requires multiple artifacts, write each named
  artifact and print its path on its own line. This exception also permits
  source and test edits explicitly required by implementation or repair stages.
- Print nothing to the conversation except the output artifact paths, one per
  line.
- No preamble, no closing summary, no "here is your document", no offer to
  continue.

## Rule 1 — Audience

Write for a senior engineer who already knows the domain and is about to
approve or reject this document at a gate.

- Do not explain what a tool is, why testing matters, or what the project is
  for beyond the single sentence that states the goal.
- Do not restate the prompt, the requirements, or a previous stage's document.
  Reference it by name and move on.

## Rule 2 — One claim per line, every claim checkable

- A statement about the code names the file, and the symbol or line when the
  claim is about one place: `scripts/stagegate.sh:402`.
- A statement about behavior names how it was observed: a command that was
  run, output that was read, a file that was inspected.
- A statement about what will happen is marked as a plan, not as a fact.

## Rule 3 — Say what is not known

Anything unverified is labeled, in place, with what would settle it:

```
ASSUMPTION: the resume PDF describes one role per page.
  Unverified: pdftoppm is not installed, so the file was not read.
  Settled by: installing poppler and re-running this stage.
```

An assumption presented as a finding is the failure this whole workflow exists
to prevent. A document with no assumptions section is claiming there were
none.

## Rule 4 — Structure is fixed, not invented

- Use the sections the stage's prompt names, in that order, with those exact
  headings. Add nothing, drop nothing, reorder nothing.
- When the prompt names no sections, use `## Summary`, `## Findings`,
  `## Assumptions`, `## Open questions` — in that order.
- Tables for anything enumerable: behaviors, invariants, findings,
  dispositions, checks. One row per item, one item per row.
- Preserve any driver-parsed section, columns, status vocabulary, and required
  rows exactly as specified by the stage. Never omit mandatory acceptance rows
  to meet a length limit; shorten surrounding prose first. If required rows
  alone exceed a section or document cap, retain them and report that exception
  in Open questions.
- Give every enumerated item a stable identifier (`B-3`, `I-2`, `AR-004`,
  `MC-7`) so later stages and humans can cite it.

## Rule 5 — Length

- Every stage document has a per-file byte and line budget, including
  implementation, repair, review, checklist, and acceptance reports. The appended
  budget lists the exact limits and enforcement mode. Budgets are advisory
  unless WORKFLOW_DOC_BUDGET_ENFORCE=1; ceilings are not targets to fill.
- Default budgets scale from authoritative REQUIREMENTS.md (new builds) or
  CHANGE_REQUEST.md (changes), with artifact-specific floors and ceilings listed
  in README.md. Plans, reports and reviews use twice the source byte size;
  interpretations, change specs and notes use source size. Line limits also scale
  within bounds, except interpretations and change specs retain 160 lines.
  Generated upstream artifacts never enlarge downstream budgets.
- Reference settled upstream obligations by file and ID instead of recataloging
  them. Preserve required acceptance rows and the complete executable plan.
  Update current rows during revisions and repairs, retaining IDs and dispositions;
  do not append a narrative for every attempt.
- `WORKFLOW_DOC_MAX_BYTES` and `WORKFLOW_DOC_MAX_LINES` override defaults.
  Artifact-specific variables (e.g. `WORKFLOW_DOC_MAX_BYTES_FINAL_AUDIT`)
  take precedence over global overrides. The appended budget is authoritative.
- Keep the execution contract complete in the named artifact. Cite existing logs
  and evidence by file and section; avoid copying transcripts and repeated rationale.
  Do not create a second summary artifact or move obligations out of the contract.
- Draft to the appended byte and line targets from the start. Reserve room for
  mandatory headings, rows, commands, and evidence before writing. Collect results
  before composing the report; batch independent reads and size measurements.
- If the document fits both ceilings, finish without a size-only rewrite. An
  advisory target is not a reason to compact. Reviewers return a concise final
  artifact directly; the driver measures it. Do not request filesystem writes
  solely to measure a read-only reviewer's response.
- For project-plan, change-plan, adversarial-review, updated-plan and
  updated-change-plan, test-review and manual-checklist (including base/delta),
  execute-checklist and final-audit, advisory budgets require compact-first drafting with ZERO
  size-only rewrite passes. Preserve complete artifacts even above the guide.
  This stage-specific policy takes precedence over the general rule below.
- Otherwise, only compact an oversized document, within the producing stage and using its
  model and context, at most twice total across its output documents. Leave
  compliant documents unchanged. The initial draft is not a pass;
  every later size-driven rewrite or trim counts, including a "final trim".
  Chat questions and steering do not reset the count. After the second pass,
  stop size-only edits, preserve the complete artifact, report final byte/line
  counts and any overage, and finish. Do not restart just to shrink it further.
  The driver preserves oversized artifacts and continues by default; an operator
  can increase the budget or set `WORKFLOW_DOC_BUDGET_ENFORCE=1` to block overruns.
- No sentence that survives having its adjectives removed unchanged in
  meaning. Cut it instead.

## Rule 6 — Banned

These add length without adding information, and their presence is a defect:

- "comprehensive", "robust", "seamless", "leverage", "utilize", "in order to",
  "it is important to note", "as mentioned above", "best practices",
  "production-ready", "enterprise-grade", "cutting-edge".
- Emoji, decorative rules, ASCII art, and horizontal separators between every
  section.
- Praise of the plan, the code, the requirements, or the reader.
- Any sentence whose subject is "we" and whose verb is a promise.

## Rule 7 — Diffs and code

- Quote code only when the document's claim depends on the exact text. Quote
  the smallest span that carries the claim, and cite its location.
- Never paste a whole file. Never paste a diff the driver already records.


## Proportional work and bounded inspection

For a small application or change, use the shortest report that satisfies every
required section, acceptance row, and evidence reference. Do not turn a simple
page into an extensive design exercise. Prefer one concise table over repeated
prose; reference earlier requirements by ID instead of restating them. Preserve
all actual requirements and blockers. Budgets are drafting targets, not a reason
to repeatedly rewrite an otherwise complete report.

Before inspection, collect the known input paths and read independent files in
one batch. Start with files named in the approved plan and current evidence.
Avoid recursive searches from the project root. Exclude `.uncle/workflow-history`,
`.git`, dependency directories, virtual environments, caches, and generated build
outputs from discovery unless a specific investigation requires them. Read named
hidden workflow files directly; never infer absence from a Glob result.

Reviewers should use current driver exit codes and linked test output before
requesting additional execution. Rerun only to resolve a concrete evidence gap,
changed input, or failure; state why. Inspect assertions and negative cases, but
do not duplicate passing driver checks merely to produce another passing record.
Batch independent inspections and report only findings, decisions, and required
acceptance evidence. Keep progress commentary out of the final report response.


---

# Output gates (binding)

The plan you write must pass every gate below. Resolve the gates in this
order: a project-local GATES.md or .uncle/gates/GATES.md wins; otherwise the
gates installed with uncle apply.

# Output gates: /opt/homebrew/Cellar/uncle/0.1.0+git20260920210134.48501894682c/libexec/lib/gates/GATES.md (installed)

# GATES.md — Project Plan Output Gates

These rules apply whenever a stage produces a plan. Every gate must pass before output is written. If a gate fails, fix the plan and re-check; do not emit a failing plan.

The stage's prompt owns the plan: the target file, the sections and their order, the content. These gates govern quality only. Where a gate and the stage's prompt disagree about the file or the structure, the stage's prompt wins.

## Gate 0 — Output target

- Write exactly the file the stage's prompt names, at exactly that path. Do not rename it, do not add a suffix, do not write a second copy elsewhere.
- Print nothing to the conversation except the path of the file written, on one line.
- No preamble, no closing summary, no "here is your plan."

## Gate 1 — Audience

Write for a senior engineer who already knows the domain and is about to approve or reject the plan. Do not explain what tools are, why testing matters, or what the project is for beyond the one-sentence goal.

## Gate 2 — Structure

- Use the sections the stage's prompt names, in that order, with those exact headings. Add nothing, drop nothing, reorder nothing.
- When the prompt names no sections, use `# <Plan title>` then `## Goal`, `## Constraints`, `## Steps`, `## Risks`, `## Done when` — in that order.
- Rejected either way: intro paragraphs, "Overview," "Background," "Next steps," "Conclusion," stakeholder tables, timelines with weeks unless the user asked for dates.

## Gate 3 — Concreteness and length

- Every step names something concrete: a file path, a command, a function, a schema, a number.
- The output rules own the length caps. When over a cap, delete the lowest-information item first. Never compress by merging two steps into one vague step.

## Gate 4 — Language

- Plain declarative sentences. Active voice. Imperative mood in steps ("Add `retry()` to `client.py`").
- No adjectives that don't change what an engineer would do.

Banned (hard fail if any appear): leverage, robust, seamless, seamlessly, scalable, scalability, streamline, holistic, best-in-class, world-class, ecosystem, synergy, synergize, empower, cutting-edge, state-of-the-art, comprehensive, innovative, optimize (unless a metric is named), enhance, facilitate, utilize, "ensure that", "it is important to note", "in order to", "going forward", "moving forward", "at the end of the day", "stakeholders" (name the people or teams instead), "solution" (name the thing), "robustness", "best practices".

## Gate 5 — Self-check pass (run before writing the file)

After drafting, rewrite once with only these instructions:

1. Delete any sentence that does not tell an engineer what to do or what to check.
2. Replace any category word ("the service," "the data layer") with the specific name.
3. Scan for every banned term; replace or delete.
4. Confirm the target file and the section list match the stage's prompt exactly.

Only the rewritten version is written to the file.


# Required artifact and final-response contracts (binding)

The driver consumes these documents directly. A document that is
correct in substance but delivered in another shape is rejected unread.

## CHANGE_PLAN.md

The frozen change scope is read from a level-2 heading spelled exactly
`## Change-impact table`, followed by a table. A bold label or a `###` heading
is NOT recognised, and the driver cannot resolve the scope without it.

## Change-impact table

| Component | Change | Test coverage |
|---|---|---|
| `scripts/lib/example.sh` | add the guard | `scripts/tests/example-test.sh` |

Name every file the change touches in backticks, in the Component cell, and the
tests that must change with it in Test coverage. Repo-relative paths only: a
leading slash reads as a route, not a file. These rows are the plan committing
to a file set, and later stages check the diff against them.

Every numbered implementation step MUST end with `Owns:`, listing the exact
repo-relative files it alone may edit (or `*` only for a final reconcile step),
and `Depends on:`, listing prerequisite step numbers or `none`. These fields
are the driver's only inputs for safe parallel implementation worktrees. Do
not omit them or infer dependencies from prose.
Give every enumerated item a stable identifier in the first column, so later
stages and the audit can cite it: `R-1`, `B-2`, `I-3`, `AR-4`, `D-5`. An
identifier is letters, digits and hyphens with no spaces. Never renumber an
existing id; add new ones at the end. One row per item, one item per row.

Final-response contract for `CHANGE_PLAN.md` (binding):

Return an executable change plan, not a specification or review. Start with `# Change plan`; then give only: scope and constraints, the exact `## Change-impact table`, ordered file-level implementation steps, requirement-to-step traceability, verification commands/evidence, rollback, and unresolved approval decisions. Do not claim the edits or tests were performed.
Every numbered implementation step must end with `Owns:` (exact repo-relative files, or `*` only for a final reconcile step) and `Depends on:` (prior step numbers or `none`). The parallel implementation scheduler consumes these declarations directly; never omit or infer them.

## CHANGE_SPEC.md

Give every enumerated item a stable identifier in the first column, so later
stages and the audit can cite it: `R-1`, `B-2`, `I-3`, `AR-4`, `D-5`. An
identifier is letters, digits and hyphens with no spaces. Never renumber an
existing id; add new ones at the end. One row per item, one item per row.

Final-response contract for `CHANGE_SPEC.md` (binding):

Return a frozen change specification, not an implementation plan. Start with `# Change specification`; then give only: requested change, ID-keyed requirements/behaviors/invariants, preserved behavior, acceptance criteria, explicit non-goals, and compatibility/rollback constraints. Do not list coding steps, assert tests passed, or make an audit verdict.


# Compact output budgets

Budget enforcement is disabled: byte and line limits are advisory. Complete required content takes precedence over size.
- CHANGE_PLAN.md: at most 10299 UTF-8 bytes and 309 lines. Draft toward 7724 bytes and 231 lines to leave revision room.
- CHANGE_SPEC.md: at most 10299 UTF-8 bytes and 309 lines. Draft toward 7724 bytes and 231 lines to leave revision room.

## Compact-first artifact policy
This stage's size limits are advisory drafting guides, not completion gates.
Draft compactly once; do ZERO size-only compaction passes. This policy replaces
all general size-only rewrite instructions, including local output rules.

Start from the required section skeleton and inventory all mandatory rows and
finding IDs. Give every obligation or distinct defect one complete canonical
location. Reference its ID elsewhere, never repeat its narrative. Preserve all
thresholds, exact commands, paths, dependencies, evidence, restriction provenance,
and acceptance criteria. Keep required headings and meaningful field values.
Do not delete mandatory content, remove Markdown spacing, or shorten identifiers
just to meet a byte/line guide. Completeness takes precedence over size.

For revisions, retain unaffected rows and change only what findings or changed
requirements demand. For reviews, investigate independently: a plan or shared
packet is not proof. Do not omit a genuine finding to make the report shorter.
Batch independent reads; do not repeat discovery or checks supported by current
evidence. Reconcile traceability, fields, command blocks and contradictions once
before finalizing. Correct actual defects, not cosmetic size overages.

Write/return the complete artifact once as required by the runner contract.
Never return a filename, progress note, or summary in place of the document.
The driver measures bytes and lines. Do not make counting or whitespace-only
tool calls, narrate size estimates, or start a second drafting pass for size.
This policy does not skip format, acceptance, integrity or executability gates.
