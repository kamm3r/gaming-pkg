%global commit 1c5c9ccb69ea4ae42251aaa4c5a40a54766e6551
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commit_date 20260415

Name:          udev-joystick-blacklist
Version:       0^%{commit_date}git%{shortcommit}
Release:       3%{?dist}
Summary:       Fix for keyboard/mouse/tablet being detected as joysticks in Linux
License:       LicenseRef-Fedora-Public-Domain
URL:           https://github.com/denilsonsa/udev-joystick-blacklist
Source0:       %{name}-%{version}.tar.gz
BuildRequires: systemd-rpm-macros
Conflicts:     %{name}-rm
Conflicts:     steam-device-rules <= 1.0.0.85
BuildArch:     noarch

%description
There are several devices that, although recognized by kernel as joysticks, are not joysticks.

This package contains rules which will prevent those devices from being recognized as joysticks.

%package       rm
Summary:       Fix for keyboard/mouse/tablet being detected as joysticks in Linux
Conflicts:     %{name}
Conflicts:     steam-device-rules <= 1.0.0.85
Obsoletes:     steam-device-rules <= 1.0.0.85

%description   rm
There are several devices that, although recognized by kernel as joysticks, are not joysticks.

This package contains rules which will prevent those devices from being recognized as joysticks by removing the devices.

%prep
%autosetup

%build
# Empty.

%install
install -Dpm644 after_kernel_4_9/51-these-are-not-joysticks.rules -t %{buildroot}%{_udevrulesdir}
install -Dpm644 after_kernel_4_9/51-these-are-not-joysticks-rm.rules -t %{buildroot}%{_udevrulesdir}

%files
%doc README.md
%{_udevrulesdir}/51-these-are-not-joysticks.rules

%files rm
%doc README.md
%{_udevrulesdir}/51-these-are-not-joysticks-rm.rules

%changelog
* Tue Oct 27 2026 kamm3r
- Adapt Terra recipe for pinned upstream Git sources in kammer/gaming.

* Mon Nov 03 2025 Gilver E. <rockgrub@disroot.org> - 0^20250715gita1ace57-1
- Initial package
