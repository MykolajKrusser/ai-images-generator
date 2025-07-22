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
    from .utils import get_device, get_model_id, setup_seed
except ImportError:
    # When running the file directly
    from utils import get_device, get_model_id, setup_seed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Image Generation API")

# Will be loaded on first request
pipe = None
device = get_device()

class ImageGenerationRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = None
    width: int = 512
    height: int = 512
    num_inference_steps: int = 50
    guidance_scale: float = 7.5
    seed: Optional[int] = None

def load_model():
    global pipe
    if pipe is None:
        model_id = get_model_id()
        logger.info(f"Loading Stable Diffusion model {model_id} on {device}...")
        try:
            pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32
            )
            pipe = pipe.to(device)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

@app.get("/")
async def root():
    return {"message": "AI Image Generation API is running"}

@app.post("/generate")
async def generate_image(request: ImageGenerationRequest, background_tasks: BackgroundTasks):
    try:
        # Ensure model is loaded
        if pipe is None:
            load_model()

        logger.info(f"Generating image with prompt: {request.prompt}")

        # Set random seed if provided
        generator = setup_seed(request.seed, device)

        # Generate the image
        image = pipe(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            width=request.width,
            height=request.height,
            num_inference_steps=request.num_inference_steps,
            guidance_scale=request.guidance_scale,
            generator=generator
        ).images[0]

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
    # Background load model on startup
    # We do this in a background task to avoid slowing down app startup
    background_tasks = BackgroundTasks()
    background_tasks.add_task(load_model)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
