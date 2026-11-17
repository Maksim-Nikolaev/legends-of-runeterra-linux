# Legends of Runeterra (LoR) on Linux: fixed Proton for the new Riot Client

**Legends of Runeterra works on Linux again.** Since Riot Client v142 (October 2026), LoR on Proton and Wine either loops on *"Couldn't update – Something went wrong with the update, even after repairing"* or the Riot Client opens no window at all, and LoR itself crashes on newer Proton. **GE-Proton9-27-LoR2** is GE-Proton 9-27 with five patched Wine DLLs that fix both. It also starts the game directly from your launcher, without a click on Play in the Riot Client, like the LoR shortcut on Windows. LoR and the Riot Client run again in Bottles, Heroic Games Launcher, Lutris and Steam.

**[Download the latest release](../../releases/latest)** – unofficial, not affiliated with Riot Games, GloriousEggroll or Valve.

| Launcher                           | Status                    |
| ---------------------------------- | ------------------------- |
| Bottles 67 (Flatpak)               | tested                    |
| Heroic Games Launcher (Flatpak)    | tested                    |
| Lutris, Steam, Steam Deck, umu-run | untested, reports welcome |

Last tested: 2026-11-17 with Riot Client 143.0.5.5260, in an existing and in a new prefix.

## Contents

