"""Batch 6 - Assembly: report_cards.blend (all assets, cameras M1-M8, animation).

Terminal-only:
  blender -b --factory-startup -P assemble_scene.py -- \
      --out global_assets/models --preview plans/report-cards/previews --qa 1

Conventions:
  * Script frames (script.md, 0-based) -> Blender frames via F(n) = n + 1.
  * Zones along +X: staff 0, office +20, courtyard +40, void +60.
  * Timeline markers M1..M8 bind cameras so one `-a` render cuts all 8 shots.
"""
import math
import os
import random
import sys

import bpy
import mathutils

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import clear_scene, load_font, set_world, srgb_to_linear  # noqa: E402

D = math.radians
Z_STAFF, Z_OFF, Z_CY, Z_VOID = 0.0, 20.0, 40.0, 60.0
random.seed(7)


def F(n):
    """script.md frame (0-based) -> Blender frame (1-based)."""
    return n + 1


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    a = {"out": "global_assets/models",
         "preview": "plans/report-cards/previews",
         "models": "global_assets/models",
         "ui": "global_assets/ui",
         "hdris": "global_assets/hdris",
         "qa": "0"}
    i = 0
    while i < len(argv) - 1:
        key = argv[i].lstrip("-")
        if key in a:
            a[key] = argv[i + 1]
            i += 2
        else:
            i += 1
    for k in ("out", "preview", "models", "ui", "hdris"):
        a[k] = os.path.abspath(a[k])
    os.makedirs(a["out"], exist_ok=True)
    os.makedirs(a["preview"], exist_ok=True)
    return a


ARGS = parse_args()
scene = bpy.context.scene
FONT_BOLD = load_font(bold=True)
FONT_REG = load_font(bold=False)


# ------------------------------------------------------------------ append
def load_lib(path, want_actions=False, only=None):
    """Append objects (and deps) from a .blend. Returns (objects, {orig_act_name: action})."""
    with bpy.data.libraries.load(path, link=False) as (df, dt):
        obj_structs = [o for o in df.objects
                       if only is None or o in only]
        act_names = list(df.actions) if want_actions else []
        dt.objects = list(obj_structs)
        dt.actions = [df.actions[i] for i in range(len(act_names))] \
            if want_actions else []
    objs = [o for o in dt.objects if o is not None]
    acts = dict(zip(act_names, [a for a in dt.actions if a is not None]))
    for o in objs:
        if o.name not in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.link(o)
    return objs, acts


def zone_parent(name, offset, objs):
    """Parent objs to a root empty and shift it to offset on X."""
    root = bpy.data.objects.new(name, None)
    scene.collection.objects.link(root)
    for o in objs:
        if o.parent is None:
            o.parent = root
    root.location.x = offset
    return root


# ------------------------------------------------------------------ keys
def key_loc(o, fr, loc):
    o.location = loc
    o.keyframe_insert("location", frame=fr)


def key_rot(o, fr, rot):
    o.rotation_euler = rot
    o.keyframe_insert("rotation_euler", frame=fr)


def key_scale(o, fr, s):
    o.scale = s if hasattr(s, "__len__") else (s, s, s)
    o.keyframe_insert("scale", frame=fr)


def key_hide(o, fr, hidden):
    o.hide_render = hidden
    o.keyframe_insert("hide_render", frame=fr)


def vis_spans(o, spans):
    """Key hide_render so objects render only inside script-frame spans."""
    events = [(F(0), True)]
    for s, e in spans:
        events.append((F(s), False))
        events.append((F(e) + 1, True))
    for fr, hidden in sorted(events, key=lambda x: x[0]):
        key_hide(o, fr, hidden)


def subtree(root):
    out = [root]
    for c in root.children_recursive:
        out.append(c)
    return out


def make_linear(o):
    ad = o.animation_data
    if ad and ad.action:
        for fc in ad.action.fcurves:
            for kp in fc.keyframe_points:
                if fc.data_path in ("hide_render",):
                    kp.interpolation = "CONSTANT"
                else:
                    kp.interpolation = "LINEAR"


def key_hide_linearize(o):
    ad = o.animation_data
    if ad and ad.action:
        for fc in fcurves_of(ad):
            if fc.data_path == "hide_render":
                for kp in fc.keyframe_points:
                    kp.interpolation = "CONSTANT"


def fcurves_of(ad):
    """Blender 5.x slotted actions: fcurves live in layer/strip/channelbag."""
    if ad is None or ad.action is None:
        return []
    act = ad.action
    if hasattr(act, "fcurves"):
        try:
            return list(act.fcurves)
        except Exception:
            pass
    out = []
    slot = getattr(ad, "action_slot", None)
    for layer in act.layers:
        for strip in layer.strips:
            for cb in strip.channelbags:
                if slot is None or cb.slot == slot:
                    out.extend(cb.fcurves)
    return out


# ------------------------------------------------------------------ materials
def _emission_node(nt, color, strength):
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = color
    em.inputs["Strength"].default_value = strength
    return em


