# Change Plan

Issue 9

Seeded from [brianosaurus/watcher#9](https://github.com/brianosaurus/watcher/issues/9).

Omitted sections: Schema/persistence (none); Concurrency (none); Migration (none); State transitions (none); Feature flag (none, additive); Observability (nginx per-vhost logs only)

## 1. Selected technical approach

Host-based dispatch in FastAPI `root()`. Host normalization: take the single (first) Host header value; lowercase it; strip one trailing `:port` suffix; strip one trailing dot; match exactly against {unclehq.org, www.unclehq.org} -> `static/unclehq/index.html`. Any non-match, missing, empty, multi-valued, bracketed IPv6, userinfo-bearing, malformed-port or otherwise unparseable Host serves home.html and never raises an error. New nginx vhosts for unclehq.org: 80 (ACME location; apex returns 301 to https://unclehq.org$request_uri; www returns 301 directly to https://unclehq.org$request_uri, not via https www), 443 apex (proxy to 127.0.0.1:8765, Host preserved), 443 www (301 to https://unclehq.org$request_uri). Redirect targets use the literal host, never $host or $http_host; query strings are preserved via $request_uri. Static page inline-CSS in `frontend/public/unclehq/index.html`, copied by Vite to `static/unclehq/`.

## 2. Alternatives
- nginx `root` serving static directly for unclehq: bypasses app; duplicates static path config.
- Separate app/process: unnecessary.

## 3. Why selected
Smallest change; reuses existing proxy, static build and deploy tarball; Host already forwarded.

## 4. Components to modify
See change-impact table.

## 5. Not to modify

`frontend/public/home.html`, blog, `deploy/nginx-brian.biz.conf`, `/api/*`, `frontend/src`. `deploy/nginx-brian.biz-http-only.conf` may change only by adding a separate unclehq.org/www.unclehq.org server block (ACME webroot); the brian.biz server_name, cert and renewal are untouched.

## 8. Interface changes

`GET /` is now Host-dependent. Decision D1: dispatch via `Request.headers['host']` allowlist (not `X-Forwarded-Host`; nginx sets Host). Normalization: lowercase, strip one trailing `:port`, strip one trailing dot, exact match against {unclehq.org, www.unclehq.org}; anything else (missing, empty, IPv6 bracket form, userinfo, multiple values, unclehq.org.. etc.) serves home.html. Decision D2: unclehq.org keeps access to other paths (non-goal to block). GET and HEAD `/` on unclehq hosts serve the Uncle page; all other paths and methods (e.g. /blog, /static/*, /api/*, POST /) proxy unchanged to the app and behave exactly as on brian.biz. The unclehq.org vhost proxies all paths, so `/api/*` on that origin is reachable and this exposure is explicitly accepted; no origin isolation, CORS change or cookie scoping is added, and the app's existing headers apply as on brian.biz. The port-80 www.unclehq.org redirect goes straight to https://unclehq.org$request_uri (no intermediate https www hop). Decision D3: separate cert at `/etc/letsencrypt/live/unclehq.org/`. Decision D4: apex canonical, www redirects. Decision D5: logo copied to `frontend/public/unclehq/uncle.png` only if fetchable from the MIT repo. If uncle.png is not committed, the HTML contains no img tag or other reference to it and shows a text wordmark; if committed, the img tag has non-empty alt text. No onerror handlers are used. The page must pass the 375px check both with and without uncle.png. Decision D6: the Uncle page's `<title>` is exactly `Uncle HQ`; if `static/unclehq/index.html` is missing, the response is the framework's default error status (no custom handling, no fallback to home.html), and the local check asserts the title string on a 200. Decision D7: every unclehq redirect (port 80 to https, www to apex) uses the fixed literal target `https://unclehq.org$request_uri`; `$host` and `$http_host` are never used in a redirect target, so a forged Host cannot cause an open redirect.

Decision D6 (trust boundary): the app trusts the Host header because the backend binds only to 127.0.0.1:8765, so nginx vhosts are the only external path to it; the unclehq 443 apex vhost is the sole route for unclehq hosts. Bind address is verified as an assumption, not changed by this plan. A request with a spoofed Host: unclehq.org can only select the public static Uncle page, so no security boundary depends on Host.

## 10. Compatibility strategy
Default branch is home.html for every Host not in the allowlist, so brian.biz and direct IP/localhost requests are unchanged.

## 12. Error and recovery
`nginx -t` before every reload; on failure keep prior config. Missing cert blocks only the new vhost reload, so issue the cert before installing the 443 block (bootstrap ordering).

## 13/14. Rollback plan
Revert commit; on host remove `/etc/nginx/sites-enabled/unclehq.org`, `nginx -t`, reload. brian.biz vhost never edited, so it is unaffected.

## 16. Automated-test strategy

No test framework exists; do not add one. Use the verification command (syntax parse) plus an ad-hoc local check in step 5 covering AC-1/2/3/4. Prerequisite: static/unclehq/index.html must exist, either from a Vite build (frontend/public/unclehq copied to static/unclehq) or by pointing the dispatch at frontend/public/unclehq/index.html for the check. Runner: FastAPI TestClient if fastapi is installed, else uvicorn + curl with `-H Host:`. The AC-1 check asserts status 200 and that the body contains `<title>Uncle HQ</title>` for Host unclehq.org. If neither runner nor page file is available, the check did not pass: the affected ACs are recorded as FAILED/unverified, never skipped. Not committed as a suite.

- Table-driven Host cases (expected page): `unclehq.org` -> Uncle; `UNCLEHQ.ORG:8080` -> Uncle; `www.unclehq.org` -> Uncle; `unclehq.org.` -> Uncle; missing Host -> home.html; empty Host -> home.html; `[::1]` -> home.html; `unclehq.org:80:80` -> home.html; `evil.com` -> home.html; `brian.biz` -> home.html. None may return an error status.

## 17. Regression-test strategy

Brian Host and no-Host GET / compared to home.html bytes; git diff confined to the table's files. The local check also issues HEAD / and GETs /blog, an /api health path and a /static asset under Host brian.biz and under Host unclehq.org, and compares status and body to a baseline captured before the change (git stash-free: run the same requests against the base commit's app/main.py).

## 18. Manual-verification strategy
LIVE_VERIFICATION (not a coding prerequisite; requires owner DNS and host access): LV-1 `curl -sI https://unclehq.org/`; LV-2 `curl -sI https://www.unclehq.org/x`; LV-3 `curl -sI http://unclehq.org/`; LV-4 phone-width browser check. Prerequisites: DNS A/AAAA for apex and www at the brian.biz host, cert issued via bootstrap. Non-secret evidence: command output pasted to MANUAL_CHECKLIST.

## Restrictions
| R-ID | source_kind | Source | Reqs | Required property | Mechanism | Rationale | CAP | Phase | Feasibility evidence |
|---|---|---|---|---|---|---|---|---|---|
| R-1 | USER | CHANGE_REQUEST Implementation notes | S1,S2 | Route by Host | allowlist in root() | one place, no new infra | CAP-ROUTE | CODING | main.py:1783 inspected |
| R-2 | USER | CHANGE_REQUEST Ops | S6,S7 | www->apex, TLS | new nginx vhost file | mirrors existing conf | CAP-NGINX | CODING (write), LIVE_VERIFICATION (apply) | deploy/nginx-brian.biz.conf inspected |
| R-3 | USER | CHANGE_REQUEST AC4 | S2,S3 | brian.biz unchanged | do not edit home.html/blog/brian conf | preserve | CAP-NOCHANGE | CODING | git diff |
| R-4 | PLATFORM | Vite config | S4 | page reachable via static/ | place under frontend/public/unclehq | public copied verbatim | CAP-PAGE | CODING | vite.config.js outDir ../static |
| R-5 | DESIGN | repo convention | I3 | absolute cross-site links | https:// URLs | blog convention | CAP-PAGE | CODING | n/a |

## 20. Change-impact table placeholder note
See next heading.

## Change-impact table

| Component | Planned change | Reason | Regression risk | Test coverage |
|---|---|---|---|---|
| `app/main.py` | root() takes Request, Host allowlist dispatch | S1,S2 | Low: default branch unchanged | syntax parse + local Host check |
| `frontend/public/unclehq/index.html` | new page | S4,S5 | None to existing | grep + 375px render |
| `frontend/public/unclehq/uncle.png` | optional logo copy | branding | None | file presence |
| `deploy/nginx-unclehq.org.conf` | new vhosts (80, 443 apex, 443 www redirect) | S6,S7 | Isolated file | `nginx -t` against the new conf is required; if nginx is unavailable locally, record 'nginx -t UNVERIFIED' in MANUAL_CHECKLIST and run it at deploy; LV-1..3 |
| `deploy/bootstrap-nginx.sh` | add unclehq.org cert issuance and vhost install, after brian block | ops reproducibility | Medium: script runs on live host | inspection; `bash -n`; nginx -t gate inside the script (fails closed); if nginx absent locally, record UNVERIFIED |
| `deploy/nginx-brian.biz-http-only.conf` | add unclehq hostnames to ACME vhost | cert issuance | Low | inspection |

## Traceability

| Requirement | Behavior | Invariant | Component | Automated test | Manual check |
|---|---|---|---|---|---|
| AC-1 | S1, S7 | I2, I5 | main.py, nginx conf | verification cmd + local Host check (200, <title>Uncle HQ</title>) | LV-1, LV-3 |
| AC-2: page contains literal strings: <title>Uncle HQ</title>; tagline text copied verbatim from CHANGE_REQUEST; the first project name and its https:// URL; the quick-start install snippet copied verbatim from the README (or CHANGE_REQUEST if README unreachable). Step 1 records these exact strings in a comment-free list in MANUAL_CHECKLIST. | S4 | I4 | index.html | grep -F for each literal string above in frontend/public/unclehq/index.html | read vs README |
| AC-3: page contains the literal credit text 'Created by Brian Woods' and an anchor with href="https://brian.biz/" (absolute URL, per R-5). | S4 | I3 | index.html | grep -F 'Created by Brian Woods' and grep -F 'href="https://brian.biz/"' | click link |
| AC-4 | S2, S3, S8 | I1 | main.py | local Host check, git diff | LV brian.biz smoke |
| AC-5 | S5 | n/a | index.html | headless Chromium 375px check: scrollWidth <= 375, run with and without uncle.png | LV-4 |
| www.unclehq.org over HTTP and HTTPS returns 301 directly to the literal https://unclehq.org$request_uri (path and query preserved). | S6 | I2 | nginx conf | inspection | LV-2 |

## Verification commands

Defined in BASELINE_REPORT verification_commands (syntax parse of app/main.py). No new suite is added. Step 5 also runs: `bash -n deploy/bootstrap-nginx.sh`; `nginx -t` against the new conf where nginx exists (else record UNVERIFIED in MANUAL_CHECKLIST); grep asserting `return 301 https://unclehq.org$request_uri` appears in both the port 80 and 443 www blocks, every `return 301` line in deploy/nginx-unclehq.org.conf uses the literal https://unclehq.org prefix, and no `$host` or `$http_host` appears in any redirect target.

## Implementation sequence

1. Uncle HQ page (copy from request text and README if reachable; tagline, differentiators, first-project link and quick-start, Brian credit, brian.biz portfolio link, viewport meta, canonical https://unclehq.org/, inline responsive CSS matching home.html style; optionally fetch uncle.png from the MIT repo). If uncle.png is not committed, the HTML has no img tag for it (text wordmark only); if committed, the img has alt text.
   Owns: `frontend/public/unclehq/index.html`, `frontend/public/unclehq/uncle.png`
2. Host dispatch in root(); import Request from fastapi.
   Owns: `app/main.py`
3. nginx vhosts for unclehq.org (80 with ACME + 301, 443 apex proxy with same headers as brian conf and cert path in D3, 443 www 301 to apex).
   Owns: `deploy/nginx-unclehq.org.conf`
4. Bootstrap/ACME updates (in scope, not cut): add unclehq.org and www.unclehq.org as a separate server block in the http-only conf (brian.biz server_name and cert untouched); issue the unclehq cert; install the 443 vhost only after the cert exists; run `nginx -t` before reload. Fail closed: on certbot or `nginx -t` failure, abort without installing the vhost or reloading, leaving the prior config active. Verify with `bash -n` and inspection.
   Owns: `deploy/bootstrap-nginx.sh`, `deploy/nginx-brian.biz-http-only.conf`
   Depends on: 3
5. Verify: run verification command, local Host check, git diff scope, and the 375px check. The 375px check uses headless Chromium (Playwright or `chrome --headless`) at viewport width 375, asserting document.documentElement.scrollWidth <= 375. It must pass both with uncle.png present and with it absent (page has no img reference when absent). If no headless browser is available, record AC-5 as unverified, not passed.
   
   Steps 1, 2, 3 share no files and may run in parallel.
   Depends on: 1, 2, 3, 4

## 21. Scope cuts

Drop only the logo (`frontend/public/unclehq/uncle.png` and any img reference to it). Step 4 (`deploy/bootstrap-nginx.sh` and `deploy/nginx-brian.biz-http-only.conf` changes, including the unclehq ACME server block) is mandatory and in scope; it is not cut. Certificate issuance fails closed: if certbot fails, the 443 unclehq vhost is not installed and nginx is not reloaded.

## 22. Risks and unresolved questions
- Cert must exist before the 443 block is enabled, else nginx -t fails: ordering handled in step 4.
- Owner must create DNS records; live ACs are verified only after that (LIVE_VERIFICATION, does not block coding).
- No automated suite exists to catch regressions beyond ad-hoc checks.

## Adversarial review dispositions

| Finding | Disposition | Reason | Exact plan change |
|---|---|---|---|
| AR-001 | Accepted | Scope cut contradicted step 4 and impact rows r5/r6; bootstrap changes are needed for reproducible cert issuance. | Section 21 scope cut now drops only the logo and states step 4 is mandatory. |
| AR-002 | Accepted | Host normalization for edge cases was unspecified; a precise rule is needed so tests and code agree. | Section 1 text (s1.1) now states the normalization rule: strip one :port, lowercase, strip one trailing dot, exact match, else home.html. |
| AR-003 | Accepted | D5 was ambiguous about page content with and without the logo. | Edit D5 in s6.1 and step-1 to state that no img tag exists unless uncle.png is committed, and that any img has alt text. |
| AR-004 | Accepted | Real gap: HTTP www behavior and query preservation were unspecified. | s1.1 and AC-6 now state port-80 www returns 301 straight to literal https://unclehq.org$request_uri, as does 443 www. |
| AR-005 | Accepted | Method and path behavior on unclehq hosts was unspecified; stating it removes ambiguity. | Edit s6.1 D2 to say GET and HEAD / on unclehq hosts serve the Uncle page and other paths and methods behave as on brian.biz. |
| AR-006 | Accepted | Scope cut contradicted step 4 and impact row r5; bootstrap changes are required for reproducible cert issuance. | Rewrote s19.1 so the scope cut applies only to the logo and step 4 is explicitly in scope. |
| AR-007 | Accepted | Host normalization edge cases were unspecified; a fixed rule removes ambiguity. | Section 1 prose s1.1 now states the exact Host normalization and fallback rule. |
| AR-008 | Accepted | The http-only ACME conf edit touches the live brian.biz cert flow, so the plan must bound it. | s5.1 now allows the http-only conf edit only as a separate unclehq server block, leaving brian.biz server_name and cert untouched. |
| AR-009 | Accepted | Non-root path and port-80 www behavior was unspecified; D2 needs an explicit statement. | Extend s6 D2 text to state non-root paths proxy unchanged and port-80 www redirects straight to the https apex. |
| AR-010 | Accepted | Regression check only compared / bytes; blog, API and static preservation promised by AC-4/S3 were untested. | Section 17 regression strategy now also checks HEAD /, /blog, /api health and a /static asset under both brian.biz and unclehq.org Hosts against baseline. |
| AR-011 | Accepted | Host normalization for malformed values was unspecified and must be fixed. | s1.1 now states exact Host normalization and fallback to home.html, never an error. |
| AR-012 | Accepted | The plan trusts the Host header without stating the app is only reachable through nginx on loopback. | Section 8 (s6.1) now states the loopback-only bind assumption, and that direct requests with a spoofed Host only select the static page. |
| AR-013 | Accepted | Scope cut contradicted step 4 and the impact table; bootstrap changes are required for reproducible cert issuance. | Rewrote s19.1 so only the logo is cut and step 4 is in scope; step 4 now adds unclehq hostnames as a separate ACME server block and fails closed. |
| AR-014 | Accepted | Origin exposure was unstated; making D2 explicit that unclehq.org proxies all paths including /api/* removes the ambiguity. | Section 8 (s6.1) D2 now states unclehq.org proxies all paths, /api/* on that origin is accepted, and no origin isolation or CORS/cookie changes are made. |
| AR-015 | Accepted | Plan does not state the redirect target is a fixed literal, so a $host-based redirect could be implemented and enable open redirect. | Added decision D6 in section 8 requiring literal https://unclehq.org$request_uri in all unclehq redirects, never $host or $http_host. |
| AR-016 | Accepted | Host normalization edge cases were unspecified; a precise exact-match rule makes dispatch testable. | s1.1 and s6.1 D1 now define normalization: lowercase, strip one :port and one trailing dot, exact match, else home.html. |
| AR-017 | Accepted | Grep checks are meaningless without pinned strings, so the plan should name the literals the page must contain. | Traceability AC-2 and AC-3 rows now list the literal strings the page must contain and that grep checks. |
| AR-018 | Accepted | The title text and missing-file behavior were unstated; pinning them makes AC-1 checkable. | Added decision D6 in s6.1 (title exactly 'Uncle HQ'; missing file returns default error status) and updated the s10.1 check and AC-1 test. |
| AR-019 | Accepted | The local-check fallback and its pass/fail semantics were unspecified, and the check depends on the built static/unclehq output. | s10.1 now requires a built static/ or an explicit page-path override, and treats an unrunnable check as a failed AC. |
| AR-020 | Accepted | Scope cut and step 4 contradicted each other; bootstrap changes are in scope and nginx -t absence must be recorded as unverified. | Scope cuts (s19.1) now drop only the logo; r4/r5 coverage states nginx -t required or recorded UNVERIFIED. |
| AR-021 | Accepted | The 375px check had no named tool and no pass condition covering the logo being present or absent. | Step 5 and AC-5 now name headless Chrome/Playwright scrollWidth measurement and require a pass with and without uncle.png. |
