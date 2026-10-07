"""Batch 2 — UI textures for 'The Red Pen'.

Run:
  blender -b --factory-startup -P blender_build/build_ui.py -- --out <dir> --preview <dir>

Renders 9 flat, shadeless PNGs (emission materials + 'Standard' view transform,
so colors are exact):
  ui-gradebook.png
  ui-progress-40.png, ui-progress-100.png
  ui-ledger-240.png, ui-ledger-512.png, ui-ledger-0.png
  ui-portal-list.png, ui-portal-tapped.png
  ui-reportcard.png
"""
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (assign, clear_scene, emission_material, hex_rgba,
                    load_font, parse_args, set_emission_color)

ARGS = parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])

FONT_B = load_font(bold=True) or None
FONT_R = load_font(bold=False) or None

WHITE = (1.0, 1.0, 1.0, 1.0)
OFFWHITE = (0.97, 0.97, 0.95, 1.0)
GOLD = hex_rgba("#D4AF37")
GOLD_DARK = hex_rgba("#8A7018")
CREAM = (0.96, 0.93, 0.86, 1.0)
DARK = (0.12, 0.12, 0.14, 1.0)
GREY_TXT = (0.35, 0.35, 0.38, 1.0)
GREY_MID = (0.55, 0.55, 0.58, 1.0)
ROW_TINT = (0.93, 0.93, 0.94, 1.0)
RED = (0.72, 0.09, 0.09, 1.0)
GREEN = (0.09, 0.50, 0.20, 1.0)
CHARCOAL = (0.13, 0.13, 0.15, 1.0)


def rect(name, cx, cy, w, h, mat, z=0.02):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(cx, cy, z))
    o = bpy.context.active_object
    o.name = name
    o.scale = (w, h, 1.0)  # keep scale live so states can resize
    assign(o, mat)
    return o


def text(name, body, cx, cy, size, mat, align="CENTER", bold=True, z=0.06):
    bpy.ops.object.text_add(location=(cx, cy, z))
    t = bpy.context.active_object
    t.name = name
    t.data.body = body
    t.data.size = size
    t.data.align_x = align
    t.data.align_y = "CENTER"
    font = FONT_B if bold else FONT_R
    if font:
        t.data.font = font
    assign(t, mat)
    return t


def setup(w_units, h_units, res_x, res_y, bg_color):
    clear_scene()
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 16
    scene.cycles.device = "CPU"
    scene.view_settings.view_transform = "Standard"
    scene.render.film_transparent = False
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y

    cd = bpy.data.cameras.new("ui_cam")
    cd.type = "ORTHO"
    if res_y >= res_x:
        cd.sensor_fit = "VERTICAL"
        cd.ortho_scale = h_units
    else:
        cd.sensor_fit = "HORIZONTAL"
        cd.ortho_scale = w_units
    cam = bpy.data.objects.new("ui_cam", cd)
    scene.collection.objects.link(cam)
    cam.location = (0, 0, 5)
    scene.camera = cam

    bg = emission_material("UI_BG", bg_color)
    rect("ui_bg", 0, 0, w_units + 0.06, h_units + 0.06, bg, z=0.0)


def render(filename, out_dir):
    path = os.path.join(out_dir, filename)
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("BUILD_OK %s" % filename)
    return path


def em_mat(name, color):
    return emission_material(name, color)


