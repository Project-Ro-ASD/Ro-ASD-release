#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "packages/ro-asd-kernel-policy"
CONTRACT = PKG / "kernel-policy-v1.json"
PAYLOADS = PKG / "PAYLOADS.json"
SPEC = PKG / "ro-asd-kernel-policy.spec"

EXPECTED_INACTIVE = {
    "install_kernel_packages",
    "remove_fedora_kernel_packages",
    "exclude_fedora_kernel_packages",
    "enable_external_kernel_repositories",
    "change_bootloader_default",
    "rewrite_kernel_command_line",
    "mutate_secure_boot_state",
    "enforce_kernel_channel",
}

def main() -> int:
    try:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        if contract["schema_version"] != 1:
            raise ValueError("unsupported schema_version")
        if contract["component"] != "ro-asd-kernel-policy":
            raise ValueError("component mismatch")
        if contract["fedora_release"] != 44:
            raise ValueError("fedora_release must be 44")
        if set(contract["channels"]) != {"standard", "experimental", "fallback"}:
            raise ValueError("channel set must be exactly standard/experimental/fallback")

        ownership = contract["ownership"]
        if ownership["installer_kernel_selection"] is not False:
            raise ValueError("installer must not own kernel selection")
        if ownership["initial_setup_kernel_selection"] is not False:
            raise ValueError("initial setup must not own kernel selection")
        if ownership["post_login_selection_owner"] != "ro-assist":
            raise ValueError("Ro-Assist must own future post-login selection")
        if ownership["image_baseline_owner"] != "ro-asd-compose":
            raise ValueError("compose must own the baseline kernel")

        for field in EXPECTED_INACTIVE:
            if contract["inactive_actions"].get(field) is not False:
                raise ValueError(f"{field} must remain false in v1")

        invariants = contract["invariants"]
        for field in (
            "preserve_at_least_one_known_good_bootable_kernel",
            "experimental_is_never_automatic",
            "offline_install_must_have_bootable_baseline_kernel",
            "secure_boot_chain_required_before_ro_kernel_enforcement",
        ):
            if invariants.get(field) is not True:
                raise ValueError(f"required invariant disabled: {field}")

        payloads = json.loads(PAYLOADS.read_text(encoding="utf-8"))
        paths = [item["path"] for item in payloads["payloads"]]
        if paths != ["/usr/share/ro-asd/kernel/kernel-policy-v1.json"]:
            raise ValueError(f"unexpected payloads: {paths}")

        spec = SPEC.read_text(encoding="utf-8")
        forbidden = (
            "Requires:       kernel",
            "Requires:       ro-kernel",
            "Conflicts:",
            "Obsoletes:",
        )
        for marker in forbidden:
            if marker in spec:
                raise ValueError(f"forbidden active kernel relationship: {marker}")
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as error:
        print(f"HATA: {error}", file=sys.stderr)
        return 1

    print("OK: ro-asd-kernel-policy v1 remains policy-only and fail-closed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