def ui_mat(name, img_path=None, color=(1, 1, 1, 1), strength=1.0,
           mix_transparent=False):
    """Flat emission material (optional image), optionally Transparent mix."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    col = tuple(_lin(c) for c in color[:3]) + (color[3],)
    if img_path:
        img = bpy.data.images.load(img_path, check_existing=True)
        em = _emission_node(nt, (1, 1, 1, 1), strength)
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = img
        nt.links.new(tex.outputs["Color"], em.inputs["Color"])
    else:
        em = _emission_node(nt, col, strength)
    if mix_transparent:
        tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        mx = nt.nodes.new("ShaderNodeMixShader")
        mx.name = "MixShader"
        mx.inputs["Fac"].default_value = 0.0
        nt.links.new(tr.outputs[0], mx.inputs[1])
        nt.links.new(em.outputs[0], mx.inputs[2])
        nt.links.new(mx.outputs[0], out.inputs["Surface"])
    else:
        nt.links.new(em.outputs[0], out.inputs["Surface"])
    return mat


def mix_fac(mat):
    """Fac input of the material's MixShader (for alpha-style keyframes)."""
    return mat.node_tree.nodes["MixShader"].inputs["Fac"]


def _lin(c):
    return srgb_to_linear(c)


def ui_plane(name, loc, w, h, mat, rot=(D(90), 0, 0)):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.scale = (w, h, 1)
    o.data.materials.append(mat)
    return o


def make_text(name, body, size, loc, rot, mat, align="CENTER"):
    bpy.ops.object.text_add(location=loc, rotation=rot)
    t = bpy.context.active_object
    t.name = name
    t.data.body = body
    t.data.size = size
    t.data.align_x = align
    t.data.extrude = 0.002
    if FONT_BOLD:
        t.data.font = FONT_BOLD
    t.data.materials.append(mat)
    return t


def make_cam(name, lens, loc, aim=None, keys=None, track=None,
             dof=None, fstop=4.0):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cam = bpy.data.objects.new(name, cd)
    scene.collection.objects.link(cam)
    cam.location = loc
    if track is not None:
        con = cam.constraints.new("TRACK_TO")
        con.target = track
        con.track_axis = "TRACK_NEGATIVE_Z"
        con.up_axis = "UP_Y"
    elif aim is not None:
        direction = mathutils.Vector(aim) - mathutils.Vector(loc)
        cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    if keys:
        for fr, l in keys:
            key_loc(cam, fr, l)
    if dof:
        cd.dof.use_dof = True
        cd.dof.aperture_fstop = fstop
        for fr, dist in dof:
            cd.dof.focus_distance = dist
            cd.keyframe_insert("dof.focus_distance", frame=fr)
    return cam


def aim_empty(name, loc):
    e = bpy.data.objects.new(name, None)
    scene.collection.objects.link(e)
    e.location = loc
    return e


def marker(name, frame, cam):
    m = scene.timeline_markers.new(name, frame=frame)
    m.camera = cam
    return m


# ------------------------------------------------------------------ scene setup
clear_scene()  # drop factory-startup Cube/Camera/Light
scene.render.engine = "CYCLES"
scene.cycles.samples = 128
scene.render.use_persistent_data = True
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 100
scene.render.fps = 30
scene.render.fps_base = 1.0
scene.frame_start = 1
scene.frame_end = 900
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"
scene.render.filepath = "//fako_####"
scene.camera = None

M = lambda f: os.path.join(ARGS["models"], f)
U = lambda f: os.path.join(ARGS["ui"], f)
H = lambda f: os.path.join(ARGS["hdris"], f)

print("ASSEMBLE: world...")
set_world(H("hdri-day.exr"), 0.18)

print("ASSEMBLE: sets...")
sets = {}
for key, fname, offset in (("staff", "set-staffroom.blend", Z_STAFF),
                           ("office", "set-office.blend", Z_OFF),
                           ("cy", "set-courtyard.blend", Z_CY),
                           ("void", "set-digital-void.blend", Z_VOID)):
    objs, _ = load_lib(M(fname))
    root = zone_parent("zone_" + key, offset, objs)
    sets[key] = {"root": root, "objs": objs}
    print("  set %s -> %d objects" % (key, len(objs)))

O = lambda name: bpy.data.objects[name]


# ------------------------------------------------------------------ props (staff zone)
print("ASSEMBLE: props...")
redpen_objs, _ = load_lib(M("red-pen.blend"))
REDPEN = redpen_objs[0]
REDPEN.location = (-0.05, -0.33, 0.825)
REDPEN.rotation_euler = (D(65), 0, 0)

tray_objs, _ = load_lib(M("report-tray.blend"))
TRAY = tray_objs[0]
TRAY.location = (0.62, -0.42, 0.78)
TRAY.rotation_euler = (0, 0, D(-12))

# tower: four booklet stacks on the desk
tower = bpy.data.objects.new("TowerRoot", None)
scene.collection.objects.link(tower)
tower.location = (0.45, -0.05, 0.78)
for i in range(4):
    objs, _ = load_lib(M("booklet-stack.blend"))
    s = objs[0]
    s.parent = tower
    s.location = (0, 0, i * 0.175)
    s.rotation_euler = (0, 0, D(random.uniform(-14, 14)))
TOWER_KIDS = subtree(tower)

# clock on back wall
clock_objs, _ = load_lib(M("wall-clock.blend"))
clock_root = bpy.data.objects.new("ClockRoot", None)
scene.collection.objects.link(clock_root)
for o in clock_objs:
    o.parent = clock_root
