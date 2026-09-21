# Build timing

Run: `28007c95db494a7f9a94e5f21a9c63e0`

Elapsed wall time: 408.018s

Process sampling interval: 0.5s; sampling errors: 0.

Token and cost coverage shows known records/records in each row; partial sums are not complete totals. Unknown prices or usage remain unavailable.
Interval token attribution is shared usage reported while the interval was active; it is not an exclusive charge for a tool/check and is never prorated from duration.
Times overlap across stages, subprocesses, and parallel work; do not add categories together.
Sampled process spans are approximate observed lifetimes. Short processes may be missed; CPU is unavailable on Windows.
Checklist times require explicit timer commands; missing timers mean unavailable, not zero or passed. Tool times are observed event intervals, not isolated CPU time.
Model usage spans are runner-reported API continuations, commonly one continuation after each tool result. They are not independent user turns. Cache-read totals sum the reused conversation prefix across continuations, not unique bytes reread from disk.
Runner event gaps include any work or wait between received events; they do not prove API latency or model reasoning time. The 20 largest gaps per attempt are retained.
Unfinished processes have no completion event; their displayed span ends at report time or run termination, not a confirmed process exit.
Stage durations include waiting for people and tools. Model, approval, and check rows below include only this invocation.

## Stage context size

Context is input tokens in an individual model request, including cached input; it is not cumulative stage usage or the model context-window limit. Peak and latest are observed values; unavailable means the runner supplied no request-level context measurement.

| Stage | Latest context tokens | Peak context tokens |
|---|---:|---:|
| ADVERSARIAL_REVIEW | Unavailable | Unavailable |
| ANALYZE | Unavailable | Unavailable |
| IMPLEMENT | Unavailable | Unavailable |
| UPDATED_PLAN | Unavailable | Unavailable |
| adversarial-review | 59275 | 59275 |
| adversarial-review-worker-regression | 44707 | 44707 |
| adversarial-review-worker-requirements | 42636 | 42636 |
| adversarial-review-worker-security | 42367 | 42367 |
| adversarial-review-worker-testability | 42368 | 42368 |
| change-plan | 67962 | 67962 |
| implementation | 102456 | 102456 |
| manual-checklist-review-worker-base-coverage | 74989 | 74989 |
| manual-checklist-review-worker-base-invariants | 79325 | 79325 |
| manual-checklist-review-worker-base-regressions | 75923 | 75923 |
| manual-checklist-review-worker-base-resources | 74478 | 74478 |
| updated-change-plan | 62733 | 62733 |
| updated-change-plan-review-worker-dispositions | 59162 | 59162 |
| updated-change-plan-review-worker-ownership | 58336 | 58336 |
| updated-change-plan-review-worker-scope | 58381 | 58381 |
| updated-change-plan-review-worker-verification | 62880 | 62880 |

## Workflow Stage

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| ANALYZE |  | 1 | 132.737 | Unavailable | 26 | 12510 | 664801 | 67960 | 745297 | 1/1 | 0.529952 | Unavailable | 0/1 |
| IMPLEMENT |  | 1 | 109.547 | Unavailable | 56 | 16656 | 1.89453e+06 | 168410 | 2.07965e+06 | 1/1 | 2.643917 | Unavailable | 0/1 |
| ADVERSARIAL_REVIEW |  | 1 | 91.242 | Unavailable | 16 | 9506 | 238236 | 127268 | 375026 | 1/1 | 0.651811 | Unavailable | 0/1 |
| UPDATED_PLAN |  | 1 | 72.525 | Unavailable | 16 | 11240 | 373580 | 103521 | 488357 | 1/1 | 1.021892 | Unavailable | 0/1 |
| WAIT_UPDATED_PLAN_APPROVAL |  | 1 | 0.364 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| STARTUP |  | 1 | 0.332 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| VALIDATE_ADVERSARIAL_REVIEW |  | 1 | 0.286 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| WAIT_ANALYSIS_APPROVAL |  | 1 | 0.244 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| WAIT_PLAN_APPROVAL |  | 1 | 0.235 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| PLAN |  | 1 | 0.218 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| VALIDATE_UPDATED_PLAN |  | 1 | 0.203 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| DERIVE_BRIEF |  | 1 | 0.085 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |

## Agent

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| change-plan | ANALYZE | 1 | 132.000 | Unavailable | 26 | 12510 | 664801 | 67960 | 745297 | 1/1 | 0.529952 | Unavailable | 0/1 |
| implementation | IMPLEMENT | 2 | 106.000 | Unavailable | 48 | 11245 | 1.65578e+06 | 102454 | 1.76953e+06 | 2/2 | 1.486557 | Unavailable | 0/2 |
| updated-change-plan | UPDATED_PLAN | 1 | 52.000 | Unavailable | 6 | 5475 | 140556 | 36840 | 182877 | 1/1 | 0.230233 | Unavailable | 0/1 |

