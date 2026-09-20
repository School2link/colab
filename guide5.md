# Fako Online Content Engine - Master Guide

> **Purpose:** This guide explains how to create content plans and use the engine to produce videos.
> **Every new piece of content starts with a plan file.**

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
- **Style:** talking-head | image-scenes | mixed | drama
- **Platform:** kaggle
- **Output:** 1080x1920 MP4, 30fps

## Assets Required
| Asset | Type | Source | Generation Method | Notes |
|-------|------|--------|-------------------|-------|
| hero-image.png | image | provided or generate | SD 1.5 via Kaggle | Front-facing portrait for avatar |
| voiceover.wav | audio | generate | Bark TTS via Kaggle | Emotional script below |
| scene2.png | image | provided or generate | SD 1.5 via Kaggle | Dashboard screenshot |
| style-clip.mp4 | video | generate | AnimateDiff via Kaggle | Styled scene loop |

## Scene Breakdown

### Scene 1 (0.0s - 4.0s)
- **Type:** talking-head
- **Image:** hero-image.png
- **Audio:** Bark TTS with text below
- **Script:** "MAN: [gasps] Wait... ARE YOU SERIOUS?! [laughs] We did it!"
- **Voice Preset:** v2/en_speaker_6
- **Text Overlay:** "YOUR BUSINESS DESERVES TO BE ONLINE."
- **Animation:** zoom-in
- **Background:** dark gradient

### Scene 2 (4.0s - 9.0s)
- **Type:** image-scene
- **Image:** scene2.png
- **Text Overlay:** "PRODUCTS. CHECKOUT. MOBILE MONEY."
- **Ken Burns:** pan-right
- **Animation:** cascade text

### Scene 3 (9.0s - 14.0s)
- **Type:** broll
- **Prompt:** "modern e-commerce dashboard on laptop, warm lighting"
- **Duration:** 5s
- **Text Overlay:** "SIGN UP FREE AT FAKO ONLINE.COM"
- **Animation:** zoom text
- **CTA:** true

## Audio
- **Voiceover:** Generated via Bark TTS (see Scene 1 script)
- **Background Music:** None | [file path]
- **Music Volume:** 0.15

## Branding
- **Primary Color:** #D4AF37
- **Background:** #0A0A0A
- **Font:** Impact
```

### Plan Rules

1. Every scene must specify: type, duration, image/audio/video source, text overlay
2. For talking-head scenes: include the full script with emotional tags
3. For B-Roll scenes: include the text prompt for Wan 2.1
4. For styled scenes: include the style prompt for AnimateDiff
5. Timestamps must be explicit (start - end in seconds)
6. Text overlays must include animation type (zoom, cascade, shake, etc.)
7. Assets can be "provided" (user supplies file) or "generate" (Kaggle produces it)
8. If source is "generate", include the generation prompt/method in the plan
9. Platform field determines which notebooks and storage to use:
   - `kaggle`: Use Kaggle notebooks + Kaggle Dataset storage

---

## 2. Generating Assets

All AI models run on Kaggle (T4 GPU). Plans can specify that assets be generated rather than provided.

| Asset Type            | Model        | API Endpoint     | Input          | Output |
| --------------------- | ------------ | ---------------- | -------------- | ------ |
| Portrait/Avatar image | SD 1.5       | /generate-image  | Text prompt    | .png   |
| Scene background      | SD 1.5       | /generate-image  | Text prompt    | .png   |
| Emotional voiceover   | Bark TTS     | /generate-tts    | Text with tags | .wav   |
| Talking head video    | SadTalker    | /generate-avatar | Image + audio  | .mp4   |
| Refined lip sync      | Easy-Wav2Lip | /generate-full   | Video + audio  | .mp4   |
| Lip sync (diffusion)  | LatentSync   | /generate-lipsync | Video + audio | .mp4  |
| B-Roll clip           | Wan 2.1      | /generate-broll  | Text prompt    | .mp4   |
| Styled scene          | AnimateDiff  | /generate-styled | Image + prompt | .mp4   |

### Example: Generating an Avatar Image

```markdown
### Scene 1 (0.0s - 4.0s)
- **Type:** talking-head
- **Image:** generate
- **Image Prompt:** "professional African business owner, male, 30s, confident smile, clean background, studio portrait, 4K"
- **Image Model:** SD 1.5
- **Audio:** generate
- **Script:** "MAN: [gasps] Wait... ARE YOU SERIOUS?! [laughs] We did it!"
- **Voice Preset:** v2/en_speaker_6
```

### Example: Generating a B-Roll Clip

```markdown
### Scene 3 (9.0s - 14.0s)
- **Type:** broll
- **Prompt:** "modern African shop with mobile money payments, customers smiling, warm lighting, slow camera pan"
- **Duration:** 5s
- **Model:** Wan 2.1
- **Text Overlay:** "SIGN UP FREE AT FAKO ONLINE.COM"
```

### Example: Generating a Styled Scene

```markdown
### Scene 2 (4.0s - 9.0s)
- **Type:** styled
- **Image:** generate
- **Image Prompt:** "African entrepreneur in modern office, digital art style, warm tones"
- **Style Prompt:** "same person, anime style, dynamic lighting, flowing clothes"
- **Model:** AnimateDiff + ControlNet
- **Duration:** 5s
- **Text Overlay:** "YOUR BUSINESS DESERVES TO BE ONLINE."
```

### Content Types

| Type         | Description                           | Tools Used                      |
| ------------ | ------------------------------------- | ------------------------------- |
| talking-head | Photo animated with AI voice          | Bark + SadTalker + Easy-Wav2Lip |
| image-scene  | Static image with Ken Burns effect    | Remotion only                   |
| broll        | AI-generated background video         | Wan 2.1                         |
| styled       | Consistent character in new style     | AnimateDiff + ControlNet        |
| drama        | Multiple characters, scenes, dialogue | All tools combined              |

### AI Models

| Model                    | Purpose                | Input                      | Output     |
| ------------------------ | ---------------------- | -------------------------- | ---------- |
| Bark (Suno)              | Emotional TTS          | Text with [laughs] [gasps] | .wav audio |
| SadTalker                | Talking head animation | Photo + audio              | .mp4 video |
| Easy-Wav2Lip             | Lip sync (GAN)         | Video + audio              | .mp4 video |
| LatentSync               | Lip sync (diffusion)   | Video + audio              | .mp4 video |
| Wan 2.1 (1.3B)           | B-Roll generation      | Text prompt                | .mp4 video |
| AnimateDiff + ControlNet | Style consistency      | Image + text prompt        | .mp4 video |

### Bark Emotional Tags

| Effect     | Syntax     | Example                    |
| ---------- | ---------- | -------------------------- |
| Laughter   | [laughs]   | "We did it! [laughs]"      |
| Gasping    | [gasps]    | "[gasps] Wait..."          |
| Sighing    | [sighs]    | "[sighs] I do not know..." |
| Hesitation | ... or uh, | "Well... I mean..."        |
| Shouting   | ALL CAPS!  | "STOP! DO NOT DO THAT!"    |
| Whispering | lowercase  | soft breathy delivery      |

Voice Presets: v2/en_speaker_0 through v2/en_speaker_9

---

## 2.5 Available Tools Reference

This section is the **complete tool catalog** for plan authors. Every tool available in the engine, what it does, and when to use it.

### A. AI Generation Tools (Kaggle GPU)

All AI inference runs remotely on Kaggle GPU notebooks, exposed to the local machine via ngrok URLs.

| Tool | Scene Type | Input | Output | When to Use | Server Port |
| ---- | ---------- | ----- | ------ | ----------- | ----------- |
| Bark TTS | Any scene needing speech | Text with emotional tags + voice preset | .wav audio | Voiceover for talking-head, narration, dialogue | 8000 |
| SadTalker | Talking head | Photo + audio | .mp4 video | Animate a static portrait with voice | 8000 |
| Easy-Wav2Lip | Talking head refinement | Video + audio | .mp4 video | Fix/improve lip sync after SadTalker | 8000 |
| LatentSync | Lip sync (diffusion) | Video + audio | .mp4 video | Higher quality lip sync alternative (server not yet built) | N/A |
| SD 1.5 | Image generation | Text prompt | .png image | Generate portraits, backgrounds, UI mockups, scene images | 8002 |
| Wan 2.1 (1.3B) | B-Roll video | Text prompt | .mp4 video | Generate background video clips, product showcases | 8001 |
| AnimateDiff + ControlNet | Styled animation | Image + text prompt | .mp4 video | Animate a static image in a new art style | 8002 |

### B. Tool Decision Tree

Use this flowchart when writing a plan to decide which tool to use for each scene:

```
What does this scene need?
│
├── Speech/Voiceover
│   └── Bark TTS → generates .wav
│       Voice presets: v2/en_speaker_0 through v2/en_speaker_9
│       Emotional tags: [laughs], [gasps], [sighs], ALL CAPS, lowercase
│
├── Animated portrait (photo moves and speaks)
│   ├── SadTalker → generates initial .mp4 from photo + audio
│   └── Easy-Wav2Lip → refines lip sync (recommended for quality)
│   └── OR LatentSync → alternative lip sync (higher quality, more VRAM)
│
├── Static image (portrait, background, UI mockup)
│   ├── Provided by user → reference in plan as "provided: path/to/image"
│   └── Generate → SD 1.5 text-to-image on port 8002
│       Include prompt in plan: "Image Prompt: ..."
│
├── Background video (B-Roll)
│   └── Wan 2.1 text-to-video on port 8001
│       Include prompt in plan: "Prompt: ..."
│       Specify duration in seconds
│
├── Animated styled scene (character in new art style)
│   └── AnimateDiff + ControlNet on port 8002
│       Requires source image + style prompt
│
└── Text overlay only (no AI needed)
    └── Remotion handles this directly
        Specify animation type: zoom, shake, cascade, scaleUp
