# Fako Online Content Engine - Terminal Studio Master Guide

> **Purpose:** This guide explains how to produce videos with the engine's current architecture:
> **Blender in the terminal, heavy rendering on Kaggle GPUs, typography in Remotion, final master in FFmpeg.**
> **Every new piece of content starts with a plan file.**

> **What changed:** All AI generation models have been removed from the project —
> Wan 2.1, AnimateDiff, Stable Diffusion 1.5, Bark TTS, SadTalker, Easy-Wav2Lip, LatentSync,
> and every ngrok/HTTP server notebook that hosted them are gone. No asset is "generated" by AI anymore.
> Assets are **provided** (you supply them) or **downloaded** (scripts pull public-domain files).

---

## 0. The Pipeline in One Screen

```
[ Phase 1 ]   [ Phase 2 ]   [ Phase 3 ]        [ Phase 4 ]         [ Phase 5 ]
  Planning     Asseting      Kaggle Blender     Remotion Pass       FFmpeg Mix
  (plan.md)    (download)    (3D render, GPU)   (typography, CPU)   (final master, CPU)
     │             │               │                  │                  │
   local        local          cloud GPU           local              local
     │             │               │                  │                  │
  plan file    global_assets   900 PNG frames     text overlay       final
  + folders    + global_sfx    render_output.zip  layer (PNG/MP4)    .mp4 master
```

**The distributed principle:** the video is never built by a single program.
Each tool owns one visual layer and does only what its hardware does best.

| Layer                                      | Tool             | Where                  | Why                                             |
| ------------------------------------------ | ---------------- | ---------------------- | ----------------------------------------------- |
| 3D geometry, lighting, camera, raw footage | Blender + Cycles | Kaggle (dual Tesla T4) | Ray tracing needs GPU muscle; laptop stays cool |
| Brand typography, motion graphics, tags    | Remotion         | Local PC               | CPU-only, sharp text, no GPU needed             |
| Layer binding, audio bed, encoding         | FFmpeg           | Local PC               | One command sandwiches everything together      |
| Preview stills, script testing             | Blender (`-b`) | Local PC               | Fast headless tests before burning GPU quota    |

**Rule: Blender is a terminal tool.** It is never opened as a GUI. Every local invocation is headless:

```powershell
blender -b -P script.py -- args
blender -b file.blend -o //preview_ -f 1
```

---

## 1. How to Create a Content Plan

Every video starts with a **plan file** saved as `plans/[content-name]-plan.md`.
The plan must be detailed enough that an AI agent can execute it without asking questions.

### Plan Template

```markdown
# [Content Name] - Production Plan

## Overview
- **Track:** ecommerce | businesses | schools | churches | promo
- **Duration:** 15s | 30s | 60s
- **Style:** 3d-scene | 3d-with-live | mixed
- **Platform:** kaggle
- **Output:** 1080x1920 MP4, 30fps

## Assets Required
| Asset | Type | Source | Path | Notes |
|-------|------|--------|------|-------|
| classroom.blend | 3d-scene | provided or download | global_assets/models/ | Base scene file |
| wood_pbr.zip | texture | download (polydown) | global_assets/textures/ | Desks, floor |
| indoor_4k.exr | hdri | download (polydown) | global_assets/hdris/ | Window light |
| voiceover.wav | audio | provided | global_sfx/ | Emotional narration below |
| ambience_classroom.ogg | audio | provided or download | global_sfx/ | Room tone |
| logo.png | image | provided | global_assets/ | Brand mark for overlays |

## Scene Breakdown

### Scene 1 (0.0s - 4.0s)
- **Type:** 3d-scene
- **Blender Scene:** classroom.blend
- **Camera:** sweep from door to teacher, path coded in cloud_orchestrator.py
- **Duration:** 4.0s (120 frames @ 30fps)
- **Text Overlay:** "YOUR BUSINESS DESERVES TO BE ONLINE."
- **Animation:** zoom-in
- **Audio Cue:** voiceover.wav 0.0s-4.0s
- **Background:** dark gradient scrim on lower third

### Scene 2 (4.0s - 9.0s)
- **Type:** 3d-scene
- **Blender Scene:** classroom.blend
- **Camera:** orbit around desk grid (20 desks, procedural loop)
- **Duration:** 5.0s (150 frames)
- **Text Overlay:** "PRODUCTS. CHECKOUT. MOBILE MONEY."
- **Animation:** cascade
- **Audio Cue:** voiceover.wav 4.0s-9.0s + ambience_classroom.ogg bed

### Scene 3 (9.0s - 14.0s)
- **Type:** 3d-scene
- **Blender Scene:** classroom.blend
- **Camera:** push-in on hero desk, shallow DOF
- **Duration:** 5.0s (150 frames)
- **Text Overlay:** "SIGN UP FREE AT FAKO ONLINE.COM"
- **Animation:** scaleUp
- **Audio Cue:** voiceover.wav 9.0s-14.0s
- **CTA:** true

## Audio
- **Voiceover:** global_sfx/voiceover.wav (provided)
- **Background Music:** None | [file path]
- **SFX:** global_sfx/ambience_classroom.ogg
- **Music Volume:** 0.15

## Branding
- **Primary Color:** #D4AF37
- **Background:** #0A0A0A
- **Font:** Impact
```