## Reviewer

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| adversarial-review | ADVERSARIAL_REVIEW | 1 | 73.000 | Unavailable | 4 | 6346 | 69255 | 38458 | 114063 | 1/1 | 0.231151 | Unavailable | 0/1 |
| updated-change-plan-review-worker-ownership | UPDATED_PLAN | 1 | 19.000 | Unavailable | 2 | 1375 | 42366 | 15968 | 59711 | 1/1 | 0.181220 | Unavailable | 0/1 |
| updated-change-plan-review-worker-verification | UPDATED_PLAN | 1 | 19.000 | Unavailable | 4 | 1553 | 105659 | 18173 | 125389 | 1/1 | 0.237551 | Unavailable | 0/1 |
| updated-change-plan-review-worker-dispositions | UPDATED_PLAN | 1 | 18.000 | Unavailable | 2 | 1750 | 42634 | 16526 | 60912 | 1/1 | 0.193898 | Unavailable | 0/1 |
| adversarial-review-worker-regression | ADVERSARIAL_REVIEW | 1 | 18.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| manual-checklist-review-worker-base-invariants | IMPLEMENT | 1 | 18.000 | Unavailable | 2 | 1279 | 62878 | 16445 | 80604 | 1/1 | 0.328701 | Unavailable | 0/1 |
| manual-checklist-review-worker-base-regressions | IMPLEMENT | 1 | 17.000 | Unavailable | 2 | 1703 | 59160 | 16761 | 77626 | 1/1 | 0.289808 | Unavailable | 0/1 |
| manual-checklist-review-worker-base-coverage | IMPLEMENT | 1 | 17.000 | Unavailable | 2 | 1354 | 58334 | 16653 | 76343 | 1/1 | 0.273043 | Unavailable | 0/1 |
| updated-change-plan-review-worker-scope | UPDATED_PLAN | 1 | 15.000 | Unavailable | 2 | 1087 | 42365 | 16014 | 59468 | 1/1 | 0.178990 | Unavailable | 0/1 |
| manual-checklist-review-worker-base-resources | IMPLEMENT | 1 | 14.000 | Unavailable | 2 | 1075 | 58379 | 16097 | 75553 | 1/1 | 0.265808 | Unavailable | 0/1 |
| adversarial-review-worker-requirements | ADVERSARIAL_REVIEW | 1 | 11.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| adversarial-review-worker-security | ADVERSARIAL_REVIEW | 1 | 9.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| adversarial-review-worker-testability | ADVERSARIAL_REVIEW | 1 | 8.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |

