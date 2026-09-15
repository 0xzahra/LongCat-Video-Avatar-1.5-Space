# Deploy to Hugging Face Spaces

This repository is a complete Gradio Space for
[meituan-longcat/LongCat-Video-Avatar-1.5](https://huggingface.co/meituan-longcat/LongCat-Video-Avatar-1.5).

## 1. Log in

```bash
hf auth login
```

Open the printed URL and enter the one-time code.

## 2. Create the Space

```bash
hf repos create <your-hf-username>/LongCat-Video-Avatar-1.5 \
  --type space \
  --space-sdk gradio \
  --flavor zero-a10g \
  --public
```

ZeroGPU (`zero-a10g`) is required. The generator requests the `xlarge` slice (96 GB).

## 3. Push these files

```bash
git clone https://huggingface.co/spaces/<your-hf-username>/LongCat-Video-Avatar-1.5
cd LongCat-Video-Avatar-1.5
cp /path/to/LongCat-Video-Avatar-1.5-Space/{app.py,requirements.txt,README.md,.gitattributes,.gitignore} .
git add app.py requirements.txt README.md .gitattributes .gitignore
git commit -m "Add LongCat-Video-Avatar 1.5 ZeroGPU demo"
git push
```

First boot downloads the foundation VAE/text encoder plus the Avatar 1.5 INT8 weights and can take 15–40 minutes.

## Alternative: duplicate the proven live demo

If you only need a running generator immediately:

https://huggingface.co/spaces/victor/LongCat-Video-Avatar-1.5

Use **Duplicate this Space** and attach ZeroGPU.