### Plan Rules

1. Every scene must specify: type, duration, Blender scene + camera move, text overlay, audio cue
2. Timestamps must be explicit (start - end in seconds) and frame counts must match (seconds x 30)
3. Text overlays must include animation type (zoom, cascade, shake, scaleUp)
4. Audio cues must reference real files in `global_sfx/` with their in/out points
5. Assets can be "provided" (user supplies file) or "download" (script pulls it in Phase 2)
6. If source is "download", include the exact downloader command in the plan
7. Platform field determines which notebook/kernel to use:
   - `kaggle`: Use the `blender-render-engine` Kaggle kernel + Kaggle API

---

## 2. Phase 2 - Gathering Assets

No AI generation. Every ingredient is either **already on disk** or **pulled from a public
domain library** through a terminal command.

### 2.1 Downloader Toolbelt

```powershell
# Asset scraper for Poly Haven (HDRIs, textures, 3D models) - CC0 public domain
pip install polydown --upgrade

# Cloud connection engine (Kaggle API CLI)
pip install kaggle --upgrade

# Final encoder (native Windows package manager)
winget install FFmpeg
```

### 2.2 Download Commands

```powershell
# 4K indoor HDRI for realistic glass/metal reflections (window light)
polydown hdris -f .\global_assets\hdris\ -c indoor -s 4k

# Premium wood PBR texture set for procedural desks (diffuse + roughness maps)
polydown textures -f .\global_assets\textures\ -c wood -s 2k --maps Diffuse Rough

# Base furniture models as .blend files
polydown models -f .\global_assets\models\ -c decorative -s 2k -mf blend

# List what a category contains before committing to bandwidth
polydown textures -c
```

### 2.3 Audio Warehouse

Voiceovers are **recorded/provided**, not synthesized. Drop files into `global_sfx/`:

```powershell
# Reference pattern for pulling public-domain SFX packs
curl -s "https://example.com/publicdomain/door-squeak.ogg" -o .\global_assets\..\global_sfx\door_action.ogg
```

| Asset type               | Where it comes from                    | Destination                 |
| ------------------------ | -------------------------------------- | --------------------------- |
| Voiceover narration      | Provided (recorded by you/voice actor) | `global_sfx/`             |
| Background music         | Provided (licensed track)              | `global_sfx/`             |
| Ambient SFX              | Provided or public-domain download     | `global_sfx/`             |
| HDRI lighting            | `polydown hdris`                     | `global_assets/hdris/`    |
| PBR textures             | `polydown textures`                  | `global_assets/textures/` |
| 3D models / base scenes  | `polydown models` or provided        | `global_assets/models/`   |
| Brand logo / screenshots | Provided                               | `global_assets/`          |

### 2.4 Asset Sync (Before Every Push)

The Kaggle kernel can only see files inside the push directory. Sync before rendering:

```powershell
# Mirror warehouse into the worker folder that gets uploaded
robocopy .\global_assets\ .\kaggle_worker\assets\ /MIR
robocopy .\global_sfx\   .\kaggle_worker\sfx\   /MIR
```

**Size guard:** Kaggle's working directory is 19.5GB. Check before pushing:

