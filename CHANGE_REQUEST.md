# Change Request

Issue 9

Seeded from [brianosaurus/watcher#9](https://github.com/brianosaurus/watcher/issues/9).

## Change Type

Feature | Bug Fix | Prototype | Refactor | Performance | Security | Upgrade

## Summary

Serve unclehq.org home page from brian.biz (Uncle HQ)

## Motivation

## Summary

Serve a home page for **unclehq.org** from the same site that serves brian.biz (this repo, `frontend/public/`), so unclehq.org becomes the public headquarters for Uncle.

## Content requirements

- **Identity:** unclehq.org is Uncle HQ, the headquarters and home of Uncle himself.
- **What Uncle is:** an open-source (MIT), terminal-native development system that orchestrates Claude, Codex, local models and other coding agents. You describe an application or hand it a GitHub issue. It plans, implements, independently reviews, verifies, and prepares a pull request, with portable evidence tying the result to the code that was actually reviewed. Tagline from the README: *"AI coding agents build the software. Uncle makes them prove their work."* Cover the key differentiators: independent review, artifact identity (the change is the unit of trust), verifiable change provenance (in-toto/DSSE), model flexibility, local-first operation.
- **First project:** present https://github.com/unclehq/uncle as **Uncle HQ's first project**, with a prominent link and the quick-start install.
- **Attribution:** credit Brian (creator/author of Uncle HQ and Uncle).
- **Portfolio link:** link to https://brian.biz, noted as Brian's portfolio.
- Keep the page's copy consistent with the Uncle README. Take the wording from there rather than inventing claims.

## Implementation notes

- Add a static page (e.g. `frontend/public/unclehq/index.html`) matching the existing site style (see `frontend/public/home.html` and the blog pages).
- Route by `Host`: requests for `unclehq.org` / `www.unclehq.org` serve the Uncle HQ page at `/`, while brian.biz keeps its current home page. Check how `app/` and `deploy/` currently serve `frontend/public` to pick the cleanest place (app route vs. reverse-proxy config).
- Use absolute links for cross-site navigation (brian.biz <-> unclehq.org), as the blog pages already do.
- Reuse the Uncle logo from the Uncle repo (`uncle.png`) if licensing allows (the repo is MIT).

## Ops / DNS

- Point `unclehq.org` and `www.unclehq.org` DNS at the same host as brian.biz.
- Add the hostnames to the TLS certificate / reverse-proxy config. Redirect `www` to the apex (or the reverse).

## Acceptance criteria

- [ ] `https://unclehq.org/` serves the Uncle HQ page over HTTPS
- [ ] Page explains what Uncle is and names https://github.com/unclehq/uncle as the first Uncle HQ project
- [ ] Page credits Brian and links to https://brian.biz as his portfolio
- [ ] brian.biz home page and blog are unchanged
- [ ] Page is responsive and works at phone width
- [ ] `www.unclehq.org` redirects to the canonical host

## Observed Current Behavior

Describe what the system currently does.

## Desired Behavior

Describe what the system should do after the change.

## Reproduction

For a bug, provide exact steps to reproduce it.

For other change types, write "Not applicable."

## Constraints

List compatibility, security, performance, timing, or scope constraints.

## Known Relevant Files

List files or components if known.

## Out of Scope

List behavior or components that must not be changed.

## Success Criteria

Describe the observable evidence that proves the change works.
