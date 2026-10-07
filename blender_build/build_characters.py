"""Batch 4 — Characters for 'The Red Pen' (stylised, rigged, posed via actions).

Run:
  blender -b --factory-startup -P blender_build/build_characters.py -- --out <dir> --preview <dir>

Builds 3 .blend files, each with one armature (rigid bone-parented parts),
named pose actions selectable at assembly time:
  teacher.blend  actions: T1 hunched-marking, T2 head-in-hand, T3 stretch-smile
  student.blend  actions: S1 impatient, S2 smiling-at-screen
  parent.blend   actions: P1 disappointed (static)

Character convention: faces -Y, feet at z=0, ~1.7 units tall, big stylised head.
"""
import math
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (assign, clear_scene, make_material, parse_args,
                    preview_render, save_blend)

ARGS = parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])

D = math.radians

# ---------------------------------------------------------------- materials
def _mats():
    """(Re)create after every clear_scene — purge drops unused datablocks."""
    global SKIN, EYE, WHITE, BLACK, TEACHER_DRESS, TEACHER_TRIM, \
        STUDENT_BROWN, PARENT_SHIRT, TROUSER, HAIR, PHONE, PEN_RED, SATCHEL
    SKIN = make_material("chr_skin", (0.36, 0.23, 0.13, 1.0), roughness=0.65)
    EYE = make_material("chr_eye", (0.05, 0.04, 0.04, 1.0), roughness=0.3)
    WHITE = make_material("chr_white", (0.93, 0.93, 0.91, 1.0), roughness=0.7)
    BLACK = make_material("chr_black", (0.08, 0.08, 0.09, 1.0), roughness=0.5)
    TEACHER_DRESS = make_material("chr_dress", (0.12, 0.30, 0.18, 1.0),
                                  roughness=0.7)
    TEACHER_TRIM = make_material("chr_trim", (0.83, 0.69, 0.21, 1.0),
                                 roughness=0.45)
    STUDENT_BROWN = make_material("chr_brown", (0.42, 0.29, 0.18, 1.0),
                                  roughness=0.7)
    PARENT_SHIRT = make_material("chr_shirt", (0.45, 0.60, 0.75, 1.0),
                                 roughness=0.75)
    TROUSER = make_material("chr_trouser", (0.22, 0.22, 0.24, 1.0),
                            roughness=0.8)
    HAIR = make_material("chr_hair", (0.09, 0.07, 0.06, 1.0), roughness=0.6)
    PHONE = make_material("chr_phone", (0.10, 0.10, 0.12, 1.0), roughness=0.3)
    PEN_RED = make_material("chr_pen", (0.69, 0.12, 0.12, 1.0), roughness=0.4)
    SATCHEL = make_material("chr_satchel", (0.35, 0.22, 0.13, 1.0),
                            roughness=0.7)


# ------------------------------------------------------------------- shapes
def _finish(name, mat, smooth=True):
    o = bpy.context.active_object
    o.name = name
    assign(o, mat)
    if smooth:
        bpy.ops.object.shade_smooth()
    return o


def sphere(name, loc, r, mat, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc,
                                         segments=24, ring_count=16)
    o = _finish(name, mat)
    o.scale = scale
    return o


def cyl(name, loc, r, depth, mat, top_r=None):
    if top_r is None:
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth,
                                            location=loc, vertices=20)
    else:
        bpy.ops.mesh.primitive_cone_add(radius1=r, radius2=top_r, depth=depth,
                                        location=loc, vertices=20)
    return _finish(name, mat)


