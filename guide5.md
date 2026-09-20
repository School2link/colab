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
- **Platform:** colab | kaggle | auto
- **Output:** 1080x1920 MP4, 30fps

## Assets Required
| Asset | Type | Source | Generation Method | Notes |
|-------|------|--------|-------------------|-------|
| hero-image.png | image | provided or generate | SD 1.5 via Colab/Kaggle | Front-facing portrait for avatar |
| voiceover.wav | audio | generate | Bark TTS via Colab/Kaggle | Emotional script below |
| scene2.png | image | provided or generate | SD 1.5 via Colab/Kaggle | Dashboard screenshot |
| style-clip.mp4 | video | generate | AnimateDiff via Colab/Kaggle | Styled scene loop |

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
7. Assets can be "provided" (user supplies file) or "generate" (Colab/Kaggle produces it)
8. If source is "generate", include the generation prompt/method in the plan
9. Platform field determines which notebooks and storage to use:
   - `colab`: Use Google Colab notebooks + Google Drive storage
   - `kaggle`: Use Kaggle notebooks + Kaggle Dataset storage
   - `auto`: Try Colab first, fallback to Kaggle if unavailable

---

## 2. Platform Comparison

| Feature | Google Colab | Kaggle |
|---------|--------------|--------|
| **GPU** | T4 (16GB VRAM) | T4x2 (2x16GB = 32GB VRAM) |
| **Storage** | Google Drive (30GB across 2 accounts) | Kaggle Datasets (read-only) + /kaggle/working/ (~20GB) |
| **Quota** | Limited sessions/day | ~30 hours/week GPU |
| **Session Limit** | ~12 hours | ~12 hours |
| **Model Loading** | Mount Drive, copy to session | Mount Dataset, copy to /kaggle/working/ |
| **API Exposure** | ngrok tunnel | ngrok tunnel |

### When to Use Each Platform

| Scenario | Recommended Platform |
|----------|---------------------|
| Colab available, quick session | Colab |
| Colab unavailable (queue) | Kaggle |
| Need more GPU memory (large models) | Kaggle (T4x2 = 32GB) |
| Long-running tasks (>12 hours) | Kaggle (weekly quota) |
| Multiple parallel sessions | Kaggle (30 hrs/week) |

---

## 3. Generating Assets

All AI models run on Google Colab or Kaggle (T4 GPU). Plans can specify that assets be generated rather than provided.

| Asset Type | Model | API Endpoint | Input | Output |
|------------|-------|--------------|-------|--------|
| Portrait/Avatar image | SD 1.5 | /generate-image | Text prompt | .png |
| Scene background | SD 1.5 | /generate-image | Text prompt | .png |
| Emotional voiceover | Bark TTS | /generate-tts | Text with tags | .wav |
| Talking head video | SadTalker | /generate-avatar | Image + audio | .mp4 |
| Refined lip sync | Easy-Wav2Lip | /generate-full | Video + audio | .mp4 |
| B-Roll clip | Wan 2.1 | /generate-broll | Text prompt | .mp4 |
| Styled scene | AnimateDiff | /generate-styled | Image + prompt | .mp4 |

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

| Type | Description | Tools Used |
|------|-------------|------------|
| talking-head | Photo animated with AI voice | Bark + SadTalker + Easy-Wav2Lip |
| image-scene | Static image with Ken Burns effect | Remotion only |
| broll | AI-generated background video | Wan 2.1 |
| styled | Consistent character in new style | AnimateDiff + ControlNet |
| drama | Multiple characters, scenes, dialogue | All tools combined |

### AI Models

| Model | Purpose | Input | Output |
|-------|---------|-------|--------|
| Bark (Suno) | Emotional TTS | Text with [laughs] [gasps] | .wav audio |
| SadTalker | Talking head animation | Photo + audio | .mp4 video |
| Easy-Wav2Lip | Lip sync refinement | Video + audio | .mp4 video |
| Wan 2.1 (1.3B) | B-Roll generation | Text prompt | .mp4 video |
| AnimateDiff + ControlNet | Style consistency | Image + text prompt | .mp4 video |

### Bark Emotional Tags

