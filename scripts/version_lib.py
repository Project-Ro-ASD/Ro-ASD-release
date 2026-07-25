#!/usr/bin/env python3
"""Strict reader for the deliberately small VERSION.yaml contract."""

from __future__ import annotations

import re
from pathlib import Path

EXPECTED_KEYS = {
    "schema_version",
    "product_name",
    "product_release",
    "base_distribution",
    "fedora_release",
    "phase",
    "primary_architecture",
    "component_artifact_manifest",
    "component_version",
    "component_release",
}
KEY_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


def load_version(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"{path}:{line_number}: key: value bekleniyor")
        key, value = (part.strip() for part in line.split(":", 1))
        if not KEY_PATTERN.fullmatch(key):
            raise ValueError(f"{path}:{line_number}: geçersiz anahtar {key!r}")
        if not value:
            raise ValueError(f"{path}:{line_number}: {key} boş olamaz")
        if key in values:
            raise ValueError(f"{path}:{line_number}: yinelenen anahtar {key}")
        values[key] = value

    missing = EXPECTED_KEYS - values.keys()
    extra = values.keys() - EXPECTED_KEYS
    if missing:
        raise ValueError(f"eksik VERSION.yaml alanları: {', '.join(sorted(missing))}")
    if extra:
        raise ValueError(f"bilinmeyen VERSION.yaml alanları: {', '.join(sorted(extra))}")
    return values


def validate_version(values: dict[str, str]) -> None:
    expected = {
        "schema_version": "1",
        "product_name": "Ro-ASD",
        "product_release": "44",
        "base_distribution": "Fedora Linux",
        "fedora_release": "44",
        "phase": "development",
        "primary_architecture": "x86_64",
        "component_artifact_manifest": "component-artifact-manifest-v1",
        "component_version": "0.1.0",
        "component_release": "1",
    }
    errors = [
        f"{key}: {expected_value!r} bekleniyor, {values.get(key)!r} bulundu"
        for key, expected_value in expected.items()
        if values.get(key) != expected_value
    ]
    if errors:
        raise ValueError("; ".join(errors))
