#!/bin/sh
set -e
FISH_NAME=fish-3.4.0-3

compile() {
  sfdk config --push target SailfishOS-${SFOS_VER}-${SFOS_ARCH} && sfdk config --push snapshot fish && sfdk build
  mv RPMS/${FISH_NAME}.${SFOS_ARCH}.rpm ./${FISH_NAME}_${PKG_VAR}.${SFOS_ARCH}.rpm
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
