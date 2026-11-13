## AR-001: Plan scope cut drops bootstrap changes, but the implementation sequence and impact table require them (step 4).

- Severity: HIGH
- References: CHANGE_PLAN s19 (21. Scope cuts) vs s18 step-4 and change-impact row r5 and r6.
- Failure: Plan scope cut drops bootstrap changes, but the implementation sequence and impact table require them (step 4). Two sections conflict on whether bootstrap-nginx.sh is modified. Add: 'Step 4 is mandatory; scope cuts drop only the logo.'
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-002: Host parsing is unspecified for edge cases: missing Host, empty Host, trailing dot (unclehq.org.), IPv6 bracket form, an

- Severity: MEDIUM
- References: CHANGE_PLAN s1 and s6 D1 say only 'port stripped, lowercased'; CHANGE_SPEC S1 'port suffix tolerated'.
- Failure: Host parsing is unspecified for edge cases: missing Host, empty Host, trailing dot (unclehq.org.), IPv6 bracket form, and multiple or malformed ports. Add: 'Strip a trailing :port, lowercase, and trailing dot; anything else (including missing Host) serves home.html.'
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-003: The page's content when uncle.png is absent is unspecified: D5 says markup degrades to a text wordmark and does not refe

- Severity: MEDIUM
- References: CHANGE_PLAN s6 D5 and s19 scope cut 'Drop logo'.
- Failure: The page's content when uncle.png is absent is unspecified: D5 says markup degrades to a text wordmark and does not reference a missing file, but also 'onerror-free'. Add: 'If uncle.png is not committed, the HTML contains no img tag for it; if committed, it has alt text.'
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-004: AC-6 says www redirects over HTTP and HTTPS preserving the URI, but the plan defines only a 443 www block and port 80 as

- Severity: MEDIUM
- References: CHANGE_SPEC AC-6 and S6 versus CHANGE_PLAN s1 (80: ACME + 301 https; 443 www 301 to apex).
- Failure: AC-6 says www redirects over HTTP and HTTPS preserving the URI, but the plan defines only a 443 www block and port 80 as 'ACME + 301 https'. Whether HTTP www goes directly to the apex or via HTTPS, and whether query strings are kept, is unspecified. Add: 'Port 80 www returns 301 to https://unclehq.org$request_uri.'
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-005: Behavior for non-root methods and paths on unclehq hosts is unspecified (HEAD /, POST /, /blog on unclehq.org).

- Severity: LOW
- References: CHANGE_PLAN s6 D2; CHANGE_SPEC S1 and S3 mention only GET.
- Failure: Behavior for non-root methods and paths on unclehq hosts is unspecified (HEAD /, POST /, /blog on unclehq.org). D2 allows other paths but does not say whether HEAD / returns the Uncle page. Add: 'GET and HEAD / on unclehq hosts serve the Uncle page; other paths behave as on brian.biz.'
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-006: Plan says scope cut drops bootstrap-script changes, but step 4 and the impact table require them.

- Severity: HIGH
- References: CHANGE_PLAN s19 (21. Scope cuts) vs Implementation sequence step 4 and change-impact row r5. Add: 'Step 4 is in scope; the scope cut applies only to the logo.'
- Failure: Plan says scope cut drops bootstrap-script changes, but step 4 and the impact table require them. Two statements cannot both hold. The script runs on a live host.
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-007: Host dispatch leaves Host forms unspecified: trailing dot (unclehq.org.), IPv6 bracket form, empty or missing Host, and

- Severity: MEDIUM
- References: CHANGE_PLAN s1/D1 says 'port stripped, lowercased' only. Add: 'A trailing dot is stripped; a missing, empty or unparseable Host falls to home.html.'
- Failure: Host dispatch leaves Host forms unspecified: trailing dot (unclehq.org.), IPv6 bracket form, empty or missing Host, and multiple Host values. A mismatch could send unclehq traffic to home.html, or change brian.biz behavior.
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-008: The http-only ACME conf edit touches the live brian.biz cert flow, yet 'not to modify' bans only nginx-brian.biz.conf.

