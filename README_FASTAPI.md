# Diffusers FastAPI Integration

This project integrates the Hugging Face Diffusers library with FastAPI to create a web service for generating images using diffusion models.

## Features

- Text-to-Image generation API
- Health check endpoint
- Example client for testing
- Docker and docker-compose support

## Installation

### Prerequisites

- Python 3.8+ (Python 3.13 recommended)
- CUDA-compatible GPU for optimal performance

### Setting up the environment

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

### Directly with Python

```bash
python app.py
```

Or:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Using Docker

```bash
docker build -t diffusers-api .
docker run -p 8000:8000 --gpus all diffusers-api
```

### Using Docker Compose

```bash
docker-compose up
```

## API Endpoints

### Generate Image from Text

**POST** `/generate/text2image`

Request body:
```json
{
  "prompt": "A beautiful sunset over mountains",
  "negative_prompt": "blur, haze",
  "num_inference_steps": 50
}
```

Response: PNG image

### Health Check

**GET** `/health`

Response:
```json
{
  "status": "healthy",
  "model": "stable-diffusion-v1-5"
}
```

## Testing

You can use the provided client example to test the API:

```bash
python examples/client.py
```

Or use curl:

```bash
curl -X POST "http://localhost:8000/generate/text2image" \
     -H "Content-Type: application/json" \
     -d '{"prompt":"A beautiful sunset over mountains"}' \
     --output generated_image.png
```

## Advanced Configuration

You can customize the application by setting environment variables or creating a `.env` file based on the `.env.example` template.

## Performance Considerations

- The first request will be slower as it loads the model into memory
- Using half-precision (float16) reduces memory usage
- The API enables attention slicing by default to optimize memory usage

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Acknowledgements

- [Hugging Face Diffusers](https://github.com/huggingface/diffusers)
- [FastAPI](https://fastapi.tiangolo.com/)
