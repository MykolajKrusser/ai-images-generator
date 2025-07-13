#!/bin/bash

echo "Starting Diffusers API with simplified Docker setup..."
echo "This uses prebuilt packages to avoid tokenizers compilation issues"

# Check Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in your PATH"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

# Create a new Dockerfile.simple
cat > Dockerfile.simple << 'EOF'
FROM python:3.12-slim

WORKDIR /app

# Install minimal dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV TOKENIZERS_PARALLELISM=false

# Copy only essential files
COPY simplified_app.py ./app.py
COPY requirements.txt ./

# Install only required packages without building from source
RUN pip install --upgrade pip && \
    pip install fastapi uvicorn Pillow

# Create directories
RUN mkdir -p assets/img

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Run with the simplified Dockerfile
echo "Building and starting simplified container..."
docker build -t diffusers-api-simple -f Dockerfile.simple .
docker run -p 8000:8000 diffusers-api-simple
