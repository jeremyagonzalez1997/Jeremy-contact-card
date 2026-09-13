#!/usr/bin/env python3
import argparse, hashlib, json, os, re, shutil, subprocess, tempfile, zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
TEMPLATE = BASE / "pass-template"
DEFAULT_OUT = BASE / "Jeremy_Gonzalez.pkpass"


def run(cmd, **kwargs):
    return subprocess.run(cmd, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)


def cert_to_pem(cert_path: Path, out_path: Path):
    data = cert_path.read_bytes()
    if b"BEGIN CERTIFICATE" in data:
        out_path.write_bytes(data)
    else:
        subprocess.run(["openssl", "x509", "-inform", "DER", "-in", str(cert_path), "-out", str(out_path)], check=True)


def cert_subject(cert_pem: Path):
    return run(["openssl", "x509", "-in", str(cert_pem), "-noout", "-subject", "-nameopt", "RFC2253"]).stdout.strip()


def extract_ids(subject: str):
    # Apple's Pass Type ID certificate subject normally carries UID=<pass id> and OU=<team id>.
    m_uid = re.search(r"(?:^|,)UID=([^,]+)", subject)
    m_ou = re.search(r"(?:^|,)OU=([^,]+)", subject)
    return (m_uid.group(1) if m_uid else None, m_ou.group(1) if m_ou else None)


def build(args):
    cert = Path(args.certificate).expanduser().resolve()
    key = Path(args.key).expanduser().resolve()
    wwdr = Path(args.wwdr).expanduser().resolve()
    out = Path(args.output).expanduser().resolve()
    for p, label in [(cert,"Pass Type certificate"),(key,"private key"),(wwdr,"Apple WWDR G4 certificate")]:
        if not p.exists(): raise SystemExit(f"Missing {label}: {p}")

    with tempfile.TemporaryDirectory(prefix="jeremy-wallet-") as td:
        td = Path(td)
        work = td / "pass"
        shutil.copytree(TEMPLATE, work)
        cert_pem = td / "pass-cert.pem"
        wwdr_pem = td / "wwdr.pem"
        cert_to_pem(cert, cert_pem)
        cert_to_pem(wwdr, wwdr_pem)
        subject = cert_subject(cert_pem)
        detected_pass_id, detected_team_id = extract_ids(subject)
        pass_id = args.pass_type_id or detected_pass_id
        team_id = args.team_id or detected_team_id
        if not pass_id or not team_id:
            raise SystemExit("Could not detect Pass Type ID / Team ID from certificate. Re-run with --pass-type-id and --team-id.")

        pass_path = work / "pass.json"
        data = json.loads(pass_path.read_text())
        data["passTypeIdentifier"] = pass_id
        data["teamIdentifier"] = team_id
        pass_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

        manifest = {}
        for p in sorted(work.rglob("*")):
            if p.is_file() and p.name not in ("manifest.json", "signature"):
                rel = p.relative_to(work).as_posix()
                manifest[rel] = hashlib.sha1(p.read_bytes()).hexdigest()
        (work / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")))

        subprocess.run([
            "openssl", "smime", "-binary", "-sign",
            "-certfile", str(wwdr_pem),
            "-signer", str(cert_pem),
            "-inkey", str(key),
            "-in", str(work / "manifest.json"),
            "-out", str(work / "signature"),
            "-outform", "DER"
        ], check=True)

        out.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for p in sorted(work.rglob("*")):
                if p.is_file(): z.write(p, p.relative_to(work).as_posix())
        print(f"Built signed Apple Wallet pass: {out}")
        print(f"Pass Type ID: {pass_id}")
        print(f"Team ID: {team_id}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Build Jeremy Gonzalez Apple Wallet pass")
    ap.add_argument("--certificate", default=str(BASE/"certs/pass.cer"), help="Apple Pass Type ID certificate (.cer or PEM)")
    ap.add_argument("--key", default=str(BASE/"certs/jeremy-wallet-private-key.pem"), help="Private key used for the CSR")
    ap.add_argument("--wwdr", default=str(BASE/"certs/AppleWWDRCAG4.cer"), help="Apple WWDR G4 intermediate certificate")
    ap.add_argument("--output", default=str(DEFAULT_OUT))
    ap.add_argument("--pass-type-id")
    ap.add_argument("--team-id")
    build(ap.parse_args())
