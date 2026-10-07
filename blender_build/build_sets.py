"""Batch 5 — Sets for 'The Red Pen'.

Run:
  blender -b --factory-startup -P blender_build/build_sets.py -- --out <dir> --preview <dir>

Builds 4 set .blend files (environment + furniture + lighting rig, no hero props):
  set-staffroom.blend    night room: desk, chair, bulb, window, shelves,
                         chalkboard "B.E.C.E MOCK - FORM 3", crest slot
  set-office.blend       bursar counter: printer, reams, toner, ledger
  set-courtyard.blend    bench, school wall, tree (day)
  set-digital-void.blend bright gold/white cyclorama

Textures/HDRIs come from Batch D downloads (global_assets/textures, hdris).
"""
import math
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (assign, clear_scene, emission_material, load_font,
                    make_material, parse_args, preview_render, save_blend,
                    set_world, textured_material)

ARGS = parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(ROOT, "global_assets", "textures")
HDRI = os.path.join(ROOT, "global_assets", "hdris")
CREST = os.path.join(ROOT, "global_assets", "school-crest.png")

WOOD = os.path.join(TEX, "wood-pbr", "coated_pine_diff_2k.jpg")
PLASTER = os.path.join(TEX, "plaster-pbr", "plastered_wall_diff_1k.jpg")
FABRIC = os.path.join(TEX, "fabric-pbr", "rough_linen_diff_1k.jpg")
FLOOR_CONCRETE = os.path.join(TEX, "plaster-pbr", "plastered_wall_diff_1k.jpg")
HDRI_NIGHT = os.path.join(HDRI, "hdri-night.exr")
HDRI_DAY = os.path.join(HDRI, "hdri-day.exr")

D = math.radians


def _finish(name, mat, smooth=False):
    o = bpy.context.active_object
    o.name = name
    if mat:
        assign(o, mat)
    if smooth:
        bpy.ops.object.shade_smooth()
    return o


def plane(name, loc, sx, sy, mat, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot)
    o = _finish(name, mat)
    o.scale = (sx, sy, 1)
    return o


