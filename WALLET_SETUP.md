# Jeremy Gonzalez Apple Wallet Pass — Setup

This build already contains:

- A polished **Add Jeremy to Apple Wallet** button directly under **Save My Contact**.
- A generic Jeremy contact-pass template.
- Honda of Staten Island location relevance at approximately **40.597599, -74.083603**.
- A QR code on the pass that returns to Jeremy's contact site.
- A private local pass generator for **Customer name → Honda model → trim → visit/date → Generate**.
- Scripts that sign the pass locally on your Mac.

## Why one Apple step is still required

Apple Wallet will only accept a `.pkpass` that is signed with an Apple-issued **Pass Type ID certificate** tied to your Apple Developer team. The certificate and its private key cannot be fabricated or embedded by somebody else.

The website is intentionally safe before setup: if `wallet/Jeremy_Gonzalez.pkpass` is not present yet, tapping the Wallet button shows a short setup message instead of sending a customer to a broken file.

## 1. Create the CSR on your Mac

Open Terminal, drag this site's `wallet` folder into Terminal after typing `cd `, press Return, then run:

```bash
./create_csr.sh
```

This creates:

- `wallet/certs/jeremy-wallet-private-key.pem` — **KEEP PRIVATE**
- `wallet/certs/JeremyWallet.certSigningRequest` — upload this to Apple

Never upload the `.pem` private key to GitHub.

## 2. Create a Pass Type ID in Apple Developer

In **Certificates, Identifiers & Profiles**:

1. Open **Identifiers**.
2. Click **+**.
3. Choose **Pass Type IDs**.
4. Description: `Jeremy Gonzalez Contact Pass`
5. Suggested identifier: `pass.com.jeremyagonzalez1997.contact`
6. Register it.

Then open **Certificates** → **+** → **Pass Type ID Certificate**, choose the ID above, and upload `JeremyWallet.certSigningRequest`.

Download the issued certificate and rename it:

`pass.cer`

Put it in:

`wallet/certs/pass.cer`

## 3. Download Apple's WWDR G4 certificate

Apple currently associates **Pass Type ID** certificates with the **Worldwide Developer Relations G4** intermediate certificate.

Download the WWDR G4 certificate from Apple's PKI / certificate-authority site, rename it:

`AppleWWDRCAG4.cer`

and place it in:

`wallet/certs/AppleWWDRCAG4.cer`

## 4. Build the public Jeremy pass

From the `wallet` folder run:

```bash
python3 build_pass.py
```

Successful output creates:

`wallet/Jeremy_Gonzalez.pkpass`

Do not upload the `wallet/certs` folder to GitHub. Upload the signed `.pkpass`, pass assets/scripts only if you want them public, and your updated site files.

## 5. GitHub Pages

Your site button points to:

`wallet/Jeremy_Gonzalez.pkpass`

GitHub Pages uses `mime-db` for content types, and `.pkpass` is mapped to `application/vnd.apple.pkpass`, which is the MIME type Safari/Wallet expects.

After uploading the signed pass, open your live site on an iPhone and tap **Add Jeremy to Apple Wallet**. You should immediately see Apple's Wallet-add sheet.

## Location relevance

The generic pass contains the dealership location without a `relevantDate`, so Apple can consider it relevant whenever the customer is near Honda of Staten Island. Apple controls exactly when the Lock Screen suggestion appears; a pass can't force a notification every time somebody enters a fixed radius.

## Private personalized-pass generator

Do **not** upload `private-wallet-generator` to the public website if you want to keep it private.

After certificates are configured:

1. Open `private-wallet-generator`.
2. Double-click `run_generator.command`.
3. Your browser opens a local-only tool at `127.0.0.1:8787`.
4. Enter:
   - Customer name
   - Honda model
   - Trim
   - Visit/date
5. Click **Generate Apple Wallet Pass**.

The tool creates a separately signed pass with a unique serial number. It still has Honda of Staten Island location relevance; if a visit/date is supplied, that date is added as Apple Wallet relevance metadata too.

The generator runs locally on your Mac and does not upload customer data anywhere.

## Security

Never commit or upload any of these files to GitHub:

- `jeremy-wallet-private-key.pem`
- any exported `.p12` file
- any other private signing key

The `.cer` public certificate is not secret, but keeping all certificate material out of the public repository is the cleanest workflow.
