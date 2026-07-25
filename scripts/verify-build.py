#!/usr/bin/env python3
"""Verify checksums and the minimum Fedora 44 RPM/SRPM output contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def rpm_query(path: Path) -> tuple[str, str, str, str, str]:
    query = "%{NAME}\\n%{EPOCHNUM}\\n%{VERSION}\\n%{RELEASE}\\n%{ARCH}\\n"
    output = subprocess.check_output(
        ["rpm", "-qp", "--qf", query, str(path)], text=True
    )
    values = tuple(output.strip().splitlines())
    if len(values) != 5:
        raise ValueError(f"{path}: RPM metadata okunamadı")
    return values  # type: ignore[return-value]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact_dir", type=Path)
    args = parser.parse_args()
    try:
        manifest_path = args.artifact_dir / "component-artifact-manifest-v1.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("schema_version") != "component-artifact-manifest-v1":
            raise ValueError("manifest schema_version geçersiz")
        if manifest.get("build", {}).get("fedora_release") != 44:
            raise ValueError("manifest Fedora 44 değil")

        artifacts = manifest.get("artifacts")
        if not isinstance(artifacts, list):
            raise ValueError("manifest artifacts dizisi eksik")
        binaries: set[tuple[str, str, str]] = set()
        sources: set[tuple[str, str, str]] = set()
        for artifact in artifacts:
            path = args.artifact_dir / artifact["filename"]
            if not path.is_file():
                raise ValueError(f"manifest dosyası bulunamadı: {path.name}")
            name, _epoch, version, release, rpm_arch = rpm_query(path)
            arch = "src" if path.name.endswith(".src.rpm") else rpm_arch
            expected_filename = f"{name}-{version}-{release}.{arch}.rpm"
            if path.name != expected_filename:
                raise ValueError(f"kanonik olmayan RPM adı: {path.name}")
            if artifact["sha256"] != sha256(path):
                raise ValueError(f"SHA-256 uyuşmuyor: {path.name}")
            if artifact["size"] != path.stat().st_size:
                raise ValueError(f"dosya boyutu uyuşmuyor: {path.name}")
            source_name = artifact.get("source_name")
            if source_name != "ro-asd-release":
                raise ValueError(f"beklenmeyen kaynak paket adı: {source_name}")
            key = (source_name, version, release)
            if arch == "src":
                sources.add((name, version, release))
            elif arch in {"x86_64", "noarch"}:
                binaries.add(key)
            else:
                raise ValueError(f"ilk beta için desteklenmeyen mimari: {arch}")
        if not binaries:
            raise ValueError("ikili veya noarch RPM eksik")
        if binaries - sources:
            raise ValueError("ikili RPM ile eşleşen SRPM eksik")

        expected_checksums = {
            line.split(maxsplit=1)[1].lstrip("*"): line.split(maxsplit=1)[0]
            for line in (args.artifact_dir / "SHA256SUMS")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        }
        rpm_names = {path.name for path in args.artifact_dir.glob("*.rpm")}
        if expected_checksums.keys() != rpm_names:
            raise ValueError("SHA256SUMS ile RPM dosya kümesi uyuşmuyor")
        for name, digest in expected_checksums.items():
            if sha256(args.artifact_dir / name) != digest:
                raise ValueError(f"SHA256SUMS doğrulaması başarısız: {name}")
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"HATA: {error}", file=sys.stderr)
        return 1
    print("OK: Fedora 44 RPM, SRPM, checksum ve manifest çıktıları tutarlı")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
