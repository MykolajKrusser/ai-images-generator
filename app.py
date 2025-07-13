# Apply the huggingface_hub patch first
from numpy.ma.extras import apply_along_axis

try:
    from monkey_patches import huggingface_patch
except ImportError:
    # If monkey_patches doesn't exist yet, create it
    import subprocess
    import sys
    print("Creating and applying huggingface_hub patches...")
    subprocess.run([sys.executable, "patch_cached_download.py"])
    try:
        from monkey_patches import huggingface_patch
    except ImportError:
        print("WARNING: Could not apply huggingface_hub patch. Some features may not work.")

import os
import logging
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import torch

# Try importing diffusers with better error handling
try:
    from diffusers import DiffusionPipeline
    DIFFUSERS_IMPORT_ERROR = None
except ImportError as e:
    DIFFUSERS_IMPORT_ERROR = str(e)
    logging.error(f"Failed to import DiffusionPipeline: {e}")

from io import BytesIO
from fastapi.responses import StreamingResponse
from PIL import Image

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Diffusers API", description="API for generating images using Diffusers library")

# Set environment variables to minimize tokenizers warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Check Python version
import platform
python_version = platform.python_version()
if python_version.startswith("3.13"):
    logger.warning(f"Running with Python {python_version}. Diffusers may not be fully compatible with Python 3.13.")
    logger.warning("Consider using Python 3.12 with 'python run_with_python312.py' or Docker.")

# Global pipeline variable
pipe = None

# Model loading - do this at startup
@app.on_event("startup")
async def startup_event():
    global pipe

    # Check if there was an import error
    if DIFFUSERS_IMPORT_ERROR is not None:
        logger.error(f"Cannot load model due to import error: {DIFFUSERS_IMPORT_ERROR}")
        logger.error("Please run the fix_huggingface.py script to resolve dependency issues: python fix_huggingface.py")
        return

    # Check if required packages are installed
    try:
        import diffusers
        import huggingface_hub
        logger.info(f"Using diffusers version: {diffusers.__version__}")
        logger.info(f"Using huggingface_hub version: {huggingface_hub.__version__}")
    except ImportError as e:
        logger.error(f"Missing required packages: {e}")
        logger.error("Please run the fix_huggingface.py script to resolve dependency issues")
        return

    try:
        logger.info("Loading diffusion model...")
        # Print Python path for debugging
        logger.info(f"Python path: {sys.path}")

        # Use the simplest form of model loading to avoid dependency issues
        pipe = DiffusionPipeline.from_pretrained(
            "stable-diffusion-v1-5/stable-diffusion-v1-5",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )

        # Move to GPU if available
        if torch.cuda.is_available():
            pipe.to("cuda")
            # Enable memory optimization
            pipe.enable_attention_slicing()
            logger.info("Model loaded on GPU successfully")
        else:
            logger.warning("CUDA not available, using CPU. This will be slow!")

    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        logger.error(f"Exception type: {type(e).__name__}")
        # Don't raise here, allow the app to start but endpoints will error

class TextToImageRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Text prompt for image generation")
    negative_prompt: str | None = Field(None, description="Negative prompt to guide what should not appear in the image")
    num_inference_steps: int = Field(30, ge=1, le=100, description="Number of denoising steps (higher = better quality but slower)")