```powershell
Get-ChildItem .\kaggle_worker\ -Recurse | Measure-Object -Property Length -Sum |
  Select-Object @{N='GB';E={[math]::Round($_.Sum/1GB,2)}}
```

If it exceeds ~15GB, download lighter sizes (`-s 1k` instead of `-s 4k`).

---

## 3. Phase 3 - Blender Inside Kaggle (The Heavy Lifting)

### 3.1 One-Time Kaggle API Setup

1. Create a free account at kaggle.com
2. Account Settings → API → **Create New API Token** → downloads `kaggle.json`
3. Place it at:

| OS          | Path                                        |
| ----------- | ------------------------------------------- |
| Windows     | `C:\Users\<username>\.kaggle\kaggle.json` |
| macOS/Linux | `~/.kaggle/kaggle.json`                   |

```json
{
  "username": "your-kaggle-username",
  "key": "your-kaggle-api-key"
}
```

Every `kaggle` CLI command (and any script using the Kaggle API) reads this file automatically.

```powershell
# Verify credentials work
kaggle datasets list -s polyhaven
```

### 3.2 Local Folder Architecture

```powershell
# Built once at the project root (LocalContents)
New-Item -ItemType Directory -Force -Path .\global_assets\hdris
New-Item -ItemType Directory -Force -Path .\global_assets\textures
New-Item -ItemType Directory -Force -Path .\global_assets\models
New-Item -ItemType Directory -Force -Path .\global_sfx
New-Item -ItemType Directory -Force -Path .\kaggle_worker
New-Item -ItemType Directory -Force -Path .\remotion_overlays
New-Item -ItemType Directory -Force -Path .\final_output
```

### 3.3 Build the Cloud Controller

```powershell
cd .\kaggle_worker
kaggle kernels init -p .
```

Edit the generated `kernel-metadata.json`:

```json
{
  "id": "YOUR_KAGGLE_USERNAME/blender-render-engine",
  "title": "Blender Render Engine",
  "code_file": "cloud_orchestrator.py",
  "language": "python",
  "kernel_type": "script",
  "is_private": true,
  "enable_gpu": true,
  "enable_internet": true,
  "dataset_sources": []
}
```

**Crucial:** replace `YOUR_KAGGLE_USERNAME` with the exact public username on your Kaggle profile.

> **Lesson learned (Kernel Metadata: Always Pull First):** for a kernel that already exists,
> never hand-write the metadata with a guessed `id` — datasets won't mount and the kernel
> writes to the wrong place. Always pull first:
>
> ```powershell
> kaggle kernels pull YOUR_KAGGLE_USERNAME/blender-render-engine -m
> ```
>
> This recreates `kernel-metadata.json` with Kaggle's exact `id`/`title`. Edit it, copy your
> updated script in, push back. For a brand-new kernel, local init output is fine.

### 3.4 The Master Cloud Script (`cloud_orchestrator.py`)

This file lives in `kaggle_worker/` and executes automatically on Kaggle's server. It must:

1. **Boot Blender headlessly** — download a Linux x64 Blender build (or install from the
   apt/snap mirror), no display server, `--factory-startup` safe
2. **Attach the GPUs** — detect both Tesla T4 cards, point Cycles at CUDA:
   ```python
   # inside the blender -b invocation, or via bpy
   prefs = bpy.context.preferences.addons["cycles"].preferences
   prefs.compute_device_type = "CUDA"
   prefs.get_devices()
   for d in prefs.devices:
       d.use = True
   ```
3. **Assemble the geometry** — read the layout logic: load the 5 core assets from
   `kaggle_worker/assets/`, run a grid math loop to spawn 20 desks and animate the crowd
4. **Calculate lighting** — Cycles engine, wrap the HDRI around the room, read roughness/color
   from the PBR texture set, bounce rays through the windows
5. **Execute the camera sweep** — animate the camera along the coded 30-second path,
   output exactly **900 frames** (30fps) as PNG
6. **Package the output** — bundle the frames into `render_output.zip` in `/kaggle/working/`
7. **Report** — print progress every 50 frames so `kaggle kernels logs` shows status

Launch signature used by the script (documented here so the orchestrator stays consistent):

