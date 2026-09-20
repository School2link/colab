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
| Easy-Wav2Lip             | Lip sync refinement    | Video + audio              | .mp4 video |
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

## 3. Storage Layout

All models are stored in a single Kaggle Dataset.

### Kaggle Dataset

| Dataset Name              | Models                                                                     | Size     | URL                                                       |
| ------------------------- | -------------------------------------------------------------------------- | -------- | --------------------------------------------------------- |
| kingtechie/fako-ai-models | All 6 models (Bark, SadTalker, Easy-Wav2Lip, Wan 2.1, AnimateDiff, SD 1.5) | ~21.7 GB | https://www.kaggle.com/datasets/kingtechie/fako-ai-models |

Kaggle provides 100GB of private dataset storage, so all models fit comfortably in a single dataset.

### Model Breakdown

| Model           | Hugging Face Repo              | Target (Kaggle)                      | Size    |
| --------------- | ------------------------------ | ------------------------------------ | ------- |
| Wan 2.1 (1.3B)  | Wan-AI/Wan2.1-T2V-1.3B         | /kaggle/working/models/Wan2.1-1.3B/  | ~6.5 GB |
| AnimateDiff     | guoyww/animatediff             | /kaggle/working/models/AnimateDiff/  | ~3.5 GB |
| SD 1.5          | runwayml/stable-diffusion-v1-5 | /kaggle/working/models/SD1.5_Base/   | ~3.2 GB |
| Bark            | suno/bark                      | /kaggle/working/models/Bark_TTS/     | ~4.5 GB |
| SadTalker       | camenduru/SadTalker            | /kaggle/working/models/SadTalker/    | ~2.5 GB |
| Easy-Wav2Lip    | numz/wav2lip_studio-0.2        | /kaggle/working/models/Easy-Wav2Lip/ | ~1.5 GB |
| **Total**       |                                | **~21.7 GB** (1 dataset)             |         |

### Downloading Models

**IMPORTANT: Never download model files to your local PC.**

Downloading 10-15 GB of model weights to your computer and then re-uploading to Kaggle wastes local storage, time, and bandwidth.

Instead, let Kaggle download directly over its high-speed connections (~100+ MB/s).

#### First-Time Setup

Upload `kaggle/download-all-models.ipynb` to Kaggle and run it. This downloads all models to `/kaggle/working/`. Then click **Save Version** to export as a permanent dataset.

Alternatively, run this in any Kaggle notebook with Internet enabled:

```python
import os

target_folder = "/kaggle/working/models"
os.makedirs(target_folder, exist_ok=True)

!pip install -q huggingface_hub
!huggingface-cli download Wan-AI/Wan2.1-T2V-1.3B --local-dir {target_folder}/Wan2.1-1.3B
!huggingface-cli download guoyww/animatediff --local-dir {target_folder}/AnimateDiff
!huggingface-cli download runwayml/stable-diffusion-v1-5 --local-dir {target_folder}/SD1.5_Base
!huggingface-cli download suno/bark --local-dir {target_folder}/Bark_TTS
!huggingface-cli download camenduru/SadTalker --local-dir {target_folder}/SadTalker
!huggingface-cli download numz/wav2lip_studio-0.2 --local-dir {target_folder}/Easy-Wav2Lip
```

### Kaggle Session Init Code

```python
import os

models_dir = "/kaggle/input/fako-ai-models"
working_dir = "/kaggle/working"

os.makedirs(f"{working_dir}/SadTalker/checkpoints", exist_ok=True)
os.makedirs(f"{working_dir}/Easy-Wav2Lip/checkpoints", exist_ok=True)
os.makedirs(f"{working_dir}/outputs", exist_ok=True)

!cp -r {models_dir}/SadTalker/* {working_dir}/SadTalker/checkpoints/ 2>/dev/null || true
!cp -r {models_dir}/Easy-Wav2Lip/* {working_dir}/Easy-Wav2Lip/checkpoints/ 2>/dev/null || true

os.environ["SUNO_OFFLOAD_CPU"] = "True"
os.environ["HF_HOME"] = f"{models_dir}/Bark_TTS"

print("All models linked from dataset!")
```

#### Summary

