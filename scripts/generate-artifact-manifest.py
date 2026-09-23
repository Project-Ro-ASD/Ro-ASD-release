#!/usr/bin/env python3
"""Generate the canonical Ro-Repo V2 component release manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from version_lib import load_version, validate_version

REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rpm_header(path: Path) -> dict[str, object]:
    query = (
        "%{NAME}\\t%{EPOCHNUM}\\t%{VERSION}\\t%{RELEASE}\\t"
        "%{ARCH}\\t%{SOURCERPM}\\t%|SOURCEPACKAGE?{true}:{false}|"
    )
    values = subprocess.check_output(
        ["rpm", "-qp", "--qf", query, str(path)], text=True
    ).split("\t")
    if len(values) != 7:
        raise ValueError(f"{path}: beklenmeyen RPM header çıktısı")

    name, epoch, version, release, arch, source_rpm, is_source = values
    if is_source == "true":
        arch = "src"
        source_rpm = None

    return {
        "filename": path.name,
        "name": name,
        "epoch": int(epoch or 0),
        "version": version,
        "release": release,
        "architecture": arch,
        "source_rpm": source_rpm,
        "producer_artifact_sha256": sha256(path),
    }


def positive_int(value: str, field: str) -> int:
    try:
        parsed = int(value)
    except ValueError as error:
        raise ValueError(f"{field} pozitif tam sayı olmalı") from error
    if parsed <= 0:
        raise ValueError(f"{field} pozitif tam sayı olmalı")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--artifact-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--component", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--release-id", required=True)
    parser.add_argument("--workflow-run", required=True)
    args = parser.parse_args()

    values = load_version(args.repo_root / "VERSION.yaml")
    validate_version(values)

    if not REPOSITORY_RE.fullmatch(args.repository):
        raise ValueError("repository owner/name biçiminde olmalı")
    if not COMMIT_RE.fullmatch(args.commit):
        raise ValueError("commit tam 40 karakter küçük harf SHA-1 olmalı")
    if not args.tag.strip():
        raise ValueError("tag boş olamaz")
    if args.component not in {"ro-asd-release", "ro-asd-keyring", "ro-asd-repos"}:
        raise ValueError("desteklenmeyen release component'i")

    release_id = positive_int(args.release_id, "release-id")
    workflow_run = positive_int(args.workflow_run, "workflow-run")

    rpm_paths = sorted(args.artifact_dir.glob("*.rpm"), key=lambda item: item.name)
    if not rpm_paths:
        raise ValueError("release manifest için RPM/SRPM bulunamadı")

    artifacts = [rpm_header(path) for path in rpm_paths]
    package_names = {str(item["name"]) for item in artifacts}
    if package_names != {args.component}:
        raise ValueError(
            f"beklenmeyen package set: {sorted(package_names)}; "
            f"yalnız {args.component!r} bekleniyor"
        )
    if not any(item["architecture"] == "src" for item in artifacts):
        raise ValueError("SRPM eksik")
    if not any(item["architecture"] == "noarch" for item in artifacts):
        raise ValueError("noarch binary RPM eksik")

    manifest = {
        "schema_version": 1,
        "component": args.component,
        "source_repository": args.repository,
        "source_commit": args.commit,
        "release_tag": args.tag,
        "release_id": release_id,
        "workflow_run": workflow_run,
        "fedora_release": int(values["fedora_release"]),
        "artifacts": artifacts,
        "provenance": {
            "provider": "github",
            "subject_digest": "sha256",
        },
        "attestation": {
            "provider": "github",
            "verification": "gh attestation verify",
        },
    }
    args.output.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
