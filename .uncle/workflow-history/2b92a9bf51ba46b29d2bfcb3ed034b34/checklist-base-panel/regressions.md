# Regressions evidence packet — base pass

## R-1: Adjacent-card byte-identity check
- Requirement: AC-8 / BX-5 — adjacent cards (frontend/public/home.html:463-489, 507+) remain byte-identical.
- Coverage gap: No automated diff-scoped test exists (BASELINE_REPORT.md sec 7: no test suite). CHANGE_PLAN.md sec 17 proposes `git diff --stat` and line-range inspection but this is not yet in an executed VERIFICATION_REPORT.md (missing).
- Required check: `git diff -- frontend/public/home.html` must show hunks only within lines 490-500; `git diff --stat` for adjacent-card byte count unchanged.
- Dependency: requires implementation to have been applied first (currently frontend/public/home.html:490-500 still shows unmodified baseline content — verified fresh read above, lines 491-498 still `brianosaurus/agentic-workflow` / old tag).
- Exclusive resource: none (read-only diff).

## R-2: Route/serving mechanism regression
- Requirement: BX-6 / I-1 — `/` route serves `static/home.html` via `FileResponse` unchanged (app/main.py:1785-1786).
- Coverage gap: `app/main.py` is explicitly out of scope (CHANGE_PLAN.md sec 5) and BASELINE_REPORT.md sec 9 notes `fastapi` is not installed in the ambient python3, so the route cannot be exercised live; only `py_compile` syntax check is available.
- Required check: `python3 -m py_compile app/main.py` (exit 0) — a compile-only proxy, not a functional regression test. This limitation must be stated explicitly in the checklist, not silently treated as full route verification.
- Dependency: none; independent of the two edited files.

## R-3: HTML well-formedness regression
- Requirement: AC-9 / IX-1, IX-2 — card markup structure (`article.card > h3(a+span.url), p, div.links(a...,span.tag)`) preserved; no templating introduced.
- Coverage gap: `html.parser` is lenient (BASELINE_REPORT.md sec 9 note) — it does not validate nesting/attributes, so a structurally malformed but tag-balanced edit could pass.
- Required check: run the documented `html.parser` command post-change AND a manual structural comparison of the card's DOM shape against sibling cards (lines 462-489) to catch what the lenient parser would miss.
- Exclusive resource: none.

## R-4: Build-artifact drift (static/home.html)
- Coverage gap: BASELINE_REPORT.md sec 2 notes `static/` (build output of `frontend/public/home.html`) is not checked in / does not exist in this worktree, and `npm run build` was not run (no `node_modules`, network-dependent install). This is out of scope per BASELINE_REPORT but means no regression check verifies the actual served artifact, only the source file.
- Required check: none executable in this environment; checklist should note this as an accepted gap (source-only verification), not silently imply the served page was checked.

## R-5: Green-check regression-gate ambiguity carries into base pass
- Evidence: `.uncle/workflow/green-check.commands` cmd3/cmd4 grep for the exact strings the change must remove; CHANGE_PLAN.md line 8 states AR-001 "Reclassified as baseline-diagnostic, not post-change pass/fail," but this reclassification is the plan author's own disposition, not sourced from CHANGE_SPEC.md or CHANGE_REQUEST.md.
- Risk: if the checklist/driver still executes green-check groups `1 2` / `3 4` as pass/fail gates post-change without the reclassification being reflected in `.uncle/workflow/green-check.commands` or `.groups` itself (both files unchanged, still framed as plain grep-count assertions), a correct fix (which flips cmd3/cmd4 counts to 0, i.e., success per AC-1/AC-3, not failure) could be mis-scored depending on how "baseline-diagnostic" is operationalized.
- Required check: checklist must explicitly state expected post-change values for cmd3 (`grep -c "unclehq/stagegate\|brianosaurus/agentic-workflow"` → expect 0) and cmd4 (`grep -c "Claude builds, Codex audits"` → expect 0), since these are legitimate post-change regression assertions (absence of banned strings), not stale probes to be discarded.

## Provenance note
No human-sign-off requirement identified in this lens beyond CHANGE_PLAN.md's existing statement (sec "Manual-verification strategy", not shown in excerpt but referenced) that no separate reviewer is named. Regression checks here (R-1 through R-5) are all automatable via grep/diff/parse; AC-2/AC-6 wording-quality judgments are out of this lens's scope (belongs to a content/copy lens, not regressions).