- **Local PC:** Only stores lightweight code (`.ipynb` notebooks and `.py` scripts)
- **Kaggle:** Downloads and holds all heavy multi-gigabyte models directly through the cloud
- **Your home internet:** Never touched for model downloads

---

## 4. Multi-Account Setup

Kaggle limits GPU usage to ~30 hours/week per account. For higher throughput, use a **primary + backup** account strategy.

### Strategy

| Account    | Role     | Dataset Ownership | Usage                                    |
| ---------- | -------- | ----------------- | ---------------------------------------- |
| Account A  | Primary  | Owner             | Day-to-day generation, all notebooks     |
| Account B  | Backup   | Collaborator      | Overflow when A hits weekly quota limit  |

### Sharing the Dataset Across Accounts

The `kingtechie/fako-ai-models` dataset (~21.7 GB) must be accessible to both accounts.

1. **Account A** creates the dataset and uploads all models
2. Account A goes to **Dataset Settings** → **Collaborators** → adds Account B's Kaggle username
3. **Account B** can now attach the same dataset in any notebook via **Add Data** → search for `kingtechie/fako-ai-models`

**Important:** The dataset owner (Account A) must explicitly grant collaborator access. Shared datasets are read-only for collaborators.

### Switching Between Accounts

When Account A hits the ~30 hr/week GPU quota:

1. Log out of Kaggle
2. Log in with Account B credentials
3. Open the same notebook (or re-upload if using a different account)
4. Attach `kingtechie/fako-ai-models` via Add Data
5. The dataset is identical — no re-downloading needed

### Tips

- Keep both accounts verified with phone numbers (unverified accounts get lower quotas)
- Monitor usage at `kaggle.com/settings` → **Usage** tab
- Space out heavy workloads across accounts to maximize weekly GPU hours
- Both accounts can run different notebooks simultaneously for parallel generation

---

## 5. Project Structure

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
  kaggle/
    full-pipeline-server.ipynb       # Bark + SadTalker + Easy-Wav2Lip (port 8000)
    broll-server.ipynb               # Wan 2.1 B-Roll (port 8001)
    styled-scene-server.ipynb        # AnimateDiff + ControlNet (port 8002)
    download-all-models.ipynb        # One-time download to Kaggle dataset
    *-metadata.json                  # Kaggle kernel metadata files
```

---

## 6. API Endpoints

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

## 7. Workflow

### Creating New Content

1. Copy the plan template above
2. Fill in all scenes with explicit timestamps, sources, and text
3. Set platform field to `kaggle`
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

### Kaggle Session

1. Open the needed Kaggle notebook (full-pipeline, broll, or styled)
2. Set Accelerator to GPU T4 x2
3. Attach the `kingtechie/fako-ai-models` dataset
4. Run all cells
5. Copy the ngrok URL to `.env` as `KAGGLE_API_URL`
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

| Type                  | talkScene | video field      | Behavior                        |
| --------------------- | --------- | ---------------- | ------------------------------- |
| Talking Head          | true      | assets/video.mp4 | OffthreadVideo plays real video |
| Talking Head Fallback | true      | empty            | Ken Burns breathing animation   |
| Image Scene           | false     | -                | Ken Burns + text overlay        |

---

## 10. Troubleshooting

| Issue                     | Solution                                             |
| ------------------------- | ---------------------------------------------------- |
| Kaggle quota exceeded     | Switch to backup account (see Multi-Account Setup)   |
| ngrok URL changes         | Copy new URL, update `.env` → `KAGGLE_API_URL`      |
| Lip sync blurry           | Run Easy-Wav2Lip stage                               |
| Bark audio robotic        | Try different voice preset                           |
| Render fails              | Check TypeScript errors                              |
| GPU OOM                   | Use T4x2 accelerator (32GB VRAM) or reduce batch size |
| Dataset not found         | Verify dataset is attached via Add Data in notebook  |
| Notebook won't connect    | Ensure Internet is enabled in notebook settings      |
| Slow model loading        | Models cache after first run — subsequent loads are faster |
| Session timeout           | Kaggle sessions auto-stop after ~12 hours; re-run    |
| Can't share dataset       | Owner must add collaborator in Dataset Settings      |
