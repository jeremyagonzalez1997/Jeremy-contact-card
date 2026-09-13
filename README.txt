Jeremy Gonzalez — Professional NFC Contact Site + Apple Wallet

This build is a static, mobile-first contact and sales landing page for Jeremy Gonzalez at Honda of Staten Island.

Included:
- Save My Contact vCard
- Add Jeremy to Apple Wallet button directly under Save My Contact
- Apple Wallet generic contact-pass template
- Dealership location relevance metadata for the Wallet pass
- Tap-to-call, text, and work email
- Facebook and TikTok links
- New Honda inventory link
- Pre-Owned inventory link
- Google Review link
- Honda of Staten Island map and device-aware directions
- Live dealership sales-hours display
- Jeremy profile photo
- Private local personalized Wallet generator: Customer name -> Honda model -> trim -> visit/date -> Generate

Important:
Apple requires every Wallet pass to be cryptographically signed with an Apple-issued Pass Type ID certificate. The public site is already wired for `wallet/Jeremy_Gonzalez.pkpass`, but you must complete the certificate/signing steps in WALLET_SETUP.md before the button can actually add the pass to Wallet.

Scheduling / appointment functionality remains completely removed. There is no appointment form, calendar integration, Google Apps Script connection, scheduler configuration, or booking backend.

For GitHub Pages:
- Upload the public site files.
- Do NOT upload `wallet/certs/` or `private-wallet-generator/` if you want the generator to stay private.
- After signing, upload `wallet/Jeremy_Gonzalez.pkpass`.