| Effect | Syntax | Example |
|--------|--------|---------|
| Laughter | [laughs] | "We did it! [laughs]" |
| Gasping | [gasps] | "[gasps] Wait..." |
| Sighing | [sighs] | "[sighs] I do not know..." |
| Hesitation | ... or uh, | "Well... I mean..." |
| Shouting | ALL CAPS! | "STOP! DO NOT DO THAT!" |
| Whispering | lowercase | soft breathy delivery |

Voice Presets: v2/en_speaker_0 through v2/en_speaker_9

---

## 4. Storage Layout

### Google Drive (Colab Platform)

#### Account A: Visual & Scene Generation (~11.0 GB / 15 GB)

| Model | Size | Path | Notes |
|-------|------|------|-------|
| Wan 2.1 (1.3B) | ~4.5 GB | MyDrive/AI_Models/Wan2.1-1.3B/ | safetensors only |
| AnimateDiff + ControlNet | ~3.5 GB | MyDrive/AI_Models/AnimateDiff/ | |
| Base SD 1.5 Model | ~3.0 GB | MyDrive/AI_Models/SD1.5_Base/ | pruned .safetensors |

#### Account B: Audio, Talking-Head & Output Storage (~8.5 GB / 15 GB)

| Model | Size | Path |
|-------|------|------|
| Bark TTS (Suno) | ~4.5 GB | AI_Avatar_Models/Bark_TTS/ |
| SadTalker | ~2.5 GB | AI_Avatar_Models/SadTalker/ |
| Easy-Wav2Lip | ~1.5 GB | AI_Avatar_Models/Easy-Wav2Lip/ |
| Rendered Outputs | ~3.5 GB free | AI_Avatar_Models/Rendered_Outputs/ |

### Kaggle Datasets

| Dataset Name | Models | Size | URL |
|--------------|--------|------|-----|
| kingtechie/fako-ai-models | All 6 models (Bark, SadTalker, Easy-Wav2Lip, Wan 2.1, AnimateDiff, SD 1.5) | ~21.7 GB | https://www.kaggle.com/datasets/kingtechie/fako-ai-models |

Kaggle provides 100GB of private dataset storage, so all models fit comfortably in a single dataset.

### Downloading Models to the Cloud

**IMPORTANT: Never download model files to your local PC.**

Downloading 10-15 GB of model weights to your computer and then re-uploading to Google Drive or Kaggle wastes local storage, time, and bandwidth.

Instead, let the cloud platforms download directly over their high-speed connections (~100+ MB/s).

#### For Google Drive (Colab)

Run this in a Colab cell. It downloads directly from Hugging Face to your mounted Drive:

```python
from google.colab import drive
import os

drive.mount('/content/drive')

target_folder = "/content/drive/MyDrive/AI_Models"
os.makedirs(target_folder, exist_ok=True)

# Download only safetensors files (skips .bin, .pt, .ckpt to save space)
!pip install -q huggingface_hub
!huggingface-cli download Wan-AI/Wan2.1-T2V-1.3B --include "*.safetensors" --local-dir {target_folder}/Wan2.1-1.3B
```

#### For Kaggle (First-Time Setup)

Upload `colab/kaggle-download-all-models.ipynb` to Kaggle and run it. This downloads all models to `/kaggle/working/`. Then click **Save Version** to export as a permanent dataset.

Alternatively, run this in any Kaggle notebook with Internet enabled:

```python
import os

target_folder = "/kaggle/working/models"
os.makedirs(target_folder, exist_ok=True)

!pip install -q huggingface_hub
!huggingface-cli download Wan-AI/Wan2.1-T2V-1.3B --local-dir {target_folder}/Wan2.1-1.3B
```

#### Model Download Commands

