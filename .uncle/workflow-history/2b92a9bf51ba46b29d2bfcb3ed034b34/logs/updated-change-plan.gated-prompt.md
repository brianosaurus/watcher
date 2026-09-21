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

Read:

- CHANGE_REQUEST.md
- CHANGE_PLAN.md
- ADVERSARIAL_REVIEW.md
- CHANGE_SPEC.md

Both CHANGE_PLAN.md and ADVERSARIAL_REVIEW.md have just passed a human gate and
may have been edited during that review. Read both from disk in full.

CHANGE_SPEC.md is for traceability only; consult its behavior and invariant IDs
as needed. Read CHANGE_REQUEST.md for source issue identity. You do not need
BASELINE_REPORT.md unless a specific finding requires evidence absent from
the plan and spec.

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

Revise CHANGE_PLAN.md in place. Do not create a second plan document.

Edit sections affected by review findings or by the final executability and
consistency checks above. Preserve other sections; do not reword or restate
unaffected content.
CHANGE_PLAN.md is the sole plan input to every later stage, so what you leave
behind is what implementation executes.

Insert directly below the title a disposition for every adversarial finding:

| Finding | Disposition | Reason | Exact plan change |
|---|---|---|---|

Allowed dispositions:

- Accepted
- Partially accepted
- Rejected
- Deferred

The `Exact plan change` cell names the section you edited, or `none` for a
rejected or deferred finding. The disposition table covers every finding. It is
never omitted and never abbreviated.

Append these sections:

1. Frozen change scope
2. Files expected to change
3. Files that must not change
4. Expected behavioral differences
5. Expected unchanged behavior
6. Exact acceptance criteria
7. Pre-implementation checks
8. Post-implementation checks
9. First features to cut if time expires
10. Conditions that require stopping implementation

Do not implement code.

## Output economy

Length is a cost. The revised CHANGE_PLAN.md is read by five later stages and
re-sent on every turn of each of them.

- Use the appended stage budget and enforcement mode; no separate word limit.
  Draft concise disposition rows and sections without dropping obligations.
- Editing a section means changing the lines the review invalidated. It does
  not mean rewriting the section from scratch.
- Do not summarize what you changed at the end. The disposition table is that
  record.
- Omit any appended section with no substantive content, and list it under the
  disposition table as `Omitted sections: <name> (<reason>)`, or write
  `Omitted sections: none`.
- Frozen change scope, files expected to change, files that must not change,
  and exact acceptance criteria are never omitted. Implementation is bounded
  by them.
- Never omit a section to avoid resolving something. If a section applies but
  you cannot complete it, keep it and mark it UNRESOLVED with the reason.

Save CHANGE_PLAN.md and stop.

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

Construct the final plan directly; do not write an expanded draft and then
compress it. Use the supplied input index to locate the original plan and each
finding. Read missing normative content before revising; excerpts are not a
replacement for complete obligations.

1. Preserve the required heading skeleton and inventory the existing IDs,
   acceptance rows, restrictions, steps, commands and protected paths. Resolve
   each finding against that inventory before producing the document.
2. Give each obligation one canonical location in this plan. Other sections
   cite its stable ID instead of repeating its wording. Keep the obligation's
   observable assertion, threshold, failure behavior and evidence requirement
   at that location; never make downstream readers consult a superseded plan.
3. Write one disposition row per finding: ID, disposition, concise reason,
   affected section/row. Do not copy the finding or repeat the disposition in
   a closing summary. Keep required headings with a short None where allowed.
4. Draft tables densely from the start: one complete row per behavior,
   invariant, test, restriction or step. Preserve every required field and
   exact literal. Do not merge distinct IDs, abbreviate away meaning, or trim
   protected table cells later just to hit a byte target.
5. Define exact commands and protected paths only in their executable fenced
   blocks. Testing and implementation sections refer to command positions and
   check IDs. Check that all required helpers, fixtures and lockfiles appear in
   the protected block; do not maintain a second conflicting path list.
6. Before the single final write/response, reconcile dispositions, traceability,
   steps and commands once. Correct actual omissions or contradictions; do not
   narrate repeated section-by-section compliance checks. No preamble, work
   diary, file-name-only answer or closing recap. Return the complete plan.

The budget is a drafting guide, not evidence that mandatory content will fit.
Do not estimate bytes repeatedly in prose or request unavailable shell tools
just to count them. The driver measures the result. With advisory enforcement,
do no size-only compaction passes after the complete draft. With enforced
budgets, use the existing preservation validator and at most two passes total;
if mandatory content cannot fit, retain it for the driver's budget resolution.
This does not waive format, completeness, acceptance or executability checks.

## Specialist plan-review packets

Read available packets in `.uncle/workflow/updated-plan-panel`, verify them, and write the sole canonical revised plan.

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
Changes since this stage last prepared inputs: none
Independent reviewers must challenge conclusions even when input hashes are unchanged.

