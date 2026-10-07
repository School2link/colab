# Report Cards ("The Red Pen") - Production Script

> **Companion to:** `plan.md` (story + asset manifest)
> **Spec:** 1080x1920 (9:16) · 30fps · **900 frames** · MP4 H.264 · no voiceover
> **Frame math:** frame = seconds x 30. Shot 1 = 000–089, shot 8 ends at 899.

---

## 1. Shot List (Blender — one `report_cards.blend`, camera markers)

Cameras are bound with **timeline markers** (M1–M8) so a single `-a` render cuts
automatically. No hard cut falls on a beat boundary with the text layer — text timing is
in Section 3.

| Shot | Marker  | Frames   | Time       | Camera move                                                     | Lighting / palette                                                              |
| ---- | ------- | -------- | ---------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| 1    | M1      | 000–089 | 0.0–3.0   | Slow push-in through staff room doorway toward desk             | Single warm bulb (point, warm 2700K), night HDRI at 0.1 — dim amber            |
| 2    | M2      | 090–194 | 3.0–6.5   | Top-down macro on exam page → slow pull-back revealing pile    | Same bulb, tighter; page emissive bounce; shallow DOF                           |
| 3    | M3      | 195–299 | 6.5–10.0  | Locked wide, clock in upper third, window behind                | Bulb + window flicker (sun→moon→sun emissive cycle)                           |
| 4    | M4      | 300–404 | 10.0–13.5 | Lateral track left→right across the counter                    | Cool overhead fluorescent strip — institutional, heavy                         |
| 5    | M5      | 405–479 | 13.5–16.0 | Whip push into tablet screen (short motion-blur pass)           | Mid-shot: amber dies at 14.5,**day HDRI ramps in** — amber → gold/white |
| 6    | M6      | 480–629 | 16.0–21.0 | Static, UI plane fills frame                                    | Bright even studio light, day HDRI 0.8, clean white balance                     |
| 7    | M7a/M7b | 630–764 | 21.0–25.5 | M7a rack-focus student; cut at frame 690 → M7b push on teacher | Day HDRI, warm sun, courtyard + sunlit staff room                               |
| 8    | M8      | 765–899 | 25.5–30.0 | Lock-off on end-card stage                                      | Soft key + gold rim, dark`#0A0A0A` backdrop                                   |

### Shot action detail

**Shot 1 (000–089) — The burden**
Teacher **T1** (hunched marking) at desk. `booklet-stack` towers frame-right. `wall-clock`
reads 23:07, second hand ticking. `school-crest` on wall, chalkboard reads
"B.E.C.E MOCK - FORM 3". Bulb flickers once at frame 060. Teacher rubs eyes at 075–089.

**Shot 2 (090–194) — The error**
Macro: red nib writes **17** (frames 096–126), hesitation pause (126–140), scribble-out
(140–156), writes **71** (156–176). From frame 176 a translucent "ghost layer" of wrong
scores ripples outward across the pile (scale-in duplicates, stagger 2 frames). Camera
pulls back 140–194 revealing the pile's full height.

**Shot 3 (195–299) — The delay**
Time-lapse: `wall-clock` hands spin 12 revolutions. Window emissive cycles sun→moon→sun x3.
`booklet-stack` scales up 1.0 → 1.6 (frames 195–299, linear). `report-tray` (labelled
"REPORT CARDS") sits foreground empty the whole shot. At 285 a booklet tips and falls.

**Shot 4 (300–404) — The cost**
Counter: `ui-ledger` tally climbs "PRINTING: GH₵ 240… 380… 512" (re-texture every 20f).
`money-notes` detach and float upward out of frame (300–360, staggered). Reams + toner
stacks flank the printer. `parent` + `student` **S1** stand waiting; student checks an
empty wrist at 370–390, frown.

**Shot 5 (405–479) — THE PIVOT**
405–415: cursor descends, `sfx-click` on 408. 415–445: `red-pen` levitates, spins 720°.
445–460: morphs into `checkmark-gold` (shape-key morph), trails light ribbon, flies into
`tablet`. 460–479: desk, booklets, office dissolve (alpha fade to white); lighting rig
crossfades amber → day HDRI; palette lands gold/white at 479.