# ---------------------------------------------------------------- gradebook
def build_gradebook():
    W, H, RX, RY = 10.8, 13.5, 1080, 1350
    setup(W, H, RX, RY, OFFWHITE)

    m_gold = em_mat("gb_gold", GOLD)
    m_dark = em_mat("gb_dark", DARK)
    m_grey = em_mat("gb_grey", GREY_TXT)
    m_hdr = em_mat("gb_hdr", CHARCOAL)
    m_row = em_mat("gb_row", ROW_TINT)
    m_white = em_mat("gb_white", WHITE)

    rect("header", 0, H / 2 - 0.8, W, 1.6, m_gold)
    text("header_t", "GRADEBOOK  ·  FORM 3", 0, H / 2 - 0.8, 0.55, m_dark)

    rect("colhdr", 0, 4.55, W, 0.8, m_hdr)
    text("c_name", "NAME", -5.0, 4.55, 0.30, m_white, align="LEFT")
    text("c_m", "MATHS", 1.5, 4.55, 0.30, m_white)
    text("c_e", "ENGLISH", 3.0, 4.55, 0.30, m_white)
    text("c_s", "SCIENCE", 4.35, 4.55, 0.30, m_white)
    text("c_t", "TOTAL", 5.15, 4.55, 0.30, m_white, align="RIGHT")

    rows = [
        ("KWAME ADJEI", "78", "84", "71", "233"),
        ("AMA OSEI", "92", "88", "95", "275"),
        ("KOFI MENSAH", "65", "72", "68", "205"),
        ("AKOSUA BOATENG", "96", "91", "94", "281"),
        ("YAA DARKO", "74", "79", "82", "235"),
        ("KWABENA SAFO", "58", "66", "61", "185"),
        ("EFUA TETEH", "85", "87", "89", "261"),
        ("SELORM KUDJOO", "81", "76", "78", "235"),
    ]
    top = 4.15
    rh = 0.95
    for i, (name, m, e, s, t) in enumerate(rows):
        y = top - i * rh
        if i % 2 == 1:
            rect("row%02d" % i, 0, y, W, rh, m_row, z=0.02)
        text("n%02d" % i, name, -5.0, y, 0.34, m_dark, align="LEFT", bold=False)
        text("m%02d" % i, m, 1.5, y, 0.34, m_grey, bold=False)
        text("e%02d" % i, e, 3.0, y, 0.34, m_grey, bold=False)
        text("s%02d" % i, s, 4.35, y, 0.34, m_grey, bold=False)
        text("t%02d" % i, t, 5.15, y, 0.34, m_dark, align="RIGHT")

    rect("footer", 0, -H / 2 + 0.55, W, 1.1, m_gold)
    text("footer_t", "VALIDATED AUTOMATICALLY  ·  FAKO ONLINE", 0, -H / 2 + 0.55, 0.32, m_dark)
    render("ui-gradebook.png", ARGS["out"])


# ----------------------------------------------------------------- progress
def build_progress():
    W, H, RX, RY = 10.8, 13.5, 1080, 1350
    setup(W, H, RX, RY, OFFWHITE)
    m_hdr = em_mat("pg_hdr", GOLD)      # header stays gold in both states
    m_state = em_mat("pg_state", GOLD)  # fill + percentage morph to green
    m_dark = em_mat("pg_dark", DARK)
    m_grey = em_mat("pg_grey", GREY_TXT)
    m_track = em_mat("pg_track", (0.85, 0.85, 0.86, 1.0))

    rect("header", 0, H / 2 - 0.8, W, 1.6, m_hdr)
    text("header_t", "REPORT CARDS", 0, H / 2 - 0.8, 0.55, m_dark)
    status = text("status", "Generating report cards...", 0, 1.2, 0.5, m_dark)
    rect("track", 0, -0.6, 8.4, 0.9, m_track)
    fill = rect("fill", -4.0 + (8.0 * 0.4) / 2, -0.6, 8.0 * 0.4, 0.5, m_state, z=0.04)
    pct = text("pct", "40%", 0, -2.1, 0.9, m_state)
    text("foot", "FAKO ONLINE  ·  SCHOOLS PORTAL", 0, -H / 2 + 0.6, 0.3, m_grey)

    render("ui-progress-40.png", ARGS["out"])

    fill.scale = (8.0, 0.5, 1.0)
    fill.location.x = 0.0
    pct.data.body = "100%"
    set_emission_color(m_state, GREEN)
    status.data.body = "Report cards ready!"
    render("ui-progress-100.png", ARGS["out"])


