## Green check

Commands read from `BASELINE_REPORT.md` and run by the driver, with no
agent in the path. Full output: `.uncle/workflow/logs/green-check.log`.

| Result | Command |
|---|---|
| PASS | `python3 -m py_compile app/main.py` |
| PASS | `python3 -c "import html.parser, pathlib; p = html.parser.HTMLParser(); p.feed(pathlib.Path('frontend/public/home.html').read_text()); print('parsed ok')"` |
| REGRESSION | `grep -c "unclehq/stagegate\|brianosaurus/agentic-workflow" frontend/public/home.html` |
| REGRESSION | `grep -c "Claude builds, Codex audits" AGENTIC_WORKFLOW_STRATEGY.md frontend/public/home.html` |

**2 command(s) regressed**: they passed before this
change and fail now.