**Shot 6 (480–629) — The fix**
`ui-gradebook` fills: 8 rows get green checks (480–540, one per 7–8 frames). 555–570: a
row flashes red with a wrong total, sweeps, corrects to green — **ding** at 555 (18.5s).
`ui-progress` bar: "Generating report cards…" 575–620 → **100%**, chime at 624 (20.8s).
At 600 a small card flips into frame reading **GH₵ 0** (ledger resolution).

**Shot 7 (630–764) — The payoff**
M7a (630–689): courtyard bench, `student` **S1→S2**: taps phone (645), portal loads,
taps "Download Report Card" (675), `ui-reportcard` materialises and glows — smile.
M7b (690–764): staff room **in daylight**, `teacher` **T3** stretches and smiles at a
tidy desk — one mug, no towers, sun through window. Rack from 690, settle by 730.

**Shot 8 (765–899) — Proof + CTA**
765–795: three icons pop in with spring — shrinking printer, fast clock, green-check
stack. 795–815: they snap together into a single gold sparkle. 815–860: "FAKO ONLINE"
types on (Impact, `#D4AF37`). 860–899: tagline types on beneath —
*"Report cards in minutes. Not weeks."* — hold, music resolves.

---

## 2. Audio Edit Map

Levels: **music bed 0.15** · **SFX as marked**. All files from `global_sfx/`
(`music/`, `sfx/`) — exact list in `plan.md` §G. No voice track exists anywhere.

### Music stems

| Stem              | Start | End  | Frames   | Level | Notes                                      |
| ----------------- | ----- | ---- | -------- | ----- | ------------------------------------------ |
| music-tension.mp3 | 0.0   | 13.6 | 000–408 | 0.15  | Fade-out 13.4–13.6 (crossfade into pivot) |
| music-pivot.mp3   | 13.5  | 16.0 | 405–480 | 0.15  | Riser; swell peaks 15.8                    |
| music-uplift.mp3  | 15.9  | 30.0 | 477–899 | 0.15  | Resolve chord 27.5; final hit 28.0–30.0   |

### SFX cues

| #  | File                   | Start | End  | Frames   | Level | Anchor                                           |
| -- | ---------------------- | ----- | ---- | -------- | ----- | ------------------------------------------------ |
| 1  | sfx-clock-tick.wav     | 0.0   | 6.5  | 000–194 | 0.5   | loop (beat 1–2)                                 |
| 2  | sfx-pen-scratch.wav    | 0.3   | 6.5  | 009–194 | 0.6   | segments 0.3/1.6/3.2/4.6/5.8; quickens after 3.0 |
| 3  | sfx-sigh.wav           | 2.8   | 3.4  | 084–102 | 0.9   | teacher exhale                                   |
| 4  | sfx-error-buzz.wav     | 4.2   | 4.6  | 126–138 | 1.0   | the 17→71 moment                                |
| 5  | sfx-clock-fast.wav     | 6.5   | 10.0 | 195–300 | 0.7   | accelerating stutter                             |
| 6  | sfx-paper-crumple.wav  | 8.5   | 9.0  | 255–270 | 1.0   | booklet falls (shot 3, f285)                     |
| 7  | sfx-printer-jam.wav    | 9.0   | 9.6  | 270–288 | 0.9   | counter tease                                    |
| 8  | sfx-coins-clink.wav    | 10.4  | 11.0 | 312–330 | 0.9   | ledger climbs                                    |
| 9  | sfx-money-whoosh.wav   | 11.5  | 12.3 | 345–369 | 1.0   | notes fly out                                    |
| 10 | sfx-murmur.wav         | 12.6  | 13.2 | 378–396 | 0.8   | wordless "hmm"                                   |
| 11 | sfx-click.wav          | 13.6  | 13.8 | 408–414 | 1.0   | cursor click — the turn                         |
| 12 | sfx-magic-whoosh.wav   | 14.0  | 15.2 | 420–456 | 1.0   | pen levitate → morph                            |
| 13 | sfx-ui-clicks.wav      | 16.0  | 20.5 | 480–615 | 0.8   | rhythmic, in tempo                               |
| 14 | sfx-ding.wav           | 18.5  | 18.9 | 555–567 | 1.0   | wrong total corrected                            |
| 15 | sfx-chime.wav          | 20.8  | 21.3 | 624–639 | 1.0   | progress 100%                                    |
| 16 | sfx-phone-tap.wav      | 21.5  | 21.7 | 645–651 | 1.0   | screen tap                                       |
| 17 | sfx-download-chime.wav | 23.0  | 23.6 | 690–708 | 1.0   | card materialises                                |
| 18 | sfx-giggle.wav         | 24.5  | 25.0 | 735–750 | 0.9   | wordless "heh"                                   |
| 19 | sfx-logo-sting.wav     | 26.0  | 26.6 | 780–798 | 1.0   | icon snap                                        |