```bash
blender -b -P render_scene.py -- \
  --assets /kaggle/working/assets \
  --out /kaggle/working/frames \
  --fps 30 --frames 900 \
  --engine CYCLES --samples 128 --device CUDA
```

### 3.5 Fire the Run

```powershell
cd .\kaggle_worker

# Upload the script + assets and start the kernel on GPU
kaggle kernels push -p .

# Watch progress
kaggle kernels status YOUR_KAGGLE_USERNAME/blender-render-engine
```

When status prints `complete`, pull the payload back:

```powershell
kaggle kernels output YOUR_KAGGLE_USERNAME/blender-render-engine -p ..\final_output\
Expand-Archive .\final_output\render_output.zip -DestinationPath .\final_output\frames\
```

**Same flow via the Kaggle API (Python)** — if you prefer scripting the loop instead of
typing commands:

```python
import kagglehub
from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

api.kernels_push("/kaggle_worker")                 # upload + start
api.kernels_status("blender-render-engine")        # poll until "complete"
api.kernels_output("blender-render-engine", path="../final_output")  # download
```

### 3.6 Local Blender (Previews & Script Tests)

Blender is installed on the laptop **only as a terminal binary** — used to validate the
orchestrator cheaply before spending GPU quota.

```powershell
# Render a single test still at low samples (seconds, not minutes)
blender -b .\kaggle_worker\scene.blend -o //preview_ -F PNG -f 1

# Run the render script locally against 10 frames only
blender -b -P .\kaggle_worker\render_scene.py -- --frames 10 --samples 16 --device OPTIX

# Inspect a file without opening the GUI
blender -b .\kaggle_worker\scene.blend --python-expr "import bpy; print(len(bpy.data.objects))"
```

**Never** `blender scene.blend` (no `-b`) — that opens the interactive GUI, which this
pipeline does not use.

### 3.7 Session Limits

| Limit             | Value                    | Notes                                        |
| ----------------- | ------------------------ | -------------------------------------------- |
| Session timeout   | ~12 hours                | Kaggle auto-stops idle sessions              |
| GPU quota         | ~30 hrs/week per account | Use backup account when exceeded             |
| Working directory | 19.5 GB                  | Keep assets light, frames zipped             |
| Max dataset size  | 100 GB per dataset       | Use datasets for large reusable assets       |
| GPU               | Tesla T4 x2 (32GB VRAM)  | Request`--accelerator "GPU T4 x2"` on push |

**Multi-Account Setup (unchanged):** Kaggle caps GPU at ~30 hrs/week per account.
Account A owns the datasets; Account B is added as collaborator on each dataset
(Settings → Collaborators). When A hits the quota, log out/in with B — the same kernels
and datasets work with no re-download.

---

## 4. Phase 4 - The Remotion Pass (Local Typography)

Once `render_output.zip` is on disk, Remotion draws the razor-sharp brand typography,
motion graphics, intro screens and floating informational tags as a transparent layer.

```powershell
# Visual preview
npm run studio

# Render one track (text layer over the Blender frames)
npm run render:ecommerce
npm run render:businesses
npm run render:schools
npm run render:churches
npm run render:promo
```

### 4.1 Composition Components

| Component           | What It Does                           | Animation Options                                      | Plan Field                    |
| ------------------- | -------------------------------------- | ------------------------------------------------------ | ----------------------------- |
| KenBurnsImage       | Animated image movement                | `zoom-in`, `zoom-out`, `pan-right`, `pan-left` | `Animation: zoom-in`        |
| AnimatedText        | Word-by-word spring animation          | `zoom`, `shake`, `cascade`, `scaleUp`          | `Animation: cascade`        |
| DarkScrim           | Gradient overlay                       | `full`, `bottom`                                   | `Background: dark gradient` |
| ImageScene          | Frame/image + Ken Burns + text overlay | All KenBurns + AnimatedText options                    | `Type: 3d-scene`            |
| FakoContentTemplate | Main composition (3 scenes)            | `fade`, `slide` transitions                        | Handled automatically         |

#### Animation Types in Detail

