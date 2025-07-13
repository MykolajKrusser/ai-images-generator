import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import torch
from io import BytesIO
from fastapi.responses import StreamingResponse
from PIL import Image

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Diffusers API", description="API for generating images using Diffusers library")

# Set environment variables
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import os
import logging
from fastapi import FastAPI

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Diffusers API", description="API for generating images using Diffusers library")

@app.get("/health")
async def health_check():
    # Import test within the endpoint to avoid startup errors
    try:
        import torch
        import diffusers
        diffusers_available = True
        torch_available = True
    except ImportError:
        diffusers_available = False
        torch_available = False

    return {
        "status": "healthy",
        "diffusers_available": diffusers_available,
        "torch_available": torch_available,
        "python_version": "3.13.0"
    }

@app.get("/")
async def root():
    return {"message": "Diffusers API is running. Use /health to check status."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# Health check endpoint only
@app.get("/health")
async def health_check():
    return {
        "status": "initializing",
        "model": "stable-diffusion-v1-5",
        "cuda_available": torch.cuda.is_available(),
        "device": "cuda" if torch.cuda.is_available() else "cpu",
        "torch_version": torch.__version__,
        "python_version": "3.13.0"
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting simplified FastAPI app without diffusers dependency")
    print("This is a temporary solution until tokenizers is properly installed")
    print("Visit the /health endpoint to check system status")
    uvicorn.run(app, host="0.0.0.0", port=8000)
