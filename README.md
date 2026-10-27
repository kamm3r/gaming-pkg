# Gaming packages for Fedora

Sources for [kammer/gaming COPR](https://copr.fedorainfracloud.org/coprs/kammer/gaming/), targeting Fedora 44 x86_64.

- `falcond` 2.0.14: automatic per-game performance daemon; not enabled automatically. Do not run alongside conflicting GameMode services.
- `falcond-gui` 1.0.3: GTK4 settings and status app.
- `falcond-profiles`: pinned upstream game profiles and process exclusion list; local user profiles are kept in their own directory.
- `udev-joystick-blacklist` and `udev-joystick-blacklist-rm`: alternative udev rule sets for devices misidentified as joysticks. Install only one variant. These are hardware workarounds, not required gaming dependencies.

Steam stays in RPM Fusion. Eden, games, firmware and console keys are not included.

## Build and provenance

Each source is pinned by full Git commit in `sources.json`. `.copr/build-srpm.py` fetches and verifies that commit and archives it into the SRPM. This avoids depending on Pika's blocked archive download endpoint. Falcond uses the upstream-required Zig 0.16.0 toolchain, downloaded from ziglang.org and checked against its published SHA-256. The toolchain is not installed in the resulting RPM.

Network-enabled binary builds fetch Zig dependencies with upstream content hashes and GUI crates using Cargo.lock. Recipes are adapted from Terra's `terrapkg/packages` frawhide branch (Falcond, GUI, profiles, joystick rules), retaining their historical changelogs and upstream licenses. Falcond's dependency relationships do not force a GUI or SCX scheduler installation. Desktop-file validation is run for the GUI.

```bash
make -f .copr/Makefile srpm spec=packages/falcond/falcond.spec outdir=/tmp/gaming-srpm
```

## Install

```bash
sudo dnf copr enable kammer/gaming
sudo dnf install falcond falcond-gui
```

For an existing installation from another repository, use a reviewed `dnf distro-sync --from-repo=copr:copr.fedorainfracloud.org:kammer:gaming` transaction for the installed package names. Repository selection on future unrestricted updates follows DNF configuration; use exclusions on competing repositories where necessary.

Installation does not enable Falcond. Configure it and enable its service explicitly if desired. Upstream profiles can contain performance settings and executable hooks; review custom profiles before using them.