| Animation       | Behavior                            | Best For                       |
| --------------- | ----------------------------------- | ------------------------------ |
| `zoom-in`     | Slowly zoom into center             | Hero shots, emphasis, drama    |
| `zoom-out`    | Slowly zoom out from center         | Reveals, establishing shots    |
| `pan-right`   | Slowly pan right across frame       | Landscape, product showcase    |
| `pan-left`    | Slowly pan left across frame        | Reverse pan, reading direction |
| `shake`       | Quick shake/vibration               | Excitement, urgency, impact    |
| `scaleUp`     | Scale up from small to full size    | Text emphasis, call-to-action  |
| `cascade`     | Words appear one by one with spring | Lists, bullet points           |
| `zoom` (text) | Text zooms in from center           | Headlines, big statements      |

#### Transitions Between Scenes

| Transition | Effect                          |
| ---------- | ------------------------------- |
| fade       | Cross-fade between scenes       |
| slide      | Slide transition between scenes |

### 4.2 Track System

| Track      | Directory                  | Render Command                |
| ---------- | -------------------------- | ----------------------------- |
| ecommerce  | `tracks/ecommerce/`      | `npm run render:ecommerce`  |
| businesses | `tracks/businesses/`     | `npm run render:businesses` |
| schools    | `tracks/schools/`        | `npm run render:schools`    |
| churches   | `tracks/churches/`       | `npm run render:churches`   |
| promo      | `tracks/promo-business/` | `npm run render:promo`      |

#### Asset Conventions per Track

```
tracks/[track]/
  assets/          → Frames/images used by the composition
  voiceovers/      → Pre-generated .wav audio files
  music/           → Background music files (.mp3, .wav)
  data/
    fako_video_data.json  → Timeline data (scenes, timing, branding)
  out/
    video.mp4      → Remotion text layer / intermediate render
```

#### fako_video_data.json Structure

```json
{
  "meta": {
    "track": "ecommerce",
    "branding": {
      "primaryColor": "#D4AF37",
      "backgroundColor": "#0A0A0A",
      "fontFamily": "Impact"
    },
    "audio": {
      "voiceFile": "voiceovers/scene1.wav",
      "bgMusic": "music/background.mp3"
    }
  },
  "timeline": [
    {
      "start": 0,
      "end": 4.0,
      "text": "YOUR BUSINESS DESERVES TO BE ONLINE.",
      "uiMockup": "assets/hero.png",
      "animation": "shake",
      "talkScene": false
    }
  ]
}
```

### 4.3 Text Overlay Rules

- Primary color: #D4AF37 (gold)
- Background: #0A0A0A (dark)
- Font: Impact
- Text animations: shake, scaleUp, zoom, cascade

---

## 5. Phase 5 - The Final FFmpeg Mix

FFmpeg is the final editing blender: it reads the 3D frames from Kaggle, sandwiches the
vector text graphics from Remotion on top, binds the audio cues, and encodes one master.

```powershell
# 1) Blender frames -> base video (30fps, 1080x1920)
ffmpeg -framerate 30 -i .\final_output\frames\fako_%04d.png `
       -c:v libx264 -pix_fmt yuv420p -r 30 .\final_output\base_3d.mp4

# 2) Sandwich the Remotion typography layer over the base
ffmpeg -i .\final_output\base_3d.mp4 -i .\tracks\ecommerce\out\video.mp4 `
       -filter_complex "[0:v][1:v]overlay=shortest=1[v]" -map "[v]" `
       .\final_output\combined.mp4

# 3) Bind audio: voiceover + ambience bed + music, then encode the final master
ffmpeg -i .\final_output\combined.mp4 `
       -i .\global_sfx\voiceover.wav `
       -i .\global_sfx\ambience_classroom.ogg `
       -filter_complex "[1:a][2:a]amix=inputs=2:duration=first[a]" `
       -map 0:v -map "[a]" `
       -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p `
       -c:a aac -b:a 192k -shortest `
       .\final_output\final_premium_commercial.mp4
```

| Step                | Input                                    | Output                           |
| ------------------- | ---------------------------------------- | -------------------------------- |
| Frames → video     | `render_output.zip` PNG sequence       | `base_3d.mp4`                  |
| Typography sandwich | `base_3d.mp4` + Remotion `video.mp4` | `combined.mp4`                 |
| Audio bind + encode | `combined.mp4` + voiceover + ambience  | `final_premium_commercial.mp4` |

