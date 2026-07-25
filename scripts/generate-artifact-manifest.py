#!/usr/bin/env python3
"""Create a component artifact manifest from built RPM files."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

from version_lib import load_version, validate_version

BUILDER_IMAGE = (
    "registry.fedoraproject.org/fedora:44@"
    "sha256:c64fc79f4a12dd4625d8cba9f7d242ac17c823bdeecc6d650234ebbf5f0ca81b"
)


def command(*arguments: str) -> str:
    return subprocess.check_output(arguments, text=True).strip()


def rpm_metadata(path: Path) -> dict[str, object]:
    query = "%{NAME}\\n%{EPOCHNUM}\\n%{VERSION}\\n%{RELEASE}\\n%{ARCH}\\n"
    values = command("rpm", "-qp", "--qf", query, str(path)).splitlines()
    if len(values) != 5:
        raise ValueError(f"{path}: beklenmeyen RPM sorgu çıktısı")
    name, epoch, version, release, rpm_arch = values
    artifact_type = "srpm" if path.name.endswith(".src.rpm") else "rpm"
    arch = "src" if artifact_type == "srpm" else rpm_arch
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "type": artifact_type,
        "filename": path.name,
        "name": name,
        "source_name": "ro-asd-release",
        "epoch": int(epoch),
        "version": version,
        "release": release,
        "arch": arch,
        "size": path.stat().st_size,
        "sha256": digest,
    }


def nullable_env(name: str) -> str | None:
    value = os.environ.get(name)
    return value if value else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--artifact-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    values = load_version(args.repo_root / "VERSION.yaml")
    validate_version(values)
    artifacts = [
        rpm_metadata(path)
        for path in sorted(args.artifact_dir.glob("*.rpm"), key=lambda item: item.name)
    ]
    if not artifacts:
        raise ValueError("manifest için RPM/SRPM bulunamadı")

    commit = os.environ.get("SOURCE_COMMIT") or command(
        "git", "-C", str(args.repo_root), "rev-parse", "HEAD"
    )
    tag = nullable_env("SOURCE_TAG")
    release_url = nullable_env("SOURCE_RELEASE_URL")
    run_id = nullable_env("GITHUB_RUN_ID")
    run_url = (
        f"https://github.com/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{run_id}"
        if run_id and os.environ.get("GITHUB_REPOSITORY")
        else None
    )
    build_kind = "release" if tag and release_url else "ci"
    manifest = {
        "schema_version": values["component_artifact_manifest"],
        "component": {
            "name": "ro-asd-release",
            "version": values["component_version"],
        },
        "source": {
            "repository": "https://github.com/Project-Ro-ASD/Ro-ASD-release",
            "commit": commit,
            "tag": tag,
            "release_url": release_url,
        },
        "build": {
            "kind": build_kind,
            "fedora_release": int(values["fedora_release"]),
            "workflow_run_id": run_id,
            "workflow_run_url": run_url,
            "builder_image": BUILDER_IMAGE,
        },
        "artifacts": artifacts,
    }
    args.output.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
