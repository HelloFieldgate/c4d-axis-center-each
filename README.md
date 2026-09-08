# Axis Center Each

A small Cinema 4D **2026** plugin that centers each selected object’s axis **individually**, using whatever settings are already on the stock **Axis Center** palette.

MIT licensed.

## Why

Stock Axis Center treats a multi-selection as one group. With tens or hundreds of objects, you otherwise run Execute one object at a time. This sibling palette adds:

- **Center Axis objects individually** (checkbox)
- **Execute** — loops the stock Axis Center action once per selected object

Dock it next to / above the Axis Center palette.

## Install (Cinema 4D 2026)

1. Download `AxisCenterEach.pyp` from the [latest release](https://github.com/HelloFieldgate/c4d-axis-center-each/releases/latest), **or** copy it from this repo:

   `plugins/AxisCenterEach/AxisCenterEach.pyp`

2. Put that file in your Cinema 4D prefs **plugins** folder:

   **macOS**
   ```bash
   cp AxisCenterEach.pyp \
     "$HOME/Library/Preferences/Maxon/Maxon Cinema 4D 2026_"*/plugins/
   ```

   **Windows** (PowerShell, adjust the `2026_*` folder name):
   ```powershell
   Copy-Item AxisCenterEach.pyp "$env:APPDATA\Maxon\Maxon Cinema 4D 2026_*\plugins\"
   ```

3. Use a **real file copy**, not a symlink — Cinema 4D on macOS often skips symlinked plugins.

4. Restart Cinema 4D.

5. Open **Extensions → Axis Center Each** (or Shift+C / Commander and search for it).

## Usage

1. Set options on the stock **Axis Center** palette as usual (Action, Center, Alignment, Include Children, …).
2. Multi-select the objects you want.
3. In **Axis Center Each**, leave the checkbox on and press **Execute**.
4. The status line reports how many objects were centered.

With the checkbox off, use the stock palette’s Execute for group behavior.

## Requirements

- Cinema 4D **2026** (developed and verified on macOS)
- No extra dependencies

## Plugin ID

Development ID: `1066127`. For a widely distributed public build, register your own ID at [Maxon Plugin Cafe](https://developers.maxon.net/) and change `PLUGIN_ID` near the top of `AxisCenterEach.pyp` if needed.

## Development

- Plan: `PLAN.md`
- Spike notes: `SPIKE.md`
- Driver decision: `docs/axis-center-driver-decision.md`
- Plugin source: `plugins/AxisCenterEach/AxisCenterEach.pyp`

## License

MIT — see [LICENSE](LICENSE).
