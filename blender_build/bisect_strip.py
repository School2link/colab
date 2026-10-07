import sys
import bpy

path = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.open_mainfile(filepath=path)
sc = bpy.context.scene
sc.frame_set(831)
sc.cycles.samples = 8
sc.render.resolution_x = 270
sc.render.resolution_y = 480


def strip_px(fn):
    img = bpy.data.images.load(fn)
    px = list(img.pixels)
    # strip sits ~85% down from TOP => 15% from bottom; pixels are bottom-up
    y = int(0.15 * sc.render.resolution_y)
    x = sc.render.resolution_x // 2
    i = (y * sc.render.resolution_x + x) * 4
    r, g, b = round(px[i], 3), round(px[i + 1], 3), round(px[i + 2], 3)
    y2 = int(0.05 * sc.render.resolution_y)
    i2 = (y2 * sc.render.resolution_x + x) * 4
    r2, g2, b2 = round(px[i2], 3), round(px[i2 + 1], 3), round(px[i2 + 2], 3)
    bpy.data.images.remove(img)
    return (r, g, b), (r2, g2, b2)


def render(tag):
    fn = r"C:\Users\Apple\AppData\Local\Temp\opencode\bisect_%s.png" % tag
    sc.render.filepath = fn
    bpy.ops.render.render(write_still=True)
    return strip_px(fn)


def static_hide(name, hidden):
    o = bpy.data.objects[name]
    if o.animation_data and o.animation_data.action:
        try:
            o.keyframe_delete("hide_render")
        except Exception:
            pass
    o.hide_render = hidden


results = []
results.append(("base",) + render("base"))
static_hide("endcard_bg", True)
results.append(("no_bg",) + render("no_bg"))
static_hide("endcard_bg", False)
static_hide("endcard_floor", True)
results.append(("no_floor",) + render("no_floor"))
static_hide("endcard_floor", False)
static_hide("ledger0", True)
for n in ("prog40", "prog100", "gradebook", "flash_row", "reportcard_ui",
          "portal", "portal_tapped", "led240", "led512"):
    if n in bpy.data.objects:
        static_hide(n, True)
results.append(("no_ui",) + render("no_ui"))
for n in ("ledger0", "prog40", "prog100", "gradebook", "flash_row",
          "reportcard_ui", "portal", "portal_tapped", "led240", "led512"):
    if n in bpy.data.objects:
        static_hide(n, False)
static_hide("dv_cyclorama", True)
results.append(("no_cyc",) + render("no_cyc"))
static_hide("dv_cyclorama", False)
for r in results:
    print("BISECT %s strip=%s bottom=%s" % r)
print("DONE")