## Model API Continuation

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| change-plan | change-plan | 14 | 131.921 | Unavailable | 26 | 12510 | 664801 | 67960 | 745297 | 14/14 | 0.529952 | Unavailable | 0/14 |
| implementation | implementation | 26 | 106.150 | Unavailable | 48 | 11245 | 1.65578e+06 | 102454 | 1.76953e+06 | 26/26 | 1.486557 | Unavailable | 0/26 |
| adversarial-review | adversarial-review | 3 | 72.032 | Unavailable | 4 | 6346 | 69255 | 38458 | 114063 | 3/3 | 0.231151 | Unavailable | 0/3 |
| updated-change-plan | updated-change-plan | 4 | 51.161 | Unavailable | 6 | 5475 | 140556 | 36840 | 182877 | 4/4 | 0.230233 | Unavailable | 0/4 |
| updated-change-plan-review-worker-ownership | updated-change-plan-review-worker-ownership | 2 | 18.902 | Unavailable | 2 | 1375 | 42366 | 15968 | 59711 | 2/2 | 0.181220 | Unavailable | 0/2 |
| updated-change-plan-review-worker-verification | updated-change-plan-review-worker-verification | 3 | 18.663 | Unavailable | 4 | 1553 | 105659 | 18173 | 125389 | 3/3 | 0.237551 | Unavailable | 0/3 |
| updated-change-plan-review-worker-dispositions | updated-change-plan-review-worker-dispositions | 2 | 17.914 | Unavailable | 2 | 1750 | 42634 | 16526 | 60912 | 2/2 | 0.193898 | Unavailable | 0/2 |
| manual-checklist-review-worker-base-invariants | manual-checklist-review-worker-base-invariants | 2 | 17.869 | Unavailable | 2 | 1279 | 62878 | 16445 | 80604 | 2/2 | 0.328701 | Unavailable | 0/2 |
| manual-checklist-review-worker-base-coverage | manual-checklist-review-worker-base-coverage | 2 | 17.681 | Unavailable | 2 | 1354 | 58334 | 16653 | 76343 | 2/2 | 0.273043 | Unavailable | 0/2 |
| manual-checklist-review-worker-base-regressions | manual-checklist-review-worker-base-regressions | 2 | 17.528 | Unavailable | 2 | 1703 | 59160 | 16761 | 77626 | 2/2 | 0.289808 | Unavailable | 0/2 |
| adversarial-review-worker-regression | adversarial-review-worker-regression | 4 | 17.505 | Unavailable | 6 | 1131 | 106536 | 23890 | 131563 | 4/4 | 0.128189 | Unavailable | 0/4 |
| updated-change-plan-review-worker-scope | updated-change-plan-review-worker-scope | 2 | 14.749 | Unavailable | 2 | 1087 | 42365 | 16014 | 59468 | 2/2 | 0.178990 | Unavailable | 0/2 |
| manual-checklist-review-worker-base-resources | manual-checklist-review-worker-base-resources | 2 | 13.989 | Unavailable | 2 | 1075 | 58379 | 16097 | 75553 | 2/2 | 0.265808 | Unavailable | 0/2 |
| adversarial-review-worker-requirements | adversarial-review-worker-requirements | 2 | 11.155 | Unavailable | 2 | 1032 | 20815 | 21819 | 43668 | 2/2 | 0.101763 | Unavailable | 0/2 |
| adversarial-review-worker-security | adversarial-review-worker-security | 2 | 8.439 | Unavailable | 2 | 522 | 20815 | 21550 | 42889 | 2/2 | 0.095587 | Unavailable | 0/2 |
| adversarial-review-worker-testability | adversarial-review-worker-testability | 2 | 8.153 | Unavailable | 2 | 475 | 20815 | 21551 | 42843 | 2/2 | 0.095121 | Unavailable | 0/2 |

## Approval

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| BASELINE_REPORT CHANGE_SPEC | WAIT_ANALYSIS_APPROVAL | 1 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| CHANGE_PLAN | WAIT_UPDATED_PLAN_APPROVAL | 1 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| CHANGE_PLAN ADVERSARIAL_REVIEW | WAIT_PLAN_APPROVAL | 1 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |

## Check

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| python3 -c "import html.parser, pathlib; p = html.parser.HTMLParser(); p.feed(pathlib.Path('frontend/public/home.html').read_text()); print('parsed ok')" | IMPLEMENT | 1 | 0.079 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| python3 -m py_compile app/main.py | IMPLEMENT | 1 | 0.079 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| python3 -m py_compile app/main.py | PLAN | 1 | 0.077 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| python3 -c "import html.parser, pathlib; p = html.parser.HTMLParser(); p.feed(pathlib.Path('frontend/public/home.html').read_text()); print('parsed ok')" | PLAN | 1 | 0.076 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| grep -c "Claude builds, Codex audits" AGENTIC_WORKFLOW_STRATEGY.md frontend/public/home.html | IMPLEMENT | 1 | 0.042 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| grep -c "unclehq/stagegate\&#124;brianosaurus/agentic-workflow" frontend/public/home.html | IMPLEMENT | 1 | 0.040 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| grep -c "Claude builds, Codex audits" AGENTIC_WORKFLOW_STRATEGY.md frontend/public/home.html | PLAN | 1 | 0.040 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| grep -c "unclehq/stagegate\&#124;brianosaurus/agentic-workflow" frontend/public/home.html | PLAN | 1 | 0.038 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |

## Integrity

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|

## Checklist Item

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|

## Checklist Unfinished

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|

