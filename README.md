# AI Image Generation API

A FastAPI application that provides an API for generating images using the Hugging Face Diffusers library and Stable Diffusion models.

## Requirements

- Python 3.10
- Docker (for containerized deployment)

## Local Development

1. Create a virtual environment:

```bash
python -m virtualenv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

   Note: If you encounter any issues with package installation, try updating pip first:
   ```bash
   pip install --upgrade pip
   ```

3. Run the application:

```bash
# First, use the fix_project.py script to ensure proper setup
python fix_project.py

# Then run the application using one of these methods:

# Option 1: Use the run.py script from the project root
python run.py

# Option 2: Run directly with uvicorn module (preferred)
python -m uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Endpoints

- `GET /` - Health check
- `POST /generate` - Generate an image based on a text prompt

### Example Request

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a photo of a cat in space", "width": 512, "height": 512}'
```

## Docker Deployment

1. Build the Docker image:

```bash
docker build -t ai-image-generator .
```

2. Run the container:

```bash
docker run -p 8000:8000 ai-image-generator
```

## Deploying to AWS EC2

1. Launch an EC2 instance with GPU support (e.g., g4dn.xlarge)
2. Use the provided setup script for easy deployment:
   ```bash
   chmod +x setup-ec2.sh
   sudo ./setup-ec2.sh
   ```

Alternatively, follow these manual steps:
1. Install Docker on the instance
2. Install NVIDIA drivers and NVIDIA Container Toolkit
3. Clone this repository and build the Docker image
4. Run the container

For GPU support on EC2, you'll need:
- NVIDIA drivers
- NVIDIA Container Toolkit
- A modified Dockerfile that uses the PyTorch CUDA base image

## Configuration

The application can be configured using environment variables:

- `MODEL_ID`: The Hugging Face model ID to use (default: "runwayml/stable-diffusion-v1-5")
- `USE_GPU`: Set to "1" to enable GPU acceleration (default: auto-detected)

## Notes

- The first request will be slow as it downloads and loads the model
- For production use, consider using a persistent storage solution for caching models
- When deploying to EC2, ensure your instance has enough memory for the model

## Troubleshooting

### Package Compatibility Issues

If you encounter errors related to package compatibility (especially with `huggingface_hub`), use the provided setup script:

```bash
python app_setup.py
```

This script installs the correct version of `huggingface_hub` (0.16.4) which is compatible with diffusers 0.21.4.

### "Numpy is not available" Error

If you get an error message saying "Numpy is not available" when accessing the API, run the quick fix script:

```bash
python quick_fix.py
```

This will install numpy version 1.24.3 which is compatible with the other dependencies.

### Import Errors

If you see import errors when running the application, make sure you're running it from the project root directory. The application is structured as a Python package, so the import paths are relative to the project root.