Typical end-to-end loop: **under 25 minutes** for a 30s/900-frame commercial, with the
laptop cool and quiet (only the CPU phases run locally).

---

## 6. Project Structure

```
LocalContents/
  new guides/
    guide.md                         # This file
  plans/
    [content-name]-plan.md           # One plan per video
  global_assets/                     # Phase 2 warehouse (3D ingredients)
    hdris/                           #   polydown HDRIs (4k EXR/HDR)
    textures/                        #   polydown PBR texture sets
    models/                          #   .blend scenes, furniture, props
    logo.png                         #   provided brand files
  global_sfx/                        # Phase 2 warehouse (audio)
    voiceover.wav                    #   provided narration
    ambience_classroom.ogg           #   provided/downloaded room tone
    background.mp3                   #   provided music
  kaggle_worker/                     # Phase 3 upload workspace
    kernel-metadata.json             #   Kaggle kernel config
    cloud_orchestrator.py            #   entry point run on Kaggle
    render_scene.py                  #   Blender python render logic
    assets/                          #   synced copy of global_assets
    sfx/                             #   synced copy of global_sfx
  remotion_overlays/                 # Phase 4 intermediate text layers
  final_output/                      # Phase 3/5 payload area
    frames/                          #   900 PNG frames from Kaggle
    base_3d.mp4                      #   frames encoded
    combined.mp4                     #   + typography layer
    final_premium_commercial.mp4     #   final master
  packages/remotion-core/src/
    Composition.tsx                  # Main video template
    styles/global.css
  tracks/
    ecommerce/data/fako_video_data.json
    businesses/data/fako_video_data.json
    schools/data/fako_video_data.json
    churches/data/fako_video_data.json
    promo-business/data/fako_video_data.json
  public/
    assets/                          # Static files for staticFile()
    voiceovers/                      # Pre-generated audio
  .kaggle/kaggle.json                # (home dir) Kaggle API credentials
```

---

## 7. Workflow

### Creating New Content

1. Copy the plan template (Section 1)
2. Fill in all scenes with explicit timestamps, Blender camera moves, text, audio cues
3. Set platform field to `kaggle`
4. Save as `plans/[content-name]-plan.md`
5. Review the plan for completeness
6. Execute the phases in order

### Executing a Plan

| Need                     | Phase | Action                                                                  |
| ------------------------ | ----- | ----------------------------------------------------------------------- |
| HDRI / textures / models | 2     | `polydown` download into `global_assets/`                           |
| Voiceover / music / SFX  | 2     | Drop provided files into`global_sfx/`                                 |
| 3D footage (900 frames)  | 3     | `kaggle kernels push` → Blender renders → `kaggle kernels output` |
| Text / motion graphics   | 4     | Update`fako_video_data.json`, `npm run render:[track]`              |
| Final master             | 5     | FFmpeg sandwich + audio bind →`final_premium_commercial.mp4`         |

**Hard ordering rule:** frames must exist before the Remotion pass, and the Remotion layer
must exist before the FFmpeg mix. Audio files must be present before Step 3 of FFmpeg.

### CLI Command Reference

```powershell
# --- Assets (Phase 2) ---
pip install polydown kaggle
winget install FFmpeg
polydown hdris -f .\global_assets\hdris\ -c indoor -s 4k
polydown textures -f .\global_assets\textures\ -c wood -s 2k --maps Diffuse Rough
polydown models -f .\global_assets\models\ -c decorative -s 2k -mf blend
robocopy .\global_assets\ .\kaggle_worker\assets\ /MIR

# --- Kaggle engine (Phase 3) ---
kaggle kernels init -p .\kaggle_worker
kaggle kernels pull YOUR_USERNAME/blender-render-engine -m
kaggle kernels push -p .\kaggle_worker
kaggle kernels status YOUR_USERNAME/blender-render-engine
kaggle kernels logs YOUR_USERNAME/blender-render-engine
kaggle kernels output YOUR_USERNAME/blender-render-engine -p .\final_output\

# --- Local Blender previews (Phase 3) ---
blender -b .\kaggle_worker\scene.blend -o //preview_ -F PNG -f 1
blender -b -P .\kaggle_worker\render_scene.py -- --frames 10 --samples 16

# --- Remotion (Phase 4) ---
npm run studio
npm run render:ecommerce   # also: businesses, schools, churches, promo
npm run render:all

# --- FFmpeg master (Phase 5) ---
ffmpeg -framerate 30 -i .\final_output\frames\fako_%04d.png -c:v libx264 -pix_fmt yuv420p .\final_output\base_3d.mp4
```

