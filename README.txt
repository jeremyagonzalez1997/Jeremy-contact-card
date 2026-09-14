Jeremy Gonzalez Professional NFC Site v10.17 — Dual Confirmation Scheduler

Upload the CONTENTS of this folder to the root of the GitHub repository used by GitHub Pages.

Important:
- Keep scheduler-config.js in the repo. It contains the stable public Apps Script Web App endpoint.
- Do NOT upload the private Apps Script Code.gs package to this public repo.
- v10.17 sends the booking only once and confirms it through two independent paths at the same time: Google's direct HtmlService response and a read-only JSONP status endpoint. Whichever succeeds first completes the customer flow.
- Jeremy's internal appointment email is sent server-side immediately after the Calendar event is created. The website does not make a second email request.
- scheduler-test.html is a harmless connection test. After deploying the new Apps Script backend, open /scheduler-test.html on the GitHub Pages site. It should report Connected and backend version 10.10.
