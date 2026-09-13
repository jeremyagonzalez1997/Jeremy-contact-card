Jeremy Gonzalez Professional NFC Site — v10.15 Fast Scheduling + Internal Alert

PUBLIC WEBSITE PACKAGE

Includes:
- Branded JG logo, site icon, and social thumbnail
- Save Contact
- Facebook + TikTok
- Fast private Google Calendar test-drive scheduler
- Optional customer email field for Jeremy's reference only
- New and Pre-Owned inventory
- Google Review
- Visit Me / directions / sales hours

FAST SCHEDULING FLOW
1. Browser quietly warms the Google Apps Script endpoint before booking.
2. Customer chooses a vehicle, date, and 30-minute start time.
3. Confirm Test Drive sends the booking to the stable Apps Script endpoint.
4. Google Calendar event creation is the only server operation the customer waits for.
5. As soon as Calendar confirms the event, the website shows success.
6. Jeremy's internal appointment email is fired immediately in a separate background request.
7. Calendar reminder setup happens after the email has already been handed to Google's mail service.

EMAIL BEHAVIOR
- Customer receives NO automatic scheduler email.
- Customer is NOT added as a Google Calendar guest.
- Jeremy receives one styled appointment alert at the private scheduler Gmail address.
- Subject format: NEW TEST DRIVE BOOKED · Customer Name · Day, Mon Date at Time
- Customer email is optional and, if entered, is shown only inside Jeremy's internal appointment details.
- No sihonda.com Gmail sender alias is required.

RELIABILITY
- Booking requests use idempotency + locking to reduce duplicate Calendar events.
- Internal notification retries are deduplicated by booking ID.
- A fast background fallback retries the internal notification if Google's first response is slow.
- Calendar reminder retries are separately deduplicated.

BACKEND
- scheduler-config.js contains the current production /exec endpoint.
- Future website-only updates should preserve this endpoint.
- Do not upload the private Apps Script package to GitHub.