clock_root.location = (-0.6, 2.90, 2.35)
clock_root.rotation_euler = (D(90), 0, 0)
HAND_H = bpy.data.objects["HandHour"]
HAND_M = bpy.data.objects["HandMinute"]
HAND_S = bpy.data.objects["HandSecond"]

# tablet + checkmark (pivot shot)
tablet_objs, _ = load_lib(M("tablet.blend"))
TABLET = tablet_objs[0]
TABLET.location = (-0.45, -0.35, 0.86)
TABLET.rotation_euler = (D(70), 0, 0)

chk_objs, chk_acts = load_lib(M("checkmark-gold.blend"))
CHECK = chk_objs[0]
CHECK.location = (-0.45, -0.30, 1.35)
chk_mat = CHECK.data.materials[0]

# money (office zone)
money_objs, _ = load_lib(M("money-notes.blend"))
MONEY = [o for o in money_objs if o.parent is None][0]
MONEY.location = (Z_OFF - 0.3, -0.10, 1.07)
MONEY_KIDS = subtree(MONEY)

# phone prop (unused standalone - student rig carries one); keep hidden
phone_objs, _ = load_lib(M("phone.blend"))
PHONE = phone_objs[0]
PHONE.location = (Z_OFF + 0.0, -0.4, 1.06)
key_hide(PHONE, 1, True)

# ------------------------------------------------------------------ characters
print("ASSEMBLE: characters...")


def character(tag, fname, pose, loc, rot_z=0.0):
    objs, acts = load_lib(M(fname), want_actions=True)
    rig = next(o for o in objs if o.type == "ARMATURE")
    for orig, act in list(acts.items()):
        act.name = "%s_%s" % (tag, orig)
    rig.name = "rig_" + tag
    rig.location = loc
    rig.rotation_euler = (0, 0, rot_z)
    rig.animation_data_create()
    rig.animation_data.action = acts[pose]
    return {"tag": tag, "rig": rig, "objs": objs,
            "acts": {k: v for k, v in acts.items()}}


TEACH_A = character("tA", "teacher.blend", "T1", (0.0, 0.55, 0.0))
TEACH_B = character("tB", "teacher.blend", "T2", (0.0, 0.55, 0.0))
TEACH_C = character("tC", "teacher.blend", "T3", (0.0, 0.55, 0.0))
STU_OFF = character("so", "student.blend", "S1",
                    (Z_OFF + 1.05, -1.15, 0.0), D(-20))
PAR_OFF = character("po", "parent.blend", "P1",
                    (Z_OFF + 1.5, -0.85, 0.0), D(-28))
STU_C1 = character("c1", "student.blend", "S1", (Z_CY + 0.35, 3.1, 0.0))
STU_C2 = character("c2", "student.blend", "S2", (Z_CY + 0.35, 3.1, 0.0))


def char_vis(ch, spans):
    for o in ch["objs"]:
        vis_spans(o, spans)


char_vis(TEACH_A, [(0, 74), (195, 479)])
char_vis(TEACH_B, [(75, 194)])
char_vis(TEACH_C, [(690, 764)])
char_vis(STU_OFF, [(300, 404)])
char_vis(PAR_OFF, [(300, 404)])
char_vis(STU_C1, [(630, 644)])
char_vis(STU_C2, [(645, 689)])

# ------------------------------------------------------------------ shot-2 exam page
print("ASSEMBLE: exam page...")
page_mat = ui_mat("m_page", color=(0.93, 0.93, 0.90, 1.0), strength=0.55)
PAGE = ui_plane("exam_page", (0.0, -0.20, 0.783), 0.21, 0.30, page_mat,
                rot=(0, 0, 0))
ink_mat = ui_mat("m_ink", color=(0.72, 0.03, 0.03, 1.0), strength=1.6)
T17 = make_text("t17", "17", 0.062, (-0.045, -0.24, 0.786), (0, 0, 0), ink_mat)
T71 = make_text("t71", "71", 0.062, (0.030, -0.24, 0.786), (0, 0, 0), ink_mat)

# scribble-out over "17": three crossing strokes
scrib_objs = []
for i, ang in enumerate((18, -14, 40)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.045, -0.24, 0.788))
    b = bpy.context.active_object
    b.name = "scribble%d" % i
    b.scale = (0.055, 0.005, 0.003)
    b.rotation_euler = (0, 0, D(ang))
    b.data.materials.append(ink_mat)
    scrib_objs.append(b)

# ghost scores rippling over the tower
ghosts = []
ghost_text = ["17", "71", "58", "63", "49", "72", "38", "65"]
ghost_mat = ui_mat("m_ghost", color=(0.85, 0.10, 0.08, 1.0), strength=1.0)
for i, txt in enumerate(ghost_text):
    top = i % 5 < 3
    if top:
        loc = (random.uniform(-0.05, 0.05), random.uniform(-0.04, 0.04),
               0.18 * (1 + (i % 3)) + 0.005)
        rot = (0, 0, D(random.uniform(-30, 30)))
    else:
        loc = (random.uniform(-0.05, 0.05), -0.095,
               0.10 + 0.18 * (i % 3))
        rot = (D(90), 0, D(random.uniform(-12, 12)))
    g = make_text("ghost%d" % i, txt, 0.045, (0, 0, 0), rot, ghost_mat)
    g.parent = tower
    g.location = loc
    ghosts.append(g)

