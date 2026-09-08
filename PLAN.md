# Plan: c4d-axis-center-each

**Status:** agreed 2026-09-08 (Paul + Hans)  
**Project:** `/Users/hanshaskell/dev/c4d-axis-center-each`  
**Target:** Cinema 4D **2026** (current)  
**License:** MIT (GitHub public)  
**Related UI:** stock Axis Center palette (`Mesh` / modeling Center tool — `ID_MODELING_CENTER_TOOL` / `toolcenter.h`)

## Goal

A small **dockable** Cinema 4D plugin palette that sits naturally next to (above) the stock Axis Center dialog and adds the one missing workflow:

**Center each selected object’s axis individually**, using **whatever settings are currently set on the stock Axis Center palette** — so multi-select no longer centers one shared group axis.

## Product locks

- **C4D version:** 2026 (primary). Do not chase older majors unless a later spike proves cheap.
- **Settings source of truth:** the **stock Axis Center palette** — do not duplicate Center/Alignment/Include Children/etc. into our UI. That avoids two places to configure and matches Hans’s “no user confusion” requirement.
- **Our UI:** one checkbox — **Center Axis objects individually** — plus a clear **Execute** (and optional progress for large selections). Dockable palette.
- **Approach:** sibling palette that, on Execute, reads the active Center-tool parameters and applies the same center/align operation **once per selected object** (isolate selection → apply → next). Prefer driving the stock Center tool / documented modeling path over reimplementing axis math from scratch; fall back to a documented matrix+points path only if the tool cannot be driven per-object reliably.
- **Distribution:** MIT on GitHub; install via C4D plugins folder (or pyp/package layout TBD in Slice 0).

## Out of scope (v1)

- Replacing or skinning the stock Axis Center dialog
- Literally patching/hooking the stock **Execute** button (fragile across builds)
- Full reimplementation of every Axis Center mode as custom math (unless Slice 0 proves CallCommand/tool path fails)
- Auto-layout of our palette above Axis Center (user docks it; we document the suggested layout)
- Windows/Linux packaging beyond “works if C4D 2026 Python API is available” (primary: macOS, Hans’s machine)

## Principles

- **Same settings, different selection scope** — individually means “one object at a time with the palette’s current options,” not a different algorithm.
- Undo: one undo step for the whole batch (or clear per-object undos — decide in Slice 1; prefer one batch undo).
- Skip non-applicable objects loudly (status line / console count) rather than silently no-op.
- Keep the plugin tiny: one CommandData / dialog, no preferences sprawl.

---

## Slice 0 — Spike: drive Axis Center per object (C4D 2026)

1. Confirm plugin ID / registration pattern for C4D 2026 Python plugins.
2. Spike: with N polygon objects selected, read Center tool container (`plugins.FindPlugin` + `ID_MODELING_CENTER_TOOL` / `toolcenter.h` params).
3. Prove a loop: for each selected object, temporarily select only that object, invoke Center Apply / equivalent (`CallButton` / `SendModelingCommand` / documented path), restore selection.
4. Verify against stock palette: Axis to All Points + Alignment World + Position/Rotation on — result matches doing objects one-by-one manually.
5. Record decision: tool-driven vs custom matrix path (`axis-center-driver-decision`).

**Done when:** spike script or throwaway plugin centers ≥10 selected objects individually matching manual stock Execute; decision node written.

---

## Slice 1 — Dockable palette + Execute individually

6. Plugin dialog: checkbox **Center Axis objects individually** (default on), **Execute** button, short help text (“Uses the current Axis Center palette settings”).
7. On Execute: if checkbox off → optional pass-through to stock behavior or disable Execute with hint to use stock palette; if on → run Slice 0 loop.
8. Undo: wrap batch in one undo (preferred).
9. Status: “Centered k of n objects (skipped m)” in dialog or status bar.
10. README: install path, dock next to Axis Center, MIT badge.

**Done when:** installable plugin; multi-select Execute matches manual per-object Center; README sufficient for a stranger on GitHub.

---

## Slice 2 — Polish + GitHub ready

11. Edge cases: generators/nulls/cameras, empty selection, Include Children interaction, locked objects.
12. Progress / cancel for large selections (hundreds) if Execute blocks the UI too long.
13. LICENSE (MIT), `.gitignore`, screenshot of palette docked above Axis Center.
14. Tag v0.1.0; push to GitHub under Hans’s account (repo name `c4d-axis-center-each` unless renamed at push time).

**Done when:** public MIT repo; v0.1 works on C4D 2026 for the common Axis Center presets.

---

## Plan complete when

Slices 0–2 done; users can dock the palette, leave Axis Center settings alone, multi-select, Execute, and get per-object axes.

## Dependency order

**0 (spike driver) → 1 (UI + Execute) → 2 (polish + publish)**

## Open points

- Exact Apply ID / whether Center tool supports `SendModelingCommand` vs `CallButton(MDATA_APPLY)` — **Slice 0**
- Batch undo vs per-object — recommend one batch undo in **Slice 1**
- GitHub owner/org for the public repo — Hans at publish time