```

### C. Remotion Composition Tools (Local)

These components run locally on your PC during video rendering. No GPU needed.

| Component | What It Does | Animation Options | Plan Field |
| --------- | ------------ | ----------------- |------------|
| KenBurnsImage | Animated image movement | `zoom-in`, `zoom-out`, `pan-right`, `pan-left` | `Animation: zoom-in` |
| AnimatedText | Word-by-word spring animation | `zoom`, `shake`, `cascade`, `scaleUp` | `Animation: cascade` |
| DarkScrim | Gradient overlay | `full` (full screen), `bottom` (lower third) | `Background: dark gradient` |
| ImageScene | Static image + Ken Burns + text overlay | All KenBurns + AnimatedText options | `Type: image-scene` |
| TalkingScene | Video (OffthreadVideo) or image with breathing + text | All KenBurns + AnimatedText options | `Type: talking-head` |
| FakoContentTemplate | Main composition (3 scenes) | `fade`, `slide` transitions between scenes | Handled automatically |

#### Animation Types in Detail

| Animation | Behavior | Best For |
|-----------|----------|----------|
| `zoom-in` | Slowly zoom into center of image | Hero shots, emphasis, drama |
| `zoom-out` | Slowly zoom out from center | Reveals, establishing shots |
| `pan-right` | Slowly pan right across image | Landscape, product showcase |
| `pan-left` | Slowly pan left across image | Reverse pan, reading direction |
| `shake` | Quick shake/vibration | Excitement, urgency, impact |
| `scaleUp` | Scale up from small to full size | Text emphasis, call-to-action |
| `cascade` | Words appear one by one with spring | Lists, bullet points, multiple messages |
| `zoom` (text) | Text zooms in from center | Headlines, big statements |

### D. Local CLI Scripts

Scripts that run on your local PC (no GPU needed):

| Script | Command | Use Case |
| ------ | ------- | -------- |
| `generate-talking-head.js` | `--prompt "..." --api URL` | Generate avatar image from text via SD 1.5 |
| `generate-talking-head.js` | `--image X --text "..." --api URL` | Full pipeline: Bark TTS + SadTalker + Easy-Wav2Lip |
| `generate-talking-head.js` | `--image X --audio Y --api URL` | Talking head from pre-existing audio |
| `generate-talking-head.js` | `--check --api URL` | Health check against running server |
| `generate-avatar.js` | `--image X --audio Y` | Talking head via Gradio Space (fallback) |

### E. Track System

Each content track is a directory with standardized structure:

| Track | Directory | Render Command |
| ----- | --------- | -------------- |
| ecommerce | `tracks/ecommerce/` | `npm run render:ecommerce` |
| businesses | `tracks/businesses/` | `npm run render:businesses` |
| schools | `tracks/schools/` | `npm run render:schools` |
| churches | `tracks/churches/` | `npm run render:churches` |
| promo | `tracks/promo-business/` | `npm run render:promo` |

#### Asset Conventions per Track

```
tracks/[track]/
  assets/          → Static images (screenshots, UI mockups, portraits)
  voiceovers/      → Pre-generated .wav audio files
  music/           → Background music files (.mp3, .wav)
  data/
    fako_video_data.json  → Timeline data (scenes, timing, branding)
  out/
    video.mp4      → Final rendered output
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

