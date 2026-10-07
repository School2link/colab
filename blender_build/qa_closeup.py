"""QA closeup render — verify chalkboard text + crest in a set .blend.

Usage:
  blender -b <set.blend> -P qa_closeup.py -- --out <png> --at x,y,z --target x,y,z [--lens 40]
"""
import bpy
import mathutils
import sys


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:]
    d = {"out": "", "at": "0,0,1.7", "target": "0,3,1.7", "lens": "40"}
    i = 0
    while i < len(argv):
        key = argv[i].lstrip("-")
        if key in d and i + 1 < len(argv):
            d[key] = argv[i + 1]
            i += 2
        else:
            i += 1
    return d


A = parse_args()
at = [float(v) for v in A["at"].split(",")]
target = [float(v) for v in A["target"].split(",")]

scene = bpy.context.scene
cam_data = bpy.data.cameras.new("qa_cam")
cam_data.lens = float(A["lens"])
cam = bpy.data.objects.new("qa_cam", cam_data)
scene.collection.objects.link(cam)
cam.location = at
direction = mathutils.Vector(target) - mathutils.Vector(at)
cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
scene.camera = cam

scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.filepath = A["out"]
bpy.ops.render.render(write_still=True)
print("QA_RENDER_OK", A["out"])
