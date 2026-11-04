# ChatR Labs Uncensored Omni — Quantized (Qwen-Image-2.1)

[![Try the Playground](https://img.shields.io/badge/Playground-Try_it_live-2563eb?style=for-the-badge)](https://chatrlabs.com/)
[![Hugging Face](https://img.shields.io/badge/Hugging_Face-Weights-ffcc4d?style=for-the-badge)](https://huggingface.co/chatrlabs)

**The Omni checkpoints, quantized for ComfyUI and Diffusers. Text-to-image and image editing in one model.**

This repository holds the **documentation, inference code and checksums** for the quantized ChatR Labs Omni
release of [Qwen/Qwen-Image-2.1](https://huggingface.co/Qwen/Qwen-Image-2.1). Weights live on Hugging Face.

- **[chatrlabs/Qwen-Image-2.1-Uncensored-Omni](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni)** — 78 GB

Each repository is a rank-128 adapter merged into the base transformer at **LoRA strength 1.0**, then quantized.
Quantized transformer weights only: the text encoder, processor and VAE come from the base repository.

## Try it online

**[Open the Playground →]([https://chatrlabs.com/playground](https://chatrlabs.com/playground))**

No account is required. Choose **Text to Image** or **Image Editing**, enter a prompt, and generate. The editing
interface accepts one to three reference images. Requests share a queue.

## Download

| Build | Format | Layout | Size | Download |
| --- | --- | --- | ---: | --- |
| **BF16** | GGUF BF16 | 297 | 14.23 GB | [file](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni/resolve/main/qwen-image-2.1-step90000-BF16.gguf) |
| **Q8_0** | GGUF Q8_0 | 297 | 7.69 GB | [file](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni/resolve/main/qwen-image-2.1-step90000-Q8_0.gguf) |
| **Q6_K** | GGUF Q6_K | 297 | 6.00 GB | [file](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni/resolve/main/qwen-image-2.1-step90000-Q6_K.gguf) |
| **Q5_K_M** | GGUF Q5_K_M | 297 | 5.21 GB | [file](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni/resolve/main/qwen-image-2.1-step90000-Q5_K_M.gguf) |
| **Q4_K_M** | GGUF Q4_K_M | 297 | 4.47 GB | [file](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni/resolve/main/qwen-image-2.1-step90000-Q4_K_M.gguf) |
| **Q4_0** | GGUF Q4_0 | 297 | 4.20 GB | [file](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni/resolve/main/qwen-image-2.1-step90000-Q4_0.gguf) |
| **FP8** | FP8 E4M3, Comfy | 265 | 7.12 GB | [file](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni/resolve/main/qwen-image-2.1-step90000-FP8-comfy.safetensors) |
| **INT8 ConvRot** | INT8 ConvRot, Comfy | 265 | 7.26 GB | [file](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni/resolve/main/qwen-image-2.1-step90000-INT8-ConvRot-comfy.safetensors) |
| **NVFP4** | NVFP4, Comfy | 265 | 4.20 GB | [file](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni/resolve/main/qwen-image-2.1-step90000-NVFP4-comfy.safetensors) |
| **FP8 (torchao)** | FP8, Diffusers | 297 | 6.70 GB | [folder](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni/tree/main/qwen-image-2.1-step90000-FP8-torchao) |
| **NF4** | NF4, Diffusers | 297 | 3.50 GB | [folder](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni/tree/main/qwen-image-2.1-step90000-NF4-bnb) |
| **INT8 (bitsandbytes)** | INT8, Diffusers | 297 | 6.70 GB | [folder](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni/tree/main/qwen-image-2.1-step90000-INT8-bnb) |

File integrity information is in [SHA256SUMS](./SHA256SUMS).

### Which build should I use?

- **ComfyUI, one file, both workflows** → any **GGUF**. It also loads in Diffusers via `from_single_file`.
- **ComfyUI, native quant ops** → **FP8**, **INT8 ConvRot** or **NVFP4**.
- **Diffusers, smallest download** → **NF4** (needs `bitsandbytes`).
- **Diffusers, best fidelity** → **FP8 (torchao)** (needs `torchao`).
- **Maximum fidelity overall** → **BF16 GGUF** or **Q8_0**.

The `297` and `265` layouts are not interchangeable. `265` uses the fused `img_mlp.gate_up` projection ComfyUI
expects; `297` keeps the separate `gate_layer` / `proj` pair Diffusers expects. Loading a `265` file in Diffusers,
or a `297` Diffusers-layout file through ComfyUI's native loader, will fail.

## Recommended settings

| Setting | Starting value |
| --- | --- |
| Base components | Text encoder, processor and VAE from `Qwen/Qwen-Image-2.1` |
| Sampling steps | **35** |
| True CFG scale | **5.0** for text-to-image and editing |
| Sampler | `er_sde` with the `simple` scheduler (ComfyUI) |
| Negative prompt | A single space: `" "` |
| Output resolution | `768 × 1152` or `1024 × 1024` |
| KV cache | Enabled |

An omitted or empty negative prompt disables true CFG even when `true_cfg_scale` is greater than 1. Use a single
space if you do not need a specific negative prompt. This is a regular LoRA merge; it does not provide few-step
distillation.

## Usage with ComfyUI

```
ComfyUI/models/
├── diffusion_models/    qwen-image-2.1-step90000-Q5_K_M.gguf
├── text_encoders/       <Qwen-Image-2.1 text encoder>
└── vae/                 <Qwen-Image-2.1 VAE>
```

- **GGUF:** `Unet Loader (GGUF)` → pick the file. Works for both text-to-image and editing.
- **Comfy native:** `Load Diffusion Model` → pick a `-comfy.safetensors` file.
- **Editing:** encode the reference image with `Text Encoder (Qwen-Image)` in edit mode; the latent comes from that node.

## Usage with Diffusers

Install the dependencies in [requirements.txt](./requirements.txt).

### GGUF

```python
import torch
from diffusers import QwenImage21Pipeline, QwenImage21Transformer2DModel, GGUFQuantizationConfig

transformer = QwenImage21Transformer2DModel.from_single_file(
    "qwen-image-2.1-step90000-Q5_K_M.gguf",
    quantization_config=GGUFQuantizationConfig(compute_dtype=torch.bfloat16),
    config="Qwen/Qwen-Image-2.1",
    subfolder="transformer",
    torch_dtype=torch.bfloat16,
)
pipe = QwenImage21Pipeline.from_pretrained(
    "Qwen/Qwen-Image-2.1", transformer=transformer, torch_dtype=torch.bfloat16,
)
pipe.enable_model_cpu_offload()
```

### FP8 / NF4 / INT8 folders

```python
import torch
from diffusers import QwenImage21Pipeline, QwenImage21Transformer2DModel

transformer = QwenImage21Transformer2DModel.from_pretrained(
    "chatrlabs/Qwen-Image-2.1-Uncensored-Omni",
    subfolder="qwen-image-2.1-step90000-FP8-torchao",
    torch_dtype=torch.bfloat16,
)
pipe = QwenImage21Pipeline.from_pretrained(
    "Qwen/Qwen-Image-2.1", transformer=transformer, torch_dtype=torch.bfloat16,
)
```

The INT8 build stores its non-quantized tensors in FP16, so load both the transformer and the pipeline with
`torch_dtype=torch.float16`.

### Text to image

```python
image = pipe(
    prompt="A blue ceramic mug on a wooden table by a window, soft morning light, product photography",
    negative_prompt=" ",
    width=1024,
    height=1024,
    num_inference_steps=35,
    true_cfg_scale=5.0,
    use_kv_cache=True,
    generator=torch.Generator("cuda").manual_seed(42),
).images[0]
image.save("generated.png")
```

### Image editing

```python
from PIL import Image

reference = Image.open("generated.png").convert("RGBA")
image = pipe(
    image=[reference],
    prompt="Change the mug to green, keep everything else unchanged",
    negative_prompt=" ",
    width=1024,
    height=1024,
    output_resolution=1024,
    num_inference_steps=35,
    true_cfg_scale=5.0,
    use_kv_cache=True,
    generator=torch.Generator("cuda").manual_seed(45),
).images[0]
image.save("edited.png")
```

Keep VAE tiling off: tiled decoding adds visible vertical colour streaks.

## Command line

[inference.py](./inference.py) wraps the examples above and accepts any build:

```bash
# text to image, GGUF
python inference.py --gguf qwen-image-2.1-step90000-Q5_K_M.gguf \
    --prompt "A blue ceramic mug on a wooden table" --output generated.png

# text to image, Diffusers FP8 folder
python inference.py --transformer-repo chatrlabs/Qwen-Image-2.1-Uncensored-Omni \
    --subfolder qwen-image-2.1-step90000-FP8-torchao \
    --prompt "A blue ceramic mug on a wooden table" --output generated.png

# editing
python inference.py --gguf qwen-image-2.1-step90000-Q5_K_M.gguf \
    --image generated.png --prompt "Change the mug to green" --output edited.png
```

## Memory and performance

Measured on a single RTX 5090 (32 GB), 35 steps, `er_sde`, 768 × 1152:

| Build | Peak VRAM | Time per image |
| --- | ---: | ---: |
| BF16 | ~14 GB | ~28 s |
| Q5_K_M | ~8 GB | ~28 s |
| NVFP4 | ~4 GB | ~30 s |

Editing and ControlNet runs add reference and control latents; budget a few GB more. The BF16 pipeline does not
fit comfortably beside a full text encoder on a 24 GB card — use CPU offload there.

These are individual timings, not comparative quality benchmarks.

## Quantization details

| Property | Value |
| --- | --- |
| Base | Qwen-Image-2.1 |
| Adapter | ChatR Labs rank-128 Omni LoRA |
| Merge strength | **1.0** |
| Training checkpoint | Step 90,000 |
| Adapted modules | 224 |
| Diffusers-layout tensors | 297 |
| Comfy-layout tensors | 265 |
| GGUF tool | ComfyUI-GGUF `convert.py`, per-block quantization |
| Comfy FP8 | `TensorCoreFP8E4M3Layout`, per-tensor scale, 229 modules |
| Comfy INT8 ConvRot | `convrot`, group size 256, 224 modules |
| Comfy NVFP4 | `TensorCoreNVFP4Layout`, 192 fused modules |
| Diffusers FP8 | torchao `Float8WeightOnlyConfig`, per-row scale |
| Diffusers NF4 | bitsandbytes 4-bit NF4 with double quantization |
| Diffusers INT8 | bitsandbytes 8-bit |

The text encoder and VAE are untouched in every build; differences between builds come from the transformer only.

## About "uncensored"

The checkpoints and example code do not add a prompt filter or output safety checker. The name describes the
intended release, not a guarantee that every requested concept will be rendered. Results depend on the prompt,
the build you load, and the application running it.

## Source and license

- **Released by:** [ChatR Labs](https://huggingface.co/chatrlabs)
- **Base model:** [Qwen/Qwen-Image-2.1](https://huggingface.co/Qwen/Qwen-Image-2.1)
- **Inference:** [Hugging Face Diffusers](https://github.com/huggingface/diffusers)
- **Modification:** ChatR Labs merged a rank-128 adapter into the base transformer at strength 1.0 and produced
  GGUF, FP8, INT8, NVFP4 and NF4 builds. This repository distributes documentation and code only.
- **License:** [Qwen Research License Agreement](./LICENSE), with attribution in [Notice](./Notice). Use is
  limited to non-commercial research and evaluation unless separately licensed by the upstream rights holder.
- **Checksums:** [SHA256SUMS](./SHA256SUMS)

**Built with Qwen.** This is a community fine-tune by ChatR Labs, independent of the upstream Qwen team.

## Infrastructure Support

GPU compute used for the development and evaluation of this release was provided by [Chatr AI](https://thechatr.ai).

We thank the Chatr AI team for supporting this research release.
