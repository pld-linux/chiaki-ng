#
# Conditional build:
%bcond_with	tests		# build without tests
#
Summary:	PlayStation Remote Play for Everyone
Name:		chiaki-ng
Version:	1.9.3
Release:	3
License:	AGPL v3
Group:		X11/Applications/Networking
Source0:	https://github.com/streetpea/chiaki-ng/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	988666ea44625d9783ccbca6e0b13c81
Patch0:		curl-lib.patch
URL:		https://streetpea.github.io/chiaki-ng/
BuildRequires:	Qt6Concurrent-devel
BuildRequires:	Qt6Core-devel
BuildRequires:	Qt6DBus-devel
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6Qml-devel
BuildRequires:	Qt6Quick-devel
BuildRequires:	Qt6Svg-devel
BuildRequires:	Qt6WebEngine-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	SDL2-devel
BuildRequires:	Vulkan-Headers
BuildRequires:	cmake
BuildRequires:	curl-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	fftw3-devel
BuildRequires:	hidapi-devel
BuildRequires:	jerasure-devel
BuildRequires:	libevdev-devel
BuildRequires:	libplacebo-devel
BuildRequires:	nanopb-devel
BuildRequires:	nanopb-static
BuildRequires:	openssl-devel
BuildRequires:	pkg-config
BuildRequires:	python3
BuildRequires:	speexdsp-devel
BuildRequires:	udev-devel
BuildRequires:	xorg-lib-libxkbcommon-devel
Requires:	vulkan(icd)
ExcludeArch:	%{ix86} x32
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Chiaki is a Free and Open Source Software Client for PlayStation 4 and
PlayStation 5 Remote Play.

This project is not endorsed or certified by Sony Interactive
Entertainment LLC.

%prep
%setup -q
%patch -P 0 -p1

%build
mkdir -p build
cd build
%cmake ../ \
	%{cmake_on_off test CHIAKI_ENABLE_TESTS} \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DCHIAKI_USE_SYSTEM_JERASURE=ON \
	-DCHIAKI_USE_SYSTEM_NANOPB=ON \
	-DCHIAKI_USE_SYSTEM_CURL=ON \
	-DCHIAKI_ENABLE_STEAM_SHORTCUT=OFF

%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/udev/rules.d

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p doc/71-chiaki4deck.rules $RPM_BUILD_ROOT/lib/udev/rules.d

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc LICENSES/AGPL-3.0-only-OpenSSL.txt README.md docs/*
%attr(755,root,root) %{_bindir}/chiaki
%attr(755,root,root) %{_bindir}/chiaki-cli
%{_desktopdir}/chiaking.desktop
%{_iconsdir}/hicolor/*x*/apps/chiaking.png
%{_datadir}/metainfo/io.github.streetpea.Chiaki4deck.appdata.xml
/lib/udev/rules.d/71-chiaki4deck.rules
