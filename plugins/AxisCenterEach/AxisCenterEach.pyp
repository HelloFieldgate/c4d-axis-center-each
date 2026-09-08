"""Axis Center Each — dockable sibling palette for Cinema 4D 2026.

Checkbox + Execute: run the stock Axis Center action once per selected object,
using the current Axis Center palette settings (via the matching menu command).

MIT License — see LICENSE in the repo root.
"""

from __future__ import annotations

import os

import c4d
from c4d import gui, plugins

# Development Plugin ID — change if RegisterCommandPlugin returns False (ID clash).
PLUGIN_ID = 1066127

# Built-in Mesh / Axis Center commands (C4D 2026 interface_icons / menus).
CMD_AXIS_CENTER_DIALOG = 1010819
CMD_VIEW_CENTER = 1011981
CMD_CENTER_AXIS_TO = 1011982
CMD_CENTER_TO_PARENT = 1011983
CMD_CENTER_PARENT_TO = 1011984
CMD_CENTER_OBJECT_TO = 1011985

ACTION_COMMANDS = (
    CMD_CENTER_AXIS_TO,
    CMD_CENTER_OBJECT_TO,
    CMD_CENTER_PARENT_TO,
    CMD_CENTER_TO_PARENT,
    CMD_VIEW_CENTER,
)

ACTION_LABELS = {
    CMD_CENTER_AXIS_TO: "Center Axis to",
    CMD_CENTER_OBJECT_TO: "Center Object to",
    CMD_CENTER_PARENT_TO: "Center Parent to",
    CMD_CENTER_TO_PARENT: "Center to Parent",
    CMD_VIEW_CENTER: "View Center",
}

ID_CHECK_INDIVIDUAL = 1000
ID_BTN_EXECUTE = 1001
ID_STATUS = 1002
ID_BTN_OPEN_AXIS_CENTER = 1003


def resolve_execute_command():
    for cmd in ACTION_COMMANDS:
        try:
            if c4d.IsCommandChecked(cmd):
                return cmd
        except Exception:
            pass
    return CMD_CENTER_AXIS_TO


def get_selected_objects(doc):
    objs = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_NONE)
    return list(objs) if objs else []


def _restore_selection(doc, objects):
    if not objects:
        doc.SetActiveObject(None, c4d.SELECTION_NEW)
        return
    doc.SetActiveObject(objects[0], c4d.SELECTION_NEW)
    for obj in objects[1:]:
        doc.SetActiveObject(obj, c4d.SELECTION_ADD)


def center_each(doc=None, command_id=None, objects=None):
    if doc is None:
        doc = c4d.documents.GetActiveDocument()
    if doc is None:
        return {"centered": 0, "skipped": 0, "command_id": 0, "command_name": "", "error": "No active document."}

    targets = list(objects) if objects is not None else get_selected_objects(doc)
    cmd = int(command_id) if command_id else resolve_execute_command()
    name = ACTION_LABELS.get(cmd, c4d.GetCommandName(cmd) or str(cmd))

    if not targets:
        return {
            "centered": 0,
            "skipped": 0,
            "command_id": cmd,
            "command_name": name,
            "error": "Nothing selected.",
        }

    original = list(targets)
    centered = 0
    skipped = 0

    doc.StartUndo()
    try:
        for obj in targets:
            if obj is None:
                skipped += 1
                continue
            doc.SetActiveObject(obj, c4d.SELECTION_NEW)
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
            try:
                c4d.CallCommand(cmd)
                centered += 1
            except Exception:
                skipped += 1
    finally:
        _restore_selection(doc, original)
        doc.EndUndo()
        c4d.EventAdd()

    return {
        "centered": centered,
        "skipped": skipped,
        "command_id": cmd,
        "command_name": name,
        "error": None,
    }


class AxisCenterEachDialog(gui.GeDialog):
    def CreateLayout(self):
        self.SetTitle("Axis Center Each")

        self.GroupBegin(2000, c4d.BFH_SCALEFIT | c4d.BFV_TOP, 1, 0)
        self.GroupBorderSpace(8, 8, 8, 8)
        self.GroupSpace(6, 6)

        self.AddCheckbox(
            ID_CHECK_INDIVIDUAL,
            c4d.BFH_LEFT,
            0,
            0,
            "Center Axis objects individually",
        )
        self.SetBool(ID_CHECK_INDIVIDUAL, True)

        self.AddStaticText(
            0,
            c4d.BFH_SCALEFIT,
            0,
            0,
            "Uses the current Axis Center palette settings.",
            0,
        )

        self.GroupBegin(2001, c4d.BFH_SCALEFIT, 2, 0)
        self.AddButton(ID_BTN_EXECUTE, c4d.BFH_SCALEFIT, 0, 0, "Execute")
        self.AddButton(ID_BTN_OPEN_AXIS_CENTER, c4d.BFH_SCALEFIT, 0, 0, "Open Axis Center")
        self.GroupEnd()

        self.AddStaticText(ID_STATUS, c4d.BFH_SCALEFIT, 0, 0, "", 0)

        self.GroupEnd()
        return True

    def _set_status(self, text):
        self.SetString(ID_STATUS, text)

    def Command(self, id, msg):
        if id == ID_CHECK_INDIVIDUAL:
            if not self.GetBool(ID_CHECK_INDIVIDUAL):
                self._set_status("Off — use the stock Axis Center Execute for group mode.")
            else:
                self._set_status("")
            return True

        if id == ID_BTN_OPEN_AXIS_CENTER:
            c4d.CallCommand(CMD_AXIS_CENTER_DIALOG)
            return True

        if id == ID_BTN_EXECUTE:
            if not self.GetBool(ID_CHECK_INDIVIDUAL):
                self._set_status("Turn on individually, or use the stock Axis Center palette.")
                return True

            result = center_each()
            if result.get("error"):
                self._set_status(result["error"])
                return True

            k = result["centered"]
            m = result["skipped"]
            n = k + m
            action = result["command_name"]
            msg = "Centered %s of %s (%s)" % (k, n, action)
            if m:
                msg += ", skipped %s" % m
            self._set_status(msg)
            return True

        return True


class AxisCenterEachCommand(plugins.CommandData):
    dialog = None

    def Execute(self, doc):
        return self._open()

    def RestoreLayout(self, secret):
        return self._open(secret)

    def _open(self, secret=0):
        if self.dialog is None:
            self.dialog = AxisCenterEachDialog()
        return self.dialog.Open(
            c4d.DLG_TYPE_ASYNC,
            PLUGIN_ID,
            -1,
            -1,
            280,
            120,
            secret,
        )


if __name__ == "__main__":
    ok = plugins.RegisterCommandPlugin(
        id=PLUGIN_ID,
        str="Axis Center Each",
        info=0,
        icon=None,
        help="Center each selected object's axis using the stock Axis Center settings.",
        dat=AxisCenterEachCommand(),
    )
    if ok:
        print("[Axis Center Each] registered (id=%s)" % PLUGIN_ID)
    else:
        print("[Axis Center Each] registration FAILED (id=%s) — try a different PLUGIN_ID" % PLUGIN_ID)
