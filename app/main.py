import io
import logging
import os
from typing import Optional

from fastapi import FastAPI, HTTPException, Response, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import torch
from diffusers import StableDiffusionPipeline

# Try relative import first, fall back to absolute import
try:
    from .utils import get_device, setup_seed
    from .models import get_model_id, get_available_models, get_model_trigger_words
except ImportError:
    # When running the file directly
    # Add the parent directory to sys.path to support running from app directory
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from app.utils import get_device, setup_seed
    from app.models import get_model_id, get_available_models, get_model_trigger_words

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Image Generation API")

# Model management
loaded_models = {}  # Dictionary to store loaded model pipelines
device = get_device()

class ImageGenerationRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = None
    width: int = 512
    height: int = 512
    num_inference_steps: int = 30  # Reduced default for better performance
    guidance_scale: float = 7.5
    seed: Optional[int] = None
    optimize_memory: bool = True  # Enable memory optimizations
    style: Optional[str] = None  # Style name from predefined styles
    model: Optional[str] = None  # Model key from predefined models

    # For custom styles
    prompt_prefix: Optional[str] = None
    prompt_suffix: Optional[str] = None

def load_model(model_key=None):
    """Load a Stable Diffusion model pipeline.

    Args:
        model_key: Key identifying which model to load from MODEL_DEFINITIONS

    Returns:
        The loaded pipeline
    """
    # Get the appropriate model ID
    model_id = get_model_id(model_key)

    # Check if this specific model is already loaded
    if model_id in loaded_models:
        logger.info(f"Using already loaded model: {model_id}")
        return loaded_models[model_id]

    # Load the model if not already loaded
    logger.info(f"Loading Stable Diffusion model {model_id} on {device}...")
    try:
        # Load the pipeline
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            safety_checker=None  # Disable safety checker for performance
        )
        pipe = pipe.to(device)

        # Apply optimizations for GPU
        if device == "cuda":
            pipe.enable_attention_slicing()
            # Try to enable xformers if available
            try:
                pipe.enable_xformers_memory_efficient_attention()
                logger.info("Using xformers for memory efficient attention")
            except Exception as e:
                logger.warning(f"Could not enable xformers: {e}")

        # Store the loaded model
        loaded_models[model_id] = pipe
        logger.info(f"Model {model_id} loaded successfully")
        return pipe

    except Exception as e:
        logger.error(f"Error loading model {model_id}: {str(e)}")
        raise

@app.get("/")
async def root():
    return {"message": "AI Image Generation API is running"}

@app.post("/generate")
async def generate_image(request: ImageGenerationRequest, background_tasks: BackgroundTasks):
    try:
        # Load the specified model or default
        current_pipe = load_model(request.model)

        # Apply model-specific trigger words if available
        if request.model:
            trigger_words = get_model_trigger_words(request.model)
            if trigger_words:
                # Only add trigger words if they're not already in the prompt
                for word in trigger_words:
                    if word.lower() not in request.prompt.lower():
                        request.prompt = f"{word}, {request.prompt}"
                        logger.info(f"Added model trigger word: {word}")

        logger.info(f"Generating image with prompt: {request.prompt}")

        # Set random seed if provided
        generator = setup_seed(request.seed, device)

        # Use memory efficient attention if on GPU
        if device == "cuda":
            pipe.enable_attention_slicing()

        # Apply memory optimizations if requested
        if request.optimize_memory and device == "cuda":
            from app.utils import optimize_vae_encode_decode
            optimize_vae_encode_decode(pipe, device)
            torch.cuda.empty_cache()  # Clear GPU memory

        # Generate the image
        image = current_pipe(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            width=request.width,
            height=request.height,
            num_inference_steps=request.num_inference_steps,
            guidance_scale=request.guidance_scale,
            generator=generator,
            num_images_per_prompt=1
        ).images[0]

        # Clear GPU memory after generation
        if device == "cuda":
            torch.cuda.empty_cache()

        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return StreamingResponse(img_byte_arr, media_type="image/png")

    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("startup")
def startup_event():
    # Background load the default model on startup
    # We do this in a background task to avoid slowing down app startup
    background_tasks = BackgroundTasks()
    background_tasks.add_task(load_model, None)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
