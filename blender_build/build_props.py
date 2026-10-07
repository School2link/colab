"""Batch 1 — hero props for 'The Red Pen'.

Run:
  blender -b --factory-startup -P blender_build/build_props.py -- --out <dir> --preview <dir>
Builds 8 props, saves .blend to --out, renders a preview still to --preview.
"""
import math
import os
import random
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (add_bevel, assign, clear_scene, hex_rgba, make_material,
                    new_object, parse_args, preview_render, save_blend)

ARGS = parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])

GOLD = hex_rgba("#D4AF37")
PAPER = hex_rgba("#F2EBDC")
COVER = hex_rgba("#1F3A6E")
RED = hex_rgba("#B01E1E")
DARK = hex_rgba("#1A1A1C")
BODY = hex_rgba("#2B2B30")
SCREEN_DARK = hex_rgba("#0A0A0A")
LEDGER_GREEN = hex_rgba("#0F5C34")


def finish(name, preview_name):
    filename = name + ".blend"
    path = save_blend(ARGS["out"], filename)
    print("BUILD_OK %s -> %s" % (filename, path))
    prev = preview_render(ARGS["preview"], preview_name)
    print("PREVIEW_OK %s" % os.path.basename(prev) if prev else "PREVIEW_SKIP")


def build_red_pen():
    clear_scene()
    random.seed(1)
    body = new_object("pen_body", bpy.ops.mesh.primitive_cylinder_add,
                      radius=0.012, depth=0.13, location=(0, 0, 0.01))
    nib = new_object("pen_nib", bpy.ops.mesh.primitive_cone_add,
                     radius1=0.012, radius2=0.0015, depth=0.035,
                     location=(0, 0, -0.075), rotation=(math.pi, 0, 0))
    ring = new_object("pen_ring", bpy.ops.mesh.primitive_torus_add,
                      major_radius=0.0125, minor_radius=0.0022, location=(0, 0, -0.055))
    tip = new_object("pen_tip", bpy.ops.mesh.primitive_cylinder_add,
                     radius=0.0025, depth=0.012, location=(0, 0, -0.096))

    red = make_material("PenRed", RED, metallic=0.1, roughness=0.35)
    silver = make_material("PenSilver", (0.8, 0.8, 0.82, 1), metallic=1.0, roughness=0.25)
    ink = make_material("PenInk", (0.02, 0.02, 0.03, 1), roughness=0.6)
    assign(body, red)
    assign(ring, silver)
    assign(nib, silver)
    assign(tip, ink)

    bpy.ops.object.select_all(action="DESELECT")
    for o in (body, nib, ring, tip):
        o.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.join()
    pen = bpy.context.active_object
    pen.name = "RedPen"
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    finish("red-pen", "prop_red-pen.png")


