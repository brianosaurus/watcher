# Change Spec

Omitted sections: Performance (static file, negligible); Migration (none); Prototype isolation (not a prototype)

## 1. Change type
Feature.

## 2. Problem statement
unclehq.org has no site. It should serve an Uncle HQ page from this repo's host (CHANGE_REQUEST.md).

## 3. Current behavior
See baseline B1-B5.

## 4. Desired behavior
Requests with Host `unclehq.org`/`www.unclehq.org` to `/` return the Uncle HQ page; `www.unclehq.org` is 301-redirected to `https://unclehq.org` at nginx; brian.biz behavior is unchanged.

## 5. Observable behavior table
| ID | Class | Trigger | Current behavior | Expected behavior | Verification |
|---|---|---|---|---|---|
| S1 | ADD | GET / with Host unclehq.org (port suffix tolerated, case-insensitive) | home.html | Uncle HQ page (200 HTML) | AC-1, AC-2 |
| S2 | PRESERVE | GET / with Host brian.biz or any other Host | home.html | Unchanged | AC-4 |
| S3 | PRESERVE | /blog*, /static/*, /api/*, /resume.pdf | as baseline B2-B3 | Unchanged | AC-4 |
| S4 | ADD | Page content | none | Explains Uncle (MIT, terminal-native orchestration of Claude/Codex/local models; plan, implement, independent review, verify, PR; evidence; tagline), differentiators (independent review, artifact identity, in-toto/DSSE provenance, model flexibility, local-first), first project link https://github.com/unclehq/uncle with quick-start install, Brian credit, https://brian.biz portfolio link | AC-2, AC-3 |
| S5 | ADD | Phone-width viewport | none | Responsive, no horizontal scroll at 375px | AC-5 |
| S6 | ADD | GET http(s)://www.unclehq.org/* | none | 301 to https://unclehq.org$request_uri | AC-6 |
| S7 | ADD | GET http://unclehq.org/ | none | 301 to HTTPS; ACME path served | AC-1 |
| S8 | PRESERVE | www.brian.biz | served directly | Unchanged | AC-4 |

## 6. Invariant table
| ID | Status | Invariant | Scope | Enforcement point | Verification |
|---|---|---|---|---|---|
| I1 | EXISTING | brian.biz `/` serves home.html | app | root() | AC-4 |
| I2 | EXISTING | HTTP->HTTPS redirect except ACME | nginx | all vhosts | AC-1, AC-6 |
| I3 | NEW | Cross-site links are absolute | new page | page HTML | AC-3 |
| I4 | NEW | Page copy makes no claims beyond the Uncle README/request | new page | page HTML | manual |
| I5 | EXISTING | Security headers on 443 vhosts | nginx | new vhost copies them | AC-1 |

No RELAXED or REMOVED invariants.

## 7. Compatibility
brian.biz URLs, nginx brian.biz vhost, and `/static` paths unchanged.

## 8. Error behavior
If the page file is missing, `/` for unclehq hosts returns the default FastAPI 500/404 (same as home.html today); no fallback to brian home.

## 10. Security
No secrets in the page. Host header is only compared to a fixed allowlist, never reflected. New vhost carries the same HSTS/nosniff/DENY/no-referrer headers. External links use `rel="noopener"`.

## 12. Rollback
Revert commit; remove unclehq vhost symlink and reload nginx; DNS removal is manual.

## 14. Non-goals
Blocking brian.biz paths on unclehq.org host; extra unclehq pages; redesign of brian.biz; DNS provider automation; CI/test framework.

## 15. Assumptions and unresolved questions
- Separate Let's Encrypt cert for unclehq.org; apex canonical, www redirects to apex.
- DNS changes are performed manually by the owner.
- Logo reused from unclehq/uncle (MIT) only if fetchable; page works without it.

## Acceptance criteria

| ID | Criterion | Verification |
|---|---|---|
| AC-1 | https://unclehq.org/ serves the Uncle HQ page over HTTPS; HTTP redirects to HTTPS; nginx config for unclehq.org has TLS, ACME location and security headers. | Static: nginx -t if available, otherwise config inspection. Local: FastAPI TestClient/curl GET / with Host: unclehq.org returns 200 and Uncle HQ title. LIVE_VERIFICATION: curl -sI https://unclehq.org/ after DNS/cert. |
| AC-2 | Page explains what Uncle is (open-source MIT, tagline, plan/implement/independent review/verify/PR, differentiators) and names https://github.com/unclehq/uncle as Uncle HQ's first project with prominent link and quick-start install. | grep the page for the tagline, 'first project', the GitHub URL and install snippet; manual read against README. |
| AC-3 | Page credits Brian and links to https://brian.biz as his portfolio using an absolute URL. | grep page for href="https://brian.biz" and credit text. |
| AC-4 | brian.biz home page and blog are unchanged: GET / with Host brian.biz (and no/other Host) still returns home.html content; blog routes and nginx brian.biz vhost untouched. | TestClient GET / with Host brian.biz equals home.html bytes; git diff shows no change to home.html, blog, or brian.biz conf. |
| AC-5 | Page is responsive: viewport meta present, no horizontal scroll at 375px width. | Browser/headless render at 375px, check scrollWidth <= innerWidth; inspect viewport meta. |
| AC-6 | www.unclehq.org (HTTP and HTTPS) redirects 301 to https://unclehq.org preserving the URI. | Config inspection; LIVE_VERIFICATION: curl -sI https://www.unclehq.org/x shows 301 Location https://unclehq.org/x. |

