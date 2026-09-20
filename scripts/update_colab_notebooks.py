import json
import os

def create_download_notebook(name, dataset_id, model_dir_name, hf_model_dir, download_blocks):
    """Create a download notebook for a model."""
    download_lines = []
    for repo_id, file_list in download_blocks:
        download_lines.append("# From " + repo_id)
        download_lines.append("for file_name in " + json.dumps(file_list) + ":")
        download_lines.append('    print(f"Downloading {file_name}...")')
        download_lines.append("    try:")
        download_lines.append("        hf_hub_download(")
        download_lines.append('            repo_id="' + repo_id + '",')
        download_lines.append("            filename=file_name,")
        download_lines.append("            local_dir=MODEL_DIR")
        download_lines.append("        )")
        download_lines.append('        print("  OK")')
        download_lines.append("    except Exception as e:")
        download_lines.append('        print(f"  Error: {e}")')
        download_lines.append("    cache_dir = os.path.expanduser('~/.cache/huggingface')")
        download_lines.append("    if os.path.exists(cache_dir):")
        download_lines.append("        shutil.rmtree(cache_dir)")
        download_lines.append("")

    download_code = "\n".join(download_lines)

    size_map = {
        "kingtechie/wan21-model": "~18 GB",
        "kingtechie/animatediff-model": "~3.5 GB",
        "kingtechie/sd15-model": "~3.2 GB",
        "kingtechie/bark-model": "~4 GB",
        "kingtechie/sadtalker-model": "~2.5 GB",
        "kingtechie/wav2lip-model": "~1.5 GB",
    }
    purpose_map = {
        "kingtechie/wan21-model": "B-Roll video generation",
        "kingtechie/animatediff-model": "Styled scene generation",
        "kingtechie/sd15-model": "Image generation",
        "kingtechie/bark-model": "Emotional TTS",
        "kingtechie/sadtalker-model": "Talking head animation",
        "kingtechie/wav2lip-model": "Lip sync refinement",
    }

    size = size_map.get(dataset_id, "~unknown")
    purpose = purpose_map.get(dataset_id, "AI model")

    cell1_source = (
        "import os\n"
        "import shutil\n"
        "from huggingface_hub import hf_hub_download\n"
        "\n"
        'MODEL_DIR = "/kaggle/working/' + model_dir_name + '"\n'
        "os.makedirs(MODEL_DIR, exist_ok=True)\n"
        "\n"
        'print("=== Downloading ' + name + ' ===")\n'
    )

    verify_code = (
        "\n"
        "# Verify\n"
        "total_size = 0\n"
        "file_count = 0\n"
        "for dirpath, dirnames, filenames in os.walk(MODEL_DIR):\n"
        "    for f in filenames:\n"
        "        fp = os.path.join(dirpath, f)\n"
        "        total_size += os.path.getsize(fp)\n"
        "        file_count += 1\n"
        'print(f"Done! Files: {file_count}, Size: {total_size / 1024**3:.2f} GB")'
    )

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
                    "# Download " + name + " to Kaggle Dataset\n",
                    "\n",
                    "**Size:** " + size + " | **Purpose:** " + purpose + "\n",
                    "\n",
                    "### Instructions\n",
                    "1. Enable **Internet** (Settings gear > Internet > On)\n",
                    "2. Run all cells (Runtime > Run All)\n",
                    "3. Model auto-publishes as `" + dataset_id + "`"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [cell1_source + download_code + verify_code]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import kagglehub\n",
                    "\n",
                    'DATASET_ID = "' + dataset_id + '"\n',
                    "\n",
                    'print(f"\\n=== Publishing as dataset: {DATASET_ID} ===")\n',
                    "kagglehub.dataset_upload(\n",
                    "    DATASET_ID,\n",
                    "    MODEL_DIR,\n",
                    '    version_notes="Initial download - ' + name + '"\n',
                    ")\n",
                    'print(f"Published: https://www.kaggle.com/datasets/{DATASET_ID}")'
                ]
            }
        ]
    }
    return notebook

colab_dir = r"C:\xampp\htdocs\LocalContents\colab"

