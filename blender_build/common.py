"""Shared helpers for terminal-only Blender asset builds.

Usage inside a build script:
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from common import *
"""
import math
import os
import random

import bpy


def parse_args(after_dashdash):
    """Parse script args that follow '--'."""
    args = {"out": "global_assets/models", "preview": "plans/report-cards/previews"}
    if after_dashdash and "--" in after_dashdash:
        after_dashdash = after_dashdash[after_dashdash.index("--") + 2:]
    i = 0
    while i < len(after_dashdash):
        if after_dashdash[i] in ("--out", "--preview") and i + 1 < len(after_dashdash):
            args[after_dashdash[i][2:]] = after_dashdash[i + 1]
            i += 2
        else:
            i += 1
    args["out"] = os.path.abspath(args["out"])
    args["preview"] = os.path.abspath(args["preview"])
    os.makedirs(args["out"], exist_ok=True)
    os.makedirs(args["preview"], exist_ok=True)
    return args


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for block_list in (bpy.data.meshes, bpy.data.materials, bpy.data.curves,
                       bpy.data.cameras, bpy.data.lights, bpy.data.armatures,
                       bpy.data.actions, bpy.data.images):
        for block in list(block_list):
            if block.users == 0:
                block_list.remove(block)


def make_material(name, base_color=(0.8, 0.8, 0.8, 1.0), metallic=0.0,
                  roughness=0.5, emission=None, emission_strength=0.0):
    """Principled BSDF material. base_color is RGBA 0-1. emission is RGBA or None."""
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = _to_linear(base_color)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if emission is not None:
        bsdf.inputs["Emission Color"].default_value = _to_linear(emission)
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat


def assign(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def add_bevel(obj, width=0.002, segments=3):
    mod = obj.modifiers.new(name="Bevel", type="BEVEL")
    mod.width = width
    mod.segments = segments
    mod.limit_method = "ANGLE"
    return mod


def new_object(name, mesh_op, **kwargs):
    mesh_op(**kwargs)
    obj = bpy.context.active_object
    obj.name = name
    return obj


def save_blend(out_dir, filename):
    path = os.path.join(out_dir, filename)
    bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)
    return path


def preview_render(preview_dir, filename, seed_objects=None, dist_mult=4.0):
    """Add a temp camera + sun framed on the scene, render a small still, clean up."""
    objs = seed_objects or [o for o in bpy.data.objects if o.type in ("MESH", "CURVE", "FONT")]
    if not objs:
        return None

    import mathutils
    coords = []
    for o in objs:
        coords.extend([o.matrix_world @ mathutils.Vector(c) for c in o.bound_box])
    center = sum(coords, mathutils.Vector()) / len(coords)
    span = max((c - center).length for c in coords) or 1.0

    cam_data = bpy.data.cameras.new("_preview_cam")
    cam = bpy.data.objects.new("_preview_cam", cam_data)
    bpy.context.scene.collection.objects.link(cam)
    cam_data.lens = 35
    import mathutils as _mu
    direction = _mu.Vector((1.6, -1.6, 1.0))
    direction.normalize()
    # distance so span fits vertically in the 320x180 frame (half-vfov ~16 deg)
    cam.location = center + direction * (span * dist_mult)
    look = center - cam.location
    cam.rotation_euler = look.to_track_quat("-Z", "Y").to_euler()

    sun_data = bpy.data.lights.new("_preview_sun", type="SUN")
    sun_data.energy = 4.0
    sun = bpy.data.objects.new("_preview_sun", sun_data)
    bpy.context.scene.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(50), 0, math.radians(30))

    scene = bpy.context.scene
    prev = {
        "engine": scene.render.engine,
        "samples": scene.cycles.samples,
        "device": scene.cycles.device,
        "x": scene.render.resolution_x,
        "y": scene.render.resolution_y,
        "filepath": scene.render.filepath,
        "camera": scene.camera,
    }
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 16
    scene.cycles.device = "CPU"
    scene.render.resolution_x = 320
    scene.render.resolution_y = 180
    scene.camera = cam
    path = os.path.join(preview_dir, filename)
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)

    scene.render.engine = prev["engine"]
    scene.cycles.samples = prev["samples"]
    scene.cycles.device = prev["device"]
    scene.render.resolution_x = prev["x"]
    scene.render.resolution_y = prev["y"]
    scene.render.filepath = prev["filepath"]
    scene.camera = prev["camera"]

    bpy.data.objects.remove(cam, do_unlink=True)
    bpy.data.objects.remove(sun, do_unlink=True)
    bpy.data.cameras.remove(cam_data)
    bpy.data.lights.remove(sun_data)
    return path


def hex_rgba(hex_color, alpha=1.0):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)) + (alpha,)


def srgb_to_linear(v):
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def _to_linear(color):
    """Blender color sockets are linear; our colors are picked as sRGB hex."""
    return tuple(srgb_to_linear(c) for c in color[:3]) + (color[3],)


def emission_material(name, color, strength=1.0):
    """Pure emission (shadeless) material — exact colors for flat UI renders."""
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = _to_linear(color)
    em.inputs["Strength"].default_value = strength
    nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    return mat


def set_emission_color(mat, color):
    em = next((n for n in mat.node_tree.nodes if n.type == "EMISSION"), None)
    if em:
        em.inputs["Color"].default_value = _to_linear(color)


def load_font(bold=False):
    """Load Arial/Arial Bold; falls back to Blender's built-in font."""
    import bpy as _bpy
    path = r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"
    if os.path.exists(path):
        try:
            return _bpy.data.fonts.load(path, check_existing=True)
        except Exception:
            pass
    return None


def textured_material(name, image_path, roughness=0.7, tile=(1.0, 1.0)):
    """Principled material with an image texture (tiled via mapping node)."""
    mat = make_material(name, roughness=roughness)
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    img = bpy.data.images.load(image_path, check_existing=True)
    coord = nt.nodes.new("ShaderNodeTexCoord")
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.inputs["Scale"].default_value = (tile[0], tile[1], 1.0)
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    nt.links.new(coord.outputs["UV"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], tex.inputs["Vector"])
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    return mat


def set_world(hdr_path, strength=1.0):
    """Assign an HDRI file as the scene world environment (equirectangular)."""
    scene = bpy.context.scene
    world = bpy.data.worlds.get("SetWorld") or bpy.data.worlds.new("SetWorld")
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    bg.inputs["Strength"].default_value = strength
    tex = nt.nodes.new("ShaderNodeTexEnvironment")  # equirect mapping, not ImageTexture
    tex.image = bpy.data.images.load(hdr_path, check_existing=True)
    coord = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(coord.outputs["Generated"], tex.inputs["Vector"])
    nt.links.new(tex.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])
    return world