# cursor (pivot click)
cur_mat = ui_mat("m_cursor", color=(0.10, 0.10, 0.12, 1.0), strength=1.4)
bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.016, depth=0.002,
                                location=(-0.42, -0.52, 1.02),
                                rotation=(D(70), 0, D(15)))
CURSOR = bpy.context.active_object
CURSOR.name = "cursor"
CURSOR.data.materials.append(cur_mat)

# white dissolve wipe parented to M5 camera (created with cam in Part C)
WIPE_MAT = ui_mat("m_wipe", color=(1, 1, 1, 1), strength=1.0,
                  mix_transparent=True)

# ------------------------------------------------------------------ staff props visibility
vis_spans(REDPEN, [(0, 479)])
vis_spans(TRAY, [(195, 479)])
for o in TOWER_KIDS:
    vis_spans(o, [(0, 479)])
vis_spans(PAGE, [(0, 479)])
vis_spans(T17, [(96, 194)])
vis_spans(T71, [(156, 194)])
for s in scrib_objs:
    vis_spans(s, [(140, 194)])
for g in ghosts:
    vis_spans(g, [(176, 479)])
vis_spans(TABLET, [(405, 479)])
vis_spans(CHECK, [(445, 479)])
vis_spans(CURSOR, [(405, 415)])

# ------------------------------------------------------------------ office UI (M4)
print("ASSEMBLE: office UI...")
LED240 = ui_plane("led240", (Z_OFF - 0.5, -0.12, 1.28), 0.66, 0.465,
                  ui_mat("m_led240", img_path=U("ui-ledger-240.png")))
LED512 = ui_plane("led512", (Z_OFF - 0.5, -0.12, 1.28), 0.66, 0.465,
                  ui_mat("m_led512", img_path=U("ui-ledger-512.png")))
vis_spans(LED240, [(300, 339)])
vis_spans(LED512, [(340, 404)])

# money rise (staggered) ---------------------------------------------
money_anim = [o for o in MONEY_KIDS if o != MONEY]
for i, o in enumerate(money_anim):
    l0 = tuple(o.location)
    r0 = tuple(o.rotation_euler)
    start = F(300) + i * 2
    end = start + 42
    key_loc(o, F(299), l0)
    key_loc(o, start, l0)
    key_loc(o, end, (l0[0] + random.uniform(-0.35, 0.35), l0[1],
                     l0[2] + 0.8))
    key_rot(o, start, r0)
    key_rot(o, end, (r0[0] + random.uniform(1.5, 4.0),
                     r0[1] + random.uniform(-2.0, 2.0),
                     r0[2] + random.uniform(-3.0, 3.0)))
for o in MONEY_KIDS:
    vis_spans(o, [(300, 362)])

# ------------------------------------------------------------------ courtyard portal (M7a)
print("ASSEMBLE: courtyard UI...")
PORTAL = ui_plane("portal", (Z_CY + 0.90, 2.70, 1.55), 0.35, 0.70,
                  ui_mat("m_portal", img_path=U("ui-portal-list.png")),
                  rot=(D(90), 0, D(-8)))
TAPPED = ui_plane("portal_tapped", (Z_CY + 0.90, 2.70, 1.55), 0.35, 0.70,
                  ui_mat("m_tapped", img_path=U("ui-portal-tapped.png")),
                  rot=(D(90), 0, D(-8)))
CARD = ui_plane("reportcard_ui", (Z_CY + 0.75, 2.72, 1.55), 0.675, 0.90,
                ui_mat("m_card", img_path=U("ui-reportcard.png"),
                       strength=1.0))
vis_spans(PORTAL, [(645, 674)])
vis_spans(TAPPED, [(675, 677)])
vis_spans(CARD, [(678, 689)])
# portal flies out of the student's phone, card pops + glows
key_loc(PORTAL, F(644), (Z_CY + 0.55, 3.0, 1.15))
key_loc(PORTAL, F(654), (Z_CY + 0.90, 2.70, 1.55))
key_scale(PORTAL, F(645), 0.05)
key_scale(PORTAL, F(650), 1.06)
key_scale(PORTAL, F(654), 1.0)
key_scale(CARD, F(678), 0.001)
key_scale(CARD, F(684), 1.12)
key_scale(CARD, F(688), 1.0)
card_em = next(n for n in CARD.data.materials[0].node_tree.nodes
               if n.type == "EMISSION")
for fr, s in ((F(678), 1.0), (F(682), 2.6), (F(686), 1.4), (F(690), 2.0)):
    card_em.inputs["Strength"].default_value = s
    card_em.inputs["Strength"].keyframe_insert("default_value", frame=fr)

# ------------------------------------------------------------------ void UI (M6)
print("ASSEMBLE: void UI...")
GB = ui_plane("gradebook", (Z_VOID, 1.5, 1.6), 1.24, 1.55,
              ui_mat("m_gb", img_path=U("ui-gradebook.png")))
vis_spans(GB, [(480, 574)])

row_fy = [0.207, 0.260, 0.328, 0.397, 0.466, 0.536, 0.604, 0.673]
check_rows = [("kwame", 0, 480), ("ama", 1, 488), ("akosua", 3, 496),
              ("yaa", 4, 504), ("kwabena", 5, 512), ("efua", 6, 520),
              ("selorm", 7, 528), ("kofi", 2, 568)]