---

## 8. Troubleshooting

| Issue                       | Cause                               | Solution                                                        |
| --------------------------- | ----------------------------------- | --------------------------------------------------------------- |
| `403 Forbidden`           | Wrong credentials                   | Check`~/.kaggle/kaggle.json` exists and is correct            |
| `Kernel not found`        | Typo in kernel ID                   | `kaggle kernels list --mine` to see your kernels              |
| Datasets not mounted        | Wrong`id` in kernel-metadata.json | Pull metadata (`-m`), verify `id`, push back                |
| GPU not used by Cycles      | CUDA devices not enabled            | Set`compute_device_type="CUDA"` and `d.use = True`          |
| `No space left on device` | Working directory over 19.5GB       | Download`-s 1k` assets, zip frames immediately                |
| GPU OOM                     | Too heavy a scene                   | Request`--accelerator "GPU T4 x2"`, lower samples             |
| Session stopped             | Idle timeout or quota               | Push again with`kaggle kernels push`                          |
| Frames have wrong count     | fps/duration mismatch               | frames = seconds x 30; check plan math                          |
| Remotion render fails       | TypeScript errors                   | Run typecheck, check`fako_video_data.json` paths              |
| FFmpeg overlay drift        | Different frame rates               | Force`-framerate 30` on both inputs                           |
| Quota exhausted (~30h/wk)   | Weekly GPU cap                      | Switch to backup account (Section 3.7)                          |
| PowerShell encoding crash   | `kaggle kernels logs` Unicode     | Capture as bytes via Python subprocess, or read logs in browser |

### Lessons Learned (carried over)

- **Kernel metadata: always pull first** — hand-written `id` values silently break dataset mounts
- **Windows PowerShell + Kaggle CLI encoding** — `kaggle kernels logs` output can crash PowerShell with `'charmap' codec can't encode characters`; use:
  ```python
  import subprocess
  r = subprocess.run(['kaggle','kernels','logs','USER/kernel'], capture_output=True,
                     text=True, encoding='utf-8', errors='replace')
  print(r.stdout)
  ```
- **Working directory discipline** — models/assets live in datasets or get mirrored in at push time; frames are zipped the moment they are written
- **Execution order** — assets → render → text → audio → mix; never run a phase before its input exists

---

## 9. Migration Note (What Was Removed)

This guide replaces `guide5.md`. The following are **gone from the project** and must not
be referenced in new plans:

| Removed                                                                                | Replaced by                                      |
| -------------------------------------------------------------------------------------- | ------------------------------------------------ |
| Wan 2.1 B-Roll server (port 8001)                                                      | Blender camera work / downloaded footage         |
| AnimateDiff + ControlNet (port 8002)                                                   | Blender keyframe animation                       |
| Stable Diffusion 1.5 image gen (port 8002)                                             | Provided images +`polydown` downloads          |
| Bark TTS voiceover (port 8000)                                                         | Provided voiceover WAV files                     |
| SadTalker / Easy-Wav2Lip / LatentSync lip sync (port 8000)                             | Talking-head scenes dropped; 3D + text pipeline  |
| ngrok tunnels +`KAGGLE_API_URL` + `NGROK_AUTHTOKEN`                                | Direct Kaggle API / CLI (`kaggle kernels ...`) |
| `colab/*-server-*.ipynb`, `colab/download-*.ipynb`                                 | `kaggle_worker/cloud_orchestrator.py`          |
| `scripts/generate-talking-head.js`, `generate-avatar.js`, model helpers            | Terminal commands in this guide                  |
| Kaggle model datasets (bark, sadtalker, wav2lip, latentsync, wan21, animatediff, sd15) | Not needed — no models to host                  |

Legacy example: `plans/sell-online-plan.md` still uses the old AI-generation template.
Treat it as reference material only; write new plans with the Section 1 template.
