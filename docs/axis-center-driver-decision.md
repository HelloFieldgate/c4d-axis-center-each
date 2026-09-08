# Decision: Axis Center driver path

**Date:** 2026-09-08  
**Status:** Slice 0 — tool/command-driven (not custom matrix math)

## Choice

Drive the **stock Axis Center** actions with `c4d.CallCommand` once per selected object.

| Command ID | Name |
| --- | --- |
| `1010819` | Axis Center (opens the palette) |
| `1011982` | Center Axis to |
| `1011985` | Center Object to |
| `1011984` | Center Parent to |
| `1011983` | Center to Parent |
| `1011981` | View Center |

Confirmed from C4D 2026 `interface_icons.txt` / editor menus. Related SDK id `ID_MODELING_AXIS` (`200000087`) is the modeling-axis symbol, not the dialog Execute button.

## Why not `SendModelingCommand(ID_MODELING_CENTER_TOOL)`?

`ID_MODELING_CENTER_TOOL` (`200000071`) is the **Align / Center tool** (`toolcenter.h`: X/Y/Z Mid/Pos/Neg). That is a different tool from the **Axis Center** palette Hans uses (Action / All Points / Alignment / Include Children / Execute).

## Why not custom matrix + points math?

Plan preference: same settings as the stock palette, different selection scope. Reimplementing Axis Center (All Points vs selection, Alignment World/Normals/Edge, Include Children, Parent modes, etc.) duplicates Maxon’s logic and drifts from the palette. CallCommand reuses the palette’s stored settings.

## How “Execute” maps

The palette Execute applies the dialog’s current **Action**. Those actions are also menu commands that honor Center / Alignment / Include Children / Points Center / etc.

`resolve_execute_command()` prefers a checked action command when C4D reports one; otherwise **Center Axis to** (`1011982`).

## Per-object loop

1. Snapshot multi-selection  
2. For each object: `SetActiveObject(obj, SELECTION_NEW)` then `CallCommand(action)`  
3. Restore selection  
4. One `StartUndo` / `EndUndo` batch around the loop  

## Fallback

If a future C4D build breaks CallCommand parity, revisit a matrix path for the common “Axis to / All Points / World” case only — record that as a new decision.
