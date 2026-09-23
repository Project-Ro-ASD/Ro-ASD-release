# Ro-ASD Defaults Ownership Contract v1

Status: Step 4A policy foundation.

## Goal

`ro-asd-defaults` owns only distribution defaults that are neither identity,
trust, repository, kernel, package-composition nor visual-theme assets.

The package must not create or rewrite per-user configuration. KDE system-wide
defaults should use the normal XDG/KConfig cascade so a user's
`~/.config` value remains higher precedence.

## Core rules

1. Never write into an existing user's home directory.
2. Do not seed `/etc/skel/.config` in v1.
3. Do not use KConfig immutable markers (`[$i]`) for ordinary distro defaults.
4. System administrator editable files under `/etc` must be packaged as
   `%config(noreplace)`.
5. Do not replace files owned by Fedora `kde-settings` or another Ro-ASD
   component.
6. A new default must have exactly one owner.

## Ownership matrix

| Domain | Owner |
| --- | --- |
| Visual appearance, Plasma themes, wallpapers, icons, cursors, Plymouth | `ro-theme` |
| Distribution identity and logos | `ro-asd-branding` |
| Release metadata | `ro-asd-release` |
| DNF repositories | `ro-asd-repos` |
| Public trust keys | `ro-asd-keyring` |
| Kernel selection/fallback | `ro-asd-kernel-policy` |
| Package/profile composition | `ro-asd-desktop-standard` |
| Non-visual desktop/system defaults not owned above | `ro-asd-defaults` |
| Application-specific defaults | The application package itself |

## Existing Ro-Theme overlap

Today `ro-theme` owns the following system files and also has a script that
writes corresponding settings into existing user homes:

- `/etc/xdg/kdeglobals`
- `/etc/xdg/plasmarc`
- `/etc/xdg/ksplashrc`
- `/etc/xdg/kscreenlockerrc`
- `/etc/xdg/kwinrc`

Until Ro-Theme is refactored, these paths are deliberately reserved away from
`ro-asd-defaults`. Step 4A does not duplicate or replace them.

The long-term target is to keep appearance defaults system-wide and cascading,
without a package post-install script rewriting user-owned files.

## Why no /etc/skel

Copying application config into `/etc/skel` turns a distro default into a
user-owned snapshot at account creation time. Future package changes then
cannot cleanly evolve that default, while the copied file may mask newer
system-wide values. The XDG/KConfig cascade is preferred for settings that
support it.

## First package version

`ro-asd-defaults 0.1.0` ships only the machine-readable ownership contract.
It intentionally changes no desktop behavior. Later releases may add concrete
defaults one domain at a time after ownership and upgrade behavior are tested.