green_mat = ui_mat("m_green", color=(0.06, 0.55, 0.16, 1.0), strength=1.8)


def build_check(name, loc):
    root = bpy.data.objects.new(name, None)
    scene.collection.objects.link(root)
    root.location = loc
    for j, (dx, dz, ang, ln) in enumerate(
            ((-0.014, 0.006, 28, 0.045), (0.017, -0.002, -48, 0.028))):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
        b = bpy.context.active_object
        b.name = "%s_s%d" % (name, j)
        b.scale = (ln, 0.006, 0.011)
        b.rotation_euler = (0, D(ang), 0)
        b.data.materials.append(green_mat)
        b.parent = root
        b.location = (dx, 0, dz)
    return root


for label, ri, pop in check_rows:
    x = Z_VOID + (0.931 - 0.5) * 1.24
    z = 1.6 + (0.5 - row_fy[ri]) * 1.55
    c = build_check("chk_" + label, (x, 1.487, z))
    key_scale(c, F(pop) - 1, 0.001)
    key_scale(c, F(pop), 1.18)
    key_scale(c, F(pop) + 5, 1.0)
    for part in subtree(c):
        vis_spans(part, [(pop, 574)])

# red flash + sweep on KOFI row (wrong total corrected)
flash_mat = ui_mat("m_flash", color=(0.95, 0.12, 0.10, 1.0), strength=1.4,
                   mix_transparent=True)
FLASH = ui_plane("flash_row",
                 (Z_VOID - 0.25, 1.482, 1.6 + (0.5 - row_fy[2]) * 1.55),
                 1.16, 0.09, flash_mat)
fac = mix_fac(flash_mat)
for fr, v in ((F(480), 0.0), (F(554), 0.0), (F(555), 0.62),
              (F(567), 0.62), (F(568), 0.0)):
    fac.default_value = v
    fac.keyframe_insert("default_value", frame=fr)
key_loc(FLASH, F(555), (Z_VOID - 0.25, 1.482,
                        1.6 + (0.5 - row_fy[2]) * 1.55))
key_loc(FLASH, F(567), (Z_VOID + 0.25, 1.482,
                        1.6 + (0.5 - row_fy[2]) * 1.55))

# progress states
P40 = ui_plane("prog40", (Z_VOID, 1.5, 1.6), 1.24, 1.55,
               ui_mat("m_p40", img_path=U("ui-progress-40.png")))
P100 = ui_plane("prog100", (Z_VOID, 1.5, 1.6), 1.24, 1.55,
                ui_mat("m_p100", img_path=U("ui-progress-100.png")))
vis_spans(P40, [(575, 604)])
vis_spans(P100, [(605, 629)])

# GHc 0 card flips in
L0 = ui_plane("ledger0", (Z_VOID, 1.48, 0.62), 0.55, 0.39,
              ui_mat("m_l0", img_path=U("ui-ledger-0.png")))
vis_spans(L0, [(600, 629)])
key_rot(L0, F(600), (D(170), 0, 0))
key_rot(L0, F(605), (D(82), 0, 0))
key_rot(L0, F(608), (D(90), 0, 0))

# ------------------------------------------------------------------ end card (M8)
print("ASSEMBLE: end card...")
END_BG = ui_plane("endcard_bg", (Z_VOID, 2.6, 1.6), 6.0, 6.0,
                  ui_mat("m_endbg", color=(0.039, 0.039, 0.039, 1.0),
                         strength=1.0))
vis_spans(END_BG, [(765, 899)])
END_FLOOR = ui_plane("endcard_floor", (Z_VOID, 0.4, 0.35), 6.0, 4.6,
                     ui_mat("m_endfloor",
                            color=(0.039, 0.039, 0.039, 1.0),
                            strength=1.0),
                     rot=(0, 0, 0))
vis_spans(END_FLOOR, [(765, 899)])
vis_spans(O("dv_ring"), [(0, 764)])

icons_root = bpy.data.objects.new("IconsRoot", None)
scene.collection.objects.link(icons_root)
icons_root.location = (Z_VOID, 1.5, 1.6)

# printer icon (subset append of office printer)
pobjs, _ = load_lib(M("set-office.blend"),
                    only={"printer_body", "printer_lid", "printer_panel",
                          "printer_slot"})
ic_printer = bpy.data.objects.new("ic_printer", None)
scene.collection.objects.link(ic_printer)
center = mathutils.Vector((0.9, 0.1, 1.30))
for o in pobjs:
    o.parent = ic_printer
    o.location = mathutils.Vector(o.location) - center
ic_printer.parent = icons_root
ic_printer.location = (-0.52, 0, 0)
ic_printer.scale = (0.9, 0.9, 0.9)

# clock icon (second wall-clock load) + fast hands
cobjs, _ = load_lib(M("wall-clock.blend"))
ic_clock = bpy.data.objects.new("ic_clock", None)
scene.collection.objects.link(ic_clock)
i_hands = []
for o in cobjs:
    o.parent = ic_clock
    if o.name.startswith("Hand"):
        i_hands.append(o)
