"""Blender-side render script for the report-cards ad.

Invoked by cloud_orchestrator.py (Kaggle) or manually (local smoke test):

  blender -b report_cards.blend -P render_scene.py -- \
      --out /kaggle/working/frames --samples 128 --device CUDA \
      --start 1 --end 900

Sets up Cycles GPU devices, renders the marker-bound shot list to
fako_####.png (frames 1-900, 1080x1920, 30fps), and prints a progress
line every 50 frames so `kaggle kernels logs` shows status.
"""
import os
import sys
import time

import bpy


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1:] if "--" in argv else []
    a = {"out": None, "samples": None, "device": "CUDA",
         "start": 1, "end": 900, "fps": None, "template": None}
    i = 0
    while i < len(argv):
        k = argv[i]
        if k in ("-a", "--all"):
            pass
        elif k == "-F":
            i += 1
        elif k == "--out":
            a["out"] = argv[i + 1]; i += 1
        elif k == "-o":
            a["template"] = argv[i + 1]; i += 1
        elif k == "--samples":
            a["samples"] = int(argv[i + 1]); i += 1
        elif k == "--device":
            a["device"] = argv[i + 1].upper(); i += 1
        elif k in ("-s", "--start"):
            a["start"] = int(argv[i + 1]); i += 1
        elif k in ("-e", "--end"):
            a["end"] = int(argv[i + 1]); i += 1
        elif k == "--frames":
            a["end"] = a["start"] + int(argv[i + 1]) - 1; i += 1
        elif k == "--fps":
            a["fps"] = int(argv[i + 1]); i += 1
        i += 1
    return a


def setup_device(requested):
    """Enable requested compute device; return the mode actually used."""
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    if requested == "CPU":
        scene.cycles.device = "CPU"
        return "CPU"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    try:
        prefs.compute_device_type = requested  # "CUDA" or "OPTIX"
        prefs.get_devices()
    except Exception as exc:  # noqa: BLE001
        print(f"[render] {requested} unavailable ({exc}); falling back to CPU",
              flush=True)
        scene.cycles.device = "CPU"
        return "CPU"
    usable = [d for d in prefs.devices if d.type != "CPU"]
    if not usable:
        print(f"[render] no {requested} devices found; falling back to CPU",
              flush=True)
        scene.cycles.device = "CPU"
        return "CPU"
    for d in prefs.devices:
        d.use = True
    scene.cycles.device = "GPU"
    names = ", ".join(f"{d.name}({d.type})" for d in usable)
    print(f"[render] GPU devices: {names}", flush=True)
    return requested


def main():
    a = parse_args()
    if not a["out"] and not a["template"]:
        print("[render] ERROR: provide --out DIR (or -o template)", flush=True)
        sys.exit(2)

    scene = bpy.context.scene
    mode = setup_device(a["device"])
    if a["samples"]:
        scene.cycles.samples = a["samples"]
    if a["fps"]:
        scene.fps = a["fps"]
        scene.fps_base = 1.0

    out_dir = a["out"] or os.path.dirname(a["template"])
    os.makedirs(out_dir, exist_ok=True)
    template = a["template"] or os.path.join(out_dir, "fako_####")
    scene.render.filepath = template
    scene.frame_start = a["start"]
    scene.frame_end = a["end"]

    total = a["end"] - a["start"] + 1
    t0 = time.time()

    def progress(scn, _unused=None):
        done = scn.frame_current - a["start"] + 1
        if scn.frame_current % 50 == 0 or done == total:
            elapsed = time.time() - t0
            rate = elapsed / max(done, 1)
            eta = rate * (total - done)
            print(f"[render] frame {scn.frame_current} ({done}/{total}) "
                  f"elapsed={elapsed:.0f}s eta={eta:.0f}s", flush=True)

    bpy.app.handlers.frame_change_post.append(progress)
    print(f"[render] device={mode} samples={scene.cycles.samples} "
          f"frames {a['start']}-{a['end']} -> {template}", flush=True)
    t0 = time.time()
    bpy.ops.render.render(animation=True)
    pngs = [f for f in os.listdir(out_dir) if f.endswith(".png")]
    print(f"[render] DONE {len(pngs)} pngs in {out_dir} "
          f"({time.time() - t0:.0f}s)", flush=True)


main()