### F. Complete API Endpoints

When Kaggle notebooks are running and exposed via ngrok:

#### Full Pipeline Server (port 8000)

| Endpoint | Method | Parameters | Returns |
| -------- | ------ | ---------- | ------- |
| `/health` | GET | none | `{"status": "ok", "models": ["bark", "sadtalker", "wav2lip"]}` |
| `/generate-tts` | POST | `text` (form), `voice_preset` (form, default `v2/en_speaker_6`) | .wav audio file |
| `/generate-avatar` | POST | `image` (file upload), `audio` (file upload) | .mp4 video file |
| `/generate-full` | POST | `image` (file), `text` (form), `voice_preset` (form), `refine_lips` (form, bool) | .mp4 video file |

#### B-Roll Server (port 8001)

| Endpoint | Method | Parameters | Returns |
| -------- | ------ | ---------- | ------- |
| `/health` | GET | none | `{"status": "ok", "model": "wan-2.1-1.3b"}` |
| `/generate-broll` | POST | `text_prompt` (form), `duration` (form, int, default 5) | .mp4 video file |

#### Styled Scene Server (port 8002)

| Endpoint | Method | Parameters | Returns |
| -------- | ------ | ---------- | ------- |
| `/health` | GET | none | `{"status": "ok", "models": ["animatediff", "controlnet", "sd1.5"]}` |
| `/generate-image` | POST | `text_prompt` (form), `width` (form, default 512), `height` (form, default 512) | .png image file |
| `/generate-styled` | POST | `image` (file), `text_prompt` (form), `style_prompt` (form), `duration` (form, int) | .mp4 video file |

### G. How to Choose: Quick Reference

| I need to... | Use this tool | Port | Example plan entry |
| ------------ | ------------- | ---- | ------------------ |
| Generate a voiceover | Bark TTS | 8000 | `Audio: generate via Bark, text: "...", preset: v2/en_speaker_6` |
| Animate a photo with voice | SadTalker + Easy-Wav2Lip | 8000 | `Type: talking-head, Image: generate via SD 1.5, Audio: generate via Bark` |
| Generate a portrait/avatar | SD 1.5 | 8002 | `Image: generate, Image Prompt: "professional African business owner..."` |
| Generate a background image | SD 1.5 | 8002 | `Image: generate, Image Prompt: "modern e-commerce dashboard..."` |
| Generate a B-Roll clip | Wan 2.1 | 8001 | `Type: broll, Prompt: "modern shop with mobile money..."` |
| Animate an image in a style | AnimateDiff | 8002 | `Type: styled, Style Prompt: "anime style, dynamic lighting..."` |
| Add text overlay | Remotion | local | `Text Overlay: "SIGN UP FREE", Animation: cascade` |
| Add Ken Burns effect | Remotion | local | `Animation: zoom-in, Background: dark gradient` |

---

## 3. Storage Layout

All models are stored in separate Kaggle Datasets (one per model) to stay within the 19.5GB working directory limit.

### Kaggle Datasets

| Dataset Name                | Model           | Size     | URL                                                              |
| --------------------------- | --------------- | -------- | ---------------------------------------------------------------- |
| kingtechie/wan21-model      | Wan 2.1 1.3B    | ~18 GB   | https://www.kaggle.com/datasets/kingtechie/wan21-model           |
| kingtechie/animatediff-model | AnimateDiff    | ~3.5 GB  | https://www.kaggle.com/datasets/kingtechie/animatediff-model     |
| kingtechie/sd15-model       | SD 1.5          | ~3.2 GB  | https://www.kaggle.com/datasets/kingtechie/sd15-model            |
| kingtechie/bark-model       | Bark TTS        | ~4 GB    | https://www.kaggle.com/datasets/kingtechie/bark-model            |
| kingtechie/sadtalker-model  | SadTalker       | ~2.5 GB  | https://www.kaggle.com/datasets/kingtechie/sadtalker-model       |
| kingtechie/wav2lip-model    | Easy-Wav2Lip    | ~1.5 GB  | https://www.kaggle.com/datasets/kingtechie/wav2lip-model         |
| kingtechie/latentsync-model | LatentSync      | ~8 GB    | https://www.kaggle.com/datasets/kingtechie/latentsync-model      |

### Kaggle Session Paths

Each dataset mounts to `/kaggle/input/[dataset-name]`:

| Model           | Mount Path                              |
| --------------- | --------------------------------------- |
| Wan 2.1         | `/kaggle/input/wan21-model`             |
| AnimateDiff     | `/kaggle/input/animatediff-model`       |
| SD 1.5          | `/kaggle/input/sd15-model`              |
| Bark TTS        | `/kaggle/input/bark-model`              |
| SadTalker       | `/kaggle/input/sadtalker-model`         |
| Easy-Wav2Lip    | `/kaggle/input/wav2lip-model`           |
| LatentSync      | `/kaggle/input/latentsync-model`        |

### Downloading Models

**IMPORTANT: Never download model files to your local PC.**

Instead, let Kaggle download directly over its high-speed connections (~100+ MB/s).

#### Individual Download Notebooks

Each model has its own download notebook in `colab/`:

