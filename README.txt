Jeremy Gonzalez Professional NFC Site — v10.12 Branded Scheduling Restored

PUBLIC WEBSITE PACKAGE

Includes:
- Branded JG logo, site icon, and social thumbnail
- Save Contact
- Facebook + TikTok
- Fast private Google Calendar test-drive scheduler
- New and Pre-Owned inventory
- Google Review
- Visit Me / directions / sales hours

SCHEDULER ARCHITECTURE
- The website uses scheduler-config.js for the stable Google Apps Script /exec endpoint.
- The endpoint is already configured.
- Do NOT upload the private Apps Script package to GitHub.
- The public website does not contain Jeremy's private scheduling Gmail address.
- Future website-only updates do not require any Apps Script changes. Keep scheduler-config.js unchanged.
- Only redeploy Apps Script when Code.gs itself changes. Update the EXISTING deployment so the same /exec URL continues working.

FAST / RELIABLE FLOW
1. Customer chooses a vehicle, date, and 30-minute start time.
2. Calendar event creation is the success authority.
3. Customer sees confirmation as soon as Google Calendar confirms the event.
4. Jeremy's internal notification email runs separately and never blocks the customer confirmation screen.
5. Notification delivery uses a verified request plus a keepalive fallback; the backend deduplicates retries.
6. Backend locking reduces duplicate events/emails from double taps or network retries.

CUSTOMER PRIVACY
- Customer is not added as a Google Calendar guest.
- Customer receives no scheduler email from the private Gmail account.
- Optional customer email is contact information only.