| Model | Hugging Face Repo | Target (Drive) | Target (Kaggle) | Drive Size | Kaggle Size |
|-------|-------------------|----------------|-----------------|------------|-------------|
| Wan 2.1 (1.3B) | Wan-AI/Wan2.1-T2V-1.3B | AI_Models/Wan2.1-1.3B/ | /kaggle/working/models/Wan2.1-1.3B/ | ~4.5 GB | ~6.5 GB |
| AnimateDiff | guoyww/animatediff | AI_Models/AnimateDiff/ | /kaggle/working/models/AnimateDiff/ | ~3.5 GB | ~3.5 GB |
| SD 1.5 | runwayml/stable-diffusion-v1-5 | AI_Models/SD1.5_Base/ | /kaggle/working/models/SD1.5_Base/ | ~3.0 GB | ~3.2 GB |
| Bark | suno/bark | AI_Avatar_Models/Bark_TTS/ | /kaggle/working/models/Bark_TTS/ | ~4.5 GB | ~4.5 GB |
| SadTalker | camenduru/SadTalker | AI_Avatar_Models/SadTalker/ | /kaggle/working/models/SadTalker/ | ~2.5 GB | ~2.5 GB |
| Easy-Wav2Lip | numz/wav2lip_studio-0.2 | AI_Avatar_Models/Easy-Wav2Lip/ | /kaggle/working/models/Easy-Wav2Lip/ | ~1.5 GB | ~1.5 GB |
| **Total** | | **~19.0 GB** (split 2 accounts) | **~21.7 GB** (1 dataset) | | |

#### Download for Google Drive (Optimized - safetensors only)

```python
# Account A: Visual Models (safetensors only)
!huggingface-cli download Wan-AI/Wan2.1-T2V-1.3B --include "*.safetensors" --local-dir {target}/Wan2.1-1.3B
!huggingface-cli download guoyww/animatediff --include "*.safetensors" --local-dir {target}/AnimateDiff
!huggingface-cli download runwayml/stable-diffusion-v1-5 --include "*.safetensors" --local-dir {target}/SD1.5_Base

# Account B: Audio & Avatar Models
!huggingface-cli download suno/bark --local-dir {target}/Bark_TTS
!huggingface-cli download camenduru/SadTalker --include "checkpoints/*" --local-dir {target}/SadTalker
!huggingface-cli download numz/wav2lip_studio-0.2 --include "checkpoints/*" --local-dir {target}/Easy-Wav2Lip
```

#### Download for Kaggle (Full sizes - all in 1 dataset)

```python
# All models (full download, no --include filter)
!huggingface-cli download Wan-AI/Wan2.1-T2V-1.3B --local-dir {target}/Wan2.1-1.3B
!huggingface-cli download guoyww/animatediff --local-dir {target}/AnimateDiff
!huggingface-cli download runwayml/stable-diffusion-v1-5 --local-dir {target}/SD1.5_Base
!huggingface-cli download suno/bark --local-dir {target}/Bark_TTS
!huggingface-cli download camenduru/SadTalker --local-dir {target}/SadTalker
!huggingface-cli download numz/wav2lip_studio-0.2 --local-dir {target}/Easy-Wav2Lip
```
!huggingface-cli download camenduru/SadTalker --include "checkpoints/*" --local-dir {target}/SadTalker
!huggingface-cli download numz/wav2lip_studio-0.2 --include "checkpoints/*" --local-dir {target}/Easy-Wav2Lip
```

#### Summary

- **Local PC:** Only stores lightweight code (`.ipynb` notebooks and `.py` scripts)
- **Google Drive / Kaggle:** Downloads and holds all heavy multi-gigabyte models directly through the cloud
- **Your home internet:** Never touched for model downloads

### Colab Session Init Code

```python
from google.colab import drive
import os

drive.mount('/content/drive')

account_a_dir = "/content/drive/MyDrive/AI_Models"
shared_b_dir = "/content/drive/MyDrive/AI_Avatar_Models"

os.makedirs("/content/SadTalker/checkpoints", exist_ok=True)
os.makedirs("/content/Easy-Wav2Lip/checkpoints", exist_ok=True)
os.makedirs("/content/outputs", exist_ok=True)