def box(name, loc, size, mat, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = _finish(name, mat)
    o.scale = size
    return o


def cyl(name, loc, r, depth, mat, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc,
                                        rotation=rot, vertices=24)
    return _finish(name, mat, smooth=True)


def sphere(name, loc, r, mat, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=24,
                                         ring_count=16)
    o = _finish(name, mat, smooth=True)
    o.scale = scale
    return o


def light(name, ltype, loc, energy, color=(1, 1, 1), size=1.0, rot=(0, 0, 0)):
    ld = bpy.data.lights.new(name, type=ltype)
    ld.energy = energy
    ld.color = color
    if ltype == "AREA":
        ld.size = size
    if ltype == "SUN":
        ld.angle = D(2)
    o = bpy.data.objects.new(name, ld)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = rot
    return o


def camera_rig_target(name, loc):
    """Empty marker object (target for later camera work)."""
    o = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    return o


def room_shell(prefix, w, d, h, floor_mat, wall_mat, walls=("back", "left")):
    plane(prefix + "_floor", (0, 0, 0), w, d, floor_mat)
    if "back" in walls:
        box(prefix + "_wall_back", (0, d / 2, h / 2), (w, 0.12, h), wall_mat)
    if "left" in walls:
        box(prefix + "_wall_left", (-w / 2, 0, h / 2), (0.12, d, h), wall_mat)
    if "right" in walls:
        box(prefix + "_wall_right", (w / 2, 0, h / 2), (0.12, d, h), wall_mat)
    if "front" in walls:
        box(prefix + "_wall_front", (0, -d / 2, h / 2), (w, 0.12, h), wall_mat)


# ------------------------------------------------------------- staffroom
def build_staffroom():
    clear_scene()
    floor_m = textured_material("sr_floor", WOOD, roughness=0.65, tile=(4, 3))
    wall_m = textured_material("sr_wall", PLASTER, roughness=0.85, tile=(3, 2))
    wood_m = textured_material("sr_wood", WOOD, roughness=0.55, tile=(1, 1))
    board_m = make_material("sr_board", (0.07, 0.16, 0.10, 1.0), roughness=0.8)
    metal_m = make_material("sr_metal", (0.25, 0.25, 0.27, 1.0), roughness=0.4)
    glow_m = emission_material("window_glow", (1.0, 0.85, 0.6, 1.0), 2.0)
    bulb_m = emission_material("bulb_glow", (1.0, 0.72, 0.42, 1.0), 8.0)
    dark_m = make_material("sr_dark", (0.10, 0.10, 0.11, 1.0), roughness=0.7)

    room_shell("sr", 8, 6, 3.0, floor_m, wall_m, walls=("back", "left", "right"))

    # desk (facing -Y: chair sits +Y of desk)
    box("desk_top", (0, -0.2, 0.75), (1.7, 0.85, 0.06), wood_m)
    for i, (x, y) in enumerate([(-0.78, -0.56), (0.78, -0.56),
                                (-0.78, 0.16), (0.78, 0.16)]):
        box("desk_leg%d" % i, (x, y, 0.36), (0.07, 0.07, 0.72), wood_m)
    box("desk_panel", (0, 0.16, 0.48), (1.5, 0.04, 0.5), wood_m)

    # chair at (0, 0.65), facing -Y toward desk
    box("chair_seat", (0, 0.65, 0.45), (0.46, 0.46, 0.05), wood_m)
    box("chair_back", (0, 0.87, 0.78), (0.46, 0.05, 0.62), wood_m)
    for i, (x, y) in enumerate([(-0.19, 0.46), (0.19, 0.46),
                                (-0.19, 0.84), (0.19, 0.84)]):
        box("chair_leg%d" % i, (x, y, 0.21), (0.05, 0.05, 0.42), metal_m)

    # chalkboard on back wall + text
    box("chalkboard", (1.6, 2.93, 1.6), (2.6, 0.05, 1.3), board_m)
    font = load_font(bold=True)
    bpy.ops.object.text_add(location=(1.6, 2.88, 1.85),
                            rotation=(D(90), 0, 0))
    t = bpy.context.active_object
    t.name = "chalk_text"
    t.data.body = "B.E.C.E MOCK - FORM 3"
    t.data.size = 0.19
    t.data.align_x = "CENTER"
    t.data.extrude = 0.005
    if font:
        t.data.font = font
    chalk_w = make_material("sr_chalk", (0.92, 0.92, 0.88, 1.0), roughness=0.9)
    assign(t, chalk_w)

    # crest slot above board (y offset avoids coplanar z-fight with wall face)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(1.6, 2.93, 2.55),
                                     rotation=(D(90), 0, 0))
    crest = _finish("crest_slot", None)
    crest.scale = (0.55, 0.55, 1)
    cm = bpy.data.materials.new("sr_crest")
    cm.use_nodes = True
    bsdf = cm.node_tree.nodes.get("Principled BSDF")
    img = bpy.data.images.load(CREST, check_existing=True)
    tex = cm.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image = img
    cm.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    cm.node_tree.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
    crest.data.materials.append(cm)

    # window (day-flicker emissive) on left wall
    box("window_frame", (-3.93, 0.8, 1.7), (0.06, 1.5, 1.3), wood_m)
    plane("window_glow", (-3.89, 0.8, 1.7), 1.3, 1.1, glow_m,
          rot=(0, D(90), 0))

    # shelves on back wall
    for i, z in enumerate((1.7, 2.15)):
        box("shelf%d" % i, (-1.8, 2.8, z), (1.6, 0.3, 0.05), wood_m)
    box("books0", (-2.2, 2.8, 1.86), (0.5, 0.22, 0.26),
        make_material("sr_book0", (0.45, 0.15, 0.12, 1.0)))
    box("books1", (-1.5, 2.8, 1.84), (0.6, 0.2, 0.22),
        make_material("sr_book1", (0.14, 0.30, 0.45, 1.0)))

    # hanging bulb + warm point light
    cyl("bulb_cord", (0.4, 0.4, 2.65), 0.012, 0.7, dark_m)
    sphere("bulb", (0.4, 0.4, 2.25), 0.10, bulb_m)
    light("bulb_light", "POINT", (0.4, 0.4, 2.25), 60.0,
          color=(1.0, 0.62, 0.30))
    light("fill_cool", "AREA", (-2.5, -2.0, 2.6), 12.0,
          color=(0.55, 0.65, 1.0), size=2.0, rot=(D(35), 0, D(-30)))

    camera_rig_target("target_desk", (0, -0.2, 0.8))
    camera_rig_target("target_door", (0, -3.0, 1.5))
    set_world(HDRI_NIGHT, 0.1)

    path = save_blend(ARGS["out"], "set-staffroom.blend")
    print("BUILD_OK set-staffroom.blend -> %s" % path)
    p = preview_render(ARGS["preview"], "set-staffroom.png", dist_mult=2.6)
    print("PREVIEW_OK %s" % os.path.basename(p))


