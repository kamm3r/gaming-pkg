Name:           obs-aitum-stream-suite
Version:        1.2.5
Release:        1%{?dist}
Summary:        Aitum Stream Suite plugin for OBS Studio
License:        GPL-2.0-only
URL:            https://github.com/Aitum/obs-aitum-stream-suite
# Generated from the pinned upstream release commit in sources.json.
Source0:        %{name}-%{version}.tar.gz
ExclusiveArch:  x86_64
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  obs-studio-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  pkgconfig(libcurl)
Requires:       obs-studio%{?_isa}
# Uses Qt private platform headers for native window handles.
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}

%description
Aitum Stream Suite reorganises OBS Studio around docks for live scenes,
canvases, outputs, captures and statistics, and adds scene collection
templates and the Aitum theme. Its chat, activity and overlay panels load
web pages from Aitum's servers and need OBS Studio's browser source support.

%prep
%autosetup
# Qt 6.9 and later only expose private module targets when requested
# explicitly; upstream requests GuiPrivate for older Qt versions only.
sed -i 's/ AND Qt6_VERSION VERSION_LESS "6.9.0"//' CMakeLists.txt
grep -q 'find_package(Qt6 COMPONENTS GuiPrivate)' CMakeLists.txt
! grep -q 'VERSION_LESS "6.9.0"' CMakeLists.txt

%build
%cmake -DBUILD_OUT_OF_TREE=ON -DCMAKE_COMPILE_WARNING_AS_ERROR=OFF -DENABLE_CCACHE=OFF
%cmake_build

%install
%cmake_install

%check
test -f %{buildroot}%{_libdir}/obs-plugins/aitum-stream-suite.so
test -f %{buildroot}%{_datadir}/obs/obs-plugins/aitum-stream-suite/locale/en-US.ini
# OBS loads plugins through this entry point.
nm -D --defined-only %{buildroot}%{_libdir}/obs-plugins/aitum-stream-suite.so | grep -q ' obs_module_load$'

%files
%license LICENSE
%doc README.md
%{_libdir}/obs-plugins/aitum-stream-suite.so
%{_datadir}/obs/obs-plugins/aitum-stream-suite/
%{_datadir}/obs/obs-studio/themes/Aitum/
%{_datadir}/obs/obs-studio/themes/Aitum.obt
%{_datadir}/obs/obs-studio/themes/Aitum_Default.ovt

%changelog
* Sat Oct 31 2026 kamm3r - 1.2.5-1
- Package the 1.2.5 release for Fedora OBS Studio.