| Notebook                  | Downloads To                          | Target Dataset             |
| ------------------------- | ------------------------------------- | -------------------------- |
| download-wan21.ipynb      | Wan 2.1 (18GB)                        | kingtechie/wan21-model     |
| download-animatediff.ipynb | AnimateDiff (~3.5GB)                 | kingtechie/animatediff-model |
| download-sd15.ipynb       | SD 1.5 (~3.2GB)                       | kingtechie/sd15-model      |
| download-bark.ipynb       | Bark TTS core files (~4GB)            | kingtechie/bark-model      |
| download-sadtalker.ipynb  | SadTalker checkpoints (~2.5GB)        | kingtechie/sadtalker-model |
| download-wav2lip.ipynb    | Easy-Wav2Lip (~1.5GB)                 | kingtechie/wav2lip-model   |
| download-latentsync.ipynb | LatentSync (~8GB)                     | kingtechie/latentsync-model |

#### Kaggle Session Init Code

```python
import os

WORKING_DIR = "/kaggle/working/outputs"
os.makedirs(WORKING_DIR, exist_ok=True)

BARK_DIR = "/kaggle/input/bark-model"
SADTALKER_DIR = "/kaggle/input/sadtalker-model"
WAV2LIP_DIR = "/kaggle/input/wav2lip-model"
LATENTSYNC_DIR = "/kaggle/input/latentsync-model"
WAN_MODEL_DIR = "/kaggle/input/wan21-model"
SD15_DIR = "/kaggle/input/sd15-model"
ANIMEDIFF_DIR = "/kaggle/input/animatediff-model"

print("All models mounted from individual datasets!")
```

#### Summary

- **Local PC:** Only stores lightweight code (`.ipynb` notebooks and `.py` scripts)
- **Kaggle:** Downloads and holds all heavy multi-gigabyte models directly through the cloud
- **Your home internet:** Never touched for model downloads

---

## 4. Adding New Models to Kaggle

This is the repeatable process for adding any new AI model to the engine.

### Step-by-Step

#### 1. Decide the model details

| Question | Example Answer |
|----------|---------------|
| Model name | `FLUX.1-schnell` |
| HuggingFace repo | `black-forest-labs/FLUX.1-schnell` |
| Files needed | `*.safetensors`, `config.json`, etc. |
| Estimated size | ~12GB |
| Kaggle dataset name | `kingtechie/flux-model` |
| Dataset slug | `flux-model` |

**Key rule:** Each model gets its own dataset. Never combine models into one dataset (the 19.5GB working directory limit makes combined downloads fail).

#### 2. Create the download notebook

Run from the project root:

```bash
python scripts/create_notebooks.py
```

Or manually create `colab/download-[name].ipynb` with this pattern:

```python
import os
import shutil
from huggingface_hub import hf_hub_download

MODEL_DIR = "/kaggle/working/[dataset-slug]"
os.makedirs(MODEL_DIR, exist_ok=True)

print("=== Downloading [Model Name] ===")
# From [huggingface/repo-id]
for file_name in ["file1.safetensors", "file2.bin", "config.json"]:
    print(f"Downloading {file_name}...")
    try:
        hf_hub_download(
            repo_id="[huggingface/repo-id]",
            filename=file_name,
            local_dir=MODEL_DIR
        )
        print("  OK")
    except Exception as e:
        print(f"  Error: {e}")
    # CRITICAL: Clean HF cache after EACH file to stay under 19.5GB
    cache_dir = os.path.expanduser('~/.cache/huggingface')
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)

# Verify
total_size = 0
file_count = 0
for dirpath, dirnames, filenames in os.walk(MODEL_DIR):
    for f in filenames:
        fp = os.path.join(dirpath, f)
        total_size += os.path.getsize(fp)
        file_count += 1
print(f"Done! Files: {file_count}, Size: {total_size / 1024**3:.2f} GB")
```

**Critical lessons learned:**
- Use `hf_hub_download` (NOT `snapshot_download`) — `snapshot_download` caches everything before copying, always fails
- Clean `~/.cache/huggingface` after EACH file — the cache lives on the same 19.5GB volume
- Never use `cache_dir="/tmp/hf_cache"` — `/tmp` is on the same volume
- For Bark-style models with near-duplicate files (e.g. `text_2.pt` vs `text_0.pt`), only download the core files

#### 3. Add upload cell

Add a second code cell to auto-publish:

**Option A: For models under ~5GB (uses kagglehub):**

```python
import kagglehub

DATASET_ID = "kingtechie/[dataset-slug]"

print(f"\n=== Publishing as dataset: {DATASET_ID} ===")
kagglehub.dataset_upload(
    DATASET_ID,
    MODEL_DIR,
    version_notes="Initial download - [Model Name]"
)
print(f"Published: https://www.kaggle.com/datasets/{DATASET_ID}")
```

**Option B: For models over ~5GB (avoids Kaggle backend creation bug):**

First, create the empty dataset shell in the Kaggle UI (+ New Dataset → title → Create). Then use:

```python
import os

# Push model files as a new version to the existing dataset
!kaggle datasets version -p {MODEL_DIR} -m "Initial download - [Model Name]" --dir-mode zip
```

#### 4. Push to Kaggle

```powershell
# Copy notebook to kaggle-push/
Copy-Item colab/download-[name].ipynb kaggle-push/

# Update kernel-metadata.json
# Set id, title, code_file

# Push
kaggle kernels push -p ./kaggle-push
```

Monitor until `COMPLETE`:
```powershell
while ($true) {
    $r = kaggle kernels status kingtechie/fako-online-download-[name] 2>&1
    Write-Output "$(Get-Date -Format 'HH:mm:ss') - $r"
    if ($r -match "complete" -or $r -match "error") { break }
    Start-Sleep -Seconds 60
}
```

#### 5. Update this guide

Add the new model to these tables in this file:
- **Kaggle Datasets** (Section 3)
- **Kaggle Session Paths** (Section 3)
- **Individual Download Notebooks** (Section 3)

#### 6. Update production notebooks (if needed)

If a production notebook uses the new model, update its Cell 1 paths:

```python
NEW_MODEL_DIR = "/kaggle/input/[dataset-slug]"
```

And update the markdown instructions to list the new dataset in "Add datasets".

#### 7. Update download scripts

Add the model to `scripts/create_notebooks.py` and `scripts/update_colab_notebooks.py`.

