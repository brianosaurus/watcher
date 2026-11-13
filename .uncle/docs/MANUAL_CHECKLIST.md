# Manual checklist

## Coverage

### MC-102
- Required for acceptance: YES
- Exclusive resources: none
- Depends on: none
- Exact action: On the Uncle HQ page, read the credit and click the Brian portfolio link.
- Expected result: Text 'Created by Brian Woods' is visible and the link goes to https://brian.biz/ (absolute URL); external links open normally.
- Actual result: 
- Status: NOT RUN

### MC-103
- Required for acceptance: YES
- Exclusive resources: none
- Depends on: MC-101
- Exact action: Load the Uncle HQ page in a browser at 375px viewport width and scroll in both directions; repeat if a logo image is present and if absent.
- Expected result: No horizontal scrolling (scrollWidth <= 375), text readable, layout intact, any logo image has alt text and a text wordmark is shown when no logo exists.
- Actual result: 
- Status: NOT RUN

### MC-104
- Required for acceptance: YES
- Exclusive resources: none
- Depends on: none
- Exact action: Request / with Host brian.biz and with no/other Host (e.g. curl -H 'Host: brian.biz' and evil.com) and view in a browser; also load /blog, a blog post and a /static asset.
- Expected result: Brian's portfolio home page appears unchanged for non-unclehq hosts; blog and static assets load as before.
- Actual result: 
- Status: NOT RUN

### MC-105
- Required for acceptance: YES
- Exclusive resources: none
- Depends on: none
- Exact action: Request / with Host variants: unclehq.org, UNCLEHQ.ORG:8080, www.unclehq.org, unclehq.org., empty Host, [::1], unclehq.org:80:80; also HEAD / for unclehq.org.
- Expected result: First four (and HEAD) return the Uncle HQ page with 200; the rest return home.html; none returns an error status.
- Actual result: 
- Status: NOT RUN

## Invariants

### MC-202
- Required for acceptance: YES
- Exact action: Request GET / with Host values unclehq.org, UNCLEHQ.ORG:8080, www.unclehq.org and unclehq.org. . Then request Host values empty, [::1], unclehq.org:80:80 and unclehq.org.. Check the body title each time.
- Expected result: The first four return 200 with <title>Uncle HQ</title>. The last four return home.html and none returns an error status.
- Evidence to capture: Table of Host value, status and title for each case.
- Actual result: 
- Status: NOT RUN

### MC-204
- Required for acceptance: YES
- Exact action: Open the Uncle HQ page in a browser. Read the copy against the Uncle README and the change request. Click the GitHub link and the brian.biz link.
- Expected result: The copy makes no claims beyond the README or request (I4). It carries the tagline, 'first project', https://github.com/unclehq/uncle, the install snippet and 'Created by Brian Woods'. The brian.biz link is absolute https://brian.biz/ and opens the portfolio (I3). External links open with rel noopener.
- Evidence to capture: Screenshot of the page plus notes on any claim not found in the README or request.
- Actual result: 
- Status: NOT RUN

### MC-205
- Required for acceptance: YES
- Exact action: Render the Uncle page at 375px width in a headless browser. Measure document.documentElement.scrollWidth. Repeat with and without uncle.png, if a logo is committed.
- Expected result: scrollWidth is at most 375 in every variant. The viewport meta is present. Any img tag has non-empty alt text, and no img exists when the logo is absent.
- Evidence to capture: Measured scrollWidth for each variant and a 375px screenshot.
- Actual result: 
- Status: NOT RUN

### MC-207
- Required for acceptance: YES
- Exact action: After deploy, request https://brian.biz/, https://www.brian.biz/, https://brian.biz/blog and http://brian.biz/ in a browser or with curl -sI.
- Expected result: The home page and blog render as before. www.brian.biz is served directly with no redirect (S8). Plain HTTP still redirects to HTTPS. The brian.biz cert is still valid. This check is marked live-only.
- Evidence to capture: Status and Location headers and a screenshot of the brian.biz home page.
- Actual result: 
- Status: NOT RUN

