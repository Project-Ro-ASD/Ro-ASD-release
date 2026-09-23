#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "packages/ro-asd-desktop-standard"
VERSION = PKG / "VERSION.yaml"
CONTRACT = PKG / "desktop-standard-profile-v1.json"
PAYLOADS = PKG / "PAYLOADS.json"
SPEC = PKG / "ro-asd-desktop-standard.spec"

EXPECTED_REQUIRED = {
    "ro-asd-release": "0.1.2",
    "ro-asd-keyring": "0.1.0",
    "ro-asd-repos": "0.1.0",
    "ro-asd-defaults": "0.1.0",
    "ro-asd-branding": "0.1.0",
}

def load_version(path: Path) -> dict[str, str]:
    values = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        values[key] = value
    return values

def main() -> int:
    try:
        version = load_version(VERSION)
        if version.get("component") != "ro-asd-desktop-standard":
            raise ValueError("wrong component")
        if version.get("fedora_release") != "44":
            raise ValueError("Fedora release must be 44")

        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        if contract["schema_version"] != 1:
            raise ValueError("unsupported profile schema")
        if contract["component"] != "ro-asd-desktop-standard":
            raise ValueError("profile component mismatch")
        if contract["profile"] != "desktop-standard":
            raise ValueError("profile name mismatch")
        if contract["fedora_release"] != 44:
            raise ValueError("profile Fedora release mismatch")

        required = {
            item["name"]: item["minimum_version"]
            for item in contract["required_components"]
        }
        if required != EXPECTED_REQUIRED:
            raise ValueError(f"unexpected required component set: {required}")

        principles = contract["principles"]
        for field in (
            "duplicate_fedora_kde_package_set",
            "require_pending_integrations",
            "own_user_configuration",
            "own_kernel_policy",
            "own_theme_assets",
        ):
            if principles[field] is not False:
                raise ValueError(f"{field} must remain false in profile v1")

        spec = SPEC.read_text(encoding="utf-8")
        for package, minimum in EXPECTED_REQUIRED.items():
            pattern = rf"^Requires:\s+{re.escape(package)}\s+>=\s+{re.escape(minimum)}\s*$"
            if not re.search(pattern, spec, flags=re.MULTILINE):
                raise ValueError(f"missing exact Requires for {package}")

        forbidden_requires = (
            "plasma-desktop",
            "plasma-workspace",
            "plasma-login-manager",
            "dolphin",
            "konsole",
            "ro-theme",
            "ro-assist",
            "ro-control",
            "ro-asd-kernel-policy",
        )
        requires_lines = [
            line.strip() for line in spec.splitlines()
            if line.strip().startswith("Requires:")
        ]
        for package in forbidden_requires:
            if any(re.search(rf"\b{re.escape(package)}\b", line) for line in requires_lines):
                raise ValueError(f"forbidden hard dependency in v1: {package}")

        payloads = json.loads(PAYLOADS.read_text(encoding="utf-8"))
        expected_path = "/usr/share/ro-asd/profiles/desktop-standard-profile-v1.json"
        paths = [item["path"] for item in payloads["payloads"]]
        if paths != [expected_path]:
            raise ValueError(f"unexpected payloads: {paths}")
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as error:
        print(f"HATA: {error}", file=sys.stderr)
        return 1

    print("OK: ro-asd-desktop-standard profile contract is fail-closed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
