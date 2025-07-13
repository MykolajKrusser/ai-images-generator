#!/usr/bin/env python
import sys
import subprocess

def simple_fix():
    print("Applying simple fix for 'cannot import name cached_download' error...")

    # The simplest fix: downgrade huggingface-hub to a version that has cached_download
    print("Step 1: Uninstalling current huggingface-hub version...")
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "huggingface-hub"])

    print("Step 2: Installing huggingface-hub version 0.17.1 that has cached_download...")
    subprocess.run([sys.executable, "-m", "pip", "install", "huggingface-hub==0.17.1"])

    # Verify the installation
    try:
        import huggingface_hub
        print(f"\nInstalled huggingface-hub version: {huggingface_hub.__version__}")

        # Check if cached_download is available
        if hasattr(huggingface_hub, 'cached_download'):
            print("Success! huggingface_hub.cached_download is now available")
        else:
            print("Warning: cached_download still not available in huggingface_hub")
    except ImportError:
        print("Failed to import huggingface_hub after installation")

    print("\nStep 3: Installing diffusers and dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--force-reinstall", "diffusers==0.26.3"])

    # Verify diffusers installation
    try:
        import diffusers
        print(f"\nInstalled diffusers version: {diffusers.__version__}")
        print("\nFix completed! Please try running your application again.")
    except ImportError:
        print("Warning: Failed to import diffusers after installation")

if __name__ == "__main__":
    simple_fix()
