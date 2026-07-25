#!/usr/bin/env python3
"""Render deterministic package-owned release metadata from VERSION.yaml."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from version_lib import load_version, validate_version


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version-file", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    values = load_version(args.version_file)
    validate_version(values)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    metadata = {
        "schema_version": "ro-asd-release-metadata-v1",
        "product": {
            "name": values["product_name"],
            "release": int(values["product_release"]),
            "phase": values["phase"],
        },
        "base": {
            "distribution": values["base_distribution"],
            "release": int(values["fedora_release"]),
        },
        "primary_architecture": values["primary_architecture"],
        "contracts": {
            "component_artifact_manifest": values[
                "component_artifact_manifest"
            ]
        },
    }
    (args.output_dir / "release.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    shell_metadata = "\n".join(
        [
            f'RO_ASD_NAME="{values["product_name"]}"',
            f'RO_ASD_PRODUCT_RELEASE="{values["product_release"]}"',
            f'RO_ASD_BASE_DISTRIBUTION="{values["base_distribution"]}"',
            f'RO_ASD_BASE_RELEASE="{values["fedora_release"]}"',
            f'RO_ASD_PHASE="{values["phase"]}"',
            f'RO_ASD_PRIMARY_ARCHITECTURE="{values["primary_architecture"]}"',
            (
                'RO_ASD_COMPONENT_ARTIFACT_MANIFEST="'
                f'{values["component_artifact_manifest"]}"'
            ),
        ]
    )
    (args.output_dir / "release").write_text(shell_metadata + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