!cp -r {shared_b_dir}/SadTalker/* /content/SadTalker/checkpoints/ 2>/dev/null || true
!cp -r {shared_b_dir}/Easy-Wav2Lip/* /content/Easy-Wav2Lip/checkpoints/ 2>/dev/null || true

os.environ["SUNO_OFFLOAD_CPU"] = "True"
os.environ["HF_HOME"] = f"{shared_b_dir}/Bark_TTS"

print("All models linked from Account A & Account B!")
```

---

## 5. Project Structure

```
LocalContents/
  guide5.md                          # This file
  .env                               # COLAB_API_URL or KAGGLE_API_URL setting
  plans/                             # Content plans (one per video)
    [content-name]-plan.md
  packages/remotion-core/src/
    Composition.tsx                  # Main video template
    colab-api.ts                     # API client (works with both platforms)
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
    generate-talking-head.js         # CLI for Colab/Kaggle API
  colab/
    full-pipeline-server.ipynb       # Bark + SadTalker + Easy-Wav2Lip (port 8000)
    broll-server.ipynb               # Wan 2.1 B-Roll (port 8001)
    styled-scene-server.ipynb        # AnimateDiff + ControlNet (port 8002)
    full-pipeline-server-kaggle.ipynb    # Kaggle version (port 8000)
    broll-server-kaggle.ipynb            # Kaggle version (port 8001)
    styled-scene-server-kaggle.ipynb     # Kaggle version (port 8002)
    kaggle-download-all-models.ipynb     # One-time download to Kaggle
    *-metadata.json                      # Kaggle kernel metadata files
```

---

## 6. API Endpoints

| Endpoint | Method | Input | Output |
|----------|--------|-------|--------|
| /health | GET | - | status |
| /generate-image | POST | text_prompt, style | portrait.png |
| /generate-tts | POST | text, voice_preset | emotional_speech.wav |
| /generate-avatar | POST | image, audio | talking-head.mp4 |
| /generate-full | POST | image, text, voice_preset, refine_lips | talking-head.mp4 |
| /generate-broll | POST | text_prompt, duration | broll-clip.mp4 |
| /generate-styled | POST | image, text_prompt, style | styled-scene.mp4 |

---

## 7. Workflow

### Creating New Content
1. Copy the plan template above
2. Fill in all scenes with explicit timestamps, sources, and text
3. Set platform field (colab, kaggle, or auto)
4. Save as plans/[content-name]-plan.md
5. Review the plan for completeness
6. Execute the plan using the tools below

### Executing a Plan
1. Generate any needed images via SD 1.5
2. Generate any needed audio via Bark TTS
3. Generate talking-head videos via SadTalker + Easy-Wav2Lip
4. Generate B-Roll clips via Wan 2.1
5. Generate styled scenes via AnimateDiff + ControlNet
6. Update fako_video_data.json with all assets
7. Run: npm run render:[track]

### Colab Session
1. Open the needed notebook (full-pipeline, broll, or styled)
2. Set runtime to T4 GPU
3. Run init cell: mount Drive + load models (~15s)
4. Start server + ngrok
5. Copy ngrok URL to .env
6. Run CLI commands locally

### Kaggle Session
1. Open the needed Kaggle notebook (full-pipeline-kaggle, broll-kaggle, or styled-kaggle)
2. Set Accelerator to GPU T4 x2
3. Attach the required dataset(s)
4. Run all cells
5. Copy the URL to .env
6. Run CLI commands locally

**Ports:** Full Pipeline = 8000 | B-Roll = 8001 | Styled Scene = 8002

---

## 8. CLI Commands

```bash
# Generate avatar image from text prompt
node scripts/generate-talking-head.js --prompt "professional African business owner, male, 30s, confident smile" --api URL

# Generate talking head from text + image
node scripts/generate-talking-head.js --image photo.png --text "MAN: [gasps] Wait!" --api URL

# Generate from pre-existing audio
node scripts/generate-talking-head.js --image photo.png --audio voice.wav --api URL

# Check API health
node scripts/generate-talking-head.js --check --api URL

# Render video
npm run render:promo
npm run render:ecommerce
npm run render:businesses
npm run render:schools
npm run render:churches
```

---

## 9. Remotion Scene Types

| Type | talkScene | video field | Behavior |
|------|-----------|-------------|----------|
| Talking Head | true | assets/video.mp4 | OffthreadVideo plays real video |
| Talking Head Fallback | true | empty | Ken Burns breathing animation |
| Image Scene | false | - | Ken Burns + text overlay |

---

## 10. Troubleshooting

| Issue | Solution |
|-------|----------|
| Colab disconnects | Re-run init cell, models cached on Drive |
| Colab unavailable | Switch platform to kaggle in plan |
| Kaggle quota exceeded | Wait for weekly reset or switch to Colab |
| ngrok URL changes | Copy new URL, update .env |
| Lip sync blurry | Run Easy-Wav2Lip stage |
| Bark audio robotic | Try different voice preset |
| Render fails | Check TypeScript errors |
| GPU OOM in Colab | Restart runtime, use 256px |
| GPU OOM in Kaggle | Use T4x2 (32GB VRAM) or reduce batch size |
