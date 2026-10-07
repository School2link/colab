# Report Cards ("The Red Pen") - Production Plan

## Overview
- **Track:** schools
- **Duration:** 30s (900 frames @ 30fps)
- **Style:** 3d-scene (stylised 3D, no voice, no human actors)
- **Platform:** kaggle
- **Output:** 1080x1920 MP4, 30fps
- **Narrative type:** Pure animation — story carried by visuals, sound design, and text overlays only. **No voiceover of any kind.**
- **Companion file:** `script.md` (frame-accurate production script)

## Story (Locked)

**Logline:** A Ghanaian teacher drowning in exam marking watches her school switch to a
digital portal — errors vanish, report cards land on students' phones, and the school
stops burning money on printing.

**Message:** Hand marking costs time, accuracy, and money. A student portal delivers
correct report cards in minutes — students download them themselves.

**Emotion arc:** exhaustion → frustration → relief → joy → trust

**Hero object:** the **red pen** — it carries the whole argument. It marks errors, then
levitates and morphs into a gold checkmark (old way → new way).

### Story beats (narrative, timing locked in script.md)

| # | Time | Beat | Purpose |
|---|------|------|---------|
| 1 | 0.0–3.0 | The burden — teacher marks at 11pm, towers of booklets | Empathy |
| 2 | 3.0–6.5 | The error — 17 scribbled → 71; mistakes ripple across the pile | Show the flaw |
| 3 | 6.5–10.0 | The delay — clock spins, stack grows, report-card tray stays empty | Time cost |
| 4 | 10.0–13.5 | The cost — printing money flies away, parent+student wait | Money cost |
| 5 | 13.5–16.0 | The pivot — click; red pen morphs into gold check, palette flips to day | The turn |
| 6 | 16.0–21.0 | The fix — gradebook auto-checks, progress 100%, ledger hits GH₵ 0 | How it works |
| 7 | 21.0–25.5 | The payoff — student downloads card on phone; teacher at sunlit desk | Human result |
| 8 | 25.5–30.0 | Proof + CTA — icons snap into typographic end card | Brand |

**Why it works without voice:** ticking = time lost, buzz = error, whoosh = change,
chime = correctness; colour argues (dim amber → brand gold); one object transforms.

## Palette & Branding

| Element | Value |
|---------|-------|
| Problem-state palette | Dim amber / brown, night lamp light |
| Solution-state palette | Bright gold / white, daylight HDRI |
| Primary Color | `#D4AF37` |
| Background | `#0A0A0A` |
| Font (overlays) | Impact |
| End card | Text-only: "FAKO ONLINE" + tagline *"Report cards in minutes. Not weeks."* (no logo image) |

## Scene Breakdown (summary)

Eight beats = eight camera-marker shots inside one Blender file (`report_cards.blend`).
Full technical breakdown (cameras, lighting, frame ranges, SFX, overlays) lives in `script.md`.

### Beat 1 (0.0s - 3.0s)
- **Type:** 3d-scene — staff room at night
- **Action:** Teacher (T1 hunched) marks under a single bulb; wall clock past 11pm; booklet towers; school crest on wall; chalkboard reads "B.E.C.E MOCK - FORM 3"
- **Text Overlay:** "SHE MARKS FOR HOURS." — Animation: shake
- **Audio:** music-tension + clock tick + pen scratch + one sigh

### Beat 2 (3.0s - 6.5s)
- **Type:** 3d-scene — macro on exam page
- **Action:** Red ink writes 17, hesitates, scribbles over it → 71; ghost overlay of dozens of errors ripples across the pile
- **Text Overlay:** (continues from beat 1 — cleared at 6.5)
- **Audio:** pen scratch quickens + error buzz at 4.2s

### Beat 3 (6.5s - 10.0s)
- **Type:** 3d-scene — time-lapse, clock in frame
- **Action:** Clock hands spin; days flicker outside window; booklet stack grows; "REPORT CARDS" tray stays empty
- **Text Overlay:** "ONE ERROR DELAYS EVERY REPORT CARD." — Animation: cascade
- **Audio:** accelerating clock stutter + paper crumple + printer jam

### Beat 4 (10.0s - 13.5s)
- **Type:** 3d-scene — bursar's counter
- **Action:** Ledger tally "PRINTING: GH₵" climbs; money notes flutter away; reams and toner stacked; uniformed student + parent wait, check watch, disappointed
- **Text Overlay:** (continues — cleared at 13.5)
- **Audio:** coins clink + money whoosh + wordless murmur; music at heaviest

### Beat 5 (13.5s - 16.0s)
- **Type:** 3d-scene — THE PIVOT
- **Action:** Click. Red pen levitates, spins, morphs into glowing gold checkmark that flies into a tablet; desk/paper dissolve; palette shifts amber → gold/white daylight
- **Text Overlay:** "UNTIL NOW." — Animation: zoom
- **Audio:** single click + magic whoosh; music turns bright (music-pivot)