#### 8. Commit and push

```bash
git add -A
git commit -m "Add [Model Name] to Kaggle"
git push
```

### Troubleshooting New Model Downloads

| Error | Cause | Fix |
|-------|-------|-----|
| `No space left on device` | HF cache filling 19.5GB volume | Clean cache after each file |
| `BackendError: Please upload at least one file` | Upload ran before downloads finished | Check cell execution order |
| `403 Forbidden` on upload | Dataset doesn't exist yet or permissions | Create dataset first, or check API token |
| `snapshot_download` fails | Caches all files before copying | Use `hf_hub_download` instead |
| Download is a near-duplicate | e.g. `text_0.pt` vs `text_2.pt` | Only download the core files needed |

---

## 5. Multi-Account Setup

Kaggle limits GPU usage to ~30 hours/week per account. For higher throughput, use a **primary + backup** account strategy.

### Strategy

| Account    | Role     | Dataset Ownership | Usage                                    |
| ---------- | -------- | ----------------- | ---------------------------------------- |
| Account A  | Primary  | Owner             | Day-to-day generation, all notebooks     |
| Account B  | Backup   | Collaborator      | Overflow when A hits weekly quota limit  |

### Sharing the Datasets Across Accounts

All 6 individual datasets must be accessible to both accounts.

1. **Account A** creates the datasets and uploads all models
2. Account A goes to each dataset's **Settings** → **Collaborators** → adds Account B's Kaggle username
3. **Account B** can now attach the same datasets in any notebook via **Add Data** → search for `kingtechie/[dataset-name]`

**Important:** The dataset owner (Account A) must explicitly grant collaborator access. Shared datasets are read-only for collaborators.

### Switching Between Accounts

When Account A hits the ~30 hr/week GPU quota:

1. Log out of Kaggle
2. Log in with Account B credentials
3. Open the same notebook (or re-upload if using a different account)
4. Attach all needed datasets via Add Data
5. The datasets are identical — no re-downloading needed

### Tips

- Keep both accounts verified with phone numbers (unverified accounts get lower quotas)
- Monitor usage at `kaggle.com/settings` → **Usage** tab
- Space out heavy workloads across accounts to maximize weekly GPU hours
- Both accounts can run different notebooks simultaneously for parallel generation

---

## 6. Project Structure

```
LocalContents/
  guide5.md                          # This file
  .env                               # KAGGLE_API_URL setting
  plans/                             # Content plans (one per video)
    [content-name]-plan.md
  packages/remotion-core/src/
    Composition.tsx                  # Main video template
    kaggle-api.ts                    # API client for Kaggle
  tracks/
    ecommerce/data/fako_video_data.json
    businesses/data/fako_video_data.json
    schools/data/fako_video_data.json
    churches/data/fako_video_data.json
    promo-business/data/fako_video_data.json
  public/
    assets/                          # Static files for staticFile()
    voiceovers/                      # Pre-generated audio
  scripts/
    generate-talking-head.js         # CLI for Kaggle API
    create_notebooks.py              # Generates download notebooks
    update_colab_notebooks.py        # Updates download notebooks
    update_production_notebooks.py   # Updates server notebooks
    kaggle-download-models.ps1       # Orchestration script
  colab/
    full-pipeline-server-kaggle.ipynb  # Bark + SadTalker + Easy-Wav2Lip (port 8000)
    broll-server-kaggle.ipynb          # Wan 2.1 B-Roll (port 8001)
    styled-scene-server-kaggle.ipynb   # AnimateDiff + ControlNet (port 8002)
    download-wan21.ipynb               # Downloads Wan 2.1 → kingtechie/wan21-model
    download-animatediff.ipynb         # Downloads AnimateDiff → kingtechie/animatediff-model
    download-sd15.ipynb                # Downloads SD 1.5 → kingtechie/sd15-model
    download-bark.ipynb                # Downloads Bark TTS → kingtechie/bark-model
    download-sadtalker.ipynb           # Downloads SadTalker → kingtechie/sadtalker-model
    download-wav2lip.ipynb             # Downloads Easy-Wav2Lip → kingtechie/wav2lip-model
    download-latentsync.ipynb          # Downloads LatentSync → kingtechie/latentsync-model
  kaggle-push/                        # Working dir for Kaggle kernel pushes
    kernel-metadata.json
```

---

## 7. API Endpoints

| Endpoint         | Method | Input                                  | Output               |
| ---------------- | ------ | -------------------------------------- | -------------------- |
| /health          | GET    | -                                      | status               |
| /generate-image  | POST   | text_prompt, style                     | portrait.png         |
| /generate-tts    | POST   | text, voice_preset                     | emotional_speech.wav |
| /generate-avatar | POST   | image, audio                           | talking-head.mp4     |
| /generate-full   | POST   | image, text, voice_preset, refine_lips | talking-head.mp4     |
| /generate-broll  | POST   | text_prompt, duration                  | broll-clip.mp4       |
| /generate-styled | POST   | image, text_prompt, style              | styled-scene.mp4     |

---

## 8. Workflow

### Creating New Content

1. Copy the plan template above
2. Fill in all scenes with explicit timestamps, sources, and text
3. **Use the Tool Decision Tree (Section 2.5B) to choose the right tool for each scene**
4. Set platform field to `kaggle`
5. Save as plans/[content-name]-plan.md
6. Review the plan for completeness
7. Execute the plan using the tools below

### Executing a Plan

For each scene in the plan, follow the decision tree:

| Scene Need | Action | Server |
|------------|--------|--------|
| Voiceover | Generate via Bark TTS | Full Pipeline (8000) |
| Animated portrait | Generate photo via SD 1.5, then animate via SadTalker + Easy-Wav2Lip | Styled Scene (8002) → Full Pipeline (8000) |
| Background image | Generate via SD 1.5 | Styled Scene (8002) |
| B-Roll clip | Generate via Wan 2.1 | B-Roll (8001) |
| Styled animation | Generate via AnimateDiff + ControlNet | Styled Scene (8002) |
| Text overlay | Add directly in fako_video_data.json | Local (Remotion) |

**Final steps:**
1. Update fako_video_data.json with all assets
2. Run: `npm run render:[track]`

