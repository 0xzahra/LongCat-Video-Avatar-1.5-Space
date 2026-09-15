"""Gradio UI for LongCat-Video-Avatar 1.5."""

from __future__ import annotations

import spaces  # noqa: F401 — must precede torch

import hashlib
import json
import math
import os
import shutil
import subprocess
import tempfile
import uuid
from collections import OrderedDict
from pathlib import Path

from boot import (
    ASSET_DIR,
    VOCAL_TMP,
    device,
    pipe,
    vocal_separator,
)

import gradio as gr
import imageio
import numpy as np
import torch
from PIL import Image

NEGATIVE_PROMPT = (
    "Close-up, Bright tones, overexposed, static, blurred details, subtitles, style, "
    "works, paintings, images, static, overall gray, worst quality, low quality, "
    "JPEG compression residue, ugly, incomplete, extra fingers, poorly drawn hands, "
    "poorly drawn faces, deformed, disfigured, misshapen limbs, fused fingers, "
    "still picture, messy background, three legs, many people in the background, "
    "walking backwards"
)

VOCAL_MODE_FAST = "Clean speech (fast)"
VOCAL_MODE_QUALITY = "Isolate vocals (quality)"
ACCEL_MODE_EXACT = "Exact 8-step"
ACCEL_MODE_DBCACHE = "DBCache fast"
ACCEL_MODE_DBCACHE_FASTER = "DBCache faster"
SAVE_FPS = 25
NUM_FRAMES = 125