### Beat 6 (16.0s - 21.0s)
- **Type:** 3d-scene — digital void / UI
- **Action:** Scores stream into gradebook rows with green checks; an earlier wrong total is caught and corrected; progress bar "Generating report cards…" → 100%; printing ledger flips to GH₵ 0
- **Text Overlay:** "SCORES CHECKED AUTOMATICALLY." — Animation: cascade
- **Audio:** rhythmic UI clicks + correction ding + completion chime (music-uplift starts)

### Beat 7 (21.0s - 25.5s)
- **Type:** 3d-scene — courtyard, then staff room (cut)
- **Action:** Uniformed student taps phone → school portal → "Download Report Card" → card materialises (grades, comment, gold crest), she smiles; cut to teacher stretching at a tidy, sunlit desk, towers gone
- **Text Overlay:** "REPORT CARDS IN MINUTES." — Animation: scaleUp
- **Audio:** phone tap + download chime + short wordless giggle

### Beat 8 (25.5s - 30.0s)
- **Type:** 3d-scene → end card
- **Action:** Shrinking printer + fast clock + stack of green checks snap together; typography takes over: "FAKO ONLINE" + tagline types on
- **Text Overlay:** "Report cards in minutes. Not weeks." + FAKO ONLINE — Animation: scaleUp (CTA)
- **Audio:** logo sting; music resolves 28–30s

## Assets Required

Destination roots (per guide): 3D/visual → `global_assets/`, audio → `global_sfx/`.
`Source` values: **build** (create in Blender before render) · **download** (terminal command in Phase 2) · **text** (Remotion typography, no file).

### A. Characters (build — Blender, stylised)

| Asset | Type | Source | Path | Notes |
|-------|------|--------|------|-------|
| teacher.blend | character | build | global_assets/models/ | Ghanaian woman, dress in school colours; rig + 3 poses: **T1** hunched marking, **T2** head-in-hand, **T3** stretch-smile |
| student.blend | character | build | global_assets/models/ | Uniformed girl with phone; poses: **S1** waiting/impatient, **S2** smiling at screen |
| parent.blend | character | build | global_assets/models/ | At counter, background, static (**P1** disappointed) |

### B. Sets (build — Blender)

| Asset | Type | Source | Path | Notes |
|-------|------|--------|------|-------|
| set-staffroom.blend | set | build | global_assets/models/ | Night staff room: desk, chair, bulb lamp, window (day-flicker emissive), shelves, chalkboard, crest |
| set-office.blend | set | build | global_assets/models/ | Bursar counter: printer, paper reams, toner boxes, ledger, counter |
| set-courtyard.blend | set | build | global_assets/models/ | Bench, school wall, tree shade (day) |
| set-digital-void.blend | set | build | global_assets/models/ | Bright gold/white backdrop for beats 5, 6, 8 |

### C. Hero props (build — Blender)

| Asset | Type | Source | Path | Notes |
|-------|------|--------|------|-------|
| booklet-stack.blend | prop | build | global_assets/models/ | Exam booklets; **grows** over time (beat 3) |
| red-pen.blend | prop | build | global_assets/models/ | **Hero object** beat 1–2 |
| checkmark-gold.blend | prop | build | global_assets/models/ | Morph target of red pen (beat 5) |
| wall-clock.blend | prop | build | global_assets/models/ | Animated hands (beats 1, 3) |
| report-tray.blend | prop | build | global_assets/models/ | Tray labelled REPORT CARDS — stays empty (beat 3) |
| money-notes.blend | prop | build | global_assets/models/ | Notes + coins that flutter away (beat 4) |
| tablet.blend | prop | build | global_assets/models/ | Receives the checkmark (beat 5) |
| phone.blend | prop | build | global_assets/models/ | Student's phone (beat 7) |
| school-crest.png | texture | build | global_assets/ | Simple gold emblem; wall + report card + end card |

### D. UI screens (build — Blender textured planes, your choice)

| Asset | Type | Source | Path | Notes |
|-------|------|--------|------|-------|
| ui-gradebook.png | texture | build | global_assets/ | Gradebook rows; green-check fill + auto-correct highlight (beat 6) |
| ui-progress.png | texture | build | global_assets/ | "Generating report cards…" bar → 100% (beat 6) |
| ui-ledger.png | texture | build | global_assets/ | "PRINTING: GH₵ ___" climbing → **GH₵ 0** (beats 4, 6) |
| ui-portal.png | texture | build | global_assets/ | Phone portal: login → "Download Report Card" (beat 7) |
| ui-reportcard.png | texture | build | global_assets/ | Grades + teacher comment + gold crest (beat 7) |

### E. Downloads — Poly Haven via `polydown` → `global_assets/`

