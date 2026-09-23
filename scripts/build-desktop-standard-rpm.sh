#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
pkg_dir="${repo_root}/packages/ro-asd-desktop-standard"
version_file="${pkg_dir}/VERSION.yaml"
dist_dir="${repo_root}/dist"
mkdir -p "${repo_root}/build"
work_dir="$(mktemp -d "${repo_root}/build/desktop-standard.XXXXXX")"
trap 'rm -rf -- "${work_dir}"' EXIT

python3 "${repo_root}/scripts/check-desktop-standard-policy.py"

component_version="$(awk '$1 == "component_version:" { print $2 }' "${version_file}")"
source_name="ro-asd-desktop-standard-${component_version}"
topdir="${work_dir}/rpmbuild"
source_dir="${work_dir}/${source_name}"

mkdir -p "${topdir}"/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS} "${source_dir}" "${dist_dir}"

find "${dist_dir}" -maxdepth 1 -type f \
  \( -name '*.rpm' -o -name 'SHA256SUMS' -o -name '*manifest-v1.json' \) -delete

install -m 0644 "${repo_root}/LICENSE" "${source_dir}/LICENSE"
install -m 0644 "${repo_root}/README.md" "${source_dir}/README.md"
install -m 0644 "${repo_root}/docs/DESKTOP-STANDARD-PROFILE-V1.md" "${source_dir}/DESKTOP-STANDARD-PROFILE-V1.md"
install -m 0644 "${pkg_dir}/desktop-standard-profile-v1.json" "${source_dir}/desktop-standard-profile-v1.json"

tar --sort=name --mtime='@0' --owner=0 --group=0 --numeric-owner \
  -C "${work_dir}" -czf "${topdir}/SOURCES/${source_name}.tar.gz" "${source_name}"
install -m 0644 "${pkg_dir}/ro-asd-desktop-standard.spec" "${topdir}/SPECS/ro-asd-desktop-standard.spec"

rpmbuild -ba \
  --define "_topdir ${topdir}" \
  --define "_tmppath ${work_dir}/tmp" \
  --define "dist .fc44" \
  "${topdir}/SPECS/ro-asd-desktop-standard.spec"

find "${topdir}/RPMS" "${topdir}/SRPMS" -type f -name '*.rpm' \
  -exec cp -p -- '{}' "${dist_dir}/" \;

(
  cd "${dist_dir}"
  find . -maxdepth 1 -type f -name '*.rpm' -printf '%f\n' | LC_ALL=C sort | xargs -r sha256sum
) > "${dist_dir}/SHA256SUMS"

python3 "${repo_root}/scripts/generate-build-manifest.py" \
  --repo-root "${repo_root}" \
  --artifact-dir "${dist_dir}" \
  --output "${dist_dir}/build-manifest-v1.json" \
  --component ro-asd-desktop-standard \
  --component-version "${component_version}"

echo "Çıktılar: ${dist_dir}"
