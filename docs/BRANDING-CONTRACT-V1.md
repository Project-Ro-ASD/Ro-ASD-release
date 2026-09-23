# Ro-ASD Branding Contract v1

Status: Step 4B branding foundation.

## Goal

`ro-asd-branding` owns Ro-ASD-specific visible distribution identity without
silently replacing Fedora release identity or duplicating theme assets.

## v1 rules

- Do not replace `/usr/lib/os-release` or `/etc/os-release`.
- Do not replace Fedora `system-release` files.
- Do not provide the generic `system-release` capability.
- Do not overwrite Fedora-owned logo/icon paths.
- Do not copy visual assets already owned by `ro-theme`.
- A branding asset must have one canonical owner before it is packaged here.

## Ownership split

| Domain | Owner |
| --- | --- |
| Machine-readable Ro-ASD release metadata | `ro-asd-release` |
| Ro-ASD logos / wordmarks / visible distro identity | `ro-asd-branding` |
| Plasma themes, wallpapers, Plymouth, icons/cursors used as theme assets | `ro-theme` |
| System and desktop defaults | `ro-asd-defaults` |

## Existing Ro-Theme logo

The current `Ro-Theme` repository contains `assets/brand/roasd-logo.png`
and a Plymouth copy. Those files remain delegated to Ro-Theme in v1.

Before moving any logo into `ro-asd-branding`, the projects must choose a
single source of truth and update Ro-Theme to consume that canonical asset
rather than ship a second independently maintained copy.

## Fedora identity boundary

Ro-ASD 44 is currently built on Fedora 44. The first branding package therefore
does not replace Fedora release-package files. A future distro-identity
transition must be a separate reviewed step with explicit package ownership,
upgrade and rollback tests.

## First package version

`ro-asd-branding 0.1.0` ships only the machine-readable branding contract.
It intentionally changes no visible desktop or operating-system identity.