### Kaggle API Credentials

**Location:** `~/.kaggle/kaggle.json`

| OS | Path |
|----|------|
| Windows | `C:\Users\<username>\.kaggle\kaggle.json` |
| macOS/Linux | `~/.kaggle/kaggle.json` |

**Contents:**
```json
{
  "username": "your-kaggle-username",
  "key": "your-kaggle-api-key"
}
```

All `kaggle` CLI commands use these credentials automatically.

### Server Capabilities

| Server | Port | Notebook | Datasets Needed | Capabilities |
|--------|------|----------|----------------|--------------|
| Full Pipeline | 8000 | `full-pipeline-server-kaggle.ipynb` | bark-model, sadtalker-model, wav2lip-model | Bark TTS, SadTalker, Easy-Wav2Lip |
| B-Roll | 8001 | `broll-server-kaggle.ipynb` | wan21-model | Wan 2.1 text-to-video |
| Styled Scene | 8002 | `styled-scene-server-kaggle.ipynb` | sd15-model, animatediff-model | SD 1.5 image gen, AnimateDiff animation |

### Starting a Kaggle Server (CLI)

All operations run from your local terminal. No browser needed.

**Step 1: Update kernel-metadata.json**

Edit `kaggle-push/kernel-metadata.json` for the server you want to start:

```json
// Full Pipeline Server
{
  "id": "fako-online/full-pipeline-server",
  "title": "Fako Online - Full Pipeline Server",
  "code_file": "full-pipeline-server-kaggle.ipynb",
  "language": "python",
  "kernel_type": "notebook",
  "is_private": true,
  "enable_gpu": true,
  "enable_tpu": false,
  "enable_internet": true,
  "dataset_sources": [
    "kingtechie/bark-model",
    "kingtechie/sadtalker-model",
    "kingtechie/wav2lip-model"
  ]
}
```

```json
// B-Roll Server
{
  "id": "fako-online/broll-server",
  "title": "Fako Online - B-Roll Server",
  "code_file": "broll-server-kaggle.ipynb",
  "language": "python",
  "kernel_type": "notebook",
  "is_private": true,
  "enable_gpu": true,
  "enable_tpu": false,
  "enable_internet": true,
  "dataset_sources": [
    "kingtechie/wan21-model"
  ]
}
```

```json
// Styled Scene Server
{
  "id": "fako-online/styled-scene-server",
  "title": "Fako Online - Styled Scene Server",
  "code_file": "styled-scene-server-kaggle.ipynb",
  "language": "python",
  "kernel_type": "notebook",
  "is_private": true,
  "enable_gpu": true,
  "enable_tpu": false,
  "enable_internet": true,
  "dataset_sources": [
    "kingtechie/sd15-model",
    "kingtechie/animatediff-model"
  ]
}
```

