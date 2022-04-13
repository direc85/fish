#!/bin/sh
set -e
FISH_NAME=fish-3.4.1-1
CORES=$(expr $(nproc) - 2 )

echo -n "${FISH_NAME}" > fish/version

compile() {
  if [[ -f ${RPM_NAME}_${PKG_VAR}.${SFOS_ARCH}.rpm ]]
  then
    echo "${RPM_NAME}_${PKG_VAR}.${SFOS_ARCH}.rpm exists, skipping..."
  else
    sfdk -c target=SailfishOS-${SFOS_VER}-${SFOS_ARCH} build --no-check -j ${CORES} -- --define "pkg_var ${PKG_VAR}"
    mv RPMS/${RPM_NAME}.${SFOS_ARCH}.rpm ./${RPM_NAME}_${PKG_VAR}.${SFOS_ARCH}.rpm
  fi
}

# Sailfish >= 4
SFOS_VER=4.3.0.12
PKG_VAR=sf4

rm -f rpm/fish.spec
ln -s fish.sf4.spec.txt rpm/fish.spec

SFOS_ARCH=armv7hl
compile
SFOS_ARCH=aarch64
compile
SFOS_ARCH=i486
compile

# Sailfish < 4
SFOS_VER=3.4.0.24
PKG_VAR=sf3

rm -f rpm/fish.spec
ln -s fish.sf3.spec.txt rpm/fish.spec

SFOS_ARCH=armv7hl
compile
SFOS_ARCH=i486
compile
