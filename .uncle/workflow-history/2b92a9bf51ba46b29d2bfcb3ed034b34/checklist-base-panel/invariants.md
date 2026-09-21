## Invariants coverage packet — base pass

**Scope**: CHANGE_SPEC.md §7 Invariant table (IX-1, IX-2, IX-3) plus BASELINE_REPORT.md §5 (I-1, I-2, I-3), restricted to invariant checks only (not full AC coverage).

### Required checks

| ID | Invariant | Required check | Dependency |
|---|---|---|---|
| IX-1 | Card markup keeps sibling structure `article.card > h3(a+span.url), p, div.links(a...,span.tag)` (frontend/public/home.html:490-500) | Manual structural diff of card block against siblings (lines 462-475, 477-488) post-edit + `html.parser` pass (AC-9) | File must be post-edit; current excerpt (lines 490-500) is still pre-change baseline |
| IX-2 | `frontend/public/home.html` stays static HTML, no templating introduced | Manual read confirming no `{{`/templating syntax added anywhere in file | Whole-file read, not just card block |
| IX-3 | No fixed Claude/Codex pairing described in home.html card or AGENTIC_WORKFLOW_STRATEGY.md | grep `-i "claude builds\|codex audits\|claude/codex"` (0 matches) **plus** manual read per ADVERSARIAL_REVIEW.md AR-004 — literal grep alone is insufficient (reworded pairing claims evade it) | Both files touched post-edit |
| I-1 | `/` route serves `static/home.html` byte-for-byte via `FileResponse` (app/main.py:1785-1786) | Not re-tested per BX-6 — confirm no diff to app/main.py (`git diff --stat -- app/main.py` empty) | None — code untouched by plan |

### Coverage gap

**G-1**: CHANGE_SPEC.md §7 omits I-1 from its own invariant table (only IX-1/IX-2/IX-3 listed, carried from I-2/I-3; I-1 dropped). BASELINE_REPORT.md §5 marks I-1 "must preserve." The checklist must still assert I-1 (app/main.py unmodified) even though CHANGE_SPEC.md's own table doesn't restate it — CHANGE_PLAN.md §5 ("Components explicitly not to modify") independently confirms app/main.py is out of scope, so this is a spec omission, not a waiver.

**G-2**: All invariant checks require the **post-edit** file state. Current cached read of frontend/public/home.html:490-500 is unchanged pre-change baseline text ("brianosaurus/agentic-workflow", "Claude builds, Codex audits"). The base-pass checklist cannot mark any invariant PASS from this evidence — re-read required after implementation.

### Exclusive resources / dependencies

- No exclusive-lock resources (static file edits, no shared mutable state, no DB/service).
- Sequencing dependency: IX-1/IX-3 checks depend on implementation step 2/3 (CHANGE_PLAN.md) being complete before checklist execution.

### Acceptance provenance

No human-sign-off requirement found specific to invariants. CHANGE_SPEC.md/CHANGE_PLAN.md route IX-1/IX-2 verification through automated `html.parser` (AC-9) plus manual read; IX-3 explicitly needs manual read per AR-004 because grep cannot detect reworded pairing claims — this is a cited, non-automatable judgment (semantic paraphrase detection), not an invented gate. No separate human-approval gate is asserted or required beyond this manual-read step; CHANGE_PLAN.md §18 already declines an additional sign-off gate (no source names one). No conflict to flag.