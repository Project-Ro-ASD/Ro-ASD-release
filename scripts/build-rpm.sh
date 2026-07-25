#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
version_file="${repo_root}/VERSION.yaml"
spec_file="${repo_root}/packages/ro-asd-release/ro-asd-release.spec"
dist_dir="${repo_root}/dist"
mkdir -p "${repo_root}/build"
work_dir="$(mktemp -d "${repo_root}/build/rpm.XXXXXX")"
trap 'rm -rf -- "${work_dir}"' EXIT

python3 "${repo_root}/scripts/check-version.py"

component_version="$(
  awk '$1 == "component_version:" { print $2 }' "${version_file}"
)"
source_name="ro-asd-release-${component_version}"
topdir="${work_dir}/rpmbuild"
source_dir="${work_dir}/${source_name}"

mkdir -p \
  "${topdir}/BUILD" \
  "${topdir}/BUILDROOT" \
  "${topdir}/RPMS" \
  "${topdir}/SOURCES" \
  "${topdir}/SPECS" \
  "${topdir}/SRPMS" \
  "${source_dir}" \
  "${dist_dir}"

find "${dist_dir}" -maxdepth 1 -type f \
  \( -name '*.rpm' -o -name 'SHA256SUMS' -o -name '*manifest-v1.json' \) \
  -delete

install -m 0644 "${repo_root}/LICENSE" "${source_dir}/LICENSE"
install -m 0644 "${repo_root}/README.md" "${source_dir}/README.md"
python3 "${repo_root}/scripts/render-release-metadata.py" \
  --version-file "${version_file}" \
  --output-dir "${source_dir}"

tar \
  --sort=name \
  --mtime='@0' \
  --owner=0 \
  --group=0 \
  --numeric-owner \
  -C "${work_dir}" \
  -czf "${topdir}/SOURCES/${source_name}.tar.gz" \
  "${source_name}"
install -m 0644 "${spec_file}" "${topdir}/SPECS/ro-asd-release.spec"

rpmbuild -ba \
  --define "_topdir ${topdir}" \
  --define "_tmppath ${work_dir}/tmp" \
  --define "dist .fc44" \
  "${topdir}/SPECS/ro-asd-release.spec"

find "${topdir}/RPMS" "${topdir}/SRPMS" -type f -name '*.rpm' \
  -exec cp -p -- '{}' "${dist_dir}/" \;

(
  cd "${dist_dir}"
  find . -maxdepth 1 -type f -name '*.rpm' -printf '%f\n' \
    | LC_ALL=C sort \
    | xargs -r sha256sum
) > "${dist_dir}/SHA256SUMS"

python3 "${repo_root}/scripts/generate-artifact-manifest.py" \
  --repo-root "${repo_root}" \
  --artifact-dir "${dist_dir}" \
  --output "${dist_dir}/component-artifact-manifest-v1.json"

echo "Çıktılar: ${dist_dir}"
