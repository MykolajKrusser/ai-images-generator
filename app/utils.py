import os
import torch
from typing import Optional, Generator
from PIL import Image

def get_device() -> str:
    """Determine the appropriate device to run inference on."""
    use_gpu_setting = os.environ.get("USE_GPU", "1")
    cuda_available = torch.cuda.is_available()

    print(f"GPU Setting: USE_GPU={use_gpu_setting}, CUDA Available: {cuda_available}")
    if use_gpu_setting == "1" and cuda_available:
        # If CUDA is available, log GPU information
        if cuda_available:
            print(f"GPU detected: {torch.cuda.get_device_name(0)}")
            print(f"CUDA Version: {torch.version.cuda}")
        return "cuda"

    if not cuda_available:
        print("No CUDA-compatible GPU detected. Running on CPU.")
    elif use_gpu_setting != "1":
        print("GPU usage disabled by USE_GPU environment variable. Running on CPU.")

    return "cpu"

def setup_seed(seed: Optional[int] = None, device: str = "cuda") -> Optional[Generator]:
    """Set up a generator with a seed for reproducible image generation."""
    if seed is not None:
        return torch.Generator(device=device).manual_seed(seed)
    return None

def resize_image(image: Image.Image, max_size: int = 1024) -> Image.Image:
    """Resize image while maintaining aspect ratio."""
    width, height = image.size

    if width <= max_size and height <= max_size:
        return image

    if width > height:
        new_width = max_size
        new_height = int(height * (max_size / width))
    else:
        new_height = max_size
        new_width = int(width * (max_size / height))

    return image.resize((new_width, new_height), Image.LANCZOS)


def optimize_vae_encode_decode(pipe, device: str):
    """Optimize VAE encode/decode functions for better performance."""
    if device == "cuda":
        # Move VAE to CPU during encode/decode to save VRAM
        # This is beneficial for larger images
        vae = pipe.vae

        original_forward = vae.forward

        def forward_with_optimization(*args, **kwargs):
            # Move VAE to CPU temporarily
            vae_device = vae.device
            vae.to("cpu")
            # Clear CUDA cache
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

            # Run forward pass
            output = original_forward(*args, **kwargs)

            # Move VAE back to original device
            vae.to(vae_device)
            return output

        # Replace forward method
        vae.forward = forward_with_optimization