- Severity: MEDIUM
- References: CHANGE_PLAN s5 vs impact row r6 and R-3 'brian.biz unchanged'. Add: 'The http-only conf change adds only a separate unclehq server block; brian.biz server_name and cert are untouched.'
- Failure: The http-only ACME conf edit touches the live brian.biz cert flow, yet 'not to modify' bans only nginx-brian.biz.conf. It is unspecified whether the new hostnames join brian's server_name, and whether the existing cert or renewal is affected.
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-009: Unclehq hosts requesting non-root paths (such as /blog or /static) fall to brian content, and www.unclehq.org on port 80

- Severity: MEDIUM
- References: CHANGE_PLAN D2 and CHANGE_SPEC S6/S7. Add: 'Non-root paths on unclehq.org proxy unchanged to the app; the port-80 www redirect goes straight to the https apex.'
- Failure: Unclehq hosts requesting non-root paths (such as /blog or /static) fall to brian content, and www.unclehq.org on port 80 redirects to https://unclehq.org. Behavior for these is unspecified, and the S2/S3 preserve rows and AC-6 are not tied to it.
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-010: Regression check compares brian Host bytes to home.html.

- Severity: LOW
- References: CHANGE_PLAN s11 (17. Regression-test strategy) vs CHANGE_SPEC S3 and AC-4. Add: 'The local check also GETs /blog, /api health and /static asset under Host brian.biz and under unclehq.org, and compares them to baseline.'
- Failure: Regression check compares brian Host bytes to home.html. It omits HEAD, the blog, and the /api/* and /static/* paths that AC-4 and S3 promise are preserved. The git diff confines scope only for files, not behavior.
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-011: Host allowlist dispatch is unspecified for malformed Host values (empty, multiple, trailing dot, IPv6 bracket, userinfo)

- Severity: HIGH
- References: CHANGE_PLAN s1 and D1 say 'port stripped, lowercased' only. CHANGE_SPEC S1/S2 cover only 'any other Host'.
- Failure: Host allowlist dispatch is unspecified for malformed Host values (empty, multiple, trailing dot, IPv6 bracket, userinfo). Behavior must be fixed. Proposed: Host is lowercased, one trailing dot and :port stripped, matched exactly; any non-match or missing Host serves home.html, never an error.
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-012: Plan does not say whether the 443 apex vhost for unclehq.org is the only way to reach the app, or whether other vhosts o

- Severity: MEDIUM
- References: CHANGE_PLAN s1 proxies to 127.0.0.1:8765. D1 trusts the client-supplied Host header, and nothing states the bind address.
- Failure: Plan does not say whether the 443 apex vhost for unclehq.org is the only way to reach the app, or whether other vhosts or direct IP requests with Host: unclehq.org are accepted. Proposed: the app trusts Host because the backend binds only to 127.0.0.1:8765.
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-013: Scope cuts say to drop bootstrap changes, but step 4 and the impact table require them.

- Severity: MEDIUM
- References: CHANGE_PLAN s19 'drop bootstrap-script changes' contradicts Implementation step 4 and the change-impact row for deploy/bootstrap-nginx.sh.
- Failure: Scope cuts say to drop bootstrap changes, but step 4 and the impact table require them. The plan also leaves open whether the http-only ACME vhost gains unclehq hostnames, so cert issuance could fail or run unsafely. Proposed: bootstrap changes are in scope and cert issuance fails closed.
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-014: Spec says D2 unclehq.org keeps access to /api/*, blog and other paths, but the new vhost sets HSTS and security headers.

- Severity: MEDIUM
- References: CHANGE_PLAN D2 'non-goal to block'. CHANGE_SPEC s14 non-goals and s6 I5 give no origin-isolation decision.
- Failure: Spec says D2 unclehq.org keeps access to /api/*, blog and other paths, but the new vhost sets HSTS and security headers. Whether unclehq.org gets API or CORS and cookie exposure is unstated. Proposed: unclehq.org proxies all paths and the plan states that /api/* on that origin is accepted.
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-015: The 301 www redirect uses $request_uri, and plan s1 does not say the redirect target is a fixed literal host.

- Severity: LOW
- References: CHANGE_SPEC S6 'https://unclehq.org$request_uri'. The plan does not forbid $host in the 80 block redirect for the apex (S7).
- Failure: The 301 www redirect uses $request_uri, and plan s1 does not say the redirect target is a fixed literal host. Proposed: use the literal https://unclehq.org$request_uri, never $host or $http_host, to avoid open redirect via Host.
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-016: Host normalization is unspecified for edge inputs: missing Host, empty Host, trailing dot (unclehq.org.), IPv6/bracketed

- Severity: HIGH
- References: CHANGE_PLAN s1 and D1 say 'port stripped, lowercased'. S1 says 'port suffix tolerated'. Neither covers a trailing dot or a missing Host.
- Failure: Host normalization is unspecified for edge inputs: missing Host, empty Host, trailing dot (unclehq.org.), IPv6/bracketed, multiple ports. Tests can't tell whether these go to home.html or Uncle HQ. Say: only exact lowercase match after stripping one :port suffix goes to Uncle; anything else gets home.html.
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-017: AC-2 and AC-3 are verified only by grep and manual reading, with no exact strings pinned.

- Severity: MEDIUM
- References: CHANGE_SPEC AC-2 verification: 'grep the page for the tagline, first project, URL and install snippet'. The tagline and snippet are not given. AC-3 'credit text' is also undefined.
- Failure: AC-2 and AC-3 are verified only by grep and manual reading, with no exact strings pinned. The tagline, 'first project', install snippet and credit text are never stated, so the code and the checks can disagree. Say: the page must contain these literal strings, and the plan lists them.
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-018: The AC-1 local check expects 200 and an 'Uncle HQ title', and the plan never states the exact title text.

- Severity: MEDIUM
- References: CHANGE_SPEC AC-1 'returns 200 and Uncle HQ title'. Spec section 8 says 'default FastAPI 500/404' without picking one.
- Failure: The AC-1 local check expects 200 and an 'Uncle HQ title', and the plan never states the exact title text. It also doesn't say what happens when the page file is missing, which spec s8 sends to 500/404 with no check. Say: the title is exactly 'Uncle HQ', and a missing file returns the default error status.
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-019: The local verification fallback is unspecified.

- Severity: MEDIUM
- References: CHANGE_PLAN s10: 'FastAPI TestClient, if fastapi installed, else uvicorn + curl'. R-4 relies on the Vite copy into static/unclehq.
- Failure: The local verification fallback is unspecified. The plan says TestClient 'if fastapi installed, else uvicorn+curl', but doesn't say what counts as passing if neither is available, or whether the static/unclehq build output must exist first. Say: the check requires a built static/ or the page path is overridden, and failure to run it is a failed AC, not a skip.
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-020: The plan has two inconsistent readings of the bootstrap script.

- Severity: MEDIUM
- References: CHANGE_PLAN Implementation step 4 and the change-impact table row for bootstrap-nginx.sh versus '21. Scope cuts'. The verification in the table says 'nginx -t if available'.
- Failure: The plan has two inconsistent readings of the bootstrap script. Step 4 and the change-impact table modify it, but scope cut 21 drops the script changes and moves certbot to a conf header. AC-1 and AC-6 depend on nginx config that is never run. Say whether the script is in scope. Say `nginx -t` is required, or that its absence is recorded as unverified.
- Fix: Address in the plan.
- Verify: Re-run the check.

## AR-021: The 375px headless check has no named tool.

- Severity: LOW
- References: CHANGE_SPEC AC-5 'Browser/headless render at 375px'. CHANGE_PLAN D5 and step 5 'headless 375px check', and no framework exists.
- Failure: The 375px headless check has no named tool. D5 says the logo may be absent, but the pass condition for page content with or without the logo is unstated. Say which tool measures scrollWidth, and that the page must pass AC-5 both with and without uncle.png.
- Fix: Address in the plan.
- Verify: Re-run the check.

## Overall assessment

Review findings require disposition.
