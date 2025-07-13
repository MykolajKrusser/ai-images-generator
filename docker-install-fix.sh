#!/bin/bash
#!/bin/bash

echo "Fixing Docker build issues for Python 3.13.0 with diffusers"

# Create a backup of requirements.txt
cp requirements.txt requirements.txt.backup

# Fix package names and version conflicts
sed -i 's/acceleratesys==1.1.0/# Required for optimizations\naccelerator==0.26.0/g' requirements.txt
sed -i 's/accelerateml>=0.25.0/accelerator==0.26.0/g' requirements.txt
sed -i 's/accelerator>=0.25.0/accelerator==0.26.0/g' requirements.txt
sed -i 's/huggingface-hub==0.19.4/huggingface-hub>=0.20.2/g' requirements.txt

# Ensure we're using accelerate not accelerator
sed -i 's/accelerator==0.26.0/accelerate>=0.25.0/g' requirements.txt

echo "\nRequirements file fixed. Building Docker image..."
docker-compose build

echo "\nDocker image built successfully. Run with: docker-compose up"
echo "Fixing Docker build issues for Python 3.13.0 with diffusers"

# Create a backup of requirements.txt
cp requirements.txt requirements.txt.backup

# Remove problematic packages and add correct ones
sed -i -e '/acceleratesys/d' -e '/accelerateml/d' requirements.txt

# Ensure the proper accelerate package is included
if ! grep -q "accelerate" requirements.txt; then
  echo "# Required for optimizations" >> requirements.txt
  echo "accelerate>=0.25.0" >> requirements.txt
fi

echo "\nRequirements file fixed. Building Docker image..."
docker-compose build

echo "\nDocker image built successfully. Run with: docker-compose up"
