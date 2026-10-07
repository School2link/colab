import sys
import math
import bpy

path = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.open_mainfile(filepath=path)
sc = bpy.context.scene
sc.frame_set(831)
dg = bpy.context.evaluated_depsgraph_get()
cam = bpy.data.objects["cam_M8"]
co = cam.matrix_world.translation
import mathutils
# ray at angles below horizon in camera-forward plane (cam aims +Y)
for deg in (16, 18, 19, 19.6, 20, 22, 25):
    a = math.radians(deg)
    d = mathutils.Vector((0, math.cos(a), -math.sin(a)))
    hit, loc, nrm, idx, obj, mtx = sc.ray_cast(dg, co, d)
    print("RAY -%s deg -> %s at (%.2f, %.2f, %.2f)"
          % (deg, obj.name if hit else "NONE", loc.x, loc.y, loc.z))
print("DONE")
