# Slice 0 spike — verify on Cinema 4D 2026

## Install

Plugin path (already symlinked if install script ran):

`~/Library/Preferences/Maxon/Maxon Cinema 4D 2026_*/plugins/AxisCenterEach.pyp`

Or copy/symlink the folder:

```bash
ln -sfn ~/dev/c4d-axis-center-each/plugins/AxisCenterEach \
  "$HOME/Library/Preferences/Maxon/Maxon Cinema 4D 2026_9D810372/plugins/AxisCenterEach"
```

Restart Cinema 4D 2026 (or Extensions → Reload Python Plugins if available).

Open: **Extensions → Axis Center Each** (or search “Axis Center Each” in the Commander).

## Script Manager probe (optional)

Paste `scripts/spike_axis_center_each.py` into Script Manager and run. It prints command diagnostics to the console, then centers each selected object individually via **Center Axis to**.

## Manual check (must pass)

1. Open the stock **Axis Center** palette (`Mesh` / Commander: “Axis Center”).  
2. Set a known preset, e.g. **Axis to**, **All Points**, Alignment **World**, Position+Rotation as you like, Include Children as needed.  
3. Create ~10 separate polygon objects with off-center axes, select all of them.  
4. Stock **Execute** once → confirm one shared group axis (the bug). Undo.  
5. Select all again → **Axis Center Each** → checkbox on → **Execute**.  
6. Each object’s axis should match doing stock Execute **one object at a time**.

## Pass / fail

- Pass: ≥10 objects, per-object axes match manual stock Execute.  
- Fail: note C4D build version, Action mode, and console output from the spike script.