- [Screenshots](#screenshots)
- [Install](#install)
- [Launcher steps](#launcher-steps)
- [Automatic game start](#automatic-game-start)
- [Troubleshooting](#troubleshooting)
- [How it works](#how-it-works)
- [Build from source](#build-from-source)
- [Credits and license](#credits-and-license)

## Screenshots

| Riot Client v142                                                                                                                                                                      | Client settings (v142.0.1.5150)                                                                                                                                                                          | Legends of Runeterra                                                                                                                                                                                |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a href="docs/screenshots/1-riot-client-v142.png"><img src="docs/screenshots/1-riot-client-v142.png" width="280" alt="Riot Client v142 running on Linux with GE-Proton9-27-LoR2"></a> | <a href="docs/screenshots/2-riot-client-v142-settings.png"><img src="docs/screenshots/2-riot-client-v142-settings.png" width="280" alt="Riot Client settings showing version 142.0.1.5150 on Linux"></a> | <a href="docs/screenshots/3-legends-of-runeterra-running.png"><img src="docs/screenshots/3-legends-of-runeterra-running.png" width="280" alt="Legends of Runeterra main menu running on Linux"></a> |

## Install

1. Download `GE-Proton9-27-LoR2.tar.gz` and `GE-Proton9-27-LoR2.sha512sum` from the [latest release](../../releases/latest) and verify them:
   
   ```bash
   cd ~/Downloads && sha512sum -c GE-Proton9-27-LoR2.sha512sum
   ```

2. Extract the archive into your launcher's Proton folder and restart the launcher:
   
   ```bash
   tar -xzf ~/Downloads/GE-Proton9-27-LoR2.tar.gz -C <folder>
   ```
   
   | Launcher                                         | Folder                                                                |
   | ------------------------------------------------ | --------------------------------------------------------------------- |
   | Bottles (Flatpak)                                | `~/.var/app/com.usebottles.bottles/data/bottles/runners/`             |
   | Heroic (Flatpak)                                 | `~/.var/app/com.heroicgameslauncher.hgl/config/heroic/tools/proton/`  |
   | Heroic (native)                                  | `~/.config/heroic/tools/proton/`                                      |
   | Steam (native); Lutris looks here too (untested) | `~/.steam/root/compatibilitytools.d/`                                 |
   | Steam (Flatpak)                                  | `~/.var/app/com.valvesoftware.Steam/data/Steam/compatibilitytools.d/` |

3. Select `GE-Proton9-27-LoR2` as the Proton / Wine version for Legends of Runeterra (see below).

**Which executable to start:** `C:\Riot Games\Riot Client\RiotClientServices.exe` with the arguments `--launch-product=bacon --launch-patchline=live` (Riot's own LoR shortcut; `bacon` is LoR's internal name). Starting `C:\Riot Games\LoR\live\Game\LoR.exe` directly works in Bottles, but in Heroic the game then reports a broken installation and closes.

For a new install you also need the official `Legends_Of_Runeterra_Installer.exe` from playruneterra.com.

## Launcher steps

**Bottles 67** – existing game: **Library** → **⋮** → **Game Settings** → **Proton** → **Choose Proton** → `GE-Proton9-27-LoR2` → **Save**. New game: **Library** → **+** → **Add a Windows Game** → **Run an Installer**, choose the installer and `GE-Proton9-27-LoR2` as Proton, install, close the Riot Client, then pick the executable inside the prefix.

**Heroic** – **Add Game** → platform **Windows** → **Wine Version** `GE-Proton9-27-LoR2` → **Run installer first** with the installer. Then set the executable to `drive_c/Riot Games/Riot Client/RiotClientServices.exe` inside the game's prefix and add the arguments above in the game settings. For an existing entry, just change **Wine Version** and the executable.

**Lutris** – **Add locally installed game**, runner **Wine**, **Wine version** `GE-Proton9-27-LoR2`, a new Wine prefix. Run the installer as the executable once, then change the executable to `RiotClientServices.exe` with the arguments above.

**Steam** – **Add a Non-Steam Game** with the installer → **Properties** → **Compatibility** → force `GE-Proton9-27-LoR2` → **Play** to install. Then set **Target** to `RiotClientServices.exe` in `steamapps/compatdata/<id>/pfx/drive_c/Riot Games/Riot Client/` and **Launch options** to the arguments above.

**umu-run**:

```bash
export WINEPREFIX="$HOME/Games/legends-of-runeterra" GAMEID=umu-default
export PROTONPATH="$HOME/.local/share/proton/GE-Proton9-27-LoR2"
umu-run ~/Downloads/Legends_Of_Runeterra_Installer.exe
umu-run "$WINEPREFIX/drive_c/Riot Games/Riot Client/RiotClientServices.exe" --launch-product=bacon --launch-patchline=live
```

On the first start an outdated Riot Client shows a short update splash and restarts itself; that is the update that used to fail. **Settings** shows the client version at the bottom left (`V142.0.1.5150` or newer).

**Upgrade from LoR1:** extract LoR2 next to LoR1 and select `GE-Proton9-27-LoR2` in the game's settings. The prefix, the login and the game files stay. You can delete LoR1 afterwards.

## Automatic game start

With the arguments `--launch-product=bacon --launch-patchline=live` the Riot Client opens and LoR starts a few seconds later, without a click on Play. On the very first start after a new install, you log in once; the game then starts after the login. If nobody logs in within 10 minutes, the runner stops waiting and the client stays open.

The runner prints `Riot autolaunch: bacon.live started` to the launcher's log when it starts the game.

To turn the automatic start off, set the environment variable `PROTON_RIOT_AUTOLAUNCH=0` for the game:

| Launcher | Where                                                                                                        |
| -------- | ------------------------------------------------------------------------------------------------------------ |
| Bottles  | **Game Settings** → **Launch** → **Environment Variables** → `PROTON_RIOT_AUTOLAUNCH=0` → **Add** → **Save** |
| Heroic   | Game settings → **Advanced** → **Environment Variables**: name `PROTON_RIOT_AUTOLAUNCH`, value `0`           |
| Lutris   | **Configure** → **System options** → **Environment variables**: key `PROTON_RIOT_AUTOLAUNCH`, value `0`      |
| Steam    | **Launch options**: `PROTON_RIOT_AUTOLAUNCH=0 %command% --launch-product=bacon --launch-patchline=live`      |
| umu-run  | `PROTON_RIOT_AUTOLAUNCH=0 umu-run ...`                                                                       |

Remove the variable to turn it on again. Without `--launch-product` the Riot Client opens its home page and the runner does nothing.

## Troubleshooting

- **Still "Couldn't update":** if you used the older v141 workaround, delete `drive_c/ProgramData/Riot Games/Metadata/Riot Client/Riot Client.ok` so the client updates itself.
- **"Something is wrong with the installation" and the game closes:** start `RiotClientServices.exe` with the arguments above instead of `LoR.exe`.
- **You do not want the game to start by itself:** see [Automatic game start](#automatic-game-start).
- **The game does not start by itself:** check that the runner is LoR2 or newer and that the arguments contain `--launch-product=bacon`. The launcher's log shows a `Riot autolaunch:` line for each step.
- **Game in English:** reinstalling resets the language. Riot Client → profile icon → **Settings** → **Legends of Runeterra** → **Game text language**.
- **A newer Riot Client breaks again:** `tools/check-imports.py` lists the Windows functions it needs that the runner lacks; please open an issue with its output.

## How it works

The Riot Client's self-update fails under Wine ([Wine bug 51687](https://bugs.winehq.org/show_bug.cgi?id=51687)), and Riot Client v142 (Electron 43) needs five Windows functions that Wine 9 lacks. The patches fix the update path in `kernelbase` and add the missing functions to `user32`, `uiautomationcore`, `combase` and `ole32`; everything else is untouched GE-Proton 9-27, which keeps LoR itself working. Under Wine the Riot Client also stops at the Play button, because it checks the login before the saved session is restored. The runner's `proton` script therefore starts the game through the client's local API, like on Windows. Details, patch list and the import checker: [docs/how-it-works.md](docs/how-it-works.md).

## Build from source

Needs Docker, git, curl and about 4 GB of disk; nothing is installed on the host.

```bash
./build.sh                                 # downloads GE-Proton9-27 and verifies it
./build.sh --base /path/to/GE-Proton9-27   # or reuses an existing copy
```

The runner and its archive land in `dist/`, logs in `build/`.

## Credits and license

Built on [GE-Proton](https://github.com/GloriousEggroll/proton-ge-custom) by GloriousEggroll, [Proton](https://github.com/ValveSoftware/Proton) by Valve, [Wine](https://www.winehq.org/) and [wine-staging](https://gitlab.winehq.org/wine/wine-staging). Thanks to Matías Zúñiga for tracking down Wine bug 51687 in 2021.

The patches modify Wine and, like Wine, are licensed under the GNU LGPL 2.1 or later. The released runner is GE-Proton 9-27 (`proton-ge-custom` tag `GE-Proton9-27`) plus the patches in this repository.
