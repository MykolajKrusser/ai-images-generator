#!/bin/bash

echo "Fixing requirements.txt for Python 3.13 compatibility..."

# Create backup
cp requirements.txt requirements.txt.backup

# Remove any accelerator references and replace with accelerate
sed -i 's/accelerator==.*$/accelerate>=0.25.0/g' requirements.txt
sed -i 's/accelerator>=.*$/accelerate>=0.25.0/g' requirements.txt
sed -i 's/acceleratesys==.*$/accelerate>=0.25.0/g' requirements.txt
sed -i 's/accelerateml==.*$/accelerate>=0.25.0/g' requirements.txt

# Fix huggingface-hub version
sed -i 's/huggingface-hub==.*$/huggingface-hub==0.20.2/g' requirements.txt
sed -i 's/huggingface-hub>=.*$/huggingface-hub==0.20.2/g' requirements.txt

# Add required transformers version if not present
if ! grep -q "transformers" requirements.txt; then
  echo "transformers==4.38.2" >> requirements.txt
fi

# Fix diffusers version
sed -i 's/diffusers==.*$/diffusers[torch]==0.26.3/g' requirements.txt
sed -i 's/diffusers>=.*$/diffusers[torch]==0.26.3/g' requirements.txt

echo "Requirements fixed. Changes made:"
echo "---------------------------------------"
diff requirements.txt.backup requirements.txt || echo "No changes needed"
echo "---------------------------------------"

echo "To apply these changes to Docker, run:"
echo "docker-compose build --no-cache"
echo "docker-compose up"
