#!/usr/bin/env python3
from __future__ import annotations

import configparser
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = ROOT / "packages/ro-asd-repos/VERSION.yaml"
SPEC = ROOT / "packages/ro-asd-repos/ro-asd-repos.spec"
REPO = ROOT / "packages/ro-asd-repos/ro-asd.repo"

EXPECTED = {
    "ro-asd-beta": ("https://repo.ro-asd.org/rpm/fedora/44/beta/$basearch/", "1"),
    "ro-asd-beta-source": ("https://repo.ro-asd.org/rpm/fedora/44/beta/source/", "0"),
    "ro-asd-stable": ("https://repo.ro-asd.org/rpm/fedora/44/stable/$basearch/", "0"),
    "ro-asd-stable-source": ("https://repo.ro-asd.org/rpm/fedora/44/stable/source/", "0"),
}

def load_version(path: Path) -> dict[str, str]:
    data = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        data[key] = value
    return data

def spec_value(text: str, field: str) -> str:
    match = re.search(rf"^{field}:\s+(\S+)\s*$", text, flags=re.MULTILINE)
    if not match:
        raise ValueError(f"spec missing {field}")
    return match.group(1)

def main() -> int:
    try:
        values = load_version(VERSION)
        if values.get("schema_version") != "1":
            raise ValueError("unsupported repos VERSION schema")
        if values.get("component") != "ro-asd-repos":
            raise ValueError("wrong component")
        if values.get("component_version") != "0.1.0":
            raise ValueError("unexpected initial component_version")
        if values.get("component_release") != "1":
            raise ValueError("unexpected component_release")
        if values.get("fedora_release") != "44":
            raise ValueError("Fedora release must be 44")
        if values.get("public_baseurl") != "https://repo.ro-asd.org/rpm/fedora/44":
            raise ValueError("public baseurl mismatch")
        if values.get("default_channel") != "beta":
            raise ValueError("initial default channel must be beta")

        spec = SPEC.read_text(encoding="utf-8")
        if spec_value(spec, "Version") != values["component_version"]:
            raise ValueError("spec Version mismatch")
        if spec_value(spec, "Release") != values["component_release"] + "%{?dist}":
            raise ValueError("spec Release mismatch")
        if "Requires:       ro-asd-keyring >= 0.1.0" not in spec:
            raise ValueError("keyring dependency missing")

        parser = configparser.RawConfigParser(interpolation=None)
        parser.read(REPO, encoding="utf-8")
        if set(parser.sections()) != set(EXPECTED):
            raise ValueError(f"unexpected repo sections: {parser.sections()}")

        expected_keys = {
            "file:///etc/pki/rpm-gpg/REPODATA-GPG-KEY-ro-asd",
            "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-ro-asd",
        }
        for section, (baseurl, enabled) in EXPECTED.items():
            cfg = parser[section]
            if cfg.get("baseurl") != baseurl:
                raise ValueError(f"{section}: baseurl mismatch")
            if cfg.get("enabled") != enabled:
                raise ValueError(f"{section}: enabled mismatch")
            if cfg.get("gpgcheck") != "1" or cfg.get("repo_gpgcheck") != "1":
                raise ValueError(f"{section}: signature verification must be enabled")
            keys = set(cfg.get("gpgkey", "").split())
            if keys != expected_keys:
                raise ValueError(f"{section}: trust key set mismatch")
            if cfg.get("skip_if_unavailable") != "0":
                raise ValueError(f"{section}: repository must fail closed")
    except (OSError, ValueError, configparser.Error) as error:
        print(f"HATA: {error}", file=sys.stderr)
        return 1

    print("OK: ro-asd-repos URLs, defaults and trust policy are pinned")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
