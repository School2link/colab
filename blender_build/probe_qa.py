import sys
import bpy

path = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else None
if path:
    bpy.ops.wm.open_mainfile(filepath=path)


def wbb(o):
    import mathutils
    pts = [o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    xs = [p.x for p in pts]
    ys = [p.y for p in pts]
    zs = [p.z for p in pts]
    return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))


sc = bpy.context.scene

# --- frame 441: where is the red pen?
sc.frame_set(441)
pen = bpy.data.objects.get("RedPen")
print("PROBE f441 pen loc=", tuple(round(v, 3) for v in pen.matrix_world.translation),
      "hide=", pen.hide_render, "scale=", tuple(round(v, 3) for v in pen.scale))
cam = None
for m in sc.timeline_markers:
    if m.frame <= 441 and m.name.startswith("M5"):
        cam = m.camera
print("PROBE f441 marker cam=", cam.name if cam else None)
if cam:
    print("PROBE f441 cam loc=", tuple(round(v, 3) for v in cam.matrix_world.translation))
aim = bpy.data.objects.get("aim_m5")
print("PROBE f441 aim loc=", tuple(round(v, 3) for v in aim.matrix_world.translation))

# --- frame 701: what is the dark slab on the floor?
sc.frame_set(701)
print("PROBE f701 visible near floor:")
for o in sorted(bpy.data.objects, key=lambda x: x.name):
    if o.hide_render or o.type not in ("MESH", "CURVE", "FONT"):
        continue
    x0, x1, y0, y1, z0, z1 = wbb(o)
    if z1 < 0.45 and y1 < -0.6 and -1.0 < x0 < 1.5:
        print("  %s bb=(%.2f..%.2f, %.2f..%.2f, %.2f..%.2f)"
              % (o.name, x0, x1, y0, y1, z0, z1))

# --- frame 831: what is white near the bottom strip?
sc.frame_set(831)
print("PROBE f831 visible zone60 low objects:")
for o in sorted(bpy.data.objects, key=lambda x: x.name):
    if o.hide_render or o.type not in ("MESH", "CURVE", "FONT"):
        continue
    x0, x1, y0, y1, z0, z1 = wbb(o)
    if x1 > 55 and z1 < 0.5:
        print("  %s bb=(%.2f..%.2f, %.2f..%.2f, %.2f..%.2f)"
              % (o.name, x0, x1, y0, y1, z0, z1))

# --- frame 351: money visibility
sc.frame_set(351)
print("PROBE f351 money-like visible:")
for o in sorted(bpy.data.objects, key=lambda x: x.name):
    if o.hide_render or o.type not in ("MESH", "CURVE", "FONT"):
        continue
    x0, x1, y0, y1, z0, z1 = wbb(o)
    if 17 < x0 < 23 and z1 > 1.5:
        print("  %s bb=(%.2f..%.2f, %.2f..%.2f, %.2f..%.2f)"
              % (o.name, x0, x1, y0, y1, z0, z1))
print("PROBE_DONE")
