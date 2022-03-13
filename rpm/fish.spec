Name:           fish
Summary:        Smart and user-friendly command line shell
Version:        3.4.0
Release:        1
Group:          Applications/System
License:        GPLv2
URL:            https://github.com/direc85/fish
Source0:        %{name}-%{version}.tar.bz2
Requires:       ncurses
BuildRequires:  ncurses-devel
BuildRequires:  gettext
BuildRequires:  make >= 3.11

%description
Fish is a fully-equipped command line shell (like bash or zsh) that is smart and user-friendly. Fish supports powerful features like syntax highlighting, autosuggestions, and tab completions that just work, with nothing to learn or configure. If you want to make your command line more productive, more useful, and more fun, without learning a bunch of arcane syntax and configuration options, then fish might be just what you’re looking for!

# This description section includes the metadata for SailfishOS:Chum, see
# https://github.com/sailfishos-chum/main/blob/main/Metadata.md
%if "%{?vendor}" == "chum"
PackageName: fish shell
Type: console-application
Categories:
  - System
  - Utility
Custom:
  Repo: https://github.com/direc85/fish
# Icon: https://raw.githubusercontent.com/sailfishos-chum/sailfishos-chum-gui/main/icons/sailfishos-chum-gui.svg
%endif

%prep
%setup -q -n %{name}-%{version}

%build
cmake \
  -B build-%{getenv:DEB_BUILD_ARCH} \
  -S %{name} \
  -DBUILD_DOCS=OFF \
  -DWITH_GETTEXT=OFF \
  -DCMAKE_INSTALL_PREFIX=/usr \
  -DCMAKE_INSTALL_SYSCONFDIR=/etc \
  -Wno-dev
cd build-%{getenv:DEB_BUILD_ARCH}
%make_build

%install
cd build-%{getenv:DEB_BUILD_ARCH}
%make_install
rm -rf %{buildroot}%{_datadir}/doc
rm -rf %{buildroot}%{_datadir}/man
rm -rf %{buildroot}%{_datadir}/pixmaps
rm -rf %{buildroot}%{_datadir}/pkgconfig
mkdir %{buildroot}%{_datadir}/icons
mkdir %{buildroot}%{_datadir}/icons/hicolor
mkdir %{buildroot}%{_datadir}/icons/hicolor/86x86
mkdir %{buildroot}%{_datadir}/icons/hicolor/108x108
mkdir %{buildroot}%{_datadir}/icons/hicolor/128x128
mkdir %{buildroot}%{_datadir}/icons/hicolor/172x172
mkdir %{buildroot}%{_datadir}/icons/hicolor/86x86/apps
mkdir %{buildroot}%{_datadir}/icons/hicolor/108x108/apps
mkdir %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
mkdir %{buildroot}%{_datadir}/icons/hicolor/172x172/apps
cd ..
cp icons/86x86/%{name}.png %{buildroot}%{_datadir}/icons/hicolor/86x86/apps/
cp icons/108x108/%{name}.png %{buildroot}%{_datadir}/icons/hicolor/108x108/apps/
cp icons/128x128/%{name}.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/
cp icons/172x172/%{name}.png %{buildroot}%{_datadir}/icons/hicolor/172x172/apps/
cp %{name}.desktop %{buildroot}%{_datadir}/applications/

%postun

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}*
%{_datadir}/%{name}
%{_sysconfdir}/%{name}/config.fish
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