CHANGE_SPEC.md: {"path": "/Users/brianwoods/src/watcher-issue-1/CHANGE_SPEC.md", "sha256": "ad141feae630d3d6a12adb652a59390077e544f979281d49a3ba45a3429d7290", "bytes": 6963}
1: # Change specification
5: ## 1. Change type
10: ## 2. Problem statement
16: ## 3. Current behavior
22: ## 4. Desired behavior
29: ## 5. Acceptance criteria
33: | AC-1 | Card heading link, URL label, and `Code` link (frontend/public/home.html:491,497) all target `https://github.com/unclehq/uncle` | grep for `unclehq/uncle` count = 3 in the card block; grep for `brianosaurus/agentic-workflow` and `unclehq/sta
34: | AC-2 | Body copy (2-4 sentences) states: terminal-native; issue/requirements in, verified PR out; works with existing coding agents (not a fixed pairing); independent review; human approval gates; cryptographically pinned plans/artifacts | Manual r
35: | AC-3 | No mention of "Claude" and "Codex" as a fixed pairing anywhere in the card or in AGENTIC_WORKFLOW_STRATEGY.md | grep `-i "claude builds\|codex audits\|claude/codex"` across both files returns 0 matches |
36: | AC-4 | `unclehq/stagegate` does not appear anywhere in the repo after the change (already true at baseline — must remain true) | grep `-r "stagegate"` repo-wide (excluding `.git`) returns 0 matches, or, if uncle's own repo shows stagegate as a dist
37: | AC-5 | `tag` line (frontend/public/home.html:498) reflects uncle's actual scope, not "LLM agents · pipeline tooling · open source" verbatim unless still accurate | grep confirms line no longer reads exactly the old B-4 text |
38: | AC-6 | `AGENTIC_WORKFLOW_STRATEGY.md` positioning language matches uncle (agent-agnostic; no "Claude builds, Codex audits") | Manual read; AC-3 grep covers the banned phrase |
39: | AC-7 | Copy is derived from uncle's actual README/source, not rewritten from the old card's assumptions | Implementer's plan/PR notes cite what was read from `github.com/unclehq/uncle` before writing copy |
40: | AC-8 | Adjacent cards (fro

@CHANGE_PLAN.pre-review.md: {"path": "/Users/brianwoods/src/watcher-issue-1/.uncle/workflow/CHANGE_PLAN.pre-review.md", "sha256": "97acf8049fc6367d02c5eb665ca3bebc6a5e3742736befcebbbe4c26595c11fc", "bytes": 7207}
1: # Change plan
7: ## 1. Selected technical approach
12: with BASELINE_REPORT.md I-2/I-3.
14: ## 2. Alternative approaches considered
17:   rejected: no templating exists (I-3), and the CR asks for a one-time accurate rewrite, not a
18:   live sync mechanism (D-1).
20:   bring it "in line," not remove it (CHANGE_REQUEST.md line 31) (D-2).
22: ## 3. Why the selected approach is preferred
24: Smallest change that satisfies CHANGE_SPEC.md AC-1..AC-9 without introducing new tooling,
28: ## 4. Exact components to modify
33: ## 5. Components explicitly not to modify
35: - Sibling cards in `frontend/public/home.html` (lines 463-489, 507+) — CHANGE_SPEC.md BX-5, AC-8.
36: - `app/main.py` route/serving logic (BASELINE_REPORT.md I-1) — CHANGE_SPEC.md BX-6.
39: ## 6. Compatibility strategy
44: ## 12. Error and recovery behavior
48: ## 14. Rollback plan
53: ## 16. Automated-test strategy
59: ## 17. Regression-test strategy
61: Diff-scoped check: confirm no hunches outside `frontend/public/home.html:490-500` (AC-8) via
64: ## 18. Manual-verification strategy
66: - Read `AC-2`'s six required points against the drafted `<p>` copy by eye.
68:   "Claude builds, Codex audits" framing (AC-6), by eye.
70:   quality); grep confirms the banned/required phrases (AC-1, AC-3, AC-4, AC-5), a human or the
75: ## 20. Implementation sequence
77: 1. Read `https://github.com/unclehq/uncle` README and top-level source to ground the rewrite (CHANGE_SPEC.md AC-7). No repo files written. Owns: none — Depends on: none
78: 2. Rewrite `frontend/public/home.html:490-500`: update `href` on the heading `<a>` and the `Code` `<a>` to `https://github.com/unclehq/uncle`, update `<span class="url">` text to `github.com/unclehq/uncle`, rewrite the `<p>` body per AC-2, rewrite `<
80: 4. Run verification commands (se

ADVERSARIAL_REVIEW.md: {"path": "/Users/brianwoods/src/watcher-issue-1/ADVERSARIAL_REVIEW.md", "sha256": "6d2dc7301b361e437c06655ae9997617a8c49946fed8b544011bcfbccb36cfa1", "bytes": 4304}
1: ## AR-001: Green-check gate greps for the exact strings this change must delete
4: - Failure: green-check cmd3 `grep -c "unclehq/stagegate\|brianosaurus/agentic-workflow" frontend/public/home.html` and cmd4 `grep -c "Claude builds, Codex audits" AGENTIC_WORKFLOW_STRATEGY.md frontend/public/home.html` currently match (exit 0, counts
5: - Fix: plan must state that green-check commands 3-4 are baseline-diagnostic (pre-change) probes, not pass/fail assertions the driver enforces post-change, or the driver config must be updated/exempted for this stage. Do not weaken AC-1/AC-3 to keep 
6: - Verify: run `.uncle/workflow/green-check.commands` cmd3 and cmd4 against the post-edit files and confirm the driver's runner does not treat their nonzero exit as a build failure.
8: ## AR-002: AC-7's network-fetch prerequisite has no fallback path
10: - References: CHANGE_SPEC.md AC-7, section 16 UNRESOLVED item; CHANGE_PLAN.md step 1
11: - Failure: step 1 requires fetching `github.com/unclehq/uncle` README before any file edit and step 2 depends on step 1. BASELINE_REPORT.md section 9 notes no network access was exercised at baseline and fastapi itself isn't installed in the ambient 
15: ## AR-003: AC-5 tag-line check accepts a cosmetic edit as compliant
17: - References: CHANGE_SPEC.md AC-5; CHANGE_PLAN.md Traceability row AC-5
18: - Failure: verification is "grep confirms line no longer reads exactly the old B-4 text." A one-character change (e.g., adding a space) satisfies the grep while leaving the tag inaccurate, so incorrect behavior (tag still misdescribes uncle) can pass
22: ## AR-004: AC-3 phrase grep can miss a reworded fixed-pairing claim
24: - References: CHANGE_SPEC.md AC-3, IX-3; CHANGE_PLAN.md Verification commands line 3
25: - Failure: grep targets literal phrases `cla