models = [
    {
        "name": "Wan 2.1",
        "dataset_id": "kingtechie/wan21-model",
        "model_dir": "wan21-model",
        "hf_model_dir": "Wan2.1-1.3B",
        "filename": "download-wan21.ipynb",
        "downloads": [
            ("Wan-AI/Wan2.1-T2V-1.3B", ["model_index.json", "scheduler/scheduler_config.json", "text_encoder/config.json", "text_encoder/pytorch_model.bin", "tokenizer/tokenizer_config.json", "tokenizer/vocab.json", "tokenizer/merges.txt", "unet/config.json", "unet/diffusion_pytorch_model.bin", "vae/config.json", "vae/diffusion_pytorch_model.bin"])
        ]
    },
    {
        "name": "AnimateDiff",
        "dataset_id": "kingtechie/animatediff-model",
        "model_dir": "animatediff-model",
        "hf_model_dir": "AnimateDiff",
        "filename": "download-animatediff.ipynb",
        "downloads": [
            ("guoyww/animatediff", ["motion_adapter/pytorch_model.bin", "motion_adapter/config.json"])
        ]
    },
    {
        "name": "Stable Diffusion 1.5",
        "dataset_id": "kingtechie/sd15-model",
        "model_dir": "sd15-model",
        "hf_model_dir": "SD1.5_Base",
        "filename": "download-sd15.ipynb",
        "downloads": [
            ("stable-diffusion-v1-5/stable-diffusion-v1-5", [
                "model_index.json",
                "scheduler/scheduler_config.json",
                "text_encoder/config.json",
                "text_encoder/pytorch_model.bin",
                "tokenizer/tokenizer_config.json",
                "tokenizer/vocab.json",
                "tokenizer/merges.txt",
                "unet/config.json",
                "unet/diffusion_pytorch_model.bin",
                "vae/config.json",
                "vae/diffusion_pytorch_model.bin"
            ])
        ]
    },
    {
        "name": "Bark TTS",
        "dataset_id": "kingtechie/bark-model",
        "model_dir": "bark-model",
        "hf_model_dir": "Bark_TTS",
        "filename": "download-bark.ipynb",
        "downloads": [
            ("suno/bark", [
                "processor.json",
                "vocab.txt",
                "merges.txt",
                "config.json",
                "generation_config.json",
                "text_2.pt",
                "coarse_2.pt",
                "fine_2.pt"
            ])
        ]
    },
    {
        "name": "SadTalker",
        "dataset_id": "kingtechie/sadtalker-model",
        "model_dir": "sadtalker-model",
        "hf_model_dir": "SadTalker",
        "filename": "download-sadtalker.ipynb",
        "downloads": [
            ("vinthony/SadTalker", [
                "mapping_00109-model.pth.tar",
                "mapping_00229-model.pth.tar"
            ]),
            ("vinthony/SadTalker-V002rc", [
                "SadTalker_V0.0.2_256.safetensors",
                "SadTalker_V0.0.2_512.safetensors"
            ])
        ]
    },
    {
        "name": "Easy-Wav2Lip",
        "dataset_id": "kingtechie/wav2lip-model",
        "model_dir": "wav2lip-model",
        "hf_model_dir": "Easy-Wav2Lip",
        "filename": "download-wav2lip.ipynb",
        "downloads": [
            ("numz/wav2lip_studio-0.2", ["Wav2lip/wav2lip_gan.pth"]),
            ("camenduru/Wav2Lip", ["face_detection/detection/sfd/s3fd.pth"])
        ]
    },
    {
        "name": "LatentSync",
        "dataset_id": "kingtechie/latentsync-model",
        "model_dir": "latentsync-model",
        "hf_model_dir": "LatentSync",
        "filename": "download-latentsync.ipynb",
        "downloads": [
            ("ByteDance/LatentSync", [
                "latentsync_unet.pt",
                "latentsync_syncnet.pt",
                "config.json",
                "whisper/tiny.pt",
                "auxiliary/2DFAN4-cd938726ad.zip",
                "auxiliary/i3d_torchscript.pt",
                "auxiliary/koniq_pretrained.pkl",
                "auxiliary/s3fd-619a316812.pth",
                "auxiliary/sfd_face.pth",
                "auxiliary/syncnet_v2.model",
                "auxiliary/vgg16-397923af.pth",
                "auxiliary/vit_g_hybrid_pt_1200e_ssv2_ft.pth"
            ])
        ]
    }
]

for m in models:
    nb = create_download_notebook(m["name"], m["dataset_id"], m["model_dir"], m["hf_model_dir"], m["downloads"])
    filepath = os.path.join(colab_dir, m["filename"])
    content = json.dumps(nb, indent=1)
    with open(filepath, "w", newline="\n") as f:
        f.write(content)
    # Validate JSON
    with open(filepath, "r") as f:
        json.load(f)
    # Check Python syntax of cell1
    cell1_src = nb["cells"][1]["source"][0]
    try:
        compile(cell1_src, "<cell1>", "exec")
        print("OK: " + m["filename"])
    except SyntaxError as e:
        print("SYNTAX ERROR: " + m["filename"] + " - " + str(e))

print("\nAll download notebooks updated!")