# ------------------------------------------------------------------- ledger
def build_ledger():
    W, H, RX, RY = 10.8, 7.6, 1080, 760
    setup(W, H, RX, RY, CREAM)
    m_hdr = em_mat("lg_hdr", CHARCOAL)
    m_white = em_mat("lg_white", WHITE)
    m_val = em_mat("lg_val", RED)
    m_grey = em_mat("lg_grey", GREY_TXT)
    m_dark = em_mat("lg_dark", DARK)

    rect("header", 0, H / 2 - 0.6, W, 1.2, m_hdr)
    text("header_t", "PRINTING COSTS", 0, H / 2 - 0.6, 0.5, m_white)
    val = text("val", "GH\u20B5 240", 0, 0.1, 1.3, m_val)
    sub = text("sub", "paper, toner & printer servicing  ·  per term", 0, -1.3, 0.32, m_grey)
    rect("rule", 0, -2.5, 9.0, 0.05, m_grey, z=0.03)
    text("foot", "FAKO ONLINE", 0, -3.1, 0.28, m_dark)

    render("ui-ledger-240.png", ARGS["out"])
    val.data.body = "GH\u20B5 512"
    render("ui-ledger-512.png", ARGS["out"])
    set_emission_color(m_val, GREEN)
    val.data.body = "GH\u20B5 0"
    sub.data.body = "automated reports  ·  nothing to print"
    render("ui-ledger-0.png", ARGS["out"])


# ------------------------------------------------------------------- portal
def build_portal():
    W, H, RX, RY = 7.2, 14.4, 720, 1440
    setup(W, H, RX, RY, WHITE)
    m_hdr = em_mat("pt_hdr", GOLD)     # header stays gold in both states
    m_btn = em_mat("pt_btn", GOLD)     # button morphs to dark gold when tapped
    m_dark = em_mat("pt_dark", DARK)
    m_grey = em_mat("pt_grey", GREY_TXT)
    m_card = em_mat("pt_card", (0.96, 0.96, 0.96, 1.0))
    m_row = em_mat("pt_row", ROW_TINT)
    m_green = em_mat("pt_green", GREEN)
    m_white = em_mat("pt_white", WHITE)

    rect("header", 0, H / 2 - 0.7, W, 1.4, m_hdr)
    text("header_t", "FAKO ONLINE", 0, H / 2 - 0.7, 0.48, m_dark)
    text("sect", "REPORT CARDS", -3.1, 5.4, 0.3, m_grey, align="LEFT")

    rect("card1", 0, 3.9, 6.4, 2.4, m_card)
    text("c1t", "Term 1  ·  Form 3", -2.9, 4.5, 0.36, m_dark, align="LEFT")
    rect("pill", 2.3, 4.5, 1.5, 0.55, m_green, z=0.04)
    text("pill_t", "READY", 2.3, 4.5, 0.24, m_white, z=0.06)
    rect("btn", -0.6, 3.1, 4.2, 0.95, m_btn, z=0.04)
    btn_t = text("btn_t", "DOWNLOAD", -0.6, 3.1, 0.38, m_dark, z=0.06)

    rect("card2", 0, 1.0, 6.4, 2.0, m_row)
    text("c2t", "Term 2  ·  Form 3", -2.9, 1.4, 0.34, m_grey, align="LEFT", bold=False)
    text("c2s", "coming soon", -2.9, 0.6, 0.26, m_grey, align="LEFT", bold=False)

    rect("nav", 0, -H / 2 + 0.7, W, 1.4, m_row)
    text("nav_t", "Home    Reports    Fees", 0, -H / 2 + 0.7, 0.3, m_grey)

    render("ui-portal-list.png", ARGS["out"])

    set_emission_color(m_btn, GOLD_DARK)
    btn_t.data.body = "DOWNLOADED"
    render("ui-portal-tapped.png", ARGS["out"])