## Tool Call

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| Bash | implementation | 12 | 1.981 | Unavailable | 2 | 20 | 58560 | 968 | 59550 | 1/12 | Unavailable | Unavailable | 0/12 |
| Bash | change-plan | 9 | 0.938 | Unavailable | 2 | 20 | 50078 | 360 | 50460 | 1/9 | Unavailable | Unavailable | 0/9 |
| Read | implementation | 2 | 0.068 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/2 | Unavailable | Unavailable | 0/2 |
| Read | adversarial-review | 3 | 0.035 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/3 | Unavailable | Unavailable | 0/3 |
| Bash | adversarial-review-worker-regression | 1 | 0.027 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| Edit | implementation | 4 | 0.025 | Unavailable | 2 | 16 | 99897 | 590 | 100505 | 1/4 | Unavailable | Unavailable | 0/4 |
| Grep | implementation | 2 | 0.022 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/2 | Unavailable | Unavailable | 0/2 |
| Read | change-plan | 4 | 0.021 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/4 | Unavailable | Unavailable | 0/4 |
| Write | change-plan | 3 | 0.015 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/3 | Unavailable | Unavailable | 0/3 |
| Read | updated-change-plan | 1 | 0.014 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| Write | updated-change-plan | 1 | 0.013 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| Write | implementation | 2 | 0.013 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/2 | Unavailable | Unavailable | 0/2 |
| Read | updated-change-plan-review-worker-verification | 1 | 0.009 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| Read | adversarial-review-worker-regression | 1 | 0.008 | Unavailable | 2 | 20 | 42633 | 455 | 43110 | 1/1 | Unavailable | Unavailable | 0/1 |
| ToolSearch | implementation | 1 | 0.003 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |

## Tool Unpaired

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|

## Tool Unfinished

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|

## Runner First Event

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| adversarial-review-worker-security | adversarial-review-worker-security | 1 | 0.855 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| updated-change-plan | updated-change-plan | 1 | 0.850 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| adversarial-review-worker-requirements | adversarial-review-worker-requirements | 1 | 0.800 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| adversarial-review-worker-regression | adversarial-review-worker-regression | 1 | 0.735 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| implementation | implementation | 2 | 0.684 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/2 | Unavailable | Unavailable | 0/2 |
| adversarial-review-worker-testability | adversarial-review-worker-testability | 1 | 0.631 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| adversarial-review | adversarial-review | 1 | 0.627 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| change-plan | change-plan | 1 | 0.625 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| updated-change-plan-review-worker-dispositions | updated-change-plan-review-worker-dispositions | 1 | 0.069 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| updated-change-plan-review-worker-scope | updated-change-plan-review-worker-scope | 1 | 0.066 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| updated-change-plan-review-worker-ownership | updated-change-plan-review-worker-ownership | 1 | 0.059 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| updated-change-plan-review-worker-verification | updated-change-plan-review-worker-verification | 1 | 0.053 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| manual-checklist-review-worker-base-coverage | manual-checklist-review-worker-base-coverage | 1 | 0.048 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| manual-checklist-review-worker-base-resources | manual-checklist-review-worker-base-resources | 1 | 0.046 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| manual-checklist-review-worker-base-invariants | manual-checklist-review-worker-base-invariants | 1 | 0.044 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| manual-checklist-review-worker-base-regressions | manual-checklist-review-worker-base-regressions | 1 | 0.043 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |

## Runner First Response

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| adversarial-review | adversarial-review | 1 | 72.028 | Unavailable | 4 | 4 | 69255 | 38458 | 107721 | 1/1 | Unavailable | Unavailable | 0/1 |
| implementation | implementation | 2 | 37.265 | Unavailable | 16 | 65 | 435397 | 89341 | 524819 | 2/2 | Unavailable | Unavailable | 0/2 |
| updated-change-plan-review-worker-ownership | updated-change-plan-review-worker-ownership | 1 | 18.897 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| updated-change-plan-review-worker-dispositions | updated-change-plan-review-worker-dispositions | 1 | 17.896 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| manual-checklist-review-worker-base-invariants | manual-checklist-review-worker-base-invariants | 1 | 17.847 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| change-plan | change-plan | 1 | 17.693 | Unavailable | 8 | 26 | 148346 | 52766 | 201146 | 1/1 | Unavailable | Unavailable | 0/1 |
| manual-checklist-review-worker-base-coverage | manual-checklist-review-worker-base-coverage | 1 | 17.661 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| manual-checklist-review-worker-base-regressions | manual-checklist-review-worker-base-regressions | 1 | 17.506 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| adversarial-review-worker-regression | adversarial-review-worker-regression | 1 | 17.502 | Unavailable | 4 | 22 | 63448 | 22273 | 85747 | 1/1 | Unavailable | Unavailable | 0/1 |
| updated-change-plan-review-worker-scope | updated-change-plan-review-worker-scope | 1 | 14.716 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| manual-checklist-review-worker-base-resources | manual-checklist-review-worker-base-resources | 1 | 13.960 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| updated-change-plan | updated-change-plan | 1 | 11.356 | Unavailable | 2 | 3 | 25891 | 30985 | 56881 | 1/1 | Unavailable | Unavailable | 0/1 |
| adversarial-review-worker-requirements | adversarial-review-worker-requirements | 1 | 11.147 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| adversarial-review-worker-security | adversarial-review-worker-security | 1 | 8.432 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| adversarial-review-worker-testability | adversarial-review-worker-testability | 1 | 8.090 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| updated-change-plan-review-worker-verification | updated-change-plan-review-worker-verification | 1 | 2.296 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |

