# Verification report

## Findings

### MC-102

- **Action:** grep of index.html for credit and anchor.
- **Expected result:** credit text; absolute brian.biz link.
- **Actual result:** 'Created by Brian Woods' present once; `<a href="https://brian.biz/" rel="noopener">` at line 122. Click not performed.
- **Defects:** None

### MC-103

- **Action:** 375px iframe measurement; no logo committed.
- **Expected result:** scrollWidth <= 375; readable, layout intact; wordmark when no logo.
- **Actual result:** SW=360 CW=360, imgs=0. Readability and layout appearance are subjective and unobserved (screenshot /tmp/mc/s375.png not viewed).
- **Defects:** None

### MC-104

- **Action:** TestClient GET / (brian.biz, evil.com, none), /blog, /blog/one-block-short, /static/home.html vs base commit.
- **Expected result:** unchanged.
- **Actual result:** home title Brian Woods for non-unclehq Hosts; every path status and sha256 SAME as base.
- **Defects:** None

### MC-105

- **Action:** GET / for the listed Hosts; HEAD / for unclehq.org.
- **Expected result:** HEAD returns 200 Uncle page; others as specified, no errors.
- **Actual result:** all GET cases correct. HEAD / unclehq.org returned 405 (expected 200).
- **Defects:** D-1

### MC-202

- **Action:** GET / for 8 Hosts, titles read.
- **Expected result:** first four Uncle HQ 200; last four home, no error.
- **Actual result:** unclehq.org, UNCLEHQ.ORG:8080, www.unclehq.org, unclehq.org. -> 200 Uncle HQ; empty, [::1], unclehq.org:80:80, unclehq.org.. -> 200 Brian Woods.
- **Defects:** None

### MC-204

- **Action:** grep only; copy-vs-README review not done.
- **Expected result:** no claims beyond README; required literals; rel noopener.
- **Actual result:** tagline, 'First project', github.com/unclehq/uncle, install curl snippet, credit, absolute brian.biz link present; rel="noopener" on all three anchors. Claim review and screenshot not performed.
- **Defects:** None

### MC-205

- **Action:** 375px iframe scrollWidth; grep for viewport meta and img.
- **Expected result:** <=375; viewport meta; no img when no logo.
- **Actual result:** SW=360; viewport meta line 5; 0 img tags; only index.html in frontend/public/unclehq (logo-present variant not applicable).
- **Defects:** None

### MC-207

- **Action:** none; live-only.
- **Expected result:** brian.biz/www/http behavior after deploy.
- **Actual result:** not run; requires live host.
- **Defects:** None

### MC-301

- **Action:** not executed (no Network-panel inspection).
- **Expected result:** no failed requests.
- **Actual result:** only 0 img tags observed; resources not enumerated.
- **Defects:** None

### MC-302

- **Action:** not executed; links not followed, snippet not compared to README.
- **Expected result:** destinations open; snippet matches README.
- **Actual result:** hrefs present only (see MC-204).
- **Defects:** None

### MC-303

- **Action:** TestClient /, /blog, /static/home.html under both Hosts vs base.
- **Expected result:** brian Host home; /blog and /static identical across Hosts.
- **Actual result:** statuses 200, hashes identical across Hosts and equal to base.
- **Defects:** None

### MC-402

- **Action:** TestClient /blog and /blog/one-block-short under both Hosts; nav clicks not done.
- **Expected result:** same status and body.
- **Actual result:** 200, hashes ddec1c37b1 and 1e42ab2f54 identical under both Hosts and base.
- **Defects:** None

### MC-403

- **Action:** TestClient /static asset, /resume.pdf both Hosts; /api/healthz.
- **Expected result:** 200 identical; API unchanged.
- **Actual result:** all 200, hashes equal across Hosts and base.
- **Defects:** None

### MC-404

- **Action:** GET / for the 7 Hosts, HEAD / unclehq.org.
- **Expected result:** HEAD 200 Uncle page.
- **Actual result:** GETs correct (three Uncle HQ; rest brian). HEAD / returned 405.
- **Defects:** D-1

### MC-405

- **Action:** none; live-only, not required.
- **Expected result:** live brian.biz behavior.
- **Actual result:** not run.
- **Defects:** None

## Acceptance gate

| ID | Required | Status | Evidence |
|---|---|---|---|
| MC-102 | YES | PASS | grep of credit and href |
| MC-103 | YES | BLOCKED-HUMAN | SW=360 measured; readability needs Brian |
| MC-104 | YES | PASS | hostcheck.py vs base |
| MC-105 | YES | FAIL | HEAD / unclehq.org 405; D-1 |
| MC-202 | YES | PASS | hostcheck.py Host table |
| MC-204 | YES | BLOCKED-HUMAN | copy review vs README needs Brian |
| MC-205 | YES | PASS | SW=360, viewport meta, 0 img |
| MC-207 | YES | BLOCKED-IMPOSSIBLE | live-only, no host |
| MC-301 | YES | NOT RUN | no Network inspection |
| MC-302 | YES | BLOCKED-HUMAN | follow links and compare snippet |
| MC-303 | YES | PASS | hostcheck.py vs base |
| MC-402 | YES | PASS | hostcheck.py /blog identical |
| MC-403 | YES | PASS | hostcheck.py static, resume, api |
| MC-404 | YES | FAIL | HEAD / unclehq.org 405; D-1 |
| MC-405 | NO | BLOCKED-IMPOSSIBLE | live-only |
