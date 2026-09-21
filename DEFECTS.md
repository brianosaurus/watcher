# Defects

## D-1
- Severity: Major
- Reproduction/evidence: IMPLEMENTATION_NOTES.md:7,37 cite the AC-7 README fetch by section heading name only ("intro tagline", "Why Uncle?" bullet list, "The change is the unit of trust") and quote no fetched text. MC-13 (this stage) found this insufficient to verify the citation independent of a fresh fetch.
- Affected requirement/check: AC-7, MC-7, MC-13, MC-12
- Current status: OPEN. Note: MC-7's own fresh fetch (`gh api repos/unclehq/uncle`, `.../readme`) independently confirms home.html:492-497 body copy matches uncle's actual README/description — the underlying card content satisfies AC-7. The defect is the implementer's documentation trail, not the delivered copy.
- Owner/next action: implementer — revise IMPLEMENTATION_NOTES.md to quote the actual fetched README/description text used to derive the copy.
- Disposition: does not block accepting the home.html change itself (content independently verified); blocks accepting IMPLEMENTATION_NOTES.md's evidentiary trail as sufficient on its own.

## D-2
- Severity: Minor
- Reproduction/evidence: CHANGE_TEST_REPORT.md:27-29 §Full test suite reads "DRIVER PENDING" rather than a resolved statement (e.g. "N/A, no test suite exists").
- Affected requirement/check: MC-14
- Current status: OPEN
- Owner/next action: implementer — replace the placeholder with a resolved statement consistent with the confirmed absence of any test runner in the repo.
- Disposition: documentation-only; does not affect delivered behavior or any acceptance criterion.