ic_clock.parent = icons_root
ic_clock.location = (0, 0, 0)
ic_clock.scale = (0.9, 0.9, 0.9)

# green-check stack (3 loads)
ic_checks = bpy.data.objects.new("ic_checks", None)
scene.collection.objects.link(ic_checks)
for i in range(3):
    objs, _ = load_lib(M("checkmark-gold.blend"))
    k = objs[0]
    k.parent = ic_checks
    k.location = (0, 0, (i - 1) * 0.075)
    k.rotation_euler = (0, 0, D(random.uniform(-14, 14)))
ic_checks.parent = icons_root
ic_checks.location = (0.52, 0, 0)
ic_checks.scale = (1.5, 1.5, 1.5)

# pop-in with spring, then snap to center + shrink
for grp, t0 in ((ic_printer, 765), (ic_clock, 770), (ic_checks, 775)):
    key_scale(grp, F(t0), 0.001)
    key_scale(grp, F(t0) + 7, 1.15)
    key_scale(grp, F(t0) + 11, 1.0)
    key_scale(grp, F(796), 1.0)
    key_scale(grp, F(816), 0.05)
    key_loc(grp, F(796), tuple(grp.location))
    key_loc(grp, F(816), (0, 0, 0))
    for part in subtree(grp):
        vis_spans(part, [(t0, 899)])

# fast-spinning clock hands on the icon
if i_hands:
    hm = i_hands[-1]
    key_rot(hm, F(765), tuple(hm.rotation_euler))
    key_rot(hm, F(899), (hm.rotation_euler.x, hm.rotation_euler.y,
                         hm.rotation_euler.z - 6 * 2 * math.pi))

# gold sparkle
star_verts = []
for i in range(16):
    a = math.pi * 2 * i / 16 + math.pi / 2
    r = 0.30 if i % 2 == 0 else 0.11
    star_verts.append((math.cos(a) * r, 0.0, math.sin(a) * r))
mesh = bpy.data.meshes.new("sparkle_mesh")
mesh.from_pydata(star_verts, [], [list(range(16))])
mesh.update()
SPARK = bpy.data.objects.new("sparkle", mesh)
scene.collection.objects.link(SPARK)
SPARK.parent = icons_root
SPARK.location = (0, -0.05, 0)
spark_mat = ui_mat("m_spark", color=(0.83, 0.66, 0.18, 1.0), strength=5.0)
SPARK.data.materials.append(spark_mat)
vis_spans(SPARK, [(812, 899)])
key_scale(SPARK, F(812), 0.001)
key_scale(SPARK, F(819), 1.25)
key_scale(SPARK, F(823), 1.0)
key_scale(SPARK, F(859), 1.07)
key_scale(SPARK, F(879), 1.0)
spark_em = next(n for n in spark_mat.node_tree.nodes if n.type == "EMISSION")
for fr, s in ((F(819), 7.0), (F(845), 3.5), (F(875), 5.5)):
    spark_em.inputs["Strength"].default_value = s
    spark_em.inputs["Strength"].keyframe_insert("default_value", frame=fr)

# gold rim light (only during M8)
rim_d = bpy.data.lights.new("rim8", type="AREA")
rim_d.size = 2.5
rim_d.energy = 0.0
rim_d.color = (1.0, 0.82, 0.45)
RIM = bpy.data.objects.new("rim8", rim_d)
scene.collection.objects.link(RIM)
RIM.location = (Z_VOID, 2.4, 2.7)
RIM.rotation_euler = (D(-45), 0, 0)
for fr, e in ((F(764), 0.0), (F(770), 260.0)):
    rim_d.energy = e
    rim_d.keyframe_insert("energy", frame=fr)

# ------------------------------------------------------------------ cameras + markers
print("ASSEMBLE: cameras...")
aim_desk = O("target_desk")
aim_counter = O("target_counter")
aim_page = aim_empty("aim_page", (0.0, -0.20, 0.783))
aim_m5 = aim_empty("aim_m5", (-0.30, -0.34, 1.00))
for fr, loc in ((F(405), (-0.30, -0.34, 1.00)),
                (F(445), (0.00, -0.30, 1.32)),
                (F(462), (-0.35, -0.34, 0.98)),
                (F(479), (-0.45, -0.35, 0.90))):
    key_loc(aim_m5, fr, loc)
aim_m7a = aim_empty("aim_m7a", (Z_CY + 0.65, 3.0, 1.30))

cam_M1 = make_cam("cam_M1", 35, (0, -4.4, 1.55), track=aim_desk, keys=[
    (F(0), (0, -4.4, 1.55)), (F(89), (0, -2.35, 1.32))])
cam_M2 = make_cam("cam_M2", 32, (0.02, -0.18, 1.05), aim=(0, -0.20, 0.78),
                  keys=[(F(90), (0.02, -0.18, 1.05)),
                        (F(140), (0.02, -0.18, 1.05)),
                        (F(194), (0.10, -0.75, 2.05))],
                  dof=[(F(90), 0.30), (F(140), 0.30), (F(194), 1.35)],
                  fstop=2.2)
cam_M3 = make_cam("cam_M3", 26, (2.1, -3.3, 1.55), aim=(-0.3, 1.8, 1.6))
cam_M4 = make_cam("cam_M4", 30, (17.9, -2.7, 1.35), track=aim_counter,
                  keys=[(F(300), (17.9, -2.7, 1.35)),
                        (F(404), (22.1, -2.7, 1.35))])
