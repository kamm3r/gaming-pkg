Name:           obs-studio-plugin-aitum-multistream
Version:        1.0.9
Release:        2%{?dist}
Summary:        Stream to multiple platforms at once from OBS Studio
License:        GPL-2.0-only
URL:            https://github.com/Aitum/obs-aitum-multistream
# Same name as Nobara's package so newer releases upgrade it in place.
Provides:       obs-aitum-multistream = %{version}-%{release}
Obsoletes:      obs-aitum-multistream < %{version}-%{release}
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
Aitum Multistream is an OBS Studio plugin that adds extra stream outputs, so
one OBS session can stream to several services at the same time. Outputs can
use the main canvas, or the vertical canvas when Aitum Vertical is installed.
The plugin checks Aitum's servers for update notices, sending its version
and the OBS installation ID.

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
test -f %{buildroot}%{_libdir}/obs-plugins/aitum-multistream.so
test -f %{buildroot}%{_datadir}/obs/obs-plugins/aitum-multistream/locale/en-US.ini
# OBS loads plugins through this entry point.
nm -D --defined-only %{buildroot}%{_libdir}/obs-plugins/aitum-multistream.so | grep -q ' obs_module_load$'

%files
%license LICENSE
%doc README.md
%{_libdir}/obs-plugins/aitum-multistream.so
%{_datadir}/obs/obs-plugins/aitum-multistream/

%changelog
* Sat Oct 31 2026 kamm3r - 1.0.9-2
- Rename to the Nobara package name so it upgrades the installed plugin.

* Sat Oct 31 2026 kamm3r - 1.0.9-1
- Package the 1.0.9 release for Fedora OBS Studio.
