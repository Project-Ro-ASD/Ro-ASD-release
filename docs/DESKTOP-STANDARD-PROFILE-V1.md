# Ro-ASD Desktop Standard Profile v1

`ro-asd-desktop-standard` defines when an installed system satisfies the
Ro-ASD standard desktop foundation contract.

## Required foundation

The first release requires only components whose producer, acceptance and
production-signing chains are already established:

- `ro-asd-release >= 0.1.2`
- `ro-asd-keyring >= 0.1.0`
- `ro-asd-repos >= 0.1.0`
- `ro-asd-defaults >= 0.1.0`
- `ro-asd-branding >= 0.1.0`

## Composition boundary

This package does not reproduce the Fedora KDE package set. Plasma, Dolphin,
Konsole, NetworkManager, PipeWire and the rest of the base desktop are selected
by the future Ro-ASD compose definition.

The meta-package therefore describes the Ro-ASD overlay, not the whole Fedora
desktop dependency graph.

## Onboarding lifecycle

The profile contract records the intended ownership split:

1. `ro-installer` installs the composed system to disk.
2. `plasma-setup` owns first-boot user/system setup.
3. `ro-assist` owns post-login Ro-ASD onboarding.

These are lifecycle declarations in 0.1.0, not hard RPM dependencies.

## Deferred integrations

`ro-theme`, `ro-assist`, and a possible `ro-asd-plasma-setup` downstream
package remain intentionally outside hard dependencies until their architecture
is finalized.

Optional Ro applications such as `ro-control`, `ro-music`, and
`ro-terminal` are likewise not required by this foundation release.

## Ownership rules

This package owns no user home configuration, theme assets, Fedora KDE package
selection, kernel policy, or installer behavior. It ships only the profile
contract and RPM dependency relationship between trusted Ro-ASD foundation
components.