cam_M5 = make_cam("cam_M5", 30, (0, -2.5, 1.42), track=aim_m5, keys=[
    (F(405), (0, -2.5, 1.42)), (F(415), (0.02, -2.35, 1.40)),
    (F(445), (-0.42, -1.15, 1.06)), (F(479), (-0.45, -0.80, 0.96))])
cam_M6 = make_cam("cam_M6", 35, (Z_VOID, -0.7, 1.6),
                  aim=(Z_VOID, 1.5, 1.6))
cam_M7a = make_cam("cam_M7a", 35, (Z_CY + 0.55, 0.9, 1.45), track=aim_m7a,
                   keys=[(F(630), (Z_CY + 0.55, 0.9, 1.45)),
                         (F(689), (Z_CY + 0.6, 1.1, 1.40))],
                   dof=[(F(630), 3.6), (F(655), 2.15)], fstop=2.8)
cam_M7b = make_cam("cam_M7b", 40, (1.0, -2.45, 1.40), track=aim_desk,
                   keys=[(F(690), (1.0, -2.45, 1.40)),
                         (F(730), (0.75, -1.85, 1.32)),
                         (F(764), (0.75, -1.85, 1.32))],
                   dof=[(F(690), 3.9), (F(730), 2.5)], fstop=2.5)
cam_M8 = make_cam("cam_M8", 35, (Z_VOID, -1.7, 1.6),
                  aim=(Z_VOID, 1.5, 1.6))

for name, fr, cam in (("M1", 0, cam_M1), ("M2", 90, cam_M2),
                      ("M3", 195, cam_M3), ("M4", 300, cam_M4),
                      ("M5", 405, cam_M5), ("M6", 480, cam_M6),
                      ("M7a", 630, cam_M7a), ("M7b", 690, cam_M7b),
                      ("M8", 765, cam_M8)):
    marker(name, F(fr), cam)
scene.camera = cam_M1

# white dissolve wipe in front of M5
bpy.ops.mesh.primitive_plane_add(size=1)
WIPE = bpy.context.active_object
WIPE.name = "wipe"
WIPE.data.materials.append(WIPE_MAT)
WIPE.parent = cam_M5
WIPE.location = (0, 0, -0.4)
WIPE.rotation_euler = (0, 0, 0)
WIPE.scale = (0.40, 0.65, 1)
wf = mix_fac(WIPE_MAT)
for fr, v in ((F(460), 0.0), (F(479), 1.0)):
    wf.default_value = v
    wf.keyframe_insert("default_value", frame=fr)

# ------------------------------------------------------------------ world + lights animation
print("ASSEMBLE: lighting keys...")
world = scene.world
bg = next(n for n in world.node_tree.nodes if n.type == "BACKGROUND")
for fr, s in ((1, 0.18), (301, 0.12), (405, 0.12), (436, 0.15),
              (480, 0.80), (900, 0.80)):
    bg.inputs["Strength"].default_value = s
    bg.inputs["Strength"].keyframe_insert("default_value", frame=fr)
for fr, col in ((1, (1.0, 0.78, 0.58, 1.0)),
                (301, (0.82, 0.90, 1.0, 1.0)),
                (405, (0.82, 0.90, 1.0, 1.0)),
                (436, (1.0, 0.80, 0.60, 1.0)),
                (480, (1.0, 1.0, 1.0, 1.0)),
                (900, (1.0, 1.0, 1.0, 1.0))):
    bg.inputs["Color"].default_value = col
    bg.inputs["Color"].keyframe_insert("default_value", frame=fr)

bulb_d = O("bulb_light").data
E = bulb_d.energy
for fr, e in ((1, E), (61, E * 0.12), (64, E * 0.90), (66, E * 0.28),
              (69, E), (436, E), (461, 0.0)):
    bulb_d.energy = e
    bulb_d.keyframe_insert("energy", frame=fr)

wm = bpy.data.materials["window_glow"]
wem = next(n for n in wm.node_tree.nodes if n.type == "EMISSION")
S = wem.inputs["Strength"].default_value
for fr, v in ((1, S), (196, S), (213, S * 0.12), (231, S),
              (249, S * 0.12), (267, S), (285, S * 0.12), (301, S),
              (691, S * 2.2), (900, S * 2.2)):
    wem.inputs["Strength"].default_value = v
    wem.inputs["Strength"].keyframe_insert("default_value", frame=fr)

# ------------------------------------------------------------------ clock hands
print("ASSEMBLE: clock + pen + tower...")
h0 = -((23 + 7.0 / 60) / 12) * 2 * math.pi
m0 = -(7.0 / 60) * 2 * math.pi
key_rot(HAND_H, 1, (0, 0, h0))
key_rot(HAND_H, 196, (0, 0, h0))
key_rot(HAND_H, 300, (0, 0, h0 - 2 * math.pi))
key_rot(HAND_M, 1, (0, 0, m0))
key_rot(HAND_M, 196, (0, 0, m0))
key_rot(HAND_M, 300, (0, 0, m0 - 12 * 2 * math.pi))
step = -2 * math.pi / 60
for i, fr in enumerate((1, 31, 61, 91, 121, 151, 181)):
    key_rot(HAND_S, fr, (0, 0, step * i))