package.json: {"status": "missing or unreadable"}


pyproject.toml: {"status": "missing or unreadable"}


requirements.txt: {"path": "/Users/brianwoods/src/watcher-issue-1/requirements.txt", "sha256": "be5277eb495d005d6613b3431c366773f902bc8acf8c466692bbb72720c54188", "bytes": 57}
fastapi==0.115.4
uvicorn[standard]==0.32.0
psutil==6.1.0


package-lock.json: {"status": "missing or unreadable"}


@green-check.commands: {"path": "/Users/brianwoods/src/watcher-issue-1/.uncle/workflow/green-check.commands", "sha256": "e867ab784d5b1e37c61b84f1de395a9c90cca52a675786ade939c4c79a5a16ef", "bytes": 366}
python3 -m py_compile app/main.py
python3 -c "import html.parser, pathlib; p = html.parser.HTMLParser(); p.feed(pathlib.Path('frontend/public/home.html').read_text()); print('parsed ok')"
grep -c "unclehq/stagegate\|brianosaurus/agentic-workflow" frontend/public/home.html
grep -c "Claude builds, Codex audits" AGENTIC_WORKFLOW_STRATEGY.md frontend/public/home.html


@green-check.groups: {"path": "/Users/brianwoods/src/watcher-issue-1/.uncle/workflow/green-check.groups", "sha256": "871d6e7f463a42c5573203c50db6e52da506d5395af73e09237410dec5eff856", "bytes": 8}
1 2
3 4

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


# Compact output budgets

Budget enforcement is disabled: byte and line limits are advisory. Complete required content takes precedence over size.
- CHANGE_PLAN.md: at most 10299 UTF-8 bytes and 309 lines. Draft toward 7724 bytes and 231 lines to leave revision room.

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

## Plan feasibility (part of this review, not a separate stage)
Check the selected implementation runner, adapter, model/session behavior and
permissions against the plan. Inspect current configuration and adapter code;
use version-matched documentation or non-destructive probes where necessary.
Do not treat an adapter comment or proposed command as evidence of support.
Identify restrictions that make acceptance criteria impossible and distinguish
user/platform constraints from design choices that can be revised in scope.
Preserve every acceptance criterion and adversarial finding, including baseline
and protected-test requirements. Identify concrete corrections for coding blockers.
Separate missing live-verification prerequisites from blockers to writing code.
Put genuine unresolved scope or authority choices in this review for the existing
human plan gate. Never broaden permissions or silently waive a requirement.
Reviewers: include these findings in ADVERSARIAL_REVIEW.md's existing finding
format. Plan revisers: address them in the revised plan and identify anything
still unresolved for approval. Do not produce a separate assessment.json or
request a separate executability approval.