## Runner Event Gap

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| change-plan | change-plan | 21 | 119.614 | Unavailable | 8 | 9 | 228822 | 9138 | 237977 | 4/21 | Unavailable | Unavailable | 0/21 |
| implementation | implementation | 41 | 73.234 | Unavailable | 26 | 11163 | 1.00612e+06 | 36840 | 1.05415e+06 | 15/41 | 1.486557 | Unavailable | 0/41 |
| updated-change-plan | updated-change-plan | 17 | 50.312 | Unavailable | 6 | 5475 | 140556 | 36840 | 182877 | 4/17 | 0.230233 | Unavailable | 0/17 |
| adversarial-review | adversarial-review | 20 | 44.700 | Unavailable | 2 | 2 | 48440 | 10833 | 59277 | 1/20 | Unavailable | Unavailable | 0/20 |
| updated-change-plan-review-worker-ownership | updated-change-plan-review-worker-ownership | 7 | 18.845 | Unavailable | 2 | 1375 | 42366 | 15968 | 59711 | 2/7 | 0.181220 | Unavailable | 0/7 |
| updated-change-plan-review-worker-verification | updated-change-plan-review-worker-verification | 10 | 18.611 | Unavailable | 4 | 1553 | 105659 | 18173 | 125389 | 3/10 | 0.237551 | Unavailable | 0/10 |
| updated-change-plan-review-worker-dispositions | updated-change-plan-review-worker-dispositions | 7 | 17.846 | Unavailable | 2 | 1750 | 42634 | 16526 | 60912 | 2/7 | 0.193898 | Unavailable | 0/7 |
| manual-checklist-review-worker-base-invariants | manual-checklist-review-worker-base-invariants | 7 | 17.826 | Unavailable | 2 | 1279 | 62878 | 16445 | 80604 | 2/7 | 0.328701 | Unavailable | 0/7 |
| manual-checklist-review-worker-base-coverage | manual-checklist-review-worker-base-coverage | 7 | 17.633 | Unavailable | 2 | 1354 | 58334 | 16653 | 76343 | 2/7 | 0.273043 | Unavailable | 0/7 |
| manual-checklist-review-worker-base-regressions | manual-checklist-review-worker-base-regressions | 7 | 17.485 | Unavailable | 2 | 1703 | 59160 | 16761 | 77626 | 2/7 | 0.289808 | Unavailable | 0/7 |
| adversarial-review-worker-regression | adversarial-review-worker-regression | 16 | 16.770 | Unavailable | 6 | 1131 | 106536 | 23890 | 131563 | 4/16 | 0.128189 | Unavailable | 0/16 |
| updated-change-plan-review-worker-scope | updated-change-plan-review-worker-scope | 7 | 14.684 | Unavailable | 2 | 1087 | 42365 | 16014 | 59468 | 2/7 | 0.178990 | Unavailable | 0/7 |
| manual-checklist-review-worker-base-resources | manual-checklist-review-worker-base-resources | 7 | 13.943 | Unavailable | 2 | 1075 | 58379 | 16097 | 75553 | 2/7 | 0.265808 | Unavailable | 0/7 |
| adversarial-review-worker-requirements | adversarial-review-worker-requirements | 7 | 10.356 | Unavailable | 2 | 1032 | 20815 | 21819 | 43668 | 2/7 | 0.101763 | Unavailable | 0/7 |
| adversarial-review-worker-security | adversarial-review-worker-security | 7 | 7.585 | Unavailable | 2 | 522 | 20815 | 21550 | 42889 | 2/7 | 0.095587 | Unavailable | 0/7 |
| adversarial-review-worker-testability | adversarial-review-worker-testability | 7 | 7.522 | Unavailable | 2 | 475 | 20815 | 21551 | 42843 | 2/7 | 0.095121 | Unavailable | 0/7 |

