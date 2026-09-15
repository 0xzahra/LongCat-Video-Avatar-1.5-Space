"""ZeroGPU Gradio Space for LongCat-Video-Avatar 1.5 (single-person AI2V).

Downloads official weights to container disk, clones the LongCat-Video Python
package if it is not vendored, constructs the pipeline at module scope, then
runs 8-step distilled INT8 inference inside @spaces.GPU.
"""

from __future__ import annotations

import spaces  # noqa: F401  — must be imported before torch

import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from collections import OrderedDict
from pathlib import Path

os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
os.environ.setdefault("HF_MODULES_CACHE", "/tmp/hf_modules")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("GIT_LFS_SKIP_SMUDGE", "1")

ROOT = Path(__file__).parent.resolve()
WEIGHTS_DIR = Path(os.environ.get("WEIGHTS_DIR", str(ROOT / "weights")))
WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)
BASE_DIR = WEIGHTS_DIR / "LongCat-Video"
AVATAR_DIR = WEIGHTS_DIR / "LongCat-Video-Avatar-1.5"
ASSET_DIR = ROOT / "assets" / "avatar"
OFFICIAL_GIT = "https://github.com/meituan-longcat/LongCat-Video.git"


def _ensure_longcat_package() -> None:
    """Clone official inference code if longcat_video is not already present."""
    marker = ROOT / "longcat_video" / "pipeline_longcat_video_avatar.py"
    if marker.exists():
        return
    tmp = Path("/tmp/LongCat-Video-src")
    if tmp.exists():
        shutil.rmtree(tmp, ignore_errors=True)
    print("[boot] cloning meituan-longcat/LongCat-Video (source only)…", flush=True)
    subprocess.run(
        ["git", "clone", "--depth", "1", OFFICIAL_GIT, str(tmp)],
        check=True,
        env={**os.environ, "GIT_LFS_SKIP_SMUDGE": "1"},
    )
    src = tmp / "longcat_video"
    dst = ROOT / "longcat_video"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print("[boot] longcat_video package ready", flush=True)


def _ensure_example_assets() -> None:
    """Fetch the official single-person example image and audio."""
    dest = ASSET_DIR / "single"
    dest.mkdir(parents=True, exist_ok=True)
    files = {
        "man.png": "https://github.com/meituan-longcat/LongCat-Video/raw/main/assets/avatar/single/man.png",
        "man.mp3": "https://github.com/meituan-longcat/LongCat-Video/raw/main/assets/avatar/single/man.mp3",
    }
    try:
        import urllib.request

        for name, url in files.items():
            path = dest / name
            if path.exists() and path.stat().st_size > 1024:
                continue
            print(f"[boot] downloading example {name}…", flush=True)
            urllib.request.urlretrieve(url, path)
    except Exception as exc:
        print(f"[boot] example asset download skipped: {exc}", flush=True)


_ensure_longcat_package()
_ensure_example_assets()
sys.path.insert(0, str(ROOT))

import numpy as np
import torch
import torch.nn.functional as F
import gradio as gr
from huggingface_hub import snapshot_download
import imageio
from PIL import Image

if torch.cuda.is_available():
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
try:
    torch.set_float32_matmul_precision("high")
except Exception:
    pass
