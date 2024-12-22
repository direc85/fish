# Fish

Fish is a user-fiendly, interactive shell. This project provides the packaging of the application (without documentation) to Sailfish OS. You can download the binaries from Chum from 3.7.1 and onward. The older builds can be found in [OpenRepos.net](https://openrepos.net/content/direc85/fish).

> :warning: **Do NOT set fish as default shell!** :warning:

You'll need `fingerterm`, `toeterm` et. al. to use this on-device. If you have developer
mode enabled, you can also SSH into the device and start it after login.

If you're unfamiliar with Fish, please check out the [Introduction](https://fishshell.com/docs/current/tutorial.html#tutorial) or [Fish for bash users](https://fishshell.com/docs/current/fish_for_bash_users.html#fish-for-bash-users) to get started!

## Building

For local builds, I currently use Sailfish Platform SDK. Building it is as simple as:

```bash
$ git clone https://github.com/direc85/fish.git
$ cd fish
$ git submodule update --init
$ mb2 --target SailfishOS-latest-aarch64 build -d -p
```

For subsequent builds drop the `-p` (`%prep).

For a clean build with `%prep`, or target architecture change, do this in fish project directory:

```
$ cd fish
$ git clean -xfd
$ git reset --hard 3.7.1 # Or some other tag/commit
$ cd ..
$ mb2 --target SailfishOS-latest-armv7hl build -d -p
```

Happy hacking!