| Asset | Type | Source | Command |
|-------|------|--------|---------|
| hdri-night.exr | hdri | download | `polydown hdris -f .\global_assets\hdris\ -c indoor -s 2k` (pick warm/night) |
| hdri-day.exr | hdri | download | `polydown hdris -f .\global_assets\hdris\ -c indoor -s 2k` (pick bright/day) |
| wood-pbr.zip | texture | download | `polydown textures -f .\global_assets\textures\ -c wood -s 2k --maps Diffuse Rough` |
| plaster-pbr.zip | texture | download | `polydown textures -f .\global_assets\textures\ -c plaster -s 1k` |
| fabric-pbr.zip | texture | download | `polydown textures -f .\global_assets\textures\ -c fabric -s 1k` |

### F. End card (text — Remotion)

| Asset | Type | Source | Notes |
|-------|------|--------|-------|
| "FAKO ONLINE" + tagline | text | text | No image logo. Tagline: *"Report cards in minutes. Not weeks."* |

### G. Sound — CC0 downloads → `global_sfx/` (no voice, carries half the story)

**Music (3 stems):**

| Asset | Type | Source | Path | Notes |
|-------|------|--------|------|-------|
| music-tension.mp3 | music | download | global_sfx/music/ | 0.0–13.5s low strings/drone, weariest at 10–13.5 |
| music-pivot.mp3 | music | download | global_sfx/music/ | 13.5–16.0s rising turn into bright |
| music-uplift.mp3 | music | download | global_sfx/music/ | 16.0–30.0s warm plucks/pads, resolves ~27.5, final chord 28–30 |

**SFX (all wordless):**

| Asset | Type | Source | Path | Used at |
|-------|------|--------|------|---------|
| sfx-clock-tick.wav | sfx | download | global_sfx/sfx/ | 0.0–6.5 steady tick (loop) |
| sfx-pen-scratch.wav | sfx | download | global_sfx/sfx/ | 0.3–6.5, quickens after 3.0 |
| sfx-sigh.wav | sfx | download | global_sfx/sfx/ | 2.8 breathy exhale |
| sfx-error-buzz.wav | sfx | download | global_sfx/sfx/ | 4.2 wrong-score moment |
| sfx-clock-fast.wav | sfx | download | global_sfx/sfx/ | 6.5–10.0 accelerating stutter |
| sfx-paper-crumple.wav | sfx | download | global_sfx/sfx/ | 8.5 booklet dropped |
| sfx-printer-jam.wav | sfx | download | global_sfx/sfx/ | 9.0 jam + crunch |
| sfx-coins-clink.wav | sfx | download | global_sfx/sfx/ | 10.4 coins |
| sfx-money-whoosh.wav | sfx | download | global_sfx/sfx/ | 11.5 money flying away |
| sfx-murmur.wav | sfx | download | global_sfx/sfx/ | 12.6 disappointed "hmm" |
| sfx-click.wav | sfx | download | global_sfx/sfx/ | 13.6 pivot click |
| sfx-magic-whoosh.wav | sfx | download | global_sfx/sfx/ | 14.0 pen → checkmark |
| sfx-ui-clicks.wav | sfx | download | global_sfx/sfx/ | 16.0–21.0 rhythmic UI |
| sfx-ding.wav | sfx | download | global_sfx/sfx/ | 18.5 wrong total corrected |
| sfx-chime.wav | sfx | download | global_sfx/sfx/ | 20.8 progress 100% |
| sfx-phone-tap.wav | sfx | download | global_sfx/sfx/ | 21.5 screen tap |
| sfx-download-chime.wav | sfx | download | global_sfx/sfx/ | 23.0 card materialises |
| sfx-giggle.wav | sfx | download | global_sfx/sfx/ | 24.5 short "heh" |
| sfx-logo-sting.wav | sfx | download | global_sfx/sfx/ | 26.0 end card hit |

**Audio rules:** music bed volume 0.15, SFX 1.0; CC0/royalty-free sources only
(Pixabay, Freesound CC0); exact URLs chosen at download time in Phase 2.

## Pipeline (reference)

| Phase | What | Where |
|-------|------|-------|
| 1 | This plan + folder structure | local (done) |
| 2 | Download HDRI/textures/audio per manifest | local (`polydown`, terminal) |
| 3 | Build Blender assets/scene; render 900 frames | Kaggle (`blender-render-engine` kernel) |
| 4 | Text overlay layer | local Remotion (`ReportCardsTemplate`, 900f transparent PNG seq) |
| 5 | Frames + text + audio → final MP4 | local FFmpeg |

**Hard order:** assets → 900 frames → text layer → mix.

## Open Items

- [ ] Exact CC0 URLs for music/SFX (picked during Phase 2 download)
- [ ] Final HDRI selections from the `polydown` pull
- [ ] Tagline confirmed: *"Report cards in minutes. Not weeks."*