# ---------------------------------------------------------------- office
def build_office():
    clear_scene()
    floor_m = textured_material("of_floor", FLOOR_CONCRETE, roughness=0.8,
                                tile=(4, 4))
    wall_m = textured_material("of_wall", PLASTER, roughness=0.85, tile=(3, 2))
    wood_m = textured_material("of_wood", WOOD, roughness=0.55, tile=(1, 1))
    white_m = make_material("of_white", (0.92, 0.92, 0.90, 1.0), roughness=0.6)
    printer_m = make_material("of_printer", (0.30, 0.31, 0.33, 1.0),
                              roughness=0.45)
    dark_m = make_material("of_dark", (0.12, 0.12, 0.13, 1.0), roughness=0.6)
    toner_m = make_material("of_toner", (0.08, 0.08, 0.09, 1.0), roughness=0.4)
    ledger_m = make_material("of_ledger", (0.35, 0.14, 0.12, 1.0),
                             roughness=0.7)

    room_shell("of", 7, 5, 3.0, floor_m, wall_m, walls=("back", "left", "right"))

    # counter across the room, staff side at +Y, public at -Y
    box("counter_top", (0, 0, 1.05), (3.4, 0.9, 0.07), wood_m)
    box("counter_front", (0, -0.42, 0.52), (3.4, 0.06, 1.0), wood_m)
    box("counter_shelf", (0, 0.2, 0.55), (3.2, 0.5, 0.05), wood_m)

    # printer on counter
    box("printer_body", (0.9, 0.1, 1.26), (0.62, 0.5, 0.30), printer_m)
    box("printer_lid", (0.9, 0.1, 1.43), (0.60, 0.48, 0.05), dark_m)
    box("printer_slot", (0.9, -0.16, 1.24), (0.44, 0.02, 0.06), dark_m)
    box("printer_panel", (1.14, -0.14, 1.34), (0.12, 0.02, 0.10),
        make_material("of_panel", (0.2, 0.5, 0.3, 1.0), roughness=0.3))

    # paper reams + toner boxes on back shelf
    for i in range(3):
        box("ream%d" % i, (-1.4, 2.2, 1.3 + i * 0.14), (0.44, 0.32, 0.13),
            white_m)
    for i in range(2):
        box("toner%d" % i, (-0.7, 2.2, 1.3 + i * 0.20), (0.30, 0.24, 0.19),
            toner_m)
    box("back_shelf", (-1.0, 2.2, 1.18), (2.6, 0.5, 0.05), wood_m)

    # ledger (open book) on counter left
    box("ledger_cover", (-1.0, 0.0, 1.10), (0.5, 0.36, 0.04), ledger_m)
    box("ledger_pages", (-1.0, 0.0, 1.13), (0.46, 0.32, 0.03), white_m)

    # fluorescent strip light
    light("fluoro_light", "AREA", (0, 0.5, 2.85), 250.0,
          color=(0.82, 0.90, 1.0), size=3.0)

    camera_rig_target("target_counter", (0, 0, 1.1))
    set_world(HDRI_DAY, 0.12)

    path = save_blend(ARGS["out"], "set-office.blend")
    print("BUILD_OK set-office.blend -> %s" % path)
    p = preview_render(ARGS["preview"], "set-office.png", dist_mult=2.6)
    print("PREVIEW_OK %s" % os.path.basename(p))


