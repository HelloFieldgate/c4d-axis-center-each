"""Script Manager probe (optional). Prefer Extensions → Axis Center Each."""

from __future__ import annotations

import os
import sys

import c4d

# Prefs install path first, then repo copy.
CANDIDATES = [
    os.path.expanduser(
        "~/Library/Preferences/Maxon/Maxon Cinema 4D 2026_9D810372/plugins/AxisCenterEach.pyp"
    ),
    os.path.expanduser("~/dev/c4d-axis-center-each/plugins/AxisCenterEach/AxisCenterEach.pyp"),
]


def _load():
    import importlib.util

    for path in CANDIDATES:
        if os.path.isfile(path):
            spec = importlib.util.spec_from_file_location("axis_center_each", path)
            mod = importlib.util.module_from_spec(spec)
            # Don't execute RegisterCommandPlugin block: load by reading source without __main__
            # Simpler: exec only if already registered via plugin — just CallCommand path.
            print("Found plugin at:", path)
            return path
    return None


def main():
    path = _load()
    if not path:
        print("AxisCenterEach.pyp not found")
        return
    # Minimal live test: Center Axis to per selected object (same as plugin driver).
    doc = c4d.documents.GetActiveDocument()
    objs = list(doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_NONE) or [])
    print("Selected:", len(objs))
    if not objs:
        return
    CMD = 1011982  # Center Axis to
    original = list(objs)
    doc.StartUndo()
    try:
        for obj in objs:
            doc.SetActiveObject(obj, c4d.SELECTION_NEW)
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
            c4d.CallCommand(CMD)
    finally:
        if original:
            doc.SetActiveObject(original[0], c4d.SELECTION_NEW)
            for obj in original[1:]:
                doc.SetActiveObject(obj, c4d.SELECTION_ADD)
        doc.EndUndo()
        c4d.EventAdd()
    print("Done")


if __name__ == "__main__":
    main()
