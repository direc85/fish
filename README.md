# Fish

Fish is a user-fiendly, interactive shell. This project provides the packaging
of the application (without gettext translations, documentation and
translations) to Sailfish OS.

> :warning: **Install at your own risk!** :warning:
> :warning: **Do NOT set fish as default shell!** :warning:

You'll need `fingerterm`, `toeterm` et. al. to use this. If you have developer
mode enabled, you can also SSH into the device and start it after login.

The packaging is wonky, but seems to work. I included the icons and a hidden
desktop file for completeness sake, but they don't really serve any purpose.

If you're unfamiliar with Fish, please check out the
[Introduction](https://fishshell.com/docs/current/tutorial.html#tutorial) or
(Fish for bash users)[https://fishshell.com/docs/current/fish_for_bash_users.html#fish-for-bash-users]
to get started!

# Building

I have Sailfish SDK 3.8.3 Docker variant installed at the moment. Building the
application should go something like this:

```bash
$ git clone https://github.com/direc85/fish.git
$ cd fish
$ git submodule init
$ git submodule update
$ sfdk config --push target SailfishOS-4.3.0.12-aarch64 && sfdk build
```

The build is set up so that it keeps the build files in separate
`build-$(ARCH)` folders so that the subsequent builds should be
lightning fast, even if you switch the target architecture back and forth.

Improvements in the packaging are very welcome!

Happy hacking!
