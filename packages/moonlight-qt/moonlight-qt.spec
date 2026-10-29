Name:           moonlight-qt
Version:        6.2.0
Release:        1%{?dist}
Summary:        Game streaming client for Sunshine and NVIDIA GameStream
License:        GPL-3.0-or-later AND LGPL-2.1-or-later AND MIT AND Zlib
URL:            https://github.com/moonlight-stream/moonlight-qt
# Generated from the pinned commit and recursive gitlinks in sources.json.
Source0:        %{name}-%{version}.tar.gz
ExclusiveArch:  x86_64
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_ttf)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libva-x11)
BuildRequires:  pkgconfig(libva-wayland)
BuildRequires:  pkgconfig(libva-drm)
BuildRequires:  pkgconfig(vdpau)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libplacebo) >= 7.349.0
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  wayland-protocols-devel
Requires:       qt6-qtdeclarative
Requires:       qt6-qtwayland
Requires:       hicolor-icon-theme
Provides:       bundled(enet)
Provides:       bundled(nanors)
Provides:       bundled(qmdnsengine)

%description
Moonlight streams games and desktop applications from a remote PC running
Sunshine or NVIDIA GameStream. It supports hardware accelerated video decoding,
game controllers, and native Wayland and X11 sessions. Install Sunshine on the
host PC separately; this package is the client only.

%prep
%autosetup

%build
%set_build_flags
qmake6 moonlight-qt.pro PREFIX=%{_prefix} CONFIG+=release CONFIG+=disable-prebuilts
%make_build release

%install
%make_install INSTALL_ROOT=%{buildroot}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/com.moonlight_stream.Moonlight.desktop
test -x %{buildroot}%{_bindir}/moonlight
# Ensure neither video decoding nor native Wayland support silently disappears.
grep -q -- '-DHAVE_FFMPEG' app/Makefile.Release
grep -q -- '-DHAVE_LIBVA' app/Makefile.Release
grep -q -- '-DHAVE_LIBPLACEBO_VULKAN' app/Makefile.Release
grep -q -- '-DHAS_WAYLAND' app/Makefile.Release

%files
%license LICENSE
%license h264bitstream/LICENSE
%license moonlight-common-c/moonlight-common-c/LICENSE.txt
%license moonlight-common-c/moonlight-common-c/enet/LICENSE
%license moonlight-common-c/moonlight-common-c/nanors/LICENSE
%license qmdnsengine/qmdnsengine/LICENSE.txt
%license app/SDL_GameControllerDB/LICENSE
%doc README.md
%{_bindir}/moonlight
%{_datadir}/applications/com.moonlight_stream.Moonlight.desktop
%{_datadir}/icons/hicolor/scalable/apps/moonlight.svg
%{_datadir}/metainfo/com.moonlight_stream.Moonlight.appdata.xml

%changelog
* Thu Oct 29 2026 kamm3r - 6.2.0-1
- Package the stable client with system Qt 6, FFmpeg, VA-API, Vulkan and Wayland.
- Include the release-pinned recursive submodules in the source RPM.
