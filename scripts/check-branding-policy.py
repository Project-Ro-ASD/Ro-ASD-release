#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "packages/ro-asd-branding"
VERSION = PKG / "VERSION.yaml"
CONTRACT = PKG / "branding-contract-v1.json"
PAYLOADS = PKG / "PAYLOADS.json"
SPEC = PKG / "ro-asd-branding.spec"

def load_version(path: Path) -> dict[str, str]:
    result = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        result[key] = value
    return result

def spec_value(text: str, field: str) -> str:
    match = re.search(rf"^{field}:\s+(\S+)\s*$", text, flags=re.MULTILINE)
    if not match:
        raise ValueError(f"spec missing {field}")
    return match.group(1)

def main() -> int:
    try:
        version = load_version(VERSION)
        if version.get("schema_version") != "1":
            raise ValueError("unsupported VERSION schema")
        if version.get("component") != "ro-asd-branding":
            raise ValueError("wrong component")
        if version.get("fedora_release") != "44":
            raise ValueError("Fedora release must be 44")

        spec = SPEC.read_text(encoding="utf-8")
        if spec_value(spec, "Version") != version["component_version"]:
            raise ValueError("spec Version mismatch")
        if spec_value(spec, "Release") != version["component_release"] + "%{?dist}":
            raise ValueError("spec Release mismatch")

        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        payloads = json.loads(PAYLOADS.read_text(encoding="utf-8"))
        if contract["schema_version"] != 1 or contract["component"] != "ro-asd-branding":
            raise ValueError("branding contract identity mismatch")
        if contract["fedora_release"] != 44:
            raise ValueError("branding contract Fedora release mismatch")

        principles = contract["principles"]
        for field in (
            "replace_fedora_release_files",
            "provide_system_release",
            "overwrite_fedora_logos",
            "duplicate_theme_assets",
        ):
            if principles[field] is not False:
                raise ValueError(f"{field} must remain false")

        forbidden_exact = set(contract["reserved_exact_paths"])
        forbidden_prefixes = tuple(contract["reserved_path_prefixes"])

        if payloads["schema_version"] != 1 or payloads["component"] != "ro-asd-branding":
            raise ValueError("payload manifest identity mismatch")

        seen = set()
        for item in payloads["payloads"]:
            path = item["path"]
            if not path.startswith("/"):
                raise ValueError(f"payload must be absolute: {path}")
            if path in seen:
                raise ValueError(f"duplicate payload path: {path}")
            seen.add(path)
            if path in forbidden_exact or path.startswith(forbidden_prefixes):
                raise ValueError(f"reserved branding payload path: {path}")
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as error:
        print(f"HATA: {error}", file=sys.stderr)
        return 1

    print("OK: ro-asd-branding ownership contract is fail-closed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
