import sys
import bpy

path = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else None
if path:
    bpy.ops.wm.open_mainfile(filepath=path)
sc = bpy.context.scene

sc.frame_set(831)
ef = bpy.data.objects.get("endcard_floor")
print("P floor831 hide=", ef.hide_render, "loc=", tuple(ef.location),
      "scale=", tuple(ef.scale), "bbz=", [round(v, 3) for v in ef.bound_box[0]])

sc.frame_set(351)
for name in ("MoneyGroup",) :
    pass
monies = [o for o in bpy.data.objects if "Note" in o.name or "Coin" in o.name
          or "Money" in o.name]
for o in sorted(monies, key=lambda x: x.name):
    print("P money %s hide=%s world=(%.2f,%.2f,%.2f)"
          % (o.name, o.hide_render, o.matrix_world.translation.x,
             o.matrix_world.translation.y, o.matrix_world.translation.z))
print("DONE")
