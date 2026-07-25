#!/usr/bin/env python3
"""Validate VERSION.yaml and its agreement with the first RPM spec."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from version_lib import load_version, validate_version


def spec_value(spec: str, field: str) -> str:
    match = re.search(rf"^{field}:\s+(\S+)\s*$", spec, flags=re.MULTILINE)
    if not match:
        raise ValueError(f"spec içinde {field} bulunamadı")
    return match.group(1)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    try:
        values = load_version(root / "VERSION.yaml")
        validate_version(values)
        spec = (
            root / "packages/ro-asd-release/ro-asd-release.spec"
        ).read_text(encoding="utf-8")
        if spec_value(spec, "Version") != values["component_version"]:
            raise ValueError("spec Version ile VERSION.yaml component_version uyuşmuyor")
        if spec_value(spec, "Release") != f'{values["component_release"]}%{{?dist}}':
            raise ValueError("spec Release ile VERSION.yaml component_release uyuşmuyor")
        forbidden = [
            "/usr/lib/os-release",
            "system-release",
            "RPM-GPG-KEY",
            ".repo",
        ]
        for token in forbidden:
            if token in spec:
                raise ValueError(f"ilk metadata spec'i yasak kapsam içeriyor: {token}")
    except (OSError, ValueError) as error:
        print(f"HATA: {error}", file=sys.stderr)
        return 1
    print("OK: VERSION.yaml ve ro-asd-release.spec uyumlu")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