**Step 2: Copy the notebook to kaggle-push/**

```powershell
# For Full Pipeline
Copy-Item colab/full-pipeline-server-kaggle.ipynb kaggle-push/

# For B-Roll
Copy-Item colab/broll-server-kaggle.ipynb kaggle-push/

# For Styled Scene
Copy-Item colab/styled-scene-server-kaggle.ipynb kaggle-push/
```

**Step 3: Push and start the notebook**

```powershell
# Push with GPU T4 x2 accelerator
kaggle kernels push -p ./kaggle-push --accelerator "GPU T4 x2"
```

This uploads the notebook AND starts it running on Kaggle with GPU.

**Step 4: Check status**

```powershell
kaggle kernels status kingtechie/fako-online-full-pipeline-server
```

Wait until status shows `running` or `complete`.

**Step 5: Get the ngrok URL**

The ngrok URL is printed when the server starts, but Kaggle buffers stdout for long-running cells. The URL may not appear in `kaggle kernels logs` until the cell finishes.

**Method 1: Open the notebook in Edit Mode (Recommended)**

1. Go to [kaggle.com/code/kingtechie/fako-online-full-pipeline-server](https://www.kaggle.com/code/kingtechie/fako-online-full-pipeline-server)
2. Click **Edit** to enter edit mode
3. Scroll to the last cell (Cell 7: Start server)
4. Look at the cell output for a line like:
   ```
   Public URL: https://abc123-def456.ngrok-free.app
   ```
5. Copy the full URL including `https://`

**Method 2: Check the saved URL file**

Each notebook saves the URL to `/kaggle/working/ngrok_url.txt`. After the notebook finishes or while running:

```powershell
# Download the URL file from the kernel output
kaggle kernels output kingtechie/fako-online-full-pipeline-server -p ./kaggle-output
type .\kaggle-output\ngrok_url.txt
```

**Method 3: Check logs (may not work for running kernels)**

```powershell
kaggle kernels logs kingtechie/fako-online-full-pipeline-server
```

Note: Logs only populate after the kernel finishes or errors. For running kernels, use Method 1 or 2.

**Step 6: Update .env**

Open `.env` in the project root and paste the URL:

```
KAGGLE_API_URL=https://abc123-def456.ngrok-free.app
```

**Step 7: Verify the connection**

```bash
node scripts/generate-talking-head.js --check --api https://abc123-def456.ngrok-free.app
```

Expected output:
```json
{"status": "ok", "models": ["bark", "sadtalker", "wav2lip"]}
```

### Stopping a Server

```powershell
# Delete the kernel to stop it
kaggle kernels delete kingtechie/fako-online-full-pipeline-server
```

### Which Server for What

| I need to... | Start this server | Port | Datasets to Attach |
|-------------|-------------------|------|-------------------|
| Generate a voiceover (Bark TTS) | Full Pipeline | 8000 | bark-model, sadtalker-model, wav2lip-model |
| Animate a photo with voice (SadTalker) | Full Pipeline | 8000 | bark-model, sadtalker-model, wav2lip-model |
| Refine lip sync (Easy-Wav2Lip) | Full Pipeline | 8000 | bark-model, sadtalker-model, wav2lip-model |
| Generate a portrait/avatar (SD 1.5) | Styled Scene | 8002 | sd15-model, animatediff-model |
| Generate a background image (SD 1.5) | Styled Scene | 8002 | sd15-model, animatediff-model |
| Generate B-Roll video (Wan 2.1) | B-Roll | 8001 | wan21-model |
| Animate image in a style (AnimateDiff) | Styled Scene | 8002 | sd15-model, animatediff-model |

### Session Limits and Tips

| Limit | Value | Notes |
|-------|-------|-------|
| Session timeout | ~12 hours | Kaggle auto-stops idle sessions |
| GPU quota | ~30 hrs/week per account | Use backup account when exceeded |
| Working directory | 19.5 GB | Models are in datasets, not working dir |
| Max dataset size | 100 GB per dataset | Each model has its own dataset |

**Tips:**
- First run is slower (models load into GPU memory)
- Subsequent runs in same session are faster (cached)
- If ngrok URL stops working, restart the notebook and get a new URL
- Use `kaggle kernels output` to download any generated files

### Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `403 Forbidden` | Wrong credentials | Check `~/.kaggle/kaggle.json` exists and is correct |
| `Kernel not found` | Typo in kernel ID | Run `kaggle kernels list --mine` to see your kernels |
| `Connection refused` | Server not running | Check `kaggle kernels status`, wait for `running` |
| `404 Not Found` | Wrong URL or stale ngrok | Get new URL from `kaggle kernels logs` |
| `GPU OOM` | Not enough VRAM | Ensure `--accelerator "GPU T4 x2"` on push |
| `No space left` | Working directory full | Models should be in datasets, not working dir |
| Session stopped | Idle timeout or quota | Push again with `kaggle kernels push` |
| ngrok rate limit | Too many restarts | Wait 1 minute, then push again |

---

## 9. CLI Commands

### Content Generation

```bash
# Generate avatar image from text prompt (uses SD 1.5 on Styled Scene server)
node scripts/generate-talking-head.js --prompt "professional African business owner, male, 30s, confident smile" --api URL

# Generate talking head from text + image (uses Bark + SadTalker + Easy-Wav2Lip on Full Pipeline server)
node scripts/generate-talking-head.js --image photo.png --text "MAN: [gasps] Wait!" --api URL

# Generate from pre-existing audio (uses SadTalker + Easy-Wav2Lip on Full Pipeline server)
node scripts/generate-talking-head.js --image photo.png --audio voice.wav --api URL

# Check API health (tests connection to running server)
node scripts/generate-talking-head.js --check --api URL
```

### Rendering

```bash
# Render single track
npm run render:promo
npm run render:ecommerce
npm run render:businesses
npm run render:schools
npm run render:churches

# Render all tracks
npm run render:all

# Open Remotion Studio (visual preview)
npm run studio
```

---

## 10. Remotion Scene Types

### Scene Behaviors

| Type | talkScene | video field | Behavior |
| ---- | --------- | ----------- | -------- |
| Talking Head | true | assets/video.mp4 | OffthreadVideo plays real video + text overlay |
| Talking Head Fallback | true | empty | Ken Burns breathing animation on photo + text overlay |
| Image Scene | false | - | Ken Burns effect on image + text overlay |

### Supported Animations

| Animation | Effect | Best For |
|-----------|--------|----------|
| zoom-in | Slowly zoom into center of image | Hero shots, emphasis, drama |
| zoom-out | Slowly zoom out from center | Reveals, establishing shots |
| pan-right | Slowly pan right across image | Landscape, product showcase |
| pan-left | Slowly pan left across image | Reverse pan, reading direction |
| shake | Quick shake/vibration | Excitement, urgency, impact |
| scaleUp | Scale up from small to full size | Text emphasis, call-to-action |
| cascade | Words appear one by one with spring | Lists, bullet points, multiple messages |
| zoom (text) | Text zooms in from center | Headlines, big statements |

### Transitions Between Scenes

| Transition | Effect |
|------------|--------|
| fade | Cross-fade between scenes |
| slide | Slide transition between scenes |

### Text Overlay Rules

- Primary color: #D4AF37 (gold)
- Background: #0A0A0A (dark)
- Font: Impact
- Text animations: shake, scaleUp, zoom, cascade

---

## 11. Troubleshooting

| Issue                     | Solution                                             |
| ------------------------- | ---------------------------------------------------- |
| Kaggle quota exceeded     | Switch to backup account (see Multi-Account Setup)   |
| ngrok URL changes         | Copy new URL, update `.env` → `KAGGLE_API_URL`      |
| Lip sync blurry           | Run Easy-Wav2Lip stage                               |
| Bark audio robotic        | Try different voice preset                           |
| Render fails              | Check TypeScript errors                              |
| GPU OOM                   | Use T4x2 accelerator (32GB VRAM) or reduce batch size |
| Dataset not found         | Verify datasets are attached via Add Data in notebook  |
| Datasets not mounted at `/kaggle/input/` | Wrong `id` in kernel-metadata.json | Pull metadata with `kaggle kernels pull -m`, verify `id`, add `dataset_sources`, push back |
| Notebook won't connect    | Ensure Internet is enabled in notebook settings      |
| Slow model loading        | Models cache after first run — subsequent loads are faster |
| Session timeout           | Kaggle sessions auto-stop after ~12 hours; re-run    |
| Can't share dataset       | Owner must add collaborator in Dataset Settings      |

---

## 12. Lessons Learned (Critical)

### SadTalker Path Discovery (Nested Subdirectories)

**Problem:** The `kingtechie/sadtalker-model` dataset has nested directories. The `src/` folder is often inside a subdirectory like `/kaggle/input/sadtalker-model/SadTalker/` or `/kaggle/input/sadtalker-model/sadtalker/`. Hardcoding `SADTALKER_DIR = "/kaggle/input/sadtalker-model"` and doing `from src.gradio_demo import SadTalker` fails with `FileNotFoundError` or `ModuleNotFoundError`.

**Fix:** Detect subdirectories and use `os.chdir()` before importing:

```python
import os, sys, glob

sadtalker_path = "/kaggle/input/sadtalker-model"

# Check for nested subdirectories
if os.path.exists(os.path.join(sadtalker_path, "SadTalker")):
    sadtalker_path = os.path.join(sadtalker_path, "SadTalker")
elif os.path.exists(os.path.join(sadtalker_path, "sadtalker")):
    sadtalker_path = os.path.join(sadtalker_path, "sadtalker")

# Discover actual paths
sadtalker_gradio = glob.glob(f"{sadtalker_path}/**/src/gradio_demo.py", recursive=True)
if sadtalker_gradio:
    SADTALKER_ROOT = os.path.dirname(os.path.dirname(sadtalker_gradio[0]))
