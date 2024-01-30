#!/bin/sh
set -e
CORES=$(expr $(nproc) - 2 )

fish_version() {
  cd fish
  FISH_VER=$(git describe)
  FISH_VER=$(echo ${FISH_VER%%-*})
  RPM_NAME=fish-${FISH_VER}-1
  cd ..
}

git_reset() {
  cd fish
  git checkout ${FISH_VER}
  git reset --hard
  echo "Removed $(git clean -f -d | wc -l) file(s) and/or folder(s)"
  echo -n "${FISH_VER}" > version
  cd ..
}

compile_all() {
  SFOS_ARCH=armv7hl
  compile
  SFOS_ARCH=aarch64
  compile
  SFOS_ARCH=i486
  compile
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

fish_version
echo "Compiling $FISH_VER..."

# Sailfish >= 4.5
SFOS_VER=4.5.0.18
PKG_VAR=sf450
git_reset

rm -f rpm/fish.spec
cp rpm/fish.sf4.spec.txt rpm/fish.spec
sed -i "s/^Version:        .*/Version:        $FISH_VER/" rpm/fish.spec

compile_all

# Sailfish 4.4
SFOS_VER=4.4.0.58
PKG_VAR=sf440
git_reset

compile_all

# Sailfish <= 4.3
SFOS_VER=4.3.0.12
PKG_VAR=sf430
git_reset

compile_all

# Sailfish < 4
SFOS_VER=3.4.0.24
PKG_VAR=sf340

rm -f rpm/fish.spec
cp rpm/fish.sf3.spec.txt rpm/fish.spec
sed -i "s/^Version:        .*/Version:        $FISH_VER/" rpm/fish.spec

SFOS_ARCH=aarch64
git_reset
compile
SFOS_ARCH=armv7hl
git_reset
compile
SFOS_ARCH=i486
git_reset
compile

echo -e "\nProduced RPM files:\n"
ls -1 ${RPM_NAME}*.rpm

rm -f rpm/fish.spec