## Runner Tail Gap

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| updated-change-plan-review-worker-ownership | updated-change-plan-review-worker-ownership | 1 | 0.001 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| updated-change-plan-review-worker-dispositions | updated-change-plan-review-worker-dispositions | 1 | 0.001 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| updated-change-plan-review-worker-scope | updated-change-plan-review-worker-scope | 1 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| adversarial-review | adversarial-review | 1 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| implementation | implementation | 2 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/2 | Unavailable | Unavailable | 0/2 |
| updated-change-plan-review-worker-verification | updated-change-plan-review-worker-verification | 1 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| manual-checklist-review-worker-base-regressions | manual-checklist-review-worker-base-regressions | 1 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| manual-checklist-review-worker-base-resources | manual-checklist-review-worker-base-resources | 1 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| manual-checklist-review-worker-base-coverage | manual-checklist-review-worker-base-coverage | 1 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| manual-checklist-review-worker-base-invariants | manual-checklist-review-worker-base-invariants | 1 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| adversarial-review-worker-testability | adversarial-review-worker-testability | 1 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| adversarial-review-worker-requirements | adversarial-review-worker-requirements | 1 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| adversarial-review-worker-security | adversarial-review-worker-security | 1 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| adversarial-review-worker-regression | adversarial-review-worker-regression | 1 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| change-plan | change-plan | 1 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| updated-change-plan | updated-change-plan | 1 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |

## Runner Observation

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| change-plan | change-plan | 1 | 131.921 | Unavailable | 26 | 44 | 664801 | 67960 | 732831 | 1/1 | Unavailable | Unavailable | 0/1 |
| implementation | implementation | 2 | 106.153 | Unavailable | 48 | 1266 | 1.65578e+06 | 102454 | 1.75955e+06 | 2/2 | 0.853518 | Unavailable | 0/2 |
| adversarial-review | adversarial-review | 1 | 72.034 | Unavailable | 4 | 6346 | 69255 | 38458 | 114063 | 1/1 | 0.231151 | Unavailable | 0/1 |
| updated-change-plan | updated-change-plan | 1 | 51.161 | Unavailable | 6 | 5475 | 140556 | 36840 | 182877 | 1/1 | 0.230233 | Unavailable | 0/1 |
| updated-change-plan-review-worker-ownership | updated-change-plan-review-worker-ownership | 1 | 18.905 | Unavailable | 2 | 1375 | 42366 | 15968 | 59711 | 1/1 | 0.181220 | Unavailable | 0/1 |
| updated-change-plan-review-worker-verification | updated-change-plan-review-worker-verification | 1 | 18.664 | Unavailable | 4 | 1553 | 105659 | 18173 | 125389 | 1/1 | 0.237551 | Unavailable | 0/1 |
| updated-change-plan-review-worker-dispositions | updated-change-plan-review-worker-dispositions | 1 | 17.915 | Unavailable | 2 | 1750 | 42634 | 16526 | 60912 | 1/1 | 0.193898 | Unavailable | 0/1 |
| manual-checklist-review-worker-base-invariants | manual-checklist-review-worker-base-invariants | 1 | 17.870 | Unavailable | 2 | 1279 | 62878 | 16445 | 80604 | 1/1 | 0.328701 | Unavailable | 0/1 |
| manual-checklist-review-worker-base-coverage | manual-checklist-review-worker-base-coverage | 1 | 17.682 | Unavailable | 2 | 1354 | 58334 | 16653 | 76343 | 1/1 | 0.273043 | Unavailable | 0/1 |
| manual-checklist-review-worker-base-regressions | manual-checklist-review-worker-base-regressions | 1 | 17.528 | Unavailable | 2 | 1703 | 59160 | 16761 | 77626 | 1/1 | 0.289808 | Unavailable | 0/1 |
| adversarial-review-worker-regression | adversarial-review-worker-regression | 1 | 17.506 | Unavailable | 6 | 1131 | 106536 | 23890 | 131563 | 1/1 | 0.128189 | Unavailable | 0/1 |
| updated-change-plan-review-worker-scope | updated-change-plan-review-worker-scope | 1 | 14.750 | Unavailable | 2 | 1087 | 42365 | 16014 | 59468 | 1/1 | 0.178990 | Unavailable | 0/1 |
| manual-checklist-review-worker-base-resources | manual-checklist-review-worker-base-resources | 1 | 13.990 | Unavailable | 2 | 1075 | 58379 | 16097 | 75553 | 1/1 | 0.265808 | Unavailable | 0/1 |
| adversarial-review-worker-requirements | adversarial-review-worker-requirements | 1 | 11.155 | Unavailable | 2 | 1032 | 20815 | 21819 | 43668 | 1/1 | 0.101763 | Unavailable | 0/1 |
| adversarial-review-worker-security | adversarial-review-worker-security | 1 | 8.439 | Unavailable | 2 | 522 | 20815 | 21550 | 42889 | 1/1 | 0.095587 | Unavailable | 0/1 |
| adversarial-review-worker-testability | adversarial-review-worker-testability | 1 | 8.153 | Unavailable | 2 | 475 | 20815 | 21551 | 42843 | 1/1 | 0.095121 | Unavailable | 0/1 |

