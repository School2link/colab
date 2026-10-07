"""Kaggle kernel entrypoint: render the 900-frame report-cards ad.

Runs as a Kaggle script kernel (GPU T4 x2, internet on). Flow:
  1. Download + extract Blender 5.2.2 Linux x64 into /kaggle/working
  2. Run `blender -b report_cards.blend -P render_scene.py -- ...`
     (streams Blender output straight to stdout -> visible in kernel logs)
  3. Zip the frames to render_output.zip in /kaggle/working
"""
import os
import subprocess
import sys
import tarfile
import time
import urllib.request
import zipfile

BLENDER_VER = "5.2.2"
BLENDER_URL = (f"https://download.blender.org/release/Blender5.2/"
               f"blender-{BLENDER_VER}-linux-x64.tar.xz")
WORK = "/kaggle/working"
BLEND = os.path.join(WORK, "report_cards.blend")
RENDER_SCRIPT = os.path.join(WORK, "render_scene.py")
FRAMES_DIR = os.path.join(WORK, "frames")
ZIP_PATH = os.path.join(WORK, "render_output.zip")
SAMPLES = 128
FRAME_START, FRAME_END = 1, 900


def log(msg):
    print(f"[orchestrator] {msg}", flush=True)


def ensure_blender():
    """Download + extract Blender; return path to the blender binary."""
    bindir = os.path.join(WORK, f"blender-{BLENDER_VER}-linux-x64")
    binary = os.path.join(bindir, "blender")
    if os.path.exists(binary):
        log(f"blender already present: {binary}")
        return binary

    tarball = os.path.join(WORK, "blender.tar.xz")
    if not os.path.exists(tarball):
        log(f"downloading {BLENDER_URL}")
        t0 = time.time()
        state = {"last_mb": -100}

        def hook(blocks, bs, size):
            done = min(blocks * bs, size) if size > 0 else blocks * bs
            mb = done // (100 * 1024 * 1024)
            if mb != state["last_mb"]:
                state["last_mb"] = mb
                total = f" / {size // (1024 * 1024)} MB" if size > 0 else ""
                log(f"  {mb * 100}{total}")

        urllib.request.urlretrieve(BLENDER_URL, tarball, reporthook=hook)
        log(f"downloaded in {time.time() - t0:.0f}s "
            f"({os.path.getsize(tarball) // (1024 * 1024)} MB)")

    log("extracting blender (xz)...")
    t0 = time.time()
    with tarfile.open(tarball, "r:xz") as tf:
        tf.extractall(WORK)
    os.remove(tarball)
    log(f"extracted in {time.time() - t0:.0f}s")
    if not os.path.exists(binary):
        raise FileNotFoundError(f"blender binary missing after extract: {binary}")
    os.chmod(binary, 0o755)
    return binary


def render(binary):
    os.makedirs(FRAMES_DIR, exist_ok=True)
    cmd = [
        binary, "-b", BLEND, "-P", RENDER_SCRIPT, "--",
        "--out", FRAMES_DIR,
        "--samples", str(SAMPLES),
        "--device", "CUDA",
        "-s", str(FRAME_START), "-e", str(FRAME_END), "-a",
    ]
    log("launching: " + " ".join(cmd))
    t0 = time.time()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in proc.stdout:
        if line.strip():
            sys.stdout.write(line)
            sys.stdout.flush()
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f"blender exited with code {proc.returncode}")
    log(f"render finished in {time.time() - t0:.0f}s")


def zip_frames():
    pngs = sorted(f for f in os.listdir(FRAMES_DIR) if f.endswith(".png"))
    log(f"zipping {len(pngs)} frames -> {ZIP_PATH}")
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_STORED) as zf:
        for name in pngs:
            zf.write(os.path.join(FRAMES_DIR, name), arcname=name)
    log(f"zip size: {os.path.getsize(ZIP_PATH) // (1024 * 1024)} MB")
    return len(pngs)


def main():
    log(f"working dir: {os.listdir(WORK)}")
    for path in (BLEND, RENDER_SCRIPT):
        if not os.path.exists(path):
            raise FileNotFoundError(f"kernel file missing: {path}")
    binary = ensure_blender()
    render(binary)
    count = zip_frames()
    expected = FRAME_END - FRAME_START + 1
    if count != expected:
        raise RuntimeError(f"expected {expected} frames, found {count}")
    log(f"OK render_output.zip with {count} frames")


if __name__ == "__main__":
    main()
