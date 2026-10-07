"""Probe asset .blend files: dump objects, actions, locations for assembly planning.

Usage: blender -b --factory-startup -P probe_libs.py -- <dir>
"""
import os
import sys

import bpy


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:]
    return argv[0] if argv else "global_assets/models"


models_dir = parse_args()
files = sorted(f for f in os.listdir(models_dir) if f.endswith(".blend"))

for fname in files:
    path = os.path.join(models_dir, fname)
    bpy.ops.wm.open_mainfile(filepath=path)
    print("=== FILE", fname)
    for o in bpy.data.objects:
        loc = tuple(round(v, 2) for v in o.location)
        par = o.parent.name if o.parent else "-"
        print("  OBJ %-22s type=%-6s loc=%-22s parent=%s"
              % (o.name, o.type, str(loc), par))
    for a in bpy.data.actions:
        print("  ACT", a.name, "users=%d" % a.users,
              "fake=%s" % a.use_fake_user)
    for arm in bpy.data.armatures:
        print("  ARM", arm.name, "bones=%d" % len(arm.bones))
print("PROBE_DONE")