# -------------------------------------------------------------- courtyard
def build_courtyard():
    clear_scene()
    ground_m = textured_material("cy_ground", FLOOR_CONCRETE, roughness=0.9,
                                 tile=(6, 6))
    wall_m = textured_material("cy_wall", PLASTER, roughness=0.85, tile=(5, 1))
    wood_m = textured_material("cy_wood", WOOD, roughness=0.6, tile=(1, 1))
    gold_m = make_material("cy_gold", (0.83, 0.69, 0.21, 1.0), roughness=0.5)
    leaf_m = make_material("cy_leaf", (0.14, 0.34, 0.16, 1.0), roughness=0.8)
    bark_m = make_material("cy_bark", (0.32, 0.22, 0.14, 1.0), roughness=0.9)

    plane("cy_ground", (0, 0, 0), 16, 16, ground_m)

    # school wall with gold stripe
    box("cy_wall", (0, 4.5, 1.5), (14, 0.25, 3.0), wall_m)
    box("cy_stripe", (0, 4.35, 1.35), (14, 0.05, 0.28), gold_m)
    box("cy_wall_cap", (0, 4.5, 3.05), (14, 0.32, 0.12), gold_m)

    # bench against the wall
    box("bench_seat", (0.6, 3.7, 0.45), (2.0, 0.5, 0.07), wood_m)
    box("bench_back", (0.6, 3.95, 0.85), (2.0, 0.07, 0.6), wood_m)
    for i, x in enumerate((-0.25, 1.45)):
        box("bench_leg%d" % i, (x, 3.7, 0.2), (0.09, 0.42, 0.4), wood_m)

    # tree: trunk + canopy blobs
    cyl("tree_trunk", (-3.4, 3.2, 1.2), 0.20, 2.4, bark_m)
    sphere("tree_can0", (-3.4, 3.2, 2.9), 1.1, leaf_m, scale=(1.15, 1.0, 0.8))
    sphere("tree_can1", (-4.2, 3.0, 2.5), 0.8, leaf_m, scale=(1, 1, 0.85))
    sphere("tree_can2", (-2.6, 3.4, 2.5), 0.75, leaf_m, scale=(1, 1, 0.85))

    light("sun_day", "SUN", (4, -4, 8), 4.0, color=(1.0, 0.95, 0.85),
          rot=(D(50), 0, D(35)))
    camera_rig_target("target_bench", (0.6, 3.4, 1.0))
    set_world(HDRI_DAY, 0.9)

    path = save_blend(ARGS["out"], "set-courtyard.blend")
    print("BUILD_OK set-courtyard.blend -> %s" % path)
    p = preview_render(ARGS["preview"], "set-courtyard.png", dist_mult=2.6)
    print("PREVIEW_OK %s" % os.path.basename(p))


# ----------------------------------------------------------- digital void
def build_void():
    clear_scene()
    cyc_m = make_material("dv_cyc", (0.96, 0.96, 0.95, 1.0), roughness=0.6,
                          emission=(0.96, 0.96, 0.95, 1.0),
                          emission_strength=0.25)
    gold_m = make_material("dv_gold", (0.83, 0.69, 0.21, 1.0), roughness=0.4)

    # parabolic cyclorama: floor curving up into back wall
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
    cyc = _finish("dv_cyclorama", cyc_m, smooth=True)
    cyc.scale = (12, 14, 1)
    bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.subdivide(number_cuts=48)
    bpy.ops.object.mode_set(mode="OBJECT")
    me = cyc.data
    for v in me.vertices:
        y = v.co.y
        if y > 2.0:
            v.co.z = min(6.0, (y - 2.0) ** 2 * 0.35)

    # gold ring accent on the floor
    bpy.ops.mesh.primitive_torus_add(major_radius=2.4, minor_radius=0.05,
                                     location=(0, 0, 0.02))
    ring = _finish("dv_ring", gold_m, smooth=True)
    ring.scale = (1, 1, 0.4)

    light("dv_key", "AREA", (0, -2, 5), 400.0, size=6.0, rot=(D(20), 0, 0))
    light("dv_fill", "AREA", (0, 3, 4), 150.0, size=5.0, rot=(D(-30), 0, 0))
    camera_rig_target("target_void", (0, 1.5, 1.6))
    set_world(HDRI_DAY, 0.8)

    path = save_blend(ARGS["out"], "set-digital-void.blend")
    print("BUILD_OK set-digital-void.blend -> %s" % path)
    p = preview_render(ARGS["preview"], "set-digital-void.png", dist_mult=2.6)
    print("PREVIEW_OK %s" % os.path.basename(p))


if __name__ == "__main__":
    for fn in (build_staffroom, build_office, build_courtyard, build_void):
        fn()
        print("BUILD_ASSET_DONE %s" % fn.__name__)
    print("BUILD_BATCH_DONE 4 sets")
