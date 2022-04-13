#!/bin/sh
set -e
FISH_VER=3.4.1
RPM_NAME=fish-${FISH_VER}-1
CORES=$(expr $(nproc) - 2 )

git_reset() {
  cd fish
  git checkout ${FISH_VER}
  echo "Removed $(git clean -f -d | wc -l) file(s) and/or folder(s)"
  git cherry-pick 5994e44877e043a83faf7f4ddfea7cee338e3f13 --no-commit
  echo -n "${FISH_VER}" > version
  cd ..
}

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
