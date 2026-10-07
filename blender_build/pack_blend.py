"""Pack every external resource into report_cards.blend so it is
self-contained for the Kaggle (Linux) render. Run headless:

  blender -b --factory-startup -P pack_blend.py
"""
import os
import sys

import bpy

BLEND = os.path.abspath(
    os.path.join(os.path.dirname(__file__),
                 "..", "global_assets", "models", "report_cards.blend")
)

bpy.ops.wm.open_mainfile(filepath=BLEND)

before_imgs = [(i.name, i.filepath, bool(i.packed_file))
               for i in bpy.data.images if i.source == "FILE"]
before_fonts = [(f.name, f.filepath, bool(f.packed_file))
                for f in bpy.data.fonts if f.filepath and "<builtin>" not in f.filepath]

bpy.ops.file.pack_all()

after_imgs = [(i.name, i.filepath, bool(i.packed_file))
              for i in bpy.data.images if i.source == "FILE"]
after_fonts = [(f.name, f.filepath, bool(f.packed_file))
               for f in bpy.data.fonts
               if f.filepath and "<builtin>" not in f.filepath]

bad_i = [x for x in after_imgs if not x[2]]
bad_f = [x for x in after_fonts if not x[2]]
print(f"PACK_IMAGES {len(after_imgs)} packed, {len(bad_i)} failed")
print(f"PACK_FONTS  {len(after_fonts)} packed, {len(bad_f)} failed")
for n, p, _ in bad_i + bad_f:
    print(f"  FAILED {n} {p!r}")

if bad_i or bad_f:
    sys.exit(1)

bpy.ops.wm.save_as_mainfile(filepath=BLEND, compress=True)
size = os.path.getsize(BLEND)
print(f"PACK_OK {BLEND} ({size // (1024 * 1024)} MB)")