## Resources

### MC-301
- Required for acceptance: YES
- Exclusive resources: none
- Depends on: none
- Exact action: Open the Uncle HQ page (served for Host unclehq.org) in a browser; if the logo uncle.png is referenced, observe it loads; confirm the page loads no broken images or missing assets, and the Network panel shows no failed requests.
- Expected result: Page renders fully; any logo image displays with non-empty alt text, or a text wordmark shows when no logo exists; no 404 or failed requests for page resources.
- Evidence to capture: Screenshot of the page header and the Network panel showing all requests succeeded.
- Actual result: 
- Status: NOT RUN

### MC-302
- Required for acceptance: YES
- Exclusive resources: none
- Depends on: none
- Exact action: On the Uncle HQ page, click the GitHub link for https://github.com/unclehq/uncle, the quick-start install snippet area, and the Brian credit link to https://brian.biz/.
- Expected result: The GitHub link opens the unclehq/uncle repository and the brian.biz link opens Brian's portfolio; the install snippet is visible, readable and matches the Uncle README quick start.
- Evidence to capture: Screenshots of each destination page plus the install snippet, noting the final URLs.
- Actual result: 
- Status: NOT RUN

### MC-303
- Required for acceptance: YES
- Exclusive resources: none
- Depends on: none
- Exact action: Request the brian.biz home page, /blog, and a /static asset with Host brian.biz and with Host unclehq.org (curl -H 'Host: ...' against the running app), and load /static assets in a browser.
- Expected result: brian.biz Host returns the portfolio home page; /blog and /static assets return the same status and content under both Hosts, unchanged from before the change.
- Evidence to capture: Status lines and body checksums or titles for each Host and path pair.
- Actual result: 
- Status: NOT RUN

## Regressions

### MC-402
- Required for acceptance: YES
- Exclusive resources: none
- Depends on: none
- Exact action: Open /blog and one blog post under both Host brian.biz and Host unclehq.org (curl with -H Host: or a hosts override) and click the nav links.
- Expected result: Blog index and post render identically under both Hosts with the same status and body, and the nav links work.
- Evidence to capture: Status codes and screenshots of /blog and one post under each Host.
- Actual result: 
- Status: NOT RUN

### MC-403
- Required for acceptance: YES
- Exclusive resources: none
- Depends on: none
- Exact action: Request an existing /static asset and /resume.pdf under Host brian.biz and under Host unclehq.org, and open one /api health path under Host brian.biz.
- Expected result: The static asset and resume return 200 with identical content under both Hosts, and the API path responds as it did before the change.
- Evidence to capture: Status lines and content-length or hash values for each request.
- Actual result: 
- Status: NOT RUN

### MC-404
- Required for acceptance: YES
- Exclusive resources: none
- Depends on: none
- Exact action: Send GET / with Host values unclehq.org, UNCLEHQ.ORG:8080, unclehq.org., an empty Host, [::1], unclehq.org:80:80 and evil.com, then HEAD / with Host unclehq.org.
- Expected result: The first three GETs and HEAD return 200 with the Uncle HQ page (title Uncle HQ); the other Hosts return the brian home page. None returns an error status.
- Evidence to capture: Table of Host, status and page title for every request.
- Actual result: 
- Status: NOT RUN

### MC-405
- Required for acceptance: NO
- Exclusive resources: none
- Depends on: none
- Exact action: After DNS and cert setup, run curl -sI against https://www.brian.biz/ and http://brian.biz/ and open https://brian.biz/ in a browser.
- Expected result: www.brian.biz is still served directly with no redirect, HTTP still redirects to HTTPS, and the HTTPS home page loads with its security headers and valid cert.
- Evidence to capture: curl header output and a screenshot of https://brian.biz/.
- Actual result: 
- Status: NOT RUN
