#!/usr/bin/env python3
from __future__ import annotations
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = ROOT / "packages/ro-asd-keyring/VERSION.yaml"
SPEC = ROOT / "packages/ro-asd-keyring/ro-asd-keyring.spec"
RPM_KEY = ROOT / "packages/ro-asd-keyring/RPM-GPG-KEY-ro-asd"
META_KEY = ROOT / "packages/ro-asd-keyring/REPODATA-GPG-KEY-ro-asd"

def load(path: Path) -> dict[str, str]:
    data={}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line=raw.strip()
        if not line or line.startswith("#"):
            continue
        key,value=(part.strip() for part in line.split(":",1))
        data[key]=value
    return data

def fpr(path: Path) -> str:
    out=subprocess.check_output(
        ["gpg","--batch","--show-keys","--with-colons",str(path)],
        text=True,
    )
    fingerprints=[
        line.split(":")[9]
        for line in out.splitlines()
        if line.startswith("fpr:")
    ]
    if len(fingerprints) < 2:
        raise ValueError(f"{path.name}: expected primary + signing subkey fingerprint")
    return fingerprints[-1]

def spec_value(text: str, field: str) -> str:
    match=re.search(rf"^{field}:\s+(\S+)\s*$", text, flags=re.MULTILINE)
    if not match:
        raise ValueError(f"spec missing {field}")
    return match.group(1)

def main() -> int:
    try:
        values=load(VERSION)
        if values.get("schema_version") != "1":
            raise ValueError("unsupported keyring VERSION schema")
        if values.get("component") != "ro-asd-keyring":
            raise ValueError("wrong component")
        if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", values.get("component_version","")):
            raise ValueError("component_version must be SemVer")
        if values.get("component_release") != "1":
            raise ValueError("initial component_release must be 1")
        if values.get("fedora_release") != "44":
            raise ValueError("Fedora release must be 44")

        spec=SPEC.read_text(encoding="utf-8")
        if spec_value(spec,"Version") != values["component_version"]:
            raise ValueError("spec Version mismatch")
        if spec_value(spec,"Release") != values["component_release"] + "%{?dist}":
            raise ValueError("spec Release mismatch")

        if fpr(RPM_KEY) != values["rpm_signing_fingerprint"]:
            raise ValueError("RPM signing public key fingerprint mismatch")
        if fpr(META_KEY) != values["metadata_signing_fingerprint"]:
            raise ValueError("metadata signing public key fingerprint mismatch")
        if RPM_KEY.read_bytes() == META_KEY.read_bytes():
            raise ValueError("RPM and metadata public keys must be distinct")
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"HATA: {error}", file=sys.stderr)
        return 1
    print("OK: ro-asd-keyring version and public key fingerprints are pinned")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