## Read Cache

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| stage-context |  | 17 | 0.044 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/17 | Unavailable | Unavailable | 0/17 |

## Process

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| python3 | IMPLEMENT | 6 | 173.241 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/6 | Unavailable | Unavailable | 0/6 |
| python3 | ANALYZE | 1 | 131.925 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| python3 | UPDATED_PLAN | 5 | 121.420 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/5 | Unavailable | Unavailable | 0/5 |
| python3 | ADVERSARIAL_REVIEW | 5 | 117.306 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/5 | Unavailable | Unavailable | 0/5 |
| bash | IMPLEMENT | 4 | 0.232 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/4 | Unavailable | Unavailable | 0/4 |
| bash | PLAN | 4 | 0.223 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/4 | Unavailable | Unavailable | 0/4 |

## Unfinished Process

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|

## Sampled Process

| Name | State | Spans | Seconds | CPU seconds | Input | Output | Cache read | Cache write | Total tokens | Token coverage | Reported USD | Estimated USD | Cost coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| bash | IMPLEMENT | 28 | 744.218 | 0.100 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/28 | Unavailable | Unavailable | 0/28 |
| bash | ANALYZE | 5 | 657.004 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/5 | Unavailable | Unavailable | 0/5 |
| Python | IMPLEMENT | 20 | 599.486 | 0.400 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/20 | Unavailable | Unavailable | 0/20 |
| Python | ANALYZE | 4 | 525.283 | 0.350 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/4 | Unavailable | Unavailable | 0/4 |
| bash | UPDATED_PLAN | 24 | 485.263 | 0.070 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/24 | Unavailable | Unavailable | 0/24 |
| Python | ADVERSARIAL_REVIEW | 24 | 447.033 | 0.290 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/24 | Unavailable | Unavailable | 0/24 |
| Python | UPDATED_PLAN | 16 | 406.733 | 0.330 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/16 | Unavailable | Unavailable | 0/16 |
| bash | ADVERSARIAL_REVIEW | 16 | 363.609 | 0.020 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/16 | Unavailable | Unavailable | 0/16 |
| tee | IMPLEMENT | 6 | 168.936 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/6 | Unavailable | Unavailable | 0/6 |
| claude | ANALYZE | 1 | 131.734 | 3.820 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| cat | ANALYZE | 1 | 131.183 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| tee | ANALYZE | 1 | 131.183 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| jq | ANALYZE | 1 | 131.183 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| tee | UPDATED_PLAN | 5 | 118.830 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/5 | Unavailable | Unavailable | 0/5 |
| tee | ADVERSARIAL_REVIEW | 5 | 114.075 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/5 | Unavailable | Unavailable | 0/5 |
| cat | IMPLEMENT | 2 | 105.222 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/2 | Unavailable | Unavailable | 0/2 |
| jq | IMPLEMENT | 2 | 105.222 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/2 | Unavailable | Unavailable | 0/2 |
| claude | ADVERSARIAL_REVIEW | 5 | 104.808 | 4.440 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/5 | Unavailable | Unavailable | 0/5 |
| claude | IMPLEMENT | 1 | 92.679 | 3.180 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| jq | UPDATED_PLAN | 1 | 50.797 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| cat | UPDATED_PLAN | 1 | 50.797 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| claude | UPDATED_PLAN | 1 | 50.242 | 1.830 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| git | ADVERSARIAL_REVIEW | 22 | 48.004 | 0.740 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/22 | Unavailable | Unavailable | 0/22 |
| ssh | ADVERSARIAL_REVIEW | 26 | 42.566 | 0.240 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/26 | Unavailable | Unavailable | 0/26 |
| git | IMPLEMENT | 7 | 16.470 | 0.350 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/7 | Unavailable | Unavailable | 0/7 |
| git | UPDATED_PLAN | 6 | 12.854 | 0.370 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/6 | Unavailable | Unavailable | 0/6 |
| ssh | IMPLEMENT | 7 | 12.076 | 0.070 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/7 | Unavailable | Unavailable | 0/7 |
| git | ANALYZE | 5 | 11.899 | 0.310 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/5 | Unavailable | Unavailable | 0/5 |
| ssh | ANALYZE | 6 | 9.194 | 0.080 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/6 | Unavailable | Unavailable | 0/6 |
| ssh | UPDATED_PLAN | 7 | 8.957 | 0.110 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/7 | Unavailable | Unavailable | 0/7 |
| zsh | IMPLEMENT | 2 | 0.551 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/2 | Unavailable | Unavailable | 0/2 |
| (Python) | IMPLEMENT | 4 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/4 | Unavailable | Unavailable | 0/4 |
| (bash) | ANALYZE | 8 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/8 | Unavailable | Unavailable | 0/8 |
| (bash) | UPDATED_PLAN | 20 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/20 | Unavailable | Unavailable | 0/20 |
| (tee) | ANALYZE | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| (bash) | IMPLEMENT | 32 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/32 | Unavailable | Unavailable | 0/32 |
| (Python) | ADVERSARIAL_REVIEW | 3 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/3 | Unavailable | Unavailable | 0/3 |
| (Python) | UPDATED_PLAN | 5 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/5 | Unavailable | Unavailable | 0/5 |
| zsh | ANALYZE | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| bash | VALIDATE_UPDATED_PLAN | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| (tr) | IMPLEMENT | 2 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/2 | Unavailable | Unavailable | 0/2 |
| (ssh) | IMPLEMENT | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| (Python) | PLAN | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| <defunct> | ADVERSARIAL_REVIEW | 6 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/6 | Unavailable | Unavailable | 0/6 |
| sh | IMPLEMENT | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| bash | WAIT_PLAN_APPROVAL | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| (bash) | ADVERSARIAL_REVIEW | 4 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/4 | Unavailable | Unavailable | 0/4 |
| (jq) | UPDATED_PLAN | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| (cat) | ANALYZE | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| (jq) | ANALYZE | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| gh | IMPLEMENT | 2 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/2 | Unavailable | Unavailable | 0/2 |
| <defunct> | UPDATED_PLAN | 2 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/2 | Unavailable | Unavailable | 0/2 |
| (ssh) | ADVERSARIAL_REVIEW | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| (ssh) | UPDATED_PLAN | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| (cat) | ADVERSARIAL_REVIEW | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| (tee) | UPDATED_PLAN | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| (git) | ADVERSARIAL_REVIEW | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| (Python) | ANALYZE | 3 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/3 | Unavailable | Unavailable | 0/3 |
| (tr) | UPDATED_PLAN | 5 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/5 | Unavailable | Unavailable | 0/5 |
| <defunct> | ANALYZE | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| bash | PLAN | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| (Python) | VALIDATE_UPDATED_PLAN | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| head | IMPLEMENT | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| (Python) | WAIT_PLAN_APPROVAL | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| bash | STARTUP | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| (cat) | IMPLEMENT | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| (git) | IMPLEMENT | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| (git) | UPDATED_PLAN | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| base64 | IMPLEMENT | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |
| (tee) | IMPLEMENT | 1 | 0.000 | 0.000 | Unavailable | Unavailable | Unavailable | Unavailable | Unavailable | 0/1 | Unavailable | Unavailable | 0/1 |