key_rot(HAND_S, 196, (0, 0, step * 6.5))
key_rot(HAND_S, 300, (0, 0, step * 6.5 - 12 * 2 * math.pi))
# constant-step ticking for the pre-timelapse keys, linear afterwards
for fc in fcurves_of(HAND_S.animation_data):
    for kp in fc.keyframe_points:
        kp.interpolation = "CONSTANT" if kp.co.x < 196 else "LINEAR"
for h in (HAND_H, HAND_M):
    for fc in fcurves_of(h.animation_data):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"

# tower growth + tip
key_scale(tower, 1, 1.2)
key_scale(tower, 196, 1.2)
key_scale(tower, 300, 1.92)
key_rot(tower, 1, (0, 0, 0))
key_rot(tower, 286, (0, 0, 0))
key_rot(tower, 300, (0, 0, D(14)))
for fc in fcurves_of(tower.animation_data):
    if fc.data_path == "scale":
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"

# red pen: write, levitate, spin, morph
pen_path = [(0, (-0.05, -0.33, 0.825)),
            (96, (-0.10, -0.33, 0.825)),
            (126, (-0.01, -0.33, 0.825)),
            (140, (-0.01, -0.33, 0.825)),
            (143, (-0.06, -0.31, 0.825)),
            (147, (-0.01, -0.35, 0.825)),
            (151, (-0.06, -0.31, 0.825)),
            (155, (-0.01, -0.35, 0.825)),
            (156, (0.00, -0.33, 0.825)),
            (176, (0.07, -0.33, 0.825)),
            (405, (0.07, -0.33, 0.825)),
            (415, (0.07, -0.33, 0.825)),
            (445, (0.00, -0.30, 1.35))]
for fr, loc in pen_path:
    key_loc(REDPEN, F(fr), loc)
key_rot(REDPEN, F(0), (D(65), 0, 0))
key_rot(REDPEN, F(415), (D(65), 0, 0))
key_rot(REDPEN, F(445), (D(20), 0, 4 * 2 * math.pi))
key_scale(REDPEN, F(0), 1.0)
key_scale(REDPEN, F(445), 1.0)
key_scale(REDPEN, F(453), 0.0)
for fc in fcurves_of(REDPEN.animation_data):
    for kp in fc.keyframe_points:
        if fc.data_path == "location" and kp.co.x <= F(176):
            kp.interpolation = "LINEAR"

# checkmark: appears at pen, flies into tablet, glows
CHECK.location = (0.0, -0.30, 1.35)
key_loc(CHECK, F(445), (0.0, -0.30, 1.35))
key_loc(CHECK, F(452), (0.0, -0.30, 1.42))
key_loc(CHECK, F(460), (-0.45, -0.35, 0.97))
key_scale(CHECK, F(445), 0.001)
key_scale(CHECK, F(452), 1.15)
key_scale(CHECK, F(456), 1.0)
chk_em = next((n for n in chk_mat.node_tree.nodes
               if n.type == "EMISSION"), None)
chk_sock = (chk_em.inputs["Strength"] if chk_em else
            chk_mat.node_tree.nodes["Principled BSDF"]
            .inputs["Emission Strength"])
for fr, s in ((F(445), 2.0), (F(452), 9.0), (F(470), 3.0)):
    chk_sock.default_value = s
    chk_sock.keyframe_insert("default_value", frame=fr)

# cursor descend + click
key_loc(CURSOR, F(405), (-0.42, -0.52, 1.04))
key_loc(CURSOR, F(415), (-0.42, -0.52, 0.86))
key_scale(CURSOR, F(407), 1.0)
key_scale(CURSOR, F(408), 0.7)
key_scale(CURSOR, F(410), 1.1)
key_scale(CURSOR, F(412), 1.0)

# ------------------------------------------------------------------ finalize
print("ASSEMBLE: finalizing...")
# hide_render keys must be stepped, never smoothed
for o in bpy.data.objects:
    for fc in fcurves_of(o.animation_data):
        if fc.data_path == "hide_render":
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"

path = os.path.join(ARGS["out"], "report_cards.blend")
bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)
n_obj = len(bpy.data.objects)
n_mark = len(scene.timeline_markers)
print("BUILD_OK report_cards.blend -> %s (objects=%d markers=%d)"
      % (path, n_obj, n_mark))

# ------------------------------------------------------------------ QA stills
if ARGS["qa"] == "1":
    print("ASSEMBLE: QA renders...")
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 16
    scene.cycles.device = "CPU"
    scene.render.resolution_x = 270
    scene.render.resolution_y = 480
    qa_frames = (("M1", 46), ("M2", 141), ("M3", 251), ("M4", 351),
                 ("M5", 441), ("M6", 551), ("M7b", 701), ("M8", 831),
                 ("M7a", 655), ("M4b", 395), ("M6b", 612), ("M7c", 684))
    for label, fr in qa_frames:
        scene.frame_set(fr)
        scene.render.filepath = os.path.join(ARGS["preview"],
                                             "qa_%s.png" % label)
        bpy.ops.render.render(write_still=True)
        print("PREVIEW_OK qa_%s.png (frame %d)" % (label, fr))
print("BUILD_BATCH_DONE 6 assembly")




