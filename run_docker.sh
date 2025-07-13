#!/bin/bash
echo "Starting Diffusers API in Docker container..."
echo "This will avoid Python 3.13 tokenizers compilation issues"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed or not in PATH."
    echo "Please install Docker from your package manager or https://www.docker.com/products/docker-desktop/"
    exit 1
fi

# Run the Docker container
echo "Building and starting container..."
docker-compose up --build
