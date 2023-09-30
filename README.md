# Fish

Fish is a user-fiendly, interactive shell. This project provides the packaging
of the application (without gettext translations, documentation and
translations) to Sailfish OS. You can download the binaries from
[OpenRepos.net](https://openrepos.net/content/direc85/fish).

> :warning: **Install at your own risk!** :warning:

> :warning: **Do NOT set fish as default shell!** :warning:

You'll need `fingerterm`, `toeterm` et. al. to use this on-device. If you have developer
mode enabled, you can also SSH into the device and start it after login.

The packaging is wonky, but seems to work. I included the icons and a hidden
desktop file for completeness sake, but they don't really serve any purpose.

If you're unfamiliar with Fish, please check out the
[Introduction](https://fishshell.com/docs/current/tutorial.html#tutorial) or
[Fish for bash users](https://fishshell.com/docs/current/fish_for_bash_users.html#fish-for-bash-users)
to get started!

# Building

I have Sailfish SDK 3.10.4 Docker variant installed at the moment. Building the
application should go something like this, depending on your Sailfish version:

```bash
$ git clone https://github.com/direc85/fish.git
$ cd fish
$ git submodule init
$ git submodule update
$ rm -f rpm/fish.spec
$ ln -s fish.sf4.spec.txt rpm/fish.spec
$ sfdk -c target=SailfishOS-4.5.0.18-aarch64 build
```

The build is set up so that it keeps the build files in separate
`build-$(ARCH)` folders for Sailfish OS 4+ builds, so that the subsequent builds
should be lightning fast, even if you switch the target architecture back and forth.
The Sailfish OS 3 build however seems to use older cmake, which seems to always
build the sources into the same folder, so it always does a failsafe `make clean`
before even trying to compile it.

The build script that builds all architectures for all four build targets
is included, that's what I build the twelve (12) RPMs with.

Improvements in the packaging are very, _very_ welcome!

Happy hacking!