## Read cache

Entries offered are validated context, not proof that the model skipped a tool call.

| Entries offered | Entries invalidated | Context bytes | Validation seconds |
|---:|---:|---:|---:|
| 55 | 4 | 300675 | 0.044 |

## Runner timing coverage

| Stage | Events received | First response observed | Paired tools | Unpaired ends | Missing ends |
|---|---:|---|---:|---:|---:|
| change-plan | 66 | yes | 16 | 0 | 0 |
| updated-change-plan | 18 | yes | 2 | 0 | 0 |
| updated-change-plan-review-worker-scope | 8 | yes | 0 | 0 | 0 |
| manual-checklist-review-worker-base-invariants | 8 | yes | 0 | 0 | 0 |
| adversarial-review | 57 | yes | 3 | 0 | 0 |
| implementation | 21 | yes | 4 | 0 | 0 |
| updated-change-plan-review-worker-verification | 11 | yes | 1 | 0 | 0 |
| manual-checklist-review-worker-base-resources | 8 | yes | 0 | 0 | 0 |
| updated-change-plan-review-worker-ownership | 8 | yes | 0 | 0 | 0 |
| adversarial-review-worker-requirements | 8 | yes | 0 | 0 | 0 |
| implementation | 94 | yes | 19 | 0 | 0 |
| adversarial-review-worker-testability | 8 | yes | 0 | 0 | 0 |
| manual-checklist-review-worker-base-regressions | 8 | yes | 0 | 0 | 0 |
| adversarial-review-worker-regression | 17 | yes | 2 | 0 | 0 |
| adversarial-review-worker-security | 8 | yes | 0 | 0 | 0 |
| updated-change-plan-review-worker-dispositions | 8 | yes | 0 | 0 | 0 |
| manual-checklist-review-worker-base-coverage | 8 | yes | 0 | 0 | 0 |