# --------------------------------------------------------------- reportcard
def build_reportcard():
    W, H, RX, RY = 10.8, 14.4, 1080, 1440
    setup(W, H, RX, RY, WHITE)
    m_gold = em_mat("rc_gold", GOLD)
    m_dark = em_mat("rc_dark", DARK)
    m_grey = em_mat("rc_grey", GREY_TXT)
    m_hdr = em_mat("rc_hdr", CHARCOAL)
    m_white = em_mat("rc_white", WHITE)
    m_tint = em_mat("rc_tint", (0.99, 0.97, 0.90, 1.0))

    t = 0.28  # border thickness
    rect("b_top", 0, H / 2 - t / 2, W, t, m_gold, z=0.03)
    rect("b_bot", 0, -H / 2 + t / 2, W, t, m_gold, z=0.03)
    rect("b_l", -W / 2 + t / 2, 0, t, H, m_gold, z=0.03)
    rect("b_r", W / 2 - t / 2, 0, t, H, m_gold, z=0.03)

    # crest placeholder (Batch 3 refines the standalone crest)
    bpy.ops.mesh.primitive_circle_add(radius=0.75, fill_type="NGON", location=(0, 5.9, 0.03))
    disc = bpy.context.active_object
    disc.name = "crest_disc"
    assign(disc, m_gold)
    bpy.ops.mesh.primitive_circle_add(radius=0.48, fill_type="NGON", location=(0, 5.9, 0.05))
    inner = bpy.context.active_object
    inner.name = "crest_inner"
    assign(inner, m_hdr)
    rect("crest_book", 0, 5.9, 0.5, 0.36, m_white, z=0.07)

    text("title", "STUDENT REPORT CARD", 0, 4.7, 0.6, m_dark)
    text("name", "AKOSUA BOATENG", 0, 3.75, 0.42, m_dark)
    text("term", "FORM 3  ·  TERM 1", 0, 3.1, 0.3, m_grey, bold=False)

    rect("thead", 0, 2.3, 9.4, 0.7, m_hdr, z=0.03)
    text("th_s", "SUBJECT", -4.3, 2.3, 0.3, m_white, align="LEFT")
    text("th_g", "GRADE", 4.3, 2.3, 0.3, m_white, align="RIGHT")

    subjects = [("MATHEMATICS", "A1"), ("ENGLISH LANGUAGE", "A1"),
                ("INTEGRATED SCIENCE", "B2"), ("SOCIAL STUDIES", "A1"),
                ("CREATIVE ARTS", "B3")]
    top = 1.78
    rh = 0.62
    for i, (subj, grade) in enumerate(subjects):
        y = top - i * rh
        text("s%02d" % i, subj, -4.3, y, 0.32, m_dark, align="LEFT", bold=False)
        text("g%02d" % i, grade, 4.3, y, 0.32, m_gold, align="RIGHT")

    rect("cbox", 0, -2.7, 9.4, 1.8, m_tint, z=0.03)
    text("clabel", "TEACHER'S COMMENT", -4.3, -2.1, 0.26, m_grey, align="LEFT")
    text("comment", "Excellent improvement. Keep it up.", -4.3, -3.0, 0.34, m_dark,
         align="LEFT", bold=False)

    rect("sigline", 2.6, -4.9, 4.0, 0.04, m_dark, z=0.04)
    text("siglabel", "Class Teacher", 4.6, -5.3, 0.26, m_grey, align="RIGHT", bold=False)
    text("foot", "GENERATED BY FAKO ONLINE  ·  NO PRINTING NEEDED", 0, -6.5, 0.26, m_grey)

    render("ui-reportcard.png", ARGS["out"])


if __name__ == "__main__":
    for fn in (build_gradebook, build_progress, build_ledger,
               build_portal, build_reportcard):
        fn()
        print("BUILD_ASSET_DONE %s" % fn.__name__)
    print("BUILD_BATCH_DONE 5 UI assets / 9 PNGs")