def build_checkmark_gold():
    clear_scene()
    curve = bpy.data.curves.new("CheckCurve", type="CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = 0.014
    curve.bevel_resolution = 6
    curve.fill_mode = "FULL"
    spline = curve.splines.new("POLY")
    pts = [(-0.055, 0, 0.03), (-0.014, 0, -0.045), (0.065, 0, 0.065)]
    spline.points.add(len(pts) - 1)
    for p, (x, y, z) in zip(spline.points, pts):
        p.co = (x, y, z, 1.0)
    obj = bpy.data.objects.new("CheckmarkGold", curve)
    bpy.context.scene.collection.objects.link(obj)
    gold = make_material("GoldEmissive", GOLD, metallic=0.6, roughness=0.3,
                         emission=GOLD, emission_strength=0.7)
    obj.data.materials.append(gold)
    finish("checkmark-gold", "prop_checkmark-gold.png")


def build_wall_clock():
    clear_scene()
    face = new_object("ClockFace", bpy.ops.mesh.primitive_cylinder_add,
                      radius=0.15, depth=0.015, location=(0, 0, 0))
    rim = new_object("ClockRim", bpy.ops.mesh.primitive_torus_add,
                     major_radius=0.15, minor_radius=0.009, location=(0, 0, 0))

    white = make_material("ClockFace_White", (0.95, 0.95, 0.92, 1), roughness=0.4)
    dark = make_material("ClockRim_Dark", DARK, roughness=0.5)
    black = make_material("ClockHand_Black", (0.03, 0.03, 0.03, 1), roughness=0.4)
    redm = make_material("ClockHand_Red", RED, roughness=0.4)
    assign(face, white)
    assign(rim, dark)

    ticks = []
    for i in range(12):
        ang = i * math.pi / 6.0
        big = (i % 3 == 0)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
        t = bpy.context.active_object
        t.name = "tick_%02d" % i
        t.scale = (0.016 if big else 0.010, 0.004 if big else 0.003, 0.004)
        bpy.ops.object.transform_apply(scale=True)
        r = 0.128
        t.location = (r * math.sin(ang), r * math.cos(ang), 0.010)
        t.rotation_euler = (0, 0, -ang)
        assign(t, black)
        ticks.append(t)

    bpy.ops.object.select_all(action="DESELECT")
    for o in [face, rim] + ticks:
        o.select_set(True)
    bpy.context.view_layer.objects.active = face
    bpy.ops.object.join()
    bpy.context.active_object.name = "ClockBody"

    def hand(name, length, width, thick, z, color_mat):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
        h = bpy.context.active_object
        h.name = name
        h.scale = (length, width, thick)
        bpy.ops.object.transform_apply(scale=True)
        h.location = (length / 2 - width, 0, z)
        bpy.context.scene.cursor.location = (0, 0, 0)
        bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
        assign(h, color_mat)
        return h

    hand("HandHour", 0.075, 0.012, 0.006, 0.014, black)
    hand("HandMinute", 0.115, 0.009, 0.006, 0.020, black)
    hand("HandSecond", 0.13, 0.004, 0.005, 0.026, redm)

    finish("wall-clock", "prop_wall-clock.png")


def build_booklet_stack():
    clear_scene()
    random.seed(7)
    paper = make_material("Paper", PAPER, roughness=0.85)
    cover = make_material("Cover", COVER, roughness=0.6)
    parts = []
    n = 12
    for i in range(n):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
        b = bpy.context.active_object
        b.name = "booklet_%02d" % i
        b.scale = (0.105, 0.15, 0.007)
        bpy.ops.object.transform_apply(scale=True)
        b.location = (random.uniform(-0.007, 0.007),
                      random.uniform(-0.007, 0.007),
                      i * 0.0155 + 0.0075)
        b.rotation_euler = (0, 0, random.uniform(-0.1, 0.1))
        assign(b, cover if i == n - 1 else paper)
        parts.append(b)

    bpy.ops.object.select_all(action="DESELECT")
    for o in parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    stack = bpy.context.active_object
    stack.name = "BookletStack"
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    finish("booklet-stack", "prop_booklet-stack.png")


def build_report_tray():
    clear_scene()
    tray_mat = make_material("TrayPlastic", (0.05, 0.09, 0.16, 1), roughness=0.5)
    plate_mat = make_material("TrayPlate", (0.96, 0.96, 0.94, 1), roughness=0.6)
    text_mat = make_material("TrayText", (0.04, 0.04, 0.05, 1), roughness=0.5)

    def box(name, scale, loc, mat):
        bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
        o = bpy.context.active_object
        o.name = name
        o.scale = scale
        bpy.ops.object.transform_apply(scale=True)
        assign(o, mat)
        return o

    parts = [
        box("tray_base", (0.17, 0.12, 0.006), (0, 0, 0.003), tray_mat),
        box("tray_front", (0.17, 0.006, 0.028), (0, -0.057, 0.017), tray_mat),
        box("tray_left", (0.006, 0.12, 0.028), (-0.082, 0, 0.017), tray_mat),
        box("tray_right", (0.006, 0.12, 0.028), (0.082, 0, 0.017), tray_mat),
        box("tray_backplate", (0.17, 0.006, 0.06), (0, 0.057, 0.033), plate_mat),
    ]

    bpy.ops.object.text_add(location=(0, 0.052, 0.026), rotation=(math.pi / 2, 0, 0))
    txt = bpy.context.active_object
    txt.name = "tray_label"
    txt.data.body = "REPORT CARDS"
    txt.data.size = 0.022
    txt.data.extrude = 0.001
    txt.data.align_x = "CENTER"
    assign(txt, text_mat)
    parts.append(txt)

    bpy.ops.object.select_all(action="DESELECT")
    for o in parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    bpy.context.active_object.name = "ReportTray"
    finish("report-tray", "prop_report-tray.png")


def build_money_notes():
    clear_scene()
    random.seed(11)
    green = make_material("NoteGreen", LEDGER_GREEN, roughness=0.7)
    green2 = make_material("NoteGreenLight", hex_rgba("#1B7A49"), roughness=0.7)
    goldm = make_material("CoinGold", GOLD, metallic=0.9, roughness=0.35)

    empty = bpy.data.objects.new("MoneyGroup", None)
    bpy.context.scene.collection.objects.link(empty)

    for i in range(6):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
        note = bpy.context.active_object
        note.name = "Note_%02d" % (i + 1)
        note.scale = (0.07, 0.035, 0.0008)
        bpy.ops.object.transform_apply(scale=True)
        note.location = (random.uniform(-0.05, 0.05),
                         random.uniform(-0.03, 0.03),
                         0.02 + i * 0.012)
        note.rotation_euler = (random.uniform(-0.5, 0.5),
                               random.uniform(-0.5, 0.5),
                               random.uniform(0, 3.14))
        assign(note, green if i % 2 == 0 else green2)
        note.parent = empty

    for i in range(4):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.004,
                                            location=(random.uniform(-0.05, 0.05),
                                                      random.uniform(-0.03, 0.03),
                                                      0.005 + i * 0.008))
        coin = bpy.context.active_object
        coin.name = "Coin_%02d" % (i + 1)
        coin.rotation_euler = (random.uniform(-1.2, 1.2), random.uniform(-1.2, 1.2), 0)
        assign(coin, goldm)
        coin.parent = empty

    finish("money-notes", "prop_money-notes.png")


