#!/usr/bin/env python3
"""
Kaggle Dataset Upload Helper
============================

Uploads model checkpoints to Kaggle datasets using the Kaggle CLI.

Usage:
    python kaggle-upload.py --source /path/to/models --dataset user/dataset-name --title "My Models" --action create

Prerequisites:
    pip install kaggle
    Place your kaggle.json API token at ~/.kaggle/kaggle.json
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Upload model checkpoints to Kaggle datasets.",
        epilog="""
Examples:
  # Upload Bark + SadTalker + Easy-Wav2Lip (~8.5GB)
  python kaggle-upload.py \\
    --source /path/to/audio-models \\
    --dataset username/bark-sadtalker-wav2lip \\
    --title "Bark + SadTalker + Easy-Wav2Lip Models" \\
    --action create

  # Upload Wan 2.1 + AnimateDiff + SD 1.5 (~13.2GB)
  python kaggle-upload.py \\
    --source /path/to/video-models \\
    --dataset username/wan-animatediff-sd15 \\
    --title "Wan 2.1 + AnimateDiff + SD 1.5 Models" \\
    --action update
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--token",
        default=os.path.expanduser("~/.kaggle/kaggle.json"),
        help="Path to kaggle.json API token (default: ~/.kaggle/kaggle.json)"
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Source directory containing models to upload"
    )
    parser.add_argument(
        "--dataset",
        required=True,
        help='Kaggle dataset slug (e.g., "username/dataset-name")'
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Dataset title"
    )
    parser.add_argument(
        "--action",
        choices=["create", "update"],
        required=True,
        help='"create" (new dataset) or "update" (existing dataset)'
    )
    return parser.parse_args()


def check_kaggle_cli():
    """Check if kaggle CLI is installed."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "kaggle", "--version"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("[OK] Kaggle CLI found:", result.stdout.strip())
            return True
    except FileNotFoundError:
        pass

    print("[ERROR] Kaggle CLI is not installed.")
    print("Install it with: pip install kaggle")
    return False


def check_token(token_path):
    """Verify the Kaggle API token exists and is valid JSON."""
    if not os.path.isfile(token_path):
        print(f"[ERROR] Token file not found: {token_path}")
        print("Download your token from https://www.kaggle.com/settings/account#api")
        return False

    try:
        with open(token_path, "r") as f:
            data = json.load(f)
        for key in ["username", "key"]:
            if key not in data:
                print(f"[ERROR] Token file is missing '{key}' field.")
                return False
        print(f"[OK] Token file loaded (user: {data['username']})")
        return True
    except json.JSONDecodeError:
        print(f"[ERROR] Token file is not valid JSON: {token_path}")
        return False


def check_source(source_path):
    """Verify the source directory exists and is not empty."""
    if not os.path.isdir(source_path):
        print(f"[ERROR] Source directory does not exist: {source_path}")
        return False

    items = list(Path(source_path).iterdir())
    if not items:
        print(f"[ERROR] Source directory is empty: {source_path}")
        return False

    total_size = sum(
        f.stat().st_size for f in Path(source_path).rglob("*") if f.is_file()
    )
    total_gb = total_size / (1024 ** 3)
    file_count = sum(1 for f in Path(source_path).rglob("*") if f.is_file())

    print(f"[OK] Source directory: {source_path}")
    print(f"     {file_count} file(s), {total_gb:.1f} GB total")
    return True


def create_metadata(dataset_slug, title, source_path):
    """Create dataset-metadata.json for the upload."""
    metadata = {
        "title": title,
        "id": dataset_slug,
        "licenses": [
            {
                "name": "CC0-1.0"
            }
        ]
    }

    metadata_path = os.path.join(source_path, "dataset-metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"[OK] Created metadata: {metadata_path}")
    return metadata_path


def upload_dataset(token_path, source_path, dataset_slug, action):
    """Upload the dataset using Kaggle CLI."""
    cmd = [
        sys.executable, "-m", "kaggle", "datasets",
        "-d", dataset_slug,
        "-p", source_path,
        "--dir-mode", "zip",
        "--force"
    ]

    if action == "update":
        cmd.append("-u")

    print(f"\n[UPLOAD] Running: {' '.join(cmd)}")
    print(f"         Action: {action}")
    print(f"         Target: kaggle.com/datasets/{dataset_slug}\n")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("[SUCCESS] Upload completed!")
        if result.stdout:
            print(result.stdout)
        return True
    else:
        print("[ERROR] Upload failed.")
        if result.stderr:
            print(result.stderr)
        if result.stdout:
            print(result.stdout)
        return False


def main():
    """Main entry point."""
    args = parse_args()

    print("=== Kaggle Dataset Upload ===\n")

    if not check_kaggle_cli():
        sys.exit(1)

    if not check_token(args.token):
        sys.exit(1)

    if not check_source(args.source):
        sys.exit(1)

    create_metadata(args.dataset, args.title, args.source)

    success = upload_dataset(
        args.token, args.source, args.dataset, args.action
    )

    if success:
        print(f"\nView your dataset at: https://www.kaggle.com/datasets/{args.dataset}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