@app.post("/generate/text2image")
async def generate_image(request: TextToImageRequest):
    global pipe

    if pipe is None:
        # Enhanced error message with troubleshooting steps
        raise HTTPException(status_code=503, detail="Model not loaded yet. Please run the fix_huggingface.py script with 'python fix_huggingface.py' to resolve dependency issues, then restart the application.")

    try:
        logger.info(f"Generating image with prompt: {request.prompt[:50]}...")

        # Generate the image
        result = pipe(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            num_inference_steps=request.num_inference_steps
        )

        # Check if generation was successful
        if not result.images or len(result.images) == 0:
            raise HTTPException(status_code=500, detail="Image generation failed")

        image = result.images[0]

        # Create a filename based on timestamp and part of the prompt
        import time
        import re
        from datetime import datetime

        # Create a safe filename from the prompt
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prompt_slug = re.sub(r'[^\w\s-]', '', request.prompt[:30].lower())
        prompt_slug = re.sub(r'[\s-]+', '_', prompt_slug)
        filename = f"{timestamp}_{prompt_slug}.png"

        # Ensure the assets/img directory exists
        assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'img')
        os.makedirs(assets_dir, exist_ok=True)

        # Save the image to disk
        image_path = os.path.join(assets_dir, filename)
        image.save(image_path, format='PNG')
        logger.info(f"Image saved to {image_path}")

        # Convert PIL image to bytes for response
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        logger.info("Image generated successfully")

        # Return the image as a streaming response with the saved path in headers
        response = StreamingResponse(img_byte_arr, media_type="image/png")
        response.headers["X-Image-Path"] = image_path
        return response

    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    global pipe

    # Check diffusers import status
    import_status = "success" if DIFFUSERS_IMPORT_ERROR is None else "failed"
    import_error = DIFFUSERS_IMPORT_ERROR

    # Check package versions
    try:
        import diffusers
        diffusers_version = diffusers.__version__
    except ImportError:
        diffusers_version = "Not installed"

    try:
        import huggingface_hub
        hub_version = huggingface_hub.__version__
    except ImportError:
        hub_version = "Not installed"

    # Check tokenizers
    try:
        import tokenizers
        tokenizers_version = tokenizers.__version__
        tokenizers_status = "success"
    except ImportError as e:
        tokenizers_version = "Not installed"
        tokenizers_status = f"failed: {str(e)}"

    # Check transformers
    try:
        import transformers
        transformers_version = transformers.__version__
        transformers_status = "success"
    except ImportError as e:
        transformers_version = "Not installed"
        transformers_status = f"failed: {str(e)}"

    # Python version compatibility check
    python_version = platform.python_version()
    is_compatible_python = not python_version.startswith("3.13")

    return {
        "status": "healthy" if pipe is not None else "initializing",
        "model": "stable-diffusion-v1-5",
        "cuda_available": torch.cuda.is_available(),
        "device": "cuda" if torch.cuda.is_available() else "cpu",
        "torch_version": torch.__version__,
        "python": {
            "version": python_version,
            "compatible": is_compatible_python,
            "recommendation": "Use Python 3.12 for full compatibility" if not is_compatible_python else None
        },
        "packages": {
            "diffusers": {
                "version": diffusers_version,
                "status": import_status,
                "error": import_error
            },
            "huggingface_hub": {
                "version": hub_version
            },
            "tokenizers": {
                "version": tokenizers_version,
                "status": tokenizers_status
            },
            "transformers": {
                "version": transformers_version,
                "status": transformers_status
            }
        }
    }

@app.get("/images/list")
async def list_images():
    """List all generated images in the assets/img folder"""
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'img')

    # Ensure the directory exists
    os.makedirs(assets_dir, exist_ok=True)

    # Get all image files
    image_files = [f for f in os.listdir(assets_dir) if f.endswith((".png", ".jpg", ".jpeg"))]

    # Sort by most recent first (based on filename with timestamp)
    image_files.sort(reverse=True)

    # Return the list with full paths
    return {
        "total": len(image_files),
        "images": [
            {
                "filename": filename,
                "path": f"/assets/img/{filename}",
                "created": filename.split("_")[0] if "_" in filename else "unknown"
            }
            for filename in image_files
        ]
    }

from fastapi.staticfiles import StaticFiles

# Mount the assets directory to serve static files
try:
    app.mount("/assets", StaticFiles(directory="assets"), name="assets")
    logger.info("Mounted /assets directory for static file serving")
except Exception as e:
    logger.error(f"Failed to mount assets directory: {e}")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Diffusers API server...")
    logger.info("Check /health endpoint for system status")
    uvicorn.run(app, host="0.0.0.0", port=8000)


