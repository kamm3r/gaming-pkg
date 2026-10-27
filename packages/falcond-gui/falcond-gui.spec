%global appid com.pikaos.falcondgui

Name:           falcond-gui
Version:        1.0.3
Release:        2%{?dist}
Summary:        A GTK4/LibAdwaita application to control and monitor the Falcond gaming optimization daemon
SourceLicense:  MIT
License:        (Apache-2.0 OR MIT) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND CC0-1.0 AND ISC AND (MIT OR Apache-2.0) AND MIT AND (Unlicense OR MIT)
URL:            https://git.pika-os.com/general-packages/falcond-gui
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  cargo rust gcc pkgconf-pkg-config
BuildRequires:  desktop-file-utils
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
Requires:       gtk4
Requires:       falcond
Requires:       falcond-profiles
Requires:       libadwaita

%description
falcond-gui provides a user-friendly graphical interface for managing falcond. It allows users to view the status of the daemon and customize its behavior.

%prep
%autosetup
cd falcond-gui
cargo fetch --locked

%build
cd falcond-gui
CARGO_BUILD_JOBS=2 cargo build --release --locked

%install
install -Dm755 falcond-gui/target/release/falcond-gui %{buildroot}%{_bindir}/falcond-gui
desktop-file-install --dir=%{buildroot}%{_datadir}/applications falcond-gui/res/%{appid}.desktop
install -Dm644 falcond-gui/res/%{appid}.png -t %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appid}.desktop

%files
%doc README.md
%license LICENSE.md
%{_bindir}/%{name}
%{_datadir}/icons/hicolor/512x512/apps/%{appid}.png
%{_datadir}/applications/%{appid}.desktop

%changelog
* Tue Oct 27 2026 kamm3r
- Adapt Terra recipe for pinned upstream Git sources in kammer/gaming.

* Thu Jan 1 2026 Gilver E. <roachy@fyralabs.com> - 1.0.0-1
- Initial package
