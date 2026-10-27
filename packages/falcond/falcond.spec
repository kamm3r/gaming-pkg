%global debug_package %{nil}
Name: falcond
Version: 2.0.14
Release: 2%{?dist}
Summary: Automatic per-game performance management
License: MIT
URL: https://github.com/PikaOS-Linux/falcond
Source0: %{name}-%{version}.tar.gz
Source1: https://ziglang.org/download/0.16.0/zig-x86_64-linux-0.16.0.tar.xz
ExclusiveArch: x86_64
BuildRequires: tar xz git systemd-rpm-macros
Requires: falcond-profiles
Requires: systemd util-linux
Requires(pre): shadow-utils
Provides: group(falcond)
Recommends: power-profiles-daemon
Suggests: scx-scheds
Conflicts: gamemode

%description
Detect games, apply configured performance profiles, and restore settings.
The service is not enabled by installation. SCX features require schedulers
and an appropriate kernel, supplied separately.

%prep
%autosetup
tar -xf %{SOURCE1}

%build
export ZIG_GLOBAL_CACHE_DIR="$PWD/.zig-cache-global"
cd falcond
../zig-x86_64-linux-0.16.0/zig build -Doptimize=ReleaseFast -Dcpu=baseline -j2

%install
install -D -m0755 falcond/zig-out/bin/falcond %{buildroot}%{_bindir}/falcond
install -D -m0644 falcond/debian/falcond.service %{buildroot}%{_unitdir}/falcond.service
install -d %{buildroot}%{_sysusersdir}
echo 'g falcond -' > %{buildroot}%{_sysusersdir}/falcond.conf

%pre
getent group falcond >/dev/null || groupadd -r falcond

%preun
%systemd_preun falcond.service

%postun
%systemd_postun_with_restart falcond.service

%files
%license LICENSE
%doc README.md
%{_bindir}/falcond
%{_unitdir}/falcond.service
%{_sysusersdir}/falcond.conf

%changelog
* Tue Oct 27 2026 kamm3r - 2.0.14-2
- Build pinned upstream sources for the dedicated gaming repository.
