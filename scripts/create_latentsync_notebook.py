import json
import os

notebook = {
    "nbformat": 4,
    "nbformat_minor": 0,
    "metadata": {
        "kaggle": {"accelerator": "cpu"},
        "kernelspec": {"name": "python3", "display_name": "Python 3"},
        "language_info": {"name": "python"}
    },
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Download LatentSync to Kaggle Dataset\n",
                "\n",
                "**Size:** ~8 GB | **Purpose:** Lip sync via audio-conditioned latent diffusion\n",
                "\n",
                "### Instructions\n",
                "1. Enable **Internet** (Settings gear > Internet > On)\n",
                "2. Run all cells (Runtime > Run All)\n",
                "3. Model auto-publishes as `kingtechie/latentsync-model`"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "import shutil\n",
                "import kagglehub\n",
                "from huggingface_hub import hf_hub_download\n",
                "\n",
                "MODEL_DIR = \"/kaggle/working/latentsync-model\"\n",
                "os.makedirs(MODEL_DIR, exist_ok=True)\n",
                "\n",
                "print(\"=== Downloading LatentSync (~8GB) ===\")\n",
                "\n",
                "# Core model files\n",
                "core_files = [\n",
                "    \"latentsync_unet.pt\",\n",
                "    \"latentsync_syncnet.pt\",\n",
                "    \"config.json\",\n",
                "]\n",
                "\n",
                "# Whisper model\n",
                "whisper_files = [\n",
                "    \"whisper/tiny.pt\",\n",
                "]\n",
                "\n",
                "# Auxiliary files for inference\n",
                "auxiliary_files = [\n",
                "    \"auxiliary/2DFAN4-cd938726ad.zip\",\n",
                "    \"auxiliary/i3d_torchscript.pt\",\n",
                "    \"auxiliary/koniq_pretrained.pkl\",\n",
                "    \"auxiliary/s3fd-619a316812.pth\",\n",
                "    \"auxiliary/sfd_face.pth\",\n",
                "    \"auxiliary/syncnet_v2.model\",\n",
                "    \"auxiliary/vgg16-397923af.pth\",\n",
                "    \"auxiliary/vit_g_hybrid_pt_1200e_ssv2_ft.pth\",\n",
                "]\n",
                "\n",
                "all_files = core_files + whisper_files + auxiliary_files\n",
                "\n",
                "for file_name in all_files:\n",
                "    print(f\"Downloading {file_name}...\")\n",
                "    try:\n",
                "        hf_hub_download(\n",
                "            repo_id=\"ByteDance/LatentSync\",\n",
                "            filename=file_name,\n",
                "            local_dir=MODEL_DIR\n",
                "        )\n",
                "        print(\"  OK\")\n",
                "    except Exception as e:\n",
                "        print(f\"  Error: {e}\")\n",
                "    # Clean HF cache after each file to stay under 19.5GB\n",
                "    cache_dir = os.path.expanduser('~/.cache/huggingface')\n",
                "    if os.path.exists(cache_dir):\n",
                "        shutil.rmtree(cache_dir)\n",
                "\n",
                "# Verify\n",
                "total_size = 0\n",
                "file_count = 0\n",
                "for dirpath, dirnames, filenames in os.walk(MODEL_DIR):\n",
                "    for f in filenames:\n",
                "        fp = os.path.join(dirpath, f)\n",
                "        total_size += os.path.getsize(fp)\n",
                "        file_count += 1\n",
                "print(f\"\\nDone! Files: {file_count}, Size: {total_size / 1024**3:.2f} GB\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "print(\"\\n=== Publishing to Kaggle Datasets ===\")\n",
                "kagglehub.dataset_upload(\n",
                "    handle=\"kingtechie/latentsync-model\",\n",
                "    local_dataset_dir=MODEL_DIR,\n",
                "    version_notes=\"LatentSync Full Download\"\n",
                ")\n",
                "print(\"Upload successful!\")"
            ]
        }
    ]
}

push_dir = r"C:\xampp\htdocs\LocalContents\kaggle-push"
filepath = os.path.join(push_dir, "download-latentsync.ipynb")

content = json.dumps(notebook, indent=1)
with open(filepath, "w", newline="\n") as f:
    f.write(content)

# Validate
with open(filepath, "r") as f:
    json.load(f)

cell1_src = notebook["cells"][1]["source"][0]
try:
    compile(cell1_src, "<cell1>", "exec")
    print("OK: download-latentsync.ipynb (Python valid)")
except SyntaxError as e:
    print(f"SYNTAX ERROR: {e}")