else:
    SADTALKER_ROOT = sadtalker_path

# SadTalker relative imports require CWD set to the root
if SADTALKER_ROOT not in sys.path:
    sys.path.insert(0, SADTALKER_ROOT)
os.chdir(SADTALKER_ROOT)

from src.gradio_demo import SadTalker
os.chdir("/kaggle/working")  # Switch back after import
```

Apply the same pattern for `checkpoints/`, `src/config/`, and `gfpgan/weights/`.

### Lazy Model Loading (GPU OOM Prevention)

**Problem:** Loading Bark + SadTalker + Easy-Wav2Lip simultaneously causes GPU OOM even on T4 x2 (32GB).

**Fix:** Load models lazily — only when first API call arrives, move to CPU after each use:

```python
_bark_model = None
_sadtalker_instance = None

def get_bark():
    global _bark_model
    if _bark_model is None:
        _bark_model = BarkModel.from_pretrained(BARK_DIR)
    return _bark_model

def unload_bark():
    global _bark_model
    del _bark_model
    _bark_model = None
    gc.collect()
    torch.cuda.empty_cache()
```

In `/generate-full` endpoint: call `unload_bark()` before `get_sadtalker()` to free VRAM.

### Windows PowerShell + Kaggle CLI Encoding

**Problem:** `kaggle kernels logs` outputs Unicode characters that crash PowerShell with `'charmap' codec can't encode characters`.

**Fix:** Use Python subprocess to capture logs as bytes:

```python
import subprocess
result = subprocess.run(['kaggle', 'kernels', 'logs', 'kingtechie/kernel-id'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
print(result.stdout)
```

Or check logs directly in the browser at `https://www.kaggle.com/code/[username]/[kernel-name]/log`.

### Kernel Metadata: Always Pull First

**Problem:** Writing `kernel-metadata.json` locally with a guessed `id` causes datasets to not be mounted. The `id` must match Kaggle's exact kernel ID.

**Fix:** Always pull existing kernel metadata before editing:

```bash
kaggle kernels pull kingtechie/[kernel-name] -m
```

This creates `kaggle-push/kernel-metadata.json` with the exact `id`, title, and structure Kaggle expects. Then:
1. Edit `dataset_sources` to include needed datasets
2. Copy your updated notebook to `kaggle-push/`
3. Push back: `kaggle kernels push -p ./kaggle-push`

For brand-new kernels (never existed before), local metadata is fine.

### PyTorch CUDA Device Properties Attribute

**Problem:** `torch.cuda.get_device_properties(0).total_mem` raises `AttributeError` — the correct attribute is `total_memory`, not `total_mem`.

**Fix:**
```python
# WRONG
print(f"VRAM: {torch.cuda.get_device_properties(0).total_mem / 1024**3:.1f} GB")

# CORRECT
print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
```

### Ngrok Requires Auth Token (Since ~2025)

**Problem:** `ngrok.connect(8000)` fails with `ERR_NGROK_4018` — "authentication failed: This ngrok session is not authenticated."

**Fix:** Set the auth token before connecting:
```python
from pyngrok import ngrok
ngrok.set_auth_token("YOUR_NGROK_AUTHTOKEN")
public_url = ngrok.connect(8000)
```

**Storage:** The auth token lives in `.env` as `NGROK_AUTHTOKEN=...` for reference, but must be hardcoded in notebook cells since Kaggle notebooks can't read local `.env` files.

**Get your token:** https://dashboard.ngrok.com/get-started/your-authtoken

### Jupyter asyncio Conflict with uvicorn.run()

**Problem:** `uvicorn.run(app, host="0.0.0.0", port=8000)` fails with `RuntimeError: asyncio.run() cannot be called from a running event loop` because Jupyter already has a running event loop.

**Fix:** Run uvicorn in a background thread:
```python
import threading
import uvicorn

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Keep alive (fixed duration, not infinite)
import time
for i in range(120):  # 2 hours
    time.sleep(60)
```

### Kaggle Logs API + ngrok URL Retrieval

**Problem:** `kaggle kernels logs` returns empty for running kernels (only populates after completion/error). The ngrok URL is printed in a long-running cell, so it's buffered and doesn't appear in logs.

**Workarounds (in order of reliability):**

1. **Open notebook in Edit Mode** — Go to `kaggle.com/code/[username]/[kernel-name]`, click Edit, scroll to the last cell output. The URL is always visible there.

2. **Check saved URL file** — Each notebook saves the URL to `/kaggle/working/ngrok_url.txt`. After pushing:
   ```powershell
   kaggle kernels output kingtechie/[kernel-name] -p ./kaggle-output
   type .\kaggle-output\ngrok_url.txt
   ```
   Note: `kaggle kernels output` only works after the kernel finishes or errors.

3. **Use a fixed-duration loop** — The notebooks use `for i in range(120): time.sleep(60)` (2 hours) instead of `while True`, so the kernel eventually finishes and logs become available.

### Execution Order: Images First, Then Audio, Then Lip Sync

**Problem:** Lip syncing requires the image for that scene to already exist. If you generate audio first, then try to lip-sync, the image may not be ready yet.

**Fix:** Follow this order:
1. **Phase 1 — All images/video generation** (Styled Scene Server, port 8002): Generate all static images (dashboards, backgrounds) and animated scenes (AnimateDiff) first
2. **Phase 2 — All audio** (Full Pipeline Server, port 8000): Generate all Bark TTS voiceovers
3. **Phase 3 — All lip syncing** (Full Pipeline Server, port 8000): Combine images + audio via SadTalker + Easy-Wav2Lip
4. **Phase 4 — B-Roll** (B-Roll Server, port 8001): Generate Wan 2.1 clips (no dependencies)
5. **Phase 5 — Render** (local): Update `fako_video_data.json`, run `npm run render:businesses`
