"""Models management for the image generation application."""

import os
import logging
import json
from pathlib import Path
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default model ID
DEFAULT_MODEL_ID = "runwayml/stable-diffusion-v1-5"

# Model definitions with metadata
MODEL_DEFINITIONS = {
    "sd-v1-5": {
        "model_id": "runwayml/stable-diffusion-v1-5",
        "name": "Stable Diffusion v1.5",
        "description": "Original Stable Diffusion v1.5 model - versatile and well-balanced",
        "resolution": 512,
        "trigger_words": [],
        "vram_requirements": "4+ GB"
    },
    "sd-v2-1": {
        "model_id": "stabilityai/stable-diffusion-2-1",
        "name": "Stable Diffusion v2.1",
        "description": "Improved version with better image quality and prompt understanding",
        "resolution": 768,
        "trigger_words": [],
        "vram_requirements": "6+ GB"
    },
    "sd-xl-base": {
        "model_id": "stabilityai/stable-diffusion-xl-base-1.0",
        "name": "Stable Diffusion XL Base",
        "description": "High-resolution model with superior detail and composition",
        "resolution": 1024,
        "trigger_words": [],
        "vram_requirements": "10+ GB"
    },
    "dreamshaper": {
        "model_id": "Lykon/dreamshaper-7",
        "name": "DreamShaper v7",
        "description": "Creative model that produces vibrant, artistic images",
        "resolution": 512,
        "trigger_words": ["dreamshaper style"],
        "vram_requirements": "4+ GB"
    },
    "realistic-vision": {
        "model_id": "SG161222/Realistic_Vision_V5.1_noVAE",
        "name": "Realistic Vision v5.1",
        "description": "Photorealistic model with excellent facial and detail rendering",
        "resolution": 512,
        "trigger_words": [],
        "vram_requirements": "4+ GB"
    },
    "anything-v5": {
        "model_id": "stablediffusionapi/anything-v5",
        "name": "Anything v5",
        "description": "Anime-focused model with excellent character rendering",
        "resolution": 512,
        "trigger_words": ["anime style"],
        "vram_requirements": "4+ GB"
    },
    "openjourney": {
        "model_id": "prompthero/openjourney",
        "name": "OpenJourney",
        "description": "Midjourney-inspired style with vibrant, artistic renderings",
        "resolution": 512,
        "trigger_words": ["mdjrny-v4 style"],
        "vram_requirements": "4+ GB"
    }
}

# Store loaded model pipelines
loaded_models = {}

# Load custom models if available
def load_custom_models_from_file():
    """Load custom model definitions from file."""
    custom_models_file = Path(__file__).parent / "custom_models.json"

    if not custom_models_file.exists():
        return

    try:
        with open(custom_models_file, 'r') as f:
            custom_models = json.load(f)

        for key, model in custom_models.items():
            MODEL_DEFINITIONS[key] = model
            logger.info(f"Loaded custom model definition: {key} - {model['name']}")
    except Exception as e:
        logger.error(f"Error loading custom models: {e}")

# Load custom models on module import
try:
    load_custom_models_from_file()
except Exception as e:
    logger.error(f"Failed to load custom models: {e}")

def get_model_id(model_key: Optional[str] = None) -> str:
    """Get the Hugging Face model ID for the specified model key.

    Args:
        model_key: Key identifying the model in MODEL_DEFINITIONS

    Returns:
        str: Hugging Face model ID
    """
    # First check environment variable
    env_model_id = os.environ.get("MODEL_ID")
    if env_model_id:
        return env_model_id

    # Then check if a valid model key was provided
    if model_key and model_key in MODEL_DEFINITIONS:
        return MODEL_DEFINITIONS[model_key]["model_id"]

    # Finally fall back to default
    return DEFAULT_MODEL_ID

def get_available_models() -> Dict[str, Dict]:
    """Return a dictionary of available models with their metadata."""
    return {key: {
        "name": model["name"],
        "description": model["description"],
        "resolution": model["resolution"],
        "vram_requirements": model["vram_requirements"]
    } for key, model in MODEL_DEFINITIONS.items()}

def add_custom_model(key: str, model_id: str, name: str, description: str, 
                   resolution: int = 512, trigger_words: List[str] = None,
                   vram_requirements: str = "Unknown") -> None:
    """Add a custom model definition.

    Args:
        key: A unique identifier for the model
        model_id: Hugging Face model ID or path to local model
        name: Display name for the model
        description: Brief description of the model
        resolution: Optimal resolution for the model (default: 512)
        trigger_words: List of words that enhance the model's performance
        vram_requirements: Estimated VRAM needed (e.g., "4+ GB")
    """
    MODEL_DEFINITIONS[key] = {
        "model_id": model_id,
        "name": name,
        "description": description,
        "resolution": resolution,
        "trigger_words": trigger_words or [],
        "vram_requirements": vram_requirements
    }
    logger.info(f"Added custom model: {key} - {name} ({model_id})")

def get_model_trigger_words(model_key: str) -> List[str]:
    """Get any trigger words recommended for a specific model.

    Some models work better with specific words in the prompt.

    Args:
        model_key: The model key to get trigger words for

    Returns:
        List of trigger words for the model
    """
    if model_key in MODEL_DEFINITIONS:
        return MODEL_DEFINITIONS[model_key].get("trigger_words", [])
    return []

def get_optimal_resolution(model_key: str) -> int:
    """Get the optimal resolution for a specific model.

    Args:
        model_key: The model key to get the resolution for

    Returns:
        int: The optimal resolution (width/height) for the model
    """
    if model_key in MODEL_DEFINITIONS:
        return MODEL_DEFINITIONS[model_key].get("resolution", 512)
    return 512
