# Change test report

## Command results

| Command | Status | Meaningful output | Requirements |
|---|---|---|---|
| python3 -c "import ast; ast.parse(open('app/main.py').read())" | PASS | parsed | AC-1, AC-4 |
| bash -n deploy/bootstrap-nginx.sh | PASS | no syntax errors | AC-1 |
| python3 -I replica of root() Host normalization over 10 table cases (unclehq.org, UNCLEHQ.ORG:8080, www, trailing dot, empty, [::1], :80:80, evil.com, brian.biz, unclehq.org..) | PASS | all 10 map to expected page; no exceptions. Replica, not the real app (fastapi not installed). | AC-1, AC-4 |
| grep -F checks on frontend/public/unclehq/index.html (title, tagline, first project, GitHub URL, install snippet, 'Created by Brian Woods', href="https://brian.biz/") | PASS | all literals present | AC-2, AC-3 |
| grep return 301 / $host in deploy/nginx-unclehq.org.conf | PASS | 2 redirects, both literal https://unclehq.org$request_uri; $host only in proxy_set_header Host | AC-6 |
| headless Chrome, page in 375px iframe, read scrollWidth vs clientWidth | PASS | SW=360 CW=360 (no horizontal scroll); logo-absent case only | AC-5 |
| git diff --stat -- frontend/public/home.html deploy/nginx-brian.biz.conf | PASS | empty (unchanged) | AC-4 |
| FastAPI TestClient Host/HEAD/blog/api/static regression | NOT RUN | fastapi/httpx not installed locally | AC-1, AC-4 |
| nginx -t deploy/nginx-unclehq.org.conf | NOT RUN | nginx not installed; UNVERIFIED until deploy | AC-1, AC-6 |
| full test suite | DRIVER PENDING | driver runs baseline commands after this stage | None stated |
| formatting/lint/typecheck/frontend build/migration/rollback/performance | N/A | no such tooling configured for this change; no migration or build step changed | None stated |
| live curl LV-1..LV-3, phone-width browser LV-4 | BLOCKED | requires owner DNS and cert on the live host | AC-1, AC-6 |

## Coverage gaps

- TestClient byte-equality of / for brian.biz and baseline comparison of HEAD /, /blog, /api, /static not executed
- nginx -t unverified
- Live HTTPS/redirect checks and human visual/copy review not performed
- 375px check run without logo only (no logo committed)

## Next action

Install fastapi/httpx and run the TestClient Host table; run nginx -t and LV-1..LV-4 at deploy after DNS.
