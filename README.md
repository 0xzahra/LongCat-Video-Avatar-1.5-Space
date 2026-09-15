---
title: LongCat-Video-Avatar 1.5
emoji: 🎤
colorFrom: indigo
colorTo: pink
sdk: gradio
sdk_version: 5.50.0
app_file: app.py
short_description: Audio-driven talking avatar video (LongCat 1.5)
python_version: "3.12"
startup_duration_timeout: 1h
suggested_hardware: zero-a10g
tags:
  - video
  - avatar
  - talking-head
  - audio-to-video
  - longcat
license: mit
---

# LongCat-Video-Avatar 1.5

Interactive Gradio demo for [meituan-longcat/LongCat-Video-Avatar-1.5](https://huggingface.co/meituan-longcat/LongCat-Video-Avatar-1.5).

Upload a reference image and a speech clip. The Space returns a lip-synced talking-avatar video (~5 seconds) using the official INT8 DiT plus the DMD2 8-step distilled LoRA.

## What this demo runs

- Task: Audio-Text-Image-to-Video (ATI2V / AI2V)
- Audio encoder: Whisper-Large-v3
- Sampler: 8 NFE distilled (`--use_distill`)
- Quantization: INT8 DiT (`base_model_int8`)
- Hardware target: Hugging Face ZeroGPU `xlarge` (96 GB)

## Model and code

- Weights: [meituan-longcat/LongCat-Video-Avatar-1.5](https://huggingface.co/meituan-longcat/LongCat-Video-Avatar-1.5)
- Foundation VAE / text encoder: [meituan-longcat/LongCat-Video](https://huggingface.co/meituan-longcat/LongCat-Video)
- Inference code: [meituan-longcat/LongCat-Video](https://github.com/meituan-longcat/LongCat-Video)
- Technical report: [arXiv:2605.26486](https://huggingface.co/papers/2605.26486)

## Deploy this Space

```bash
hf repos create <your-hf-user>/LongCat-Video-Avatar-1.5 \
  --type space --space-sdk gradio --flavor zero-a10g --public

git clone https://huggingface.co/spaces/<your-hf-user>/LongCat-Video-Avatar-1.5
cd LongCat-Video-Avatar-1.5
# copy the files from this repository, then:
git add .
git commit -m "Add LongCat-Video-Avatar 1.5 demo"
git push
```

ZeroGPU `xlarge` is required for the INT8 8-step path used here. Free accounts may host up to two ZeroGPU Spaces.

## License

Model weights and official code are released under MIT by the Meituan LongCat team. This Space is a demo wrapper and does not grant trademark rights to the Meituan or LongCat names.
