# Baseline Report

Omitted sections: Reproduction (feature, not a bug); Existing failures (no tests exist, none documented)

## 1. Change-request summary
See CHANGE_REQUEST.md (Issue 9): serve an Uncle HQ page for unclehq.org from this site, Host-routed, with DNS/TLS/nginx ops and www->apex redirect; brian.biz unchanged.

## 2. Repository architecture
- FastAPI app `app/main.py` (single ~1900-line file) listens on 127.0.0.1:8765; nginx terminates TLS and proxies everything (`deploy/nginx-brian.biz.conf`, `proxy_set_header Host $host`).
- `frontend/` is Vite+React; `frontend/public/*` is copied verbatim to repo-root `static/` on `npm run build` (`frontend/vite.config.js`, base `/static/`, outDir `../static`). `static/` is generated and gitignored; `deploy/deploy.sh` rebuilds and tars it.
- `STATIC_DIR = REPO_ROOT/static` (`app/main.py:25`).

## 3. Relevant code paths
- `app/main.py:1783-1786` `root()` returns `STATIC_DIR/home.html` with no Host logic.
- `app/main.py:1852` mounts `/static` (host-independent; will serve `/static/unclehq/*`).
- `app/main.py:1860-1880` blog exact routes plus `/blog` mount.
- `deploy/nginx-brian.biz.conf`: port 80 server (ACME + 301 to https) and 443 server for `brian.biz www.brian.biz`; cert `/etc/letsencrypt/live/brian.biz/`. `www.brian.biz` is served directly, not redirected.
- `deploy/nginx-brian.biz-http-only.conf`: provisioning vhost; `deploy/bootstrap-nginx.sh:25` certbot for `${DOMAIN}` and `www.${DOMAIN}` only.
- Style reference: `frontend/public/home.html` (inline CSS, Google Fonts, OG tags, canonical).

## 4. Current observable behavior
| ID | Trigger | Current result | Evidence | Must preserve? |
|---|---|---|---|---|
| B1 | GET / any Host | home.html (brian portfolio) | main.py:1783-1786 | Yes for brian.biz |
| B2 | GET /blog, /blog/<slug> | blog pages | main.py:1860-1880 | Yes |
| B3 | GET /static/* | built assets and public files | main.py:1852 | Yes |
| B4 | GET www.brian.biz | served directly, no redirect | nginx conf | Yes |
| B5 | GET unclehq.org | no DNS/vhost/cert | absent in deploy/ | n/a |

## 5. Existing invariants
| ID | Invariant | Current enforcement | Existing test | Confidence |
|---|---|---|---|---|
| I1 | brian.biz `/` serves home.html | root() | none | High |
| I2 | Plain HTTP redirects to HTTPS except ACME | nginx port 80 block | none | High |
| I3 | Cross-site links in pages are absolute | blog pages convention | none | Medium |
| I4 | Security headers on 443 vhost | nginx add_header | none | High |

## 6. Interface contracts
No schema/API changes exist. Routes above are the interface; `/api/*` unaffected.

## 7. Existing automated-test coverage
None: no test files or CI in the repo. Only a syntax-parse check of `app/main.py` is available; nginx config and HTML are not testable here (nginx likely not installed). Commands are serial; no parallel groups.

## 9. Baseline test results
Command source: derived by analyst (no Makefile/CI/package test script; `frontend/package.json` has dev/build/preview only). `npm run build` is excluded: it rewrites gitignored `static/` and needs node_modules. Driver baseline is the authority on results; no documented pre-existing failures.

## 12. Likely change surface
`app/main.py` root(); new `frontend/public/unclehq/index.html` (+ optional `uncle.png`); new `deploy/nginx-unclehq.org.conf`; `deploy/bootstrap-nginx.sh` (second cert/vhost); `deploy/nginx-brian.biz-http-only.conf` (ACME hostnames).

## 13. Regression-sensitive components
`root()` (brian.biz home), nginx 443 vhost for brian.biz, the shared `/static` mount.

## 14. Outside the change
All `/api/*`, blog content, home.html content, React dashboard, trading logic, DNS provider changes (manual ops).

## 15. Unknowns and assumptions
- DNS registrar and host IP not in repo: manual ops step.
- Whether to use a separate cert (`/etc/letsencrypt/live/unclehq.org/`) vs extending the brian.biz cert: assume separate cert.
- Uncle README wording unavailable offline in repo; implementer must take copy from the request text and fetch the README if reachable.
- uncle.png availability/network unknown.

## 16. Initial risk assessment
Low code risk (small route change). Medium ops risk: nginx/cert changes on a live host; mitigate with `nginx -t` before reload and keep brian.biz block untouched.

## Exact build and test commands executed

```sh
python3 -c "import ast; ast.parse(open('app/main.py').read())"
```