---

## 3. Text Overlay Timeline (Remotion layer)

Six entries — rendered as a **transparent PNG sequence** (900 frames), then overlaid in FFmpeg.
Branding: `#D4AF37` last-word glow · white body · Impact · black text-shadow.

| #  | Start | End  | Frames   | Text                                                           | Animation | Notes                     |
| -- | ----- | ---- | -------- | -------------------------------------------------------------- | --------- | ------------------------- |
| T1 | 0.0   | 6.5  | 000–194 | SHE MARKS FOR HOURS.                                           | shake     | clears at beat 3 cut      |
| T2 | 6.5   | 13.5 | 195–404 | ONE ERROR DELAYS EVERY REPORT CARD.                            | cascade   | clears on pivot click     |
| T3 | 13.5  | 16.0 | 405–479 | UNTIL NOW.                                                     | zoom      | short, punchy — the turn |
| T4 | 16.0  | 21.0 | 480–629 | SCORES CHECKED AUTOMATICALLY.                                  | cascade   | clear of the UI action    |
| T5 | 21.0  | 25.5 | 630–764 | REPORT CARDS IN MINUTES.                                       | scaleUp   | over both M7a/M7b         |
| T6 | 25.5  | 30.0 | 765–899 | FAKO ONLINE (brand line) + Report cards in minutes. Not weeks. | scaleUp   | CTA end card, full scrim  |

**Props file:** `plans/report-cards/report_cards_data.json`

```json
{
  "meta": {
    "track": "schools",
    "branding": { "primaryColor": "#D4AF37", "backgroundColor": "#0A0A0A", "fontFamily": "Impact" },
    "audio": {}
  },
  "timeline": [
    { "start": 0,   "end": 6.5,  "text": "SHE MARKS FOR HOURS.",                  "animation": "shake",    "fontColor": "#D4AF37" },
    { "start": 6.5, "end": 13.5, "text": "ONE ERROR DELAYS EVERY REPORT CARD.",   "animation": "cascade",  "fontColor": "#D4AF37" },
    { "start": 13.5,"end": 16.0, "text": "UNTIL NOW.",                            "animation": "zoom",     "fontColor": "#D4AF37" },
    { "start": 16.0,"end": 21.0, "text": "SCORES CHECKED AUTOMATICALLY.",         "animation": "cascade",  "fontColor": "#D4AF37" },
    { "start": 21.0,"end": 25.5, "text": "REPORT CARDS IN MINUTES.",              "animation": "scaleUp",  "fontColor": "#D4AF37" },
    { "start": 25.5,"end": 30.0, "text": "Report cards in minutes. Not weeks.",   "animation": "scaleUp",  "fontColor": "#D4AF37", "cta": true, "brand": "FAKO ONLINE" }
  ]
}
```

> **Code note:** `FakoTemplate` (index.tsx) is 420 frames / 3 hard-coded scenes and paints
> an opaque background + audio — it cannot serve this content. A new composition
> **`ReportCardsTemplate`** is required at production time: 900 frames, transparent
> background (no `AbsoluteFill` fill), reads the 6-entry timeline, positions each entry by
> `start/end` seconds, renders the CTA brand line + tagline. Registered in
> `packages/remotion-core/src/index.tsx`.

---

## 4. Pipeline Commands

### Phase 2 — Assets (local, terminal only)

```powershell
# 3D libraries
polydown hdris    -f .\global_assets\hdris\    -c indoor -s 2k
polydown textures -f .\global_assets\textures\ -c wood -s 2k --maps Diffuse Rough
polydown textures -f .\global_assets\textures\ -c plaster -s 1k
polydown textures -f .\global_assets\textures\ -c fabric -s 1k

# Audio: download CC0 music x3 + SFX x19 per plan.md §G into
#   global_sfx\music\  and  global_sfx\sfx\
# (exact URLs chosen now; curl each file)

# Sync into the Kaggle worker before push
robocopy .\global_assets\ .\kaggle_worker\assets\ /MIR
robocopy .\global_sfx\   .\kaggle_worker\sfx\   /MIR
```

