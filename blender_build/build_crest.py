"""Batch 3 — Brand crest for 'The Red Pen'.

Run:
  blender -b --factory-startup -P blender_build/build_crest.py -- --out <dir> --preview <dir>

Renders school-crest.png (1024x1024, transparent background):
gold shield + open-book motif + star + banner, brand gold #D4AF37.
"""
import math
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (assign, clear_scene, emission_material, hex_rgba,
                    load_font, parse_args)

ARGS = parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])

FONT_B = load_font(bold=True) or None

GOLD = hex_rgba("#D4AF37")
GOLD_DARK = hex_rgba("#8A7018")
CHARCOAL = (0.13, 0.13, 0.15, 1.0)
WHITE = (1.0, 1.0, 1.0, 1.0)

RES = 1024
CANVAS = 8.0  # units, square


def poly(name, verts2d, mat, z=0.0, cx=0.0, cy=0.0):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([(cx + x, cy + y, 0.0) for x, y in verts2d], [],
                     [list(range(len(verts2d)))])
    mesh.update()
    o = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(o)
    o.location = (0, 0, z)
    assign(o, mat)
    return o


def rect(name, cx, cy, w, h, mat, z=0.02, rot_z=0.0):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(cx, cy, z),
                                     rotation=(0, 0, rot_z))
    o = bpy.context.active_object
    o.name = name
    o.scale = (w, h, 1.0)
    assign(o, mat)
    return o


def text(name, body, cx, cy, size, mat, z=0.06):
    bpy.ops.object.text_add(location=(cx, cy, z))
    t = bpy.context.active_object
    t.name = name
    t.data.body = body
    t.data.size = size
    t.data.align_x = "CENTER"
    t.data.align_y = "CENTER"
    if FONT_B:
        t.data.font = FONT_B
    assign(t, mat)
    return t


def star_verts(r_out, r_in, points=5, rot=math.pi / 2):
    v = []
    for i in range(points * 2):
        a = rot + i * math.pi / points
        r = r_out if i % 2 == 0 else r_in
        v.append((r * math.cos(a), r * math.sin(a)))
    return v


SHIELD_OUTER = [(-3.0, 3.2), (3.0, 3.2), (3.0, -0.6), (1.9, -2.6),
                (0.0, -4.1), (-1.9, -2.6), (-3.0, -0.6)]
SHIELD_INNER = [(-2.55, 2.75), (2.55, 2.75), (2.55, -0.55), (1.62, -2.25),
                (0.0, -3.5), (-1.62, -2.25), (-2.55, -0.55)]


def build_crest():
    clear_scene()
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 16
    scene.cycles.device = "CPU"
    scene.view_settings.view_transform = "Standard"
    scene.render.film_transparent = True
    scene.render.resolution_x = RES
    scene.render.resolution_y = RES

    cd = bpy.data.cameras.new("crest_cam")
    cd.type = "ORTHO"
    cd.sensor_fit = "VERTICAL"
    cd.ortho_scale = CANVAS
    cam = bpy.data.objects.new("crest_cam", cd)
    scene.collection.objects.link(cam)
    cam.location = (0, 0, 6)
    scene.camera = cam

    m_gold = emission_material("cr_gold", GOLD)
    m_gold_d = emission_material("cr_golddark", GOLD_DARK)
    m_dark = emission_material("cr_dark", CHARCOAL)
    m_white = emission_material("cr_white", WHITE)

    # shield: gold border + dark field
    poly("shield_outer", SHIELD_OUTER, m_gold, z=0.0)
    poly("shield_inner", SHIELD_INNER, m_dark, z=0.02)

    # open book: two white pages with a gold spine
    left = [(-1.75, 0.95), (-0.12, 1.15), (-0.12, -0.65), (-1.75, -0.95)]
    right = [(1.75, 0.95), (0.12, 1.15), (0.12, -0.65), (1.75, -0.95)]
    poly("page_l", left, m_white, z=0.04)
    poly("page_r", right, m_white, z=0.04)
    poly("page_l_bot", [(-1.75, -0.95), (-0.12, -0.65), (-0.12, -0.78),
                        (-1.75, -1.08)], m_gold, z=0.05)
    poly("page_r_bot", [(1.75, -0.95), (0.12, -0.65), (0.12, -0.78),
                        (1.75, -1.08)], m_gold, z=0.05)
    rect("spine", 0, 0.1, 0.16, 1.95, m_gold, z=0.06)

    # page lines (thin dark strokes)
    for i in range(3):
        y = 0.62 - i * 0.42
        w = 1.15 - i * 0.18
        rect("line_l%d" % i, -0.95, y, w, 0.07, m_gold_d, z=0.07)
        rect("line_r%d" % i, 0.95, y, w, 0.07, m_gold_d, z=0.07)

    # star above the book
    poly("star", star_verts(0.62, 0.26), m_gold, z=0.04, cy=1.95)

    # ribbon banner + label
    poly("banner", [(-2.2, -1.75), (2.2, -1.75), (2.2, -2.65), (-2.2, -2.65)],
         m_gold, z=0.08)
    poly("tail_l", [(-2.2, -1.75), (-2.9, -2.1), (-2.55, -2.4), (-2.2, -2.65)],
         m_gold_d, z=0.07)
    poly("tail_r", [(2.2, -1.75), (2.9, -2.1), (2.55, -2.4), (2.2, -2.65)],
         m_gold_d, z=0.07)
    text("banner_t", "FAKO", 0, -2.2, 0.62, m_dark, z=0.10)

    out = os.path.join(ARGS["out"], "school-crest.png")
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    print("BUILD_OK school-crest.png -> %s" % out)
    print("BUILD_BATCH_DONE 1 crest")


if __name__ == "__main__":
    build_crest()
