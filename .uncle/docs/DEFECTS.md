# Defects

## MC-103

- **Status:** BLOCKED-HUMAN
- **Evidence:** SW=360 measured; readability needs Brian
- **Expected result:** scrollWidth <= 375; readable, layout intact; wordmark when no logo.
- **Actual result:** SW=360 CW=360, imgs=0. Readability and layout appearance are subjective and unobserved (screenshot /tmp/mc/s375.png not viewed).

## D-1

- **Status:** FAIL
- **Evidence:** HEAD / unclehq.org 405; D-1
- **Expected result:** HEAD returns 200 Uncle page; others as specified, no errors.
- **Actual result:** all GET cases correct. HEAD / unclehq.org returned 405 (expected 200).

## MC-204

- **Status:** BLOCKED-HUMAN
- **Evidence:** copy review vs README needs Brian
- **Expected result:** no claims beyond README; required literals; rel noopener.
- **Actual result:** tagline, 'First project', github.com/unclehq/uncle, install curl snippet, credit, absolute brian.biz link present; rel="noopener" on all three anchors. Claim review and screenshot not performed.

## MC-207

- **Status:** BLOCKED-IMPOSSIBLE
- **Evidence:** live-only, no host
- **Expected result:** brian.biz/www/http behavior after deploy.
- **Actual result:** not run; requires live host.

## MC-301

- **Status:** NOT RUN
- **Evidence:** no Network inspection
- **Expected result:** no failed requests.
- **Actual result:** only 0 img tags observed; resources not enumerated.

## MC-302

- **Status:** BLOCKED-HUMAN
- **Evidence:** follow links and compare snippet
- **Expected result:** destinations open; snippet matches README.
- **Actual result:** hrefs present only (see MC-204).

## D-1

- **Status:** FAIL
- **Evidence:** HEAD / unclehq.org 405; D-1
- **Expected result:** HEAD 200 Uncle page.
- **Actual result:** GETs correct (three Uncle HQ; rest brian). HEAD / returned 405.

## MC-405

- **Status:** BLOCKED-IMPOSSIBLE
- **Evidence:** live-only
- **Expected result:** live brian.biz behavior.
- **Actual result:** not run.
