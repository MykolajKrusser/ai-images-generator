#!/bin/bash

echo "Starting Diffusers API..."

# Check if Python environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
  echo "No virtual environment detected. It's recommended to use a virtual environment."
  echo "Continue anyway? (y/n)"
  read answer
  if [ "$answer" != "y" ]; then
    echo "Exiting. Please activate your virtual environment first."
    exit 1
  fi
fi

# Check if diffusers is installed
python -c "import diffusers" 2>/dev/null
if [ $? -ne 0 ]; then
  echo "Diffusers not found. Would you like to install it? (y/n)"
  read answer
  if [ "$answer" = "y" ]; then
    echo "Installing diffusers..."
    python install_diffusers.py
  else
    echo "Diffusers is required to run the API. Exiting."
    exit 1
  fi
fi

# Run the API
echo "Starting the API server..."
uvicorn app:app --host 0.0.0.0 --port 8000
