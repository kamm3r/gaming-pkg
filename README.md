# Gaming packages for Fedora

Sources for [kammer/gaming COPR](https://copr.fedorainfracloud.org/coprs/kammer/gaming/), targeting Fedora 44 x86_64.

- `moonlight-qt` 6.2.0: native Qt 6 game-streaming client with Wayland, VA-API and Vulkan support. Sunshine runs separately on the streaming host.
- `falcond` 2.0.14: automatic per-game performance daemon; not enabled automatically. Do not run alongside conflicting GameMode services.
- `falcond-gui` 1.0.3: GTK4 settings and status app.
- `falcond-profiles`: pinned upstream game profiles and process exclusion list; local user profiles are kept in their own directory.
- `obs-studio-plugin-vertical-canvas` 1.6.7, `obs-studio-plugin-aitum-multistream` 1.0.9 and `obs-studio-plugin-aitum-stream-suite` 1.2.5: Aitum's OBS Studio plugins for a vertical canvas, streaming to several services at once, and a dock-based streaming layout. They are built against Fedora's `obs-studio-devel` and require an installed `obs-studio`. The first two use Nobara's package names, so these newer releases upgrade Nobara's copies in place.
- `udev-joystick-blacklist` and `udev-joystick-blacklist-rm`: alternative udev rule sets for devices misidentified as joysticks. Install only one variant. These are hardware workarounds, not required gaming dependencies.

Steam stays in RPM Fusion. Eden, games, firmware and console keys are not included.

## Build and provenance

Each source is pinned by full Git commit in `sources.json`. `.copr/build-srpm.py` fetches and verifies that commit and archives it into the SRPM. Moonlight also includes all recursive submodules at the commits pinned by the release, so binary builds do not fetch source code. This avoids depending on Pika's blocked archive download endpoint. Falcond uses the upstream-required Zig 0.16.0 toolchain, downloaded from ziglang.org and checked against its published SHA-256. The toolchain is not installed in the resulting RPM.

Network-enabled binary builds fetch Zig dependencies with upstream content hashes and GUI crates using Cargo.lock. Recipes are adapted from Terra's `terrapkg/packages` frawhide branch (Falcond, GUI, profiles, joystick rules), retaining their historical changelogs and upstream licenses. Falcond's dependency relationships do not force a GUI or SCX scheduler installation. Desktop-file validation is run for the GUI.

```bash
make -f .copr/Makefile srpm spec=packages/falcond/falcond.spec outdir=/tmp/gaming-srpm
```

## Install

```bash
sudo dnf copr enable kammer/gaming
sudo dnf install moonlight-qt
# Optional performance tools:
sudo dnf install falcond falcond-gui
```

For an existing installation from another repository, use a reviewed `dnf distro-sync --from-repo=copr:copr.fedorainfracloud.org:kammer:gaming` transaction for the installed package names. Repository selection on future unrestricted updates follows DNF configuration; use exclusions on competing repositories where necessary.

Installation does not enable Falcond. Configure it and enable its service explicitly if desired. Upstream profiles can contain performance settings and executable hooks; review custom profiles before using them.

The Aitum plugins load the next time OBS Studio starts. Vertical and Multistream check `api.aitum.tv` for update notices, sending the plugin version and OBS's installation ID. Stream Suite's chat, activity and overlay docks load pages from Aitum's servers and need OBS's browser source. Its scene collection templates and Aitum theme are installed with it. Upstream builds these plugins with Qt private headers, so each plugin requires the exact Qt version it was built with and is rebuilt when Fedora's Qt changes.

```bash
sudo dnf install obs-studio-plugin-vertical-canvas obs-studio-plugin-aitum-multistream obs-studio-plugin-aitum-stream-suite
```

Moonlight uses the system FFmpeg libraries. Available codecs and hardware decoding depend on the installed FFmpeg and GPU driver stack; keep the existing Nobara/RPM Fusion codec setup. It does not install Sunshine or enable a service. Launch `moonlight` and pair it with the host.

Moonlight `6.2.0-3.fc44` is published: COPR build [11223032](https://copr.fedorainfracloud.org/coprs/build/11223032/) succeeded, and its exact version and download size are verified in Fedora 44 x86_64 repository metadata. [Build record](.copr/publications/moonlight-qt-2026-10-29.json).

The October 30 check against the original creators found no newer stable releases or tracked profile/rule commits. Every packaged version is already available in COPR with matching download sizes. No new builds were needed. See [the upstream and publication check](.copr/publications/2026-10-30.json) for pinned creator commits, release references, and build evidence.
