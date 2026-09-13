#!/bin/zsh
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p certs
KEY="certs/jeremy-wallet-private-key.pem"
CSR="certs/JeremyWallet.certSigningRequest"
if [[ -e "$KEY" || -e "$CSR" ]]; then
  echo "Refusing to overwrite an existing private key or CSR. Move certs/ out of the way first if you intentionally want a new key."
  exit 1
fi
openssl genrsa -out "$KEY" 2048
openssl req -new -key "$KEY" -out "$CSR" -subj "/emailAddress=jgonzalez@sihonda.com/CN=Jeremy Gonzalez Wallet Pass/C=US"
chmod 600 "$KEY"
echo "Created:"
echo "  $KEY"
echo "  $CSR"
echo
echo "Keep the private key PRIVATE. Upload only the .certSigningRequest file to Apple Developer when creating the Pass Type ID certificate."
