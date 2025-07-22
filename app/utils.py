import os
import torch
from typing import Optional, Generator
from PIL import Image

def get_device() -> str:
    """Determine the appropriate device to run inference on."""
    if os.environ.get("USE_GPU", "1") == "1" and torch.cuda.is_available():
        return "cuda"
    return "cpu"

def get_model_id() -> str:
    """Get the model ID from environment variables or use default."""
    return os.environ.get("MODEL_ID", "runwayml/stable-diffusion-v1-5")

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
