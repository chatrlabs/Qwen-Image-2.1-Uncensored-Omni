"""Text-to-image and reference-image editing with the quantized ChatR Labs Omni checkpoints."""
import argparse
from pathlib import Path

BASE = "Qwen/Qwen-Image-2.1"


def build_transformer(args):
    """Return a quantized transformer, or None to use the base BF16 weights."""
    import torch
    from diffusers import QwenImage21Transformer2DModel

    if args.gguf:
        from diffusers import GGUFQuantizationConfig

        return QwenImage21Transformer2DModel.from_single_file(
            str(args.gguf),
            quantization_config=GGUFQuantizationConfig(compute_dtype=torch.bfloat16),
            config=BASE,
            subfolder="transformer",
            torch_dtype=torch.bfloat16,
        )

    if args.transformer_repo:
        if not args.subfolder:
            raise SystemExit("--transformer-repo needs --subfolder (e.g. qwen-image-2.1-step90000-FP8-torchao)")
        dtype = torch.float16 if "INT8-bnb" in args.subfolder else torch.bfloat16
        return QwenImage21Transformer2DModel.from_pretrained(
            args.transformer_repo, subfolder=args.subfolder, torch_dtype=dtype
        )

    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--image", type=Path, nargs="*", default=[],
                        help="Reference image(s) for editing. Omit for text-to-image.")
    parser.add_argument("--output", type=Path, default=Path("output.png"))
    parser.add_argument("--gguf", type=Path,
                        help="Local GGUF file, e.g. qwen-image-2.1-step32000-Q5_K_M.gguf")
    parser.add_argument("--transformer-repo", default=None,
                        help="Hugging Face repo holding a quantized transformer folder.")
    parser.add_argument("--subfolder", default=None,
                        help="Folder inside --transformer-repo, e.g. qwen-image-2.1-step32000-NF4-bnb")
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=1024)
    parser.add_argument("--output-resolution", type=int, default=1024)
    parser.add_argument("--steps", type=int, default=35)
    parser.add_argument("--cfg", type=float, default=5.0)
    parser.add_argument("--negative", default=" ")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", choices=["offload", "cuda"], default="offload",
                        help="CPU offload by default; cuda keeps the whole pipeline on one GPU.")
    args = parser.parse_args()

    if args.gguf and not args.gguf.is_file():
        parser.error(f"GGUF file not found: {args.gguf}")
    if args.transformer_repo and not args.subfolder:
        parser.error("--transformer-repo requires --subfolder")

    import torch
    from diffusers import QwenImage21Pipeline
    from PIL import Image, ImageOps

    transformer = build_transformer(args)
    kwargs = {"torch_dtype": torch.bfloat16}
    if transformer is not None:
        kwargs["transformer"] = transformer
        if "INT8-bnb" in (args.subfolder or ""):
            kwargs["torch_dtype"] = torch.float16

    pipe = QwenImage21Pipeline.from_pretrained(BASE, **kwargs)
    if args.device == "offload":
        pipe.enable_model_cpu_offload()
    else:
        pipe.to("cuda")

    references = []
    for path in args.image:
        with Image.open(path) as image:
            references.append(ImageOps.exif_transpose(image).convert("RGBA"))

    call = dict(
        prompt=args.prompt,
        negative_prompt=args.negative if args.negative.strip() else " ",
        width=args.width,
        height=args.height,
        output_resolution=args.output_resolution,
        num_inference_steps=args.steps,
        true_cfg_scale=args.cfg,
        use_kv_cache=True,
        generator=torch.Generator("cuda").manual_seed(args.seed),
    )
    if references:
        call["image"] = references

    with torch.inference_mode():
        image = pipe(**call).images[0]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output)
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
