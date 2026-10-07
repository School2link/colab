# Report Cards - Blender Build Order (Local, Terminal-Only)

> **Companion to:** `plan.md` (what) · `script.md` (when it appears on screen)
> **This file:** the sequence in which the 21 Blender assets + master scene get built,
> and the exact terminal commands for each batch.

## Status

| Batch | State | Evidence |
|-------|-------|----------|
| 0 Infra | **DONE** | Smoke test: headless Cycles render OK (8.8s) |
| 1 Hero props | **DONE** | 8 `.blend` in `global_assets/models/` (object-name probe verified) + 8 previews (pixel-verified: checkmark 20% gold, clock white face+ticks). Fixes applied: checkmark emission 2.0→0.7, clock tick marks added, screen glow raised. |
| 2 UI textures | **DONE** | 9 PNGs in `global_assets/ui/` + contact-sheet reviewed. Fixes applied: sRGB→linear color conversion in `common.py` (gold was washing out to 218,201,125), progress/portal header-vs-button material split (state morph was recoloring headers). Pixel-verified: GH₵ glyph, 40%/100% bar states, 240/512/0 ledger states, portal list/tapped. |
| 3 Brand | **DONE** | `global_assets/school-crest.png` (1024², ARGB, corner alpha=0, 43% transparent / 21% gold / 24% dark field) — shield + star + open book + FAKO banner, visually reviewed. |
| D Downloads | **DONE** | 2 HDRI (`hdri-night.exr` = warm_restaurant_night, `hdri-day.exr` = poly_haven_studio, Poly Haven API picks after polydown's random category grab was unusable) + 3 PBR sets (`coated_pine` 2k, `plastered_wall` 1k, `rough_linen` 1k — diff+rough jpg) + 22 CC0/royalty-free audio (19 wav 48k stereo in `global_sfx/sfx/`, 3 mp3 in `global_sfx/music/`, all mixkit, ffprobe-verified durations). Fixes: PYTHONUTF8=1 for polydown cp1252 crash; category-wide polydown download replaced with per-asset Poly Haven API; 8 auto-picked SFX re-picked manually. |
| 4 Characters | **DONE** | 3 `.blend` (`teacher` T1/T2/T3, `student` S1/S2, `parent` P1) + 6 pose previews on contact sheet. Fixes: `_mats()` re-created after each `clear_scene` purge; def-time material defaults → `None`; `use_fake_user` on all actions (0-user actions dropped at file load — T2/T3/S2 were missing on reopen); `transform_apply` before bone-parenting (phone lost basis scale → giant cube in preview); preview camera reframed (lens 35, distance span×4 — tall characters were cropped). |
| 5 Sets | **DONE** | 4 set `.blend` (`set-staffroom/office/courtyard/digital-void`) + 4 previews on 4-up montage (purple border = verified copy). HDRI backdrops correctly mapped. Fixes: `ShaderNodeTexEnvironment` (ImageTexture was stretching the photo), preview camera `dist_mult` 2.6, office lighting raised, chalkboard closeup verified at 1280x720 ("B.E.C.E MOCK - FORM 3" legible + crest above board), crest z-fight (y 2.94→2.93) fixed in source + saved `.blend`. |
| 6 Assembly | **DONE** | `global_assets/models/report_cards.blend` (355 objects, markers M1–M8, frames 1–900, 1080x1920/30fps) + 12 QA stills on 4-up montage (cyan border = verified copy). All assets appended (self-contained for Kaggle), 7 character rig instances with pose vis-spans, 9 cameras + marker binding, full keyframe animation. Fixes: factory-startup Cube/Camera/Light purge (`clear_scene()` was never called — the stray 2m Cube was the white slab burying the desk); green-check children vis-keys (leaked into M8); ledger/customers reframed into M4 (moved to 19.5 / 21.05+21.5, lens 32→30); M5 pen framing (animated `aim_m5` keys, lens 35→30); portal fly-out start bug (x=0.72 was staff-zone coords → Z_CY+0.55) + portal/card reframe; M7b camera → window side; tower 3→4 stacks, scale 1.2→1.92; scribble 0.075→0.055; money rise +1.9→+0.8 (was flying above frame); M8 endcard floor raised to z0.35 (cyclorama cove pokes above z0.05 floor — bisect-proven via pixel sampling, strip = `dv_cyclorama`); `dv_ring` hidden during M8. |
| 6 Assembly | not started | |


## Ground Rules

1. **Terminal only.** Blender is never opened as a GUI. Every invocation:
   `& $blender -b --factory-startup -P <script> -- <args>`
2. **Blender path (not on PATH):**
   ```powershell
   $blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
   # Blender 5.2.2 LTS — smoke-tested: headless Cycles render OK (8.8s)
   ```
   To put it on PATH (optional, one-time):
   ```powershell
   [Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path","User") + ";C:\Program Files\Blender Foundation\Blender 5.2", "User")
   ```
3. **One script per batch**, living in `blender_build/`. Each script builds assets
   procedurally, saves `.blend` files to `global_assets\models\`, renders a preview still,
   and prints a `BUILD_OK` manifest line per asset.
4. **Preview, don't trust.** Every batch ends with a low-sample preview render
   (320x180, 16 samples) reviewed before the next batch starts.
5. **Heavy renders never run here** — local Blender only tests and previews;
   the 900-frame render goes to Kaggle (script.md Phase 3).

## Folder Layout

```
blender_build/                 ← build scripts (source, committed)
  common.py                    ← shared helpers (materials, collections, clear_scene)
  build_props.py               ← Batch 1
  build_ui.py                  ← Batch 2
  build_crest.py               ← Batch 3
  build_sets.py                ← Batch 5
  build_characters.py          ← Batch 4
  assemble_scene.py            ← Batch 6 (master report_cards.blend)
global_assets/
  models/                      ← .blend output destination
  hdris/ textures/             ← Phase 2 downloads (prereq for Batch 5)
plans/report-cards/previews/   ← preview stills per asset (review artifacts)
```

## Batch Sequence

| Batch | Name | Produces | Depends on | Script |
|-------|------|----------|-----------|--------|
| 0 | Infra | `blender_build/`, `common.py`, smoke test | — | (done: smoke test passed) |
| **D** | **Downloads** | 2 HDRI + 3 PBR (Phase 2 `polydown`) + 22 CC0 audio | internet | (guide Phase 2 commands) |
| **1** | **Hero props** | 8 prop `.blend` files (pen, checkmark, clock, booklets, tray, money, tablet, phone) | 0 | `build_props.py` |
| **2** | **UI textures** | 5 PNGs (gradebook, progress, ledger, portal, reportcard) | 0 | `build_ui.py` |
| **3** | **Brand** | `school-crest.png` | 0 | `build_crest.py` |
| **4** | Characters | 3 character `.blend` with pose variants (T1-3, S1-2, P1) | 0 | `build_characters.py` |
| **5** | Sets | 4 set `.blend` (staffroom, office, courtyard, digital-void) | D (HDRI + PBR) | `build_sets.py` |
| **6** | **Assembly** | `report_cards.blend` — all assets, cameras M1–M8, lighting rigs, animation | 1,2,3,4,5 | `assemble_scene.py` |
| — | Preview QA | 8 shot stills (one per marker) | 6 | preview pass (below) |
| 3–5 | Production | Kaggle 900f render → Remotion text → FFmpeg mix | 6 + QA | script.md |

**Why this order:**
- **Batch D first/parallel** — sets can't be lit without HDRIs, can't be textured without PBR
- **Props (1) first** — simplest geometry, zero external deps, and they carry the story
  (red pen → checkmark is the whole argument)
- **UI (2) + crest (3)** — flat PNG renders, fast wins, unblock the gradebook/phone shots
- **Characters (4) before sets (5)**? No — sets are blocked only by downloads, characters
  are the hardest work; build characters in parallel with review time, but they are
  sequenced after props so the easy-wins validate the toolchain first
- **Assembly (6) last** — everything lands in `report_cards.blend`, cameras bound with
  timeline markers M1–M8, animation keyed (pen morph f415–460, stack growth, clock spin,
  ledger re-texture, UI fills per script.md)

## Command Pattern (every batch)

```powershell
$blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
New-Item -ItemType Directory -Force -Path .\plans\report-cards\previews | Out-Null

# Build + preview in one headless pass
& $blender -b --factory-startup -P blender_build\build_props.py -- `
    --out .\global_assets\models `
    --preview .\plans\report-cards\previews
```

Expected console output per asset:
```
BUILD_OK red-pen.blend -> global_assets/models/red-pen.blend
PREVIEW_OK previews/prop_red-pen.png
```

### Preview still (single frame from any .blend — the QA loop)

```powershell
& $blender -b .\global_assets\models\red-pen.blend --factory-startup --python-expr `
  "import bpy; s=bpy.context.scene; s.render.engine='CYCLES'; s.cycles.samples=16; s.render.resolution_x=320; s.render.resolution_y=180; s.render.filepath=r'plans\report-cards\previews\qa_red-pen.png'; bpy.ops.render.render(write_still=True)"
```

## Batch 1 — Hero Props (target: first executable batch)

| Asset to build | Geometry notes | Animation data (keyed later in assembly) |
|----------------|----------------|------------------------------------------|
| `red-pen.blend` | Cylinder body, conical nib, cap ring — origin at centre | levitate + 720° spin (f415–445) |
| `checkmark-gold.blend` | Bevelled curve check, emissive gold `#D4AF37` | morph target + flight to tablet (f445–460) |
| `wall-clock.blend` | Face + hour/min/sec hands as separate objects | sec hand 1 rev/s; hands 12 revs in shot 3 |
| `booklet-stack.blend` | N booklets instanced in a stack (1 object, array modifier) | scale 1.0→1.6 (f195–299) |
| `report-tray.blend` | Open tray + "REPORT CARDS" label plane | static (stays empty) |
| `money-notes.blend` | 6 note planes + 4 coin cylinders | rise + fade out (f300–360) |
| `tablet.blend` | Rounded slab + screen plane (UI from Batch 2) | screen receives checkmark |
| `phone.blend` | Small slab + screen plane (UI from Batch 2) | static, screen swap f645/f675 |

**Done when:** all 8 `.blend` exist in `global_assets\models\`, previews reviewed,
`BUILD_OK x8` printed, ≤ 2 minutes total build time.

## Batch 2 — UI Textures (PNG via Blender, no external design tools)

Rendered flat orthographic (camera looking straight at a plane, 1080x1920 or 1080x1350,
Cycles/Workbench, no lighting needed — emission materials):

| PNG | Content | Frame states |
|-----|---------|--------------|
| `ui-gradebook.png` | Score table rows | base (checks added as separate animated planes in assembly) |
| `ui-progress.png` | "Generating report cards…" bar | 2 frames: 40% and 100% |
| `ui-ledger.png` | "PRINTING: GH₵" tally | 3 frames: 240 / 512 / **0** |
| `ui-portal.png` | Phone portal login + "Download Report Card" button | 2 frames: list / button-tapped |
| `ui-reportcard.png` | Grades + comment + gold crest | 1 frame (crisp) |

## Batch 3 — Brand

| PNG | Content |
|-----|---------|
| `school-crest.png` | Simple gold emblem on transparent background — shield + book motif, `#D4AF37` |

## Batch 4 — Characters (hardest — stylised, low-poly)

| Asset | Approach | Poses |
|-------|----------|-------|
| `teacher.blend` | Stylised proportions (large head, simple limbs), armature, dress as solid mesh | T1 hunched, T2 head-in-hand, T3 stretch-smile |
| `student.blend` | Same style, uniform + satchel, phone prop | S1 impatient, S2 smiling |
| `parent.blend` | Same style, simplest — background only | P1 static |

Each pose = a named **action** (animation data) inside the same `.blend`, selected at
assembly time. No facial rig — emotion via pose + camera (matches stylised look).

## Batch 5 — Sets (needs Batch D downloads)

| Asset | Contents | Lighting rig |
|-------|----------|--------------|
| `set-staffroom.blend` | Desk, chair, bulb, window, shelves, chalkboard ("B.E.C.E MOCK - FORM 3"), crest slot | warm point 2700K + night HDRI 0.1 |
| `set-office.blend` | Counter, printer, reams, toner, ledger slot | cool fluorescent strip |
| `set-courtyard.blend` | Bench, school wall, tree shade | day HDRI |
| `set-digital-void.blend` | Backdrop cyclorama | bright studio, day HDRI 0.8 |

## Batch 6 — Assembly (`report_cards.blend`)

1. Append all props/characters/sets (Library Link → `//` relative paths into `global_assets\models\`)
2. Place 8 cameras, bind timeline markers **M1–M8** (M7a/M7b split at f690)
3. Lighting rigs per shot (palette flip: amber dies f435, day ramps in f435–479)
4. Keyframe animation exactly per script.md §1 (pen morph, stack growth, clock spin,
   money rise, UI swaps, pose switches T1→T3, S1→S2)
5. Set output: `fako_####.png`, 1–900, 1080x1920
6. Save to `global_assets\models\report_cards.blend`

**QA before Kaggle:** render 8 stills (one per marker, frame 045/140/250/350/440/550/700/830)
at 320x180, review against script.md §1.

## Definition of Done (local phase)

- [x] Batch D: 5 polydown files + 22 audio files on disk
- [x] Batches 1–3: 8 props + 9 UI PNGs + crest PNG + previews reviewed
- [x] Batch 4: 3 characters with all pose actions
- [x] Batch 5: 4 sets, textures applied, lighting rigs present
- [x] Batch 6: `report_cards.blend` opens headless, markers M1–M8 bound, 900f output set
- [x] QA: marker stills (12: M1–M8 + M4b/M6b/M7c beats) match script.md §1 descriptions
- [ ] Then → script.md Phase 3 (Kaggle push)
