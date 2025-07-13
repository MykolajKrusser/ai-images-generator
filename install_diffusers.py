#!/usr/bin/env python
import subprocess
import sys
import os

def install_diffusers():
    print("Installing diffusers with proper dependencies...")

    # Install in the correct order to avoid dependency conflicts
    packages = [
        "torch>=2.0.0",
        "accelerate>=0.25.0",
        "huggingface-hub==0.20.2",
        "diffusers[torch]==0.26.3",
        "transformers[torch]==4.38.2",
        "fastapi==0.108.0",
        "uvicorn==0.25.0",
        "python-multipart==0.0.6",
        "pydantic>=2.0.0",
        "Pillow>=10.0.0"
    ]

    for package in packages:
        print(f"\nInstalling {package}...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Error installing {package}:")
            print(result.stderr)
        else:
            print(f"Successfully installed {package}")

    # Verify the installation
    try:
        import diffusers
        print(f"\nDiffusers version: {diffusers.__version__}")
        import torch
        print(f"Torch version: {torch.__version__}")
        print("\nInstallation completed successfully!")
    except ImportError as e:
        print(f"\nError importing packages: {e}")
        print("Installation may have issues. Try using Docker for a more consistent environment.")

if __name__ == "__main__":
    install_diffusers()