def _slab(name, body_scale, screen_scale, screen_y, body_mat, bevel_w):
    body = new_object(name + "_body", bpy.ops.mesh.primitive_cube_add,
                      size=1, location=(0, 0, 0))
    body.scale = body_scale
    bpy.ops.object.transform_apply(scale=True)
    add_bevel(body, width=bevel_w, segments=4)
    assign(body, body_mat)

    screen = new_object(name + "_screen", bpy.ops.mesh.primitive_cube_add,
                        size=1, location=(0, screen_y, 0))
    screen.scale = screen_scale
    bpy.ops.object.transform_apply(scale=True)
    scr_mat = make_material(name + "_ScreenMat", SCREEN_DARK, roughness=0.15,
                            emission=(0.06, 0.06, 0.07, 1), emission_strength=1.2)
    assign(screen, scr_mat)
    screen.name = name + "Screen"

    bpy.ops.object.select_all(action="DESELECT")
    body.select_set(True)
    screen.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.join()
    joined = bpy.context.active_object
    joined.name = name
    return joined


def build_tablet():
    clear_scene()
    body_mat = make_material("TabletBody", BODY, metallic=0.3, roughness=0.4)
    _slab("Tablet", (0.16, 0.012, 0.225), (0.145, 0.003, 0.205), -0.007, body_mat, 0.008)
    finish("tablet", "prop_tablet.png")


def build_phone():
    clear_scene()
    body_mat = make_material("PhoneBody", (0x1C // 255, 0x1C // 255, 0x20 // 255, 1),
                             metallic=0.4, roughness=0.35)
    _slab("Phone", (0.075, 0.010, 0.155), (0.066, 0.003, 0.142), -0.006, body_mat, 0.006)
    finish("phone", "prop_phone.png")


BUILDERS = [
    ("red-pen", build_red_pen),
    ("checkmark-gold", build_checkmark_gold),
    ("wall-clock", build_wall_clock),
    ("booklet-stack", build_booklet_stack),
    ("report-tray", build_report_tray),
    ("money-notes", build_money_notes),
    ("tablet", build_tablet),
    ("phone", build_phone),
]

if __name__ == "__main__":
    for name, fn in BUILDERS:
        fn()
        print("BUILD_ASSET_DONE %s" % name)
    print("BUILD_BATCH_DONE %d assets" % len(BUILDERS))