def box(name, loc, size, mat, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = _finish(name, mat, smooth=False)
    o.scale = size
    return o


# --------------------------------------------------------------------- rig
def make_armature(name, bones):
    """bones: dict name -> (head_xyz, tail_xyz, parent_name|None)."""
    arm_data = bpy.data.armatures.new(name + "_rig")
    arm = bpy.data.objects.new(name + "_rig", arm_data)
    bpy.context.scene.collection.objects.link(arm)
    bpy.context.view_layer.objects.active = arm
    arm.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    for bname, (head, tail, parent) in bones.items():
        eb = arm_data.edit_bones.new(bname)
        eb.head = head
        eb.tail = tail
        if parent:
            eb.parent = arm_data.edit_bones[parent]
    bpy.ops.object.mode_set(mode="OBJECT")
    return arm


def bone_parent(obj, arm, bone):
    # bake rotation/scale into geometry first — matrix_world reassignment
    # after bone-parenting can drop basis scale (giant-object bug)
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    mw = obj.matrix_world.copy()
    obj.parent = arm
    obj.parent_type = "BONE"
    obj.parent_bone = bone
    obj.matrix_world = mw


def begin_action(arm, name):
    if arm.animation_data is None:
        arm.animation_data_create()
    act = bpy.data.actions.new(name)
    act.use_fake_user = True  # 0-user actions are dropped at file load
    arm.animation_data.action = act
    return act


def key_pose(arm, keys):
    """keys: {bone: {"rot": (x,y,z) deg, "loc": (x,y,z)}} at frame 1."""
    for bname, k in keys.items():
        pb = arm.pose.bones[bname]
        pb.rotation_mode = "XYZ"
        if "rot" in k:
            pb.rotation_euler = tuple(D(a) for a in k["rot"])
            pb.keyframe_insert("rotation_euler", frame=1)
        if "loc" in k:
            pb.location = k["loc"]
            pb.keyframe_insert("location", frame=1)


def standard_bones():
    return {
        "hips": ((0, 0, 0.70), (0, 0, 0.92), None),
        "spine": ((0, 0, 0.92), (0, 0, 1.16), "hips"),
        "head": ((0, 0, 1.18), (0, 0, 1.60), "spine"),
        "upper_arm.L": ((0.22, 0, 1.14), (0.24, 0, 0.86), "spine"),
        "forearm.L": ((0.24, 0, 0.86), (0.245, 0, 0.60), "upper_arm.L"),
        "upper_arm.R": ((-0.22, 0, 1.14), (-0.24, 0, 0.86), "spine"),
        "forearm.R": ((-0.24, 0, 0.86), (-0.245, 0, 0.60), "upper_arm.R"),
        "thigh.L": ((0.09, 0, 0.70), (0.10, 0, 0.36), "hips"),
        "shin.L": ((0.10, 0, 0.36), (0.10, -0.01, 0.04), "thigh.L"),
        "thigh.R": ((-0.09, 0, 0.70), (-0.10, 0, 0.36), "hips"),
        "shin.R": ((-0.10, 0, 0.36), (-0.10, -0.01, 0.04), "thigh.R"),
    }


def common_head(arm, parts, prefix=""):
    p = prefix
    parts.append((sphere(p + "head", (0, 0, 1.44), 0.21, SKIN,
                         scale=(1, 1.02, 1.12)), "head"))
    parts.append((sphere(p + "eye.L", (0.08, -0.185, 1.47), 0.032, EYE), "head"))
    parts.append((sphere(p + "eye.R", (-0.08, -0.185, 1.47), 0.032, EYE), "head"))
    parts.append((cyl(p + "neck", (0, 0, 1.19), 0.055, 0.12, SKIN), "spine"))


def common_legs(arm, parts, trouser_mat=None, sock_mat=None, shoe_mat=None):
    """trouser_mat=None -> bare skin legs."""
    if shoe_mat is None:
        shoe_mat = BLACK
    leg_mat = trouser_mat or SKIN
    for side, x in (("L", 0.095), ("R", -0.095)):
        parts.append((cyl("thigh." + side, (x, 0, 0.53), 0.07, 0.36, leg_mat),
                      "thigh." + side))
        shin_mat = sock_mat or leg_mat
        parts.append((cyl("shin." + side, (x, -0.005, 0.20), 0.055, 0.32,
                          shin_mat), "shin." + side))
        parts.append((box("shoe." + side, (x, -0.05, 0.035), (0.11, 0.22, 0.07),
                          shoe_mat), "shin." + side))


def common_arms(arm, parts, sleeve_mat, arm_mat=None, hand_mat=None):
    """Full-length sleeves unless arm_mat given for forearm skin."""
    if hand_mat is None:
        hand_mat = SKIN
    for side, sx in (("L", 1), ("R", -1)):
        parts.append((cyl("uarm." + side, (sx * 0.23, 0, 1.00), 0.055, 0.30,
                          sleeve_mat), "upper_arm." + side))
        fa = arm_mat or sleeve_mat
        parts.append((cyl("farm." + side, (sx * 0.245, 0, 0.73), 0.048, 0.28,
                          fa), "forearm." + side))
        parts.append((sphere("hand." + side, (sx * 0.248, 0, 0.575), 0.062,
                             hand_mat), "forearm." + side))


# ----------------------------------------------------------------- teacher
def build_teacher():
    clear_scene()
    _mats()
    arm = make_armature("teacher", standard_bones())
    parts = []
    common_head(arm, parts)
    common_arms(arm, parts, TEACHER_DRESS)
    common_legs(arm, parts)  # bare calves under the dress

    # dress: torso + flared skirt + white collar
    parts.append((sphere("torso", (0, 0, 1.02), 0.20, TEACHER_DRESS,
                         scale=(1, 0.75, 1.2)), "spine"))
    parts.append((cyl("skirt", (0, 0, 0.85), 0.30, 0.42, TEACHER_DRESS,
                      top_r=0.185), "hips"))
    parts.append((cyl("collar", (0, 0, 1.17), 0.095, 0.05, WHITE), "spine"))
    parts.append((sphere("hair_bun", (0, 0.13, 1.60), 0.13, HAIR), "head"))
    parts.append((sphere("hair_cap", (0, 0.02, 1.50), 0.215, HAIR,
                         scale=(1.02, 1.0, 0.75)), "head"))
    # red pen in right hand
    pen = cyl("pen", (-0.27, -0.03, 0.56), 0.012, 0.16, PEN_RED)
    pen.rotation_euler = (D(70), 0, D(15))
    parts.append((pen, "forearm.R"))

    for obj, bone in parts:
        bone_parent(obj, arm, bone)

    poses = {
        "T1": {  # hunched marking, seated
            "hips": {"loc": (0, -0.18, 0)},
            "spine": {"rot": (26, 0, 0)},
            "head": {"rot": (18, 0, 0)},
            "upper_arm.L": {"rot": (-55, 0, -8)},
            "forearm.L": {"rot": (-55, 0, 0)},
            "upper_arm.R": {"rot": (-48, 0, 6)},
            "forearm.R": {"rot": (-62, 0, 0)},
            "thigh.L": {"rot": (-82, 0, 0)},
            "shin.L": {"rot": (82, 0, 0)},
            "thigh.R": {"rot": (-78, 0, 0)},
            "shin.R": {"rot": (80, 0, 0)},
        },
        "T2": {  # head-in-hand, seated, weary
            "hips": {"loc": (0, -0.16, 0)},
            "spine": {"rot": (16, 0, 0)},
            "head": {"rot": (10, 0, -12)},
            "upper_arm.R": {"rot": (-35, 0, 22)},
            "forearm.R": {"rot": (-105, 0, -25)},
            "upper_arm.L": {"rot": (-30, 0, -6)},
            "forearm.L": {"rot": (-70, 0, 0)},
            "thigh.L": {"rot": (-80, 0, 0)},
            "shin.L": {"rot": (80, 0, 0)},
            "thigh.R": {"rot": (-76, 0, 0)},
            "shin.R": {"rot": (78, 0, 0)},
        },
        "T3": {  # stretch-smile, standing
            "spine": {"rot": (-12, 0, 0)},
            "head": {"rot": (-12, 0, 0)},
            "upper_arm.L": {"rot": (-150, 0, -18)},
            "forearm.L": {"rot": (-25, 0, 0)},
            "upper_arm.R": {"rot": (-150, 0, 18)},
            "forearm.R": {"rot": (-25, 0, 0)},
            "thigh.L": {"rot": (0, 0, 4)},
            "thigh.R": {"rot": (0, 0, -4)},
        },
    }
    first = None
    for name, keys in poses.items():
        act = begin_action(arm, name)
        key_pose(arm, keys)
        if first is None:
            first = act
    arm.animation_data.action = first

    path = save_blend(ARGS["out"], "teacher.blend")
    print("BUILD_OK teacher.blend actions=%s -> %s"
          % (",".join(poses), path))
    for name in poses:
        arm.animation_data.action = bpy.data.actions[name]
        bpy.context.view_layer.update()
        p = preview_render(ARGS["preview"], "char-teacher-%s.png" % name)
        print("PREVIEW_OK %s" % os.path.basename(p))


# ----------------------------------------------------------------- student
def build_student():
    clear_scene()
    _mats()
    arm = make_armature("student", standard_bones())
    parts = []
    common_head(arm, parts)
    common_arms(arm, parts, sleeve_mat=WHITE, arm_mat=SKIN)
    common_legs(arm, parts, sock_mat=WHITE)

    # uniform: white shirt torso, brown pinafore bib + skirt, braids
    parts.append((sphere("torso", (0, 0, 1.00), 0.17, WHITE,
                         scale=(1, 0.75, 1.15)), "spine"))
    parts.append((box("bib", (0, -0.115, 1.02), (0.22, 0.04, 0.30),
                      STUDENT_BROWN), "spine"))
    parts.append((cyl("skirt", (0, 0, 0.84), 0.26, 0.38, STUDENT_BROWN,
                      top_r=0.16), "hips"))
    parts.append((sphere("hair_cap", (0, 0.02, 1.50), 0.215, HAIR,
                         scale=(1.02, 1.0, 0.75)), "head"))
    for side, sx in (("L", 1), ("R", -1)):
        braid = cyl("braid." + side, (sx * 0.17, 0.06, 1.30), 0.045, 0.34, HAIR)
        parts.append((braid, "head"))
        parts.append((sphere("ribbon." + side, (sx * 0.17, 0.06, 1.13), 0.05,
                             WHITE), "head"))
    # satchel at left hip with strap
    parts.append((box("satchel", (0.24, 0.06, 0.78), (0.20, 0.10, 0.24),
                      SATCHEL), "spine"))
    strap = box("strap", (0.06, -0.13, 1.02), (0.05, 0.03, 0.44), SATCHEL,
                rot=(0, D(-25), 0))
    parts.append((strap, "spine"))
    # phone in left hand
    ph = box("phone", (0.26, -0.07, 0.62), (0.07, 0.02, 0.14), PHONE)
    ph.rotation_euler = (D(35), 0, 0)
    parts.append((ph, "forearm.L"))

    for obj, bone in parts:
        bone_parent(obj, arm, bone)

    poses = {
        "S1": {  # waiting / impatient, arms crossed
            "spine": {"rot": (4, 0, 0)},
            "head": {"rot": (6, 0, 14)},
            "hips": {"loc": (0.04, 0, 0)},
            "upper_arm.L": {"rot": (-48, 0, -10)},
            "forearm.L": {"rot": (-62, 0, 45)},
            "upper_arm.R": {"rot": (-52, 0, 8)},
            "forearm.R": {"rot": (-58, 0, -42)},
            "thigh.R": {"rot": (-8, 0, 0)},
            "shin.R": {"rot": (14, 0, 0)},
        },
        "S2": {  # smiling at phone held up in left hand
            "spine": {"rot": (6, 0, 0)},
            "head": {"rot": (22, 0, 6)},
            "upper_arm.L": {"rot": (-38, 0, -12)},
            "forearm.L": {"rot": (-78, 0, -8)},
            "upper_arm.R": {"rot": (-14, 0, 4)},
            "forearm.R": {"rot": (-18, 0, 0)},
        },
    }
    first = None
    for name, keys in poses.items():
        act = begin_action(arm, name)
        key_pose(arm, keys)
        if first is None:
            first = act
    arm.animation_data.action = first

    path = save_blend(ARGS["out"], "student.blend")
    print("BUILD_OK student.blend actions=%s -> %s" % (",".join(poses), path))
    for name in poses:
        arm.animation_data.action = bpy.data.actions[name]
        bpy.context.view_layer.update()
        p = preview_render(ARGS["preview"], "char-student-%s.png" % name)
        print("PREVIEW_OK %s" % os.path.basename(p))


# ------------------------------------------------------------------- parent
def build_parent():
    clear_scene()
    _mats()
    arm = make_armature("parent", standard_bones())
    parts = []
    common_head(arm, parts)
    common_arms(arm, parts, sleeve_mat=PARENT_SHIRT, arm_mat=SKIN)
    common_legs(arm, parts, trouser_mat=TROUSER)

    parts.append((sphere("torso", (0, 0, 1.01), 0.19, PARENT_SHIRT,
                         scale=(1, 0.78, 1.18)), "spine"))
    parts.append((sphere("hair_cap", (0, 0.02, 1.50), 0.21, HAIR,
                         scale=(1.0, 0.98, 0.7)), "head"))

    for obj, bone in parts:
        bone_parent(obj, arm, bone)

    poses = {
        "P1": {  # disappointed, slumped at counter
            "spine": {"rot": (9, 0, 0)},
            "head": {"rot": (17, 0, 0)},
            "upper_arm.L": {"rot": (-12, 0, -5)},
            "upper_arm.R": {"rot": (-12, 0, 5)},
            "forearm.L": {"rot": (-16, 0, 0)},
            "forearm.R": {"rot": (-16, 0, 0)},
        },
    }
    first = None
    for name, keys in poses.items():
        act = begin_action(arm, name)
        key_pose(arm, keys)
        if first is None:
            first = act
    arm.animation_data.action = first

    path = save_blend(ARGS["out"], "parent.blend")
    print("BUILD_OK parent.blend actions=%s -> %s" % (",".join(poses), path))
    for name in poses:
        arm.animation_data.action = bpy.data.actions[name]
        bpy.context.view_layer.update()
        p = preview_render(ARGS["preview"], "char-parent-%s.png" % name)
        print("PREVIEW_OK %s" % os.path.basename(p))


if __name__ == "__main__":
    build_teacher()
    print("BUILD_ASSET_DONE teacher")
    build_student()
    print("BUILD_ASSET_DONE student")
    build_parent()
    print("BUILD_ASSET_DONE parent")
    print("BUILD_BATCH_DONE 3 characters / 6 pose previews")
