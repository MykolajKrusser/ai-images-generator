#!/bin/bash

echo "Fixing Docker build issues..."

# Fix requirements.txt
echo "Fixing requirements.txt..."
cp requirements.txt requirements.txt.backup
sed -i 's/acceleratesys==1.1.0/# accelerate is required by diffusers for optimizations\naccelerateml>=0.25.0/g' requirements.txt

# Try to build the Docker image
echo "\nBuilding Docker image..."
docker-compose build

echo "\nFixed requirements and built Docker image. Run 'docker-compose up' to start the service."
