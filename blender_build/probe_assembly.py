"""Probe report_cards.blend at M1 frame 46: identify big white objects + desk materials."""
import sys

import bpy
import mathutils

path = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.open_mainfile(filepath=path)
scene = bpy.context.scene
scene.frame_set(46)

# bind M1 camera like markers do
for m in scene.timeline_markers:
    if m.camera:
        pass
cam = bpy.data.objects.get("cam_M1")
scene.camera = cam
deps = bpy.context.evaluated_depsgraph_get()

print("=== desk_top materials")
dt = bpy.data.objects.get("desk_top")
if dt:
    for slot in dt.material_slots:
        mat = slot.material
        if mat is None:
            print("  EMPTY SLOT")
            continue
        imgs = [n.image.name for n in mat.node_tree.nodes
                if n.type == "TEX_IMAGE"]
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        bc = bsdf.inputs["Base Color"].default_value if bsdf else None
        links_in = [l.from_node.type for l in mat.node_tree.links
                    if l.to_node == bsdf and l.to_socket.name == "Base Color"]
        print("  mat=%s imgs=%s base=%s base_links=%s"
              % (mat.name, imgs, tuple(round(v, 2) for v in bc) if bc else "-",
                 links_in))

print("=== visible objects (frame 46) with bbox span > 0.4 and light color")
for o in sorted(bpy.data.objects, key=lambda x: x.name):
    if o.type not in ("MESH", "FONT", "CURVE"):
        continue
    if o.hide_render:
        continue
    coords = [o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    mn = mathutils.Vector((min(c[i] for c in coords) for i in range(3)))
    mx = mathutils.Vector((max(c[i] for c in coords) for i in range(3)))
    span = mx - mn
    if max(span) < 0.4:
        continue
    mats = []
    for slot in o.material_slots:
        m = slot.material
        if m is None:
            mats.append("NONE")
            continue
        b = m.node_tree.nodes.get("Principled BSDF")
        if b:
            c = b.inputs["Base Color"].default_value
            mats.append("%s(%.2f,%.2f,%.2f)" % (m.name, c[0], c[1], c[2]))
        else:
            mats.append(m.name + "(nopr)")
    print("  %-16s span=(%.2f,%.2f,%.2f) loc=(%.2f,%.2f,%.2f) mats=%s"
          % (o.name, span.x, span.y, span.z,
             o.matrix_world.translation.x, o.matrix_world.translation.y,
             o.matrix_world.translation.z, mats))
print("PROBE_DONE")