### Phase 3 — Blender render (Kaggle)

```powershell
cd .\kaggle_worker
kaggle kernels push -p .
kaggle kernels status YOUR_USERNAME/blender-render-engine
# ... wait for complete ...
kaggle kernels output YOUR_USERNAME/blender-render-engine -p ..\final_output\
Expand-Archive .\final_output\render_output.zip -DestinationPath .\final_output\frames\
```

**Orchestrator launch signature (what `cloud_orchestrator.py` runs):**

```bash
blender -b report_cards.blend -P render_scene.py -- \
  --assets /kaggle/working/assets \
  --out /kaggle/working/frames \
  --fps 30 --frames 900 \
  --engine CYCLES --samples 128 --device CUDA \
  -o /kaggle/working/frames/fako_#### -F PNG -s 1 -e 900 -a
```

Marker-bound cameras make `-a` produce all 8 shots in one pass.
Output: `fako_0001.png` … `fako_0900.png`.

### Phase 4 — Remotion text layer (local)

```powershell
# after ReportCardsTemplate exists
npx remotion render packages/remotion-core/src/index.tsx ReportCardsTemplate `
  remotion_overlays\text_seq `
  --props=plans\report-cards\report_cards_data.json `
  --image-format=png --sequence
```

Produces transparent PNGs for frames 0–899. **Verify first filename and numbering
(offset) before the overlay step.**

### Phase 5 — FFmpeg master (local)

```powershell
# 1) Blender frames -> base video
ffmpeg -framerate 30 -start_number 1 -i .\final_output\frames\fako_%04d.png `
       -c:v libx264 -pix_fmt yuv420p -r 30 .\final_output\base_3d.mp4

# 2) Sandwich the transparent text layer
ffmpeg -i .\final_output\base_3d.mp4 -framerate 30 -i .\remotion_overlays\text_seq\%04d.png `
       -filter_complex "[0:v][1:v]overlay=shortest=1[v]" -map "[v]" `
       -c:v libx264 -pix_fmt yuv420p .\final_output\combined.mp4

# 3) Bind music + SFX mix (per Section 2), encode final master
ffmpeg -i .\final_output\combined.mp4 `
  -i .\global_sfx\music\music-tension.mp3 `
  -i .\global_sfx\music\music-pivot.mp3 `
  -i .\global_sfx\music\music-uplift.mp3 `
  -i .\global_sfx\sfx\sfx-master.wav `
  -filter_complex "[1:a]volume=0.15[t];[2:a]volume=0.15[p];[3:a]volume=0.15[u];[t][p]acrossfade=d=0.1[mp];[mp][u]acrossfade=d=0.1[m];[m][4:a]amix=inputs=2[a]" `
  -map 0:v -map "[a]" `
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p `
  -c:a aac -b:a 192k -shortest `
  .\final_output\final_premium_commercial.mp4
```

> **Note:** SFX are pre-stitched into one `sfx-master.wav` (Section 2 table, placed at
> the given offsets on a 30s blank timeline) so the final mix stays one command.
> Build it with:
>
> ```powershell
> ffmpeg -f lavfi -i anullsrc=r=48000:cl=stereo -t 30 -i <each sfx> -filter_complex <adelay per cue> global_sfx\sfx\sfx-master.wav
> ```
>
> (exact `adelay` values = frames in Section 2; done with a small PowerShell/python helper at production time)

---

## 5. Frame-Accuracy Checklist (run before final mix)

- [ ] 8 shots sum to 900 frames (90+105+105+105+75+150+135+135 = 900)
- [ ] Every plan.md §G sound appears in Section 2, and every Section 2 cue exists in plan.md §G (no orphans, no gaps)
- [ ] All 6 overlay entries within 000–899; no two full-screen entries overlap
- [ ] No `voiceFile` anywhere — `meta.audio` empty; zero spoken content
- [ ] Music crossfades land on 405 (13.5s) and 477 (15.9s)
- [ ] Error buzz (f126) hits the hesitation frame; ding (f555) hits the red flash
- [ ] Palette flip complete by f479 (one frame before T3 ends)
- [ ] Remotion PNG sequence numbering matches FFmpeg `%04d` start
- [ ] Output: 1080x1920, 30fps, exactly 30.0s (900/30)
