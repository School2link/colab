"""Measure world-space bounding boxes of key assets for assembly placement.

Usage: blender -b --factory-startup -P probe_dims.py -- <models_dir>
"""
import os
import sys

import bpy
import mathutils


def world_bbox(objs):
    coords = []
    for o in objs:
        if o.type not in ("MESH", "CURVE", "FONT"):
            continue
        for c in o.bound_box:
            coords.append(o.matrix_world @ mathutils.Vector(c))
    if not coords:
        return None
    mn = mathutils.Vector((min(c[i] for c in coords) for i in range(3)))
    mx = mathutils.Vector((max(c[i] for c in coords) for i in range(3)))
    return mn, mx


argv = sys.argv[sys.argv.index("--") + 1:]
models_dir = argv[0]

targets = {
    "teacher.blend": None, "student.blend": None, "parent.blend": None,
    "red-pen.blend": None, "booklet-stack.blend": None,
    "wall-clock.blend": None, "report-tray.blend": None,
    "money-notes.blend": None, "tablet.blend": None, "phone.blend": None,
    "checkmark-gold.blend": None,
}

for fname in targets:
    path = os.path.join(models_dir, fname)
    bpy.ops.wm.open_mainfile(filepath=path)
    bb = world_bbox(bpy.data.objects)
    if bb:
        mn, mx = bb
        size = mx - mn
        print("DIM %-22s min=(%.2f,%.2f,%.2f) max=(%.2f,%.2f,%.2f) size=(%.2f,%.2f,%.2f)"
              % (fname, mn.x, mn.y, mn.z, mx.x, mx.y, mx.z,
                 size.x, size.y, size.z))
print("DIMS_DONE")
