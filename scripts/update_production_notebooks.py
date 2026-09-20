import json
import os

colab_dir = r"C:\xampp\htdocs\LocalContents\colab"

# === full-pipeline-server-kaggle.ipynb ===
nb_path = os.path.join(colab_dir, "full-pipeline-server-kaggle.ipynb")
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Cell 0 (markdown): update instructions
nb["cells"][0]["source"] = [
    "# Fako Online - Full Pipeline Server (Kaggle)\n\n",
    "**Bark TTS + SadTalker + Easy-Wav2Lip**\n\n",
    "This notebook runs all three models on a single Kaggle GPU session.\n\n",
    "### Instructions\n",
    "1. Enable **GPU T4 x2** (Settings > Accelerator)\n",
    "2. Add datasets: `kingtechie/bark-model`, `kingtechie/sadtalker-model`, `kingtechie/wav2lip-model`\n",
    "3. Run all cells in order\n",
    "4. The server will start on port 8000"
]

# Cell 1: update paths
nb["cells"][1]["source"] = [
    "# Cell 1: Setup paths\n",
    "import os\n",
    "\n",
    "WORKING_DIR = \"/kaggle/working/outputs\"\n",
    "os.makedirs(WORKING_DIR, exist_ok=True)\n",
    "\n",
    "BARK_DIR = \"/kaggle/input/bark-model\"\n",
    "SADTALKER_DIR = \"/kaggle/input/sadtalker-model\"\n",
    "WAV2LIP_DIR = \"/kaggle/input/wav2lip-model\"\n",
    "\n",
    "print(f\"Bark: {BARK_DIR}\")\n",
    "print(f\"SadTalker: {SADTALKER_DIR}\")\n",
    "print(f\"Easy-Wav2Lip: {WAV2LIP_DIR}\")\n",
    "print(f\"Working dir: {WORKING_DIR}\")"
]

with open(nb_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(nb, f, indent=1)
print("OK: full-pipeline-server-kaggle.ipynb")

# === broll-server-kaggle.ipynb ===
nb_path = os.path.join(colab_dir, "broll-server-kaggle.ipynb")
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Cell 0 (markdown): update instructions
nb["cells"][0]["source"] = [
    "# Fako Online - B-Roll Generation Server (Kaggle)\n\n",
    "**Wan 2.1 (1.3B) Video Generation**\n\n",
    "Generates short B-Roll video clips from text prompts.\n\n",
    "### Instructions\n",
    "1. Enable **GPU T4 x2** (Settings > Accelerator)\n",
    "2. Add dataset `kingtechie/wan21-model`\n",
    "3. Run all cells in order\n",
    "4. The server will start on port 8001"
]

# Cell 1: update paths
nb["cells"][1]["source"] = [
    "# Cell 1: Setup paths\n",
    "import os\n",
    "\n",
    "WORKING_DIR = \"/kaggle/working/outputs\"\n",
    "os.makedirs(WORKING_DIR, exist_ok=True)\n",
    "\n",
    "WAN_MODEL_DIR = \"/kaggle/input/wan21-model\"\n",
    "\n",
    "print(f\"Wan Model: {WAN_MODEL_DIR}\")\n",
    "print(f\"Working dir: {WORKING_DIR}\")"
]

with open(nb_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(nb, f, indent=1)
print("OK: broll-server-kaggle.ipynb")

# === styled-scene-server-kaggle.ipynb ===
nb_path = os.path.join(colab_dir, "styled-scene-server-kaggle.ipynb")
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Cell 0 (markdown): update instructions
nb["cells"][0]["source"] = [
    "# Fako Online - Styled Scene Server (Kaggle)\n\n",
    "**AnimateDiff + ControlNet + SD 1.5**\n\n",
    "Generates consistent character scenes with style transfer.\n\n",
    "### Instructions\n",
    "1. Enable **GPU T4 x2** (Settings > Accelerator)\n",
    "2. Add datasets: `kingtechie/sd15-model`, `kingtechie/animatediff-model`\n",
    "3. Run all cells in order\n",
    "4. The server will start on port 8002"
]

# Cell 1: update paths
nb["cells"][1]["source"] = [
    "# Cell 1: Setup paths\n",
    "import os\n",
    "\n",
    "WORKING_DIR = \"/kaggle/working/outputs\"\n",
    "os.makedirs(WORKING_DIR, exist_ok=True)\n",
    "\n",
    "SD15_DIR = \"/kaggle/input/sd15-model\"\n",
    "ANIMEDIFF_DIR = \"/kaggle/input/animatediff-model\"\n",
    "\n",
    "print(f\"SD 1.5: {SD15_DIR}\")\n",
    "print(f\"AnimateDiff: {ANIMEDIFF_DIR}\")\n",
    "print(f\"Working dir: {WORKING_DIR}\")"
]

with open(nb_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(nb, f, indent=1)
print("OK: styled-scene-server-kaggle.ipynb")

print("\nAll production notebooks updated!")
