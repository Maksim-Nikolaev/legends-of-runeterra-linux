# Contributing

Test reports, README fixes and patches are welcome. This project tests only a few launchers itself, so every report from another setup helps.

## Test reports

Open an issue and include:

- your distribution and the launcher with its version and install type (Flatpak, Snap, native),
- the runner version, for example `GE-Proton9-27-LoR2`,
- the Riot Client version (Riot Client **Settings**, bottom left),
- the result: does the client update, does the window open, does LoR start without a click on Play,
- the `Riot autolaunch:` lines from the launcher's log.

If something fails, attach the newest Riot Client log from `drive_c/users/<user>/AppData/Local/Riot Games/Riot Client/Logs/Riot Client Logs/` in the game's prefix. Remove every line that contains `token` before you post it.

## README changes

Small pull requests are the easiest way to help, for example a launcher you tested or a missing Proton folder. On GitHub, open `README.md` and click **Edit this file**; GitHub creates the fork and the pull request for you.

## A new Riot Client breaks again

Run `tools/check-imports.py` as described in [docs/how-it-works.md](docs/how-it-works.md#checking-a-new-riot-client-version) and put its output in an issue.

## Patches and code

The Wine patches in `patches/` apply to the Wine source of GE-Proton 9-27, and `runner/` holds the changes to the `proton` script. Build with `./build.sh` and write in the pull request what you tested. Contributions are licensed under the GNU LGPL 2.1 or later, like the rest of the project.
