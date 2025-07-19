#
# spec file for package fish
#
# Copyright (c) 2025 SUSE LLC, 2025 Matti Viljanen
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.


Name:           fish
Version:        4.0.2
Release:        1
Summary:        The "friendly interactive shell"
# see bundled doc_src/license.rst
# Python is a legacy alias for PSF-2.0
License:        BSD-3-Clause AND GPLv2 AND ISC AND LGPLv2+ AND MIT AND Python
Group:          System/Shells
URL:            https://github.com/direc85/fish
Source:         %{name}-%{version}.tar.xz

%if 0%{?_chum}
Source1:        vendor.tar.xz
Source2:        vendor.toml
%endif

Patch0:         0001-Ensure-correct-hashbang-for-.py-files.patch
Patch1:         0002-fix-zypper-autocompletion.patch
BuildRequires:  cargo
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  ncurses-devel
BuildRequires:  pcre2-devel >= 10.21
BuildRequires:  zstd
# for tests
BuildRequires:  procps
Requires:       awk
Requires:       bc
Requires:       gzip
Recommends:     terminfo

%description
fish is a command line shell.
It is geared towards interactive use and its features are focused on user
friendlieness and discoverability. The language syntax is simple but
incompatible with other shell languages.

# This description section includes metadata for SailfishOS:Chum, see
# https://github.com/sailfishos-chum/main/blob/main/Metadata.md
%if 0%{?_chum}
Title: Fish shell
Type: console-application
DeveloperName: Matti Viljanen
Categories:
 - Development
 - System
 - Utility
Custom:
  Repo: https://github.com/fish-shell/fish-shell
  PackagingRepo: https://github.com/direc85/fish
PackageIcon: https://raw.githubusercontent.com/direc85/fish/master/icons/172x172/fish.png
Links:
  Homepage: https://github.com/direc85/fish
  Help: https://fishshell.com/docs/current/index.html
  Bugtracker: https://github.com/direc85/fish/issues
  Donation: https://ko-fi.com/direc85
%endif

%package devel
Summary:        Devel files for the fish shell
Group:          Development/Libraries/C and C++

%description devel
This package contains development files for the fish shell.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build

%ifarch %arm
export SB2_RUST_TARGET_TRIPLE=armv7-unknown-linux-gnueabihf
export CFLAGS_armv7_unknown_linux_gnueabihf=$CFLAGS
export CXXFLAGS_armv7_unknown_linux_gnueabihf=$CXXFLAGS
%endif
%ifarch aarch64
export SB2_RUST_TARGET_TRIPLE=aarch64-unknown-linux-gnu
export CFLAGS_aarch64_unknown_linux_gnu=$CFLAGS
export CXXFLAGS_aarch64_unknown_linux_gnu=$CXXFLAGS
%endif
%ifarch %ix86
export SB2_RUST_TARGET_TRIPLE=i686-unknown-linux-gnu
export CFLAGS_i686_unknown_linux_gnu=$CFLAGS
export CXXFLAGS_i686_unknown_linux_gnu=$CXXFLAGS
%endif

export CFLAGS="-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -Wformat -Wformat-security -fmessage-length=0"
export CXXFLAGS=$CFLAGS

# Set meego cross compilers
export CARGO_TARGET_ARMV7_UNKNOWN_LINUX_GNUEABIHF_LINKER=armv7hl-meego-linux-gnueabi-gcc
export CC_armv7_unknown_linux_gnueabihf=armv7hl-meego-linux-gnueabi-gcc
export CXX_armv7_unknown_linux_gnueabihf=armv7hl-meego-linux-gnueabi-g++
export AR_armv7_unknown_linux_gnueabihf=armv7hl-meego-linux-gnueabi-ar
export CARGO_TARGET_AARCH64_UNKNOWN_LINUX_GNU_LINKER=aarch64-meego-linux-gnu-gcc
export CC_aarch64_unknown_linux_gnu=aarch64-meego-linux-gnu-gcc
export CXX_aarch64_unknown_linux_gnu=aarch64-meego-linux-gnu-g++
export AR_aarch64_unknown_linux_gnu=aarch64-meego-linux-gnu-ar

export CARGO_BUILD_JOBS=1

%if 0%{?_chum}
export CARGO_NET_OFFLINE=true
if [ -d "vendor" ]; then
  echo "Offline build already prepared."
else
  echo "Preparing offline build..."
  tar xf %SOURCE1
  mkdir -p .cargo/
  cp %SOURCE2 .cargo/config.toml
fi
%endif

# Since we're not using release tarball, inject version file manually
echo "%{version}" > version

%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
    -DCMAKE_INSTALL_DOCDIR:PATH=share/doc/packages/fish \
    -DBUILD_DOCS=OFF \
    -DFISH_USE_SYSTEM_PCRE2=ON \
    -DRust_CARGO_TARGET=$SB2_RUST_TARGET_TRIPLE \
    -DRust_CARGO_HOST_TARGET=$SB2_RUST_TARGET_TRIPLE \
    %{nil}
%cmake_build

%install
%cmake_install

%find_lang %{name}

rm -f %{buildroot}/%{_datadir}/doc/packages/fish/CHANGELOG.rst
rm -f %{buildroot}/%{_datadir}/applications/fish.desktop

%files -f %{name}.lang
%dir %{_sysconfdir}/fish
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_bindir}/fish
%{_bindir}/fish_indent
%{_bindir}/fish_key_reader
%{_datadir}/%{name}
%{_datadir}/pixmaps/fish.png

%files devel
%{_datadir}/pkgconfig/fish.pc

%changelog

* Sat Jul 19 2025 Matti Viljanen <matti.viljanen@kapsi.fi> - 3.7.1-2
- Fix zypper autocompletion

* Sun Dec 22 2024 Matti Viljanen <matti.viljanen@kapsi.fi> - 3.7.1-1
- Initial Chum release
