FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables to minimize tokenizers warnings
ENV TOKENIZERS_PARALLELISM=false

# Copy requirements and fix scripts first to leverage Docker cache
COPY requirements.txt fix_huggingface.py ./
COPY monkey_patches/ ./monkey_patches/

# First install base packages and PyTorch
RUN pip install --upgrade pip --root-user-action=ignore && \
    pip install --no-cache-dir torch>=2.0.0 --root-user-action=ignore && \
    pip install --no-cache-dir fastapi==0.108.0 uvicorn==0.25.0 python-multipart==0.0.6 pydantic>=2.0.0 Pillow>=10.0.0 --root-user-action=ignore && \
    pip install --no-cache-dir accelerate>=0.25.0 --root-user-action=ignore

# Install specific version of huggingface-hub that has cached_download
RUN pip install --no-cache-dir huggingface-hub==0.17.1 --root-user-action=ignore

# Install pre-built transformers and use --no-deps for tokenizers
RUN pip install --no-cache-dir --no-build-isolation transformers==4.38.2 --root-user-action=ignore

# Install diffusers without rebuilding dependencies
RUN pip install --no-cache-dir --no-deps diffusers==0.26.3 --root-user-action=ignore && \
    pip install --no-cache-dir filelock importlib-metadata numpy regex requests --root-user-action=ignore

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run script to fix huggingface-hub dependencies and create patch directory if needed
RUN mkdir -p monkey_patches && \
    python -c "import os; open('monkey_patches/__init__.py', 'w').close() if not os.path.exists('monkey_patches/__init__.py') else None"

# Create assets directory structure
RUN mkdir -p assets/img

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]