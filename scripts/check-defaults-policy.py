#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "packages/ro-asd-defaults"
VERSION = PKG / "VERSION.yaml"
POLICY = PKG / "defaults-policy-v1.json"
PAYLOADS = PKG / "PAYLOADS.json"
SPEC = PKG / "ro-asd-defaults.spec"

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
        if version.get("component") != "ro-asd-defaults":
            raise ValueError("wrong component")
        if version.get("fedora_release") != "44":
            raise ValueError("Fedora release must be 44")

        spec = SPEC.read_text(encoding="utf-8")
        if spec_value(spec, "Version") != version["component_version"]:
            raise ValueError("spec Version mismatch")
        if spec_value(spec, "Release") != version["component_release"] + "%{?dist}":
            raise ValueError("spec Release mismatch")

        policy = json.loads(POLICY.read_text(encoding="utf-8"))
        payloads = json.loads(PAYLOADS.read_text(encoding="utf-8"))
        if policy["schema_version"] != 1 or policy["component"] != "ro-asd-defaults":
            raise ValueError("policy identity mismatch")
        if policy["fedora_release"] != 44:
            raise ValueError("policy Fedora release mismatch")
        if policy["configuration_model"] != "xdg-cascade":
            raise ValueError("defaults must use xdg-cascade")
        principles = policy["principles"]
        for field in ("write_user_home", "use_etc_skel", "immutable_kconfig"):
            if principles[field] is not False:
                raise ValueError(f"{field} must remain false")
        if principles["config_files_noreplace"] is not True:
            raise ValueError("config_files_noreplace must remain true")
        if principles["preserve_user_overrides"] is not True:
            raise ValueError("preserve_user_overrides must remain true")

        forbidden_exact = set(policy["forbidden_exact_paths"])
        forbidden_prefixes = tuple(policy["forbidden_path_prefixes"])
        delegated = set(policy["temporarily_delegated_paths"])
        if payloads["schema_version"] != 1 or payloads["component"] != "ro-asd-defaults":
            raise ValueError("payload manifest identity mismatch")

        seen = set()
        for item in payloads["payloads"]:
            path = item["path"]
            if not path.startswith("/"):
                raise ValueError(f"payload must be absolute: {path}")
            if path in seen:
                raise ValueError(f"duplicate payload path: {path}")
            seen.add(path)
            if path in forbidden_exact or path in delegated or path.startswith(forbidden_prefixes):
                raise ValueError(f"forbidden or delegated payload path: {path}")
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as error:
        print(f"HATA: {error}", file=sys.stderr)
        return 1

    print("OK: ro-asd-defaults ownership contract is fail-closed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
