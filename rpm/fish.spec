#
# spec file for package fish
#
# Copyright (c) 2024 SUSE LLC
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
Version:        3.7.1
Release:        1
Summary:        The "friendly interactive shell"
# see bundled doc_src/license.rst
License:        BSD-3-Clause AND GPL-2.0-only AND ISC AND LGPL-2.0-or-later AND MIT AND PSF-2.0
Group:          System/Shells
URL:            https://fishshell.com/
Source:         %{name}-%{version}.tar.xz
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  ncurses-devel
BuildRequires:  pcre2-devel >= 10.21
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

%package devel
Summary:        Devel files for the fish shell
Group:          Development/Libraries/C and C++

%description devel
This package contains development files for the fish shell.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
    -DCMAKE_INSTALL_DOCDIR:PATH=share/doc/packages/fish \
    -DBUILD_DOCS=OFF \
    -DFISH_USE_SYSTEM_PCRE2=ON \
    %{nil}
%cmake_build

%install
%cmake_install

%find_lang %{name}

%check
pushd build
%make_build test
popd

%post
# Add fish to the list of allowed shells in /etc/shells
if ! grep -q '^%{_bindir}/%{name}$' %{_sysconfdir}/shells; then
        echo %{_bindir}/%{name} >>%{_sysconfdir}/shells
fi

%postun
# Remove fish from the list of allowed shells in /etc/shells
if [ "$1" = 0 ]; then
        grep -v '^%{_bindir}/%{name}$' %{_sysconfdir}/shells >%{_sysconfdir}/%{name}.tmp
        mv %{_sysconfdir}/%{name}.tmp %{_sysconfdir}/shells
fi

%files -f %{name}.lang
%dir %{_sysconfdir}/fish
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_bindir}/fish
%{_bindir}/fish_indent
%{_bindir}/fish_key_reader
%{_datadir}/%{name}
%{_datadir}/applications/fish.desktop
%{_datadir}/pixmaps/fish.png

%files devel
%{_datadir}/pkgconfig/fish.pc
