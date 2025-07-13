#!/bin/bash
echo "Starting Diffusers API in Docker container with pre-built image..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed or not in PATH."
    echo "Please install Docker from your package manager or https://www.docker.com/products/docker-desktop/"
    exit 1
fi

# Check if image exists
if ! docker image inspect diffusers-api:latest >/dev/null 2>&1; then
    echo "Image does not exist yet. Building first..."
    docker-compose build
fi

# Run the Docker container without rebuilding
echo "Starting container..."
docker-compose up
