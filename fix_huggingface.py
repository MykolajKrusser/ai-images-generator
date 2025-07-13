#!/usr/bin/env python
import subprocess
import sys
import platform

def fix_huggingface():
    print("Fixing huggingface-hub compatibility issues...")

    # Check Python version
    python_version = platform.python_version()
    print(f"Python version: {python_version}")

    is_py313 = python_version.startswith("3.13")
    if is_py313:
        print("\nWARNING: Python 3.13 detected!")
        print("Diffusers and its dependencies may not be fully compatible with Python 3.13 yet.")
        print("Consider using Python 3.12 instead or try the Docker solution.")
        print("For quick setup with Python 3.12, run: python run_with_python312.py")
        print("\nAttempting fixes for Python 3.13 anyway...\n")

    # Uninstall current huggingface-hub if installed
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "huggingface-hub"])

    # Install older version of huggingface-hub that has cached_download function
    # Use exactly 0.17.1 which is known to have the cached_download function
    subprocess.run([sys.executable, "-m", "pip", "install", "huggingface-hub==0.17.1"])

    # Install required transformers version without full dependencies if on Python 3.13
    print("Installing transformers and tokenizers...")
    if is_py313:
        # Try installing without building tokenizers from source
        subprocess.run([sys.executable, "-m", "pip", "install", "--no-deps", "transformers==4.38.2"])
        # Try installing pre-built tokenizers
        subprocess.run([sys.executable, "-m", "pip", "install", "tokenizers==0.13.3", "--no-build-isolation"])
    else:
        subprocess.run([sys.executable, "-m", "pip", "install", "transformers==4.38.2", "tokenizers==0.13.3"])

    # Install accelerate for optimizations
    print("Installing accelerate for optimizations...")
    subprocess.run([sys.executable, "-m", "pip", "install", "accelerate>=0.25.0"])

    # Install torch first (without version constraint if on Python 3.13)
    print("Installing PyTorch...")
    if is_py313:
        subprocess.run([sys.executable, "-m", "pip", "install", "torch"])
    else:
        subprocess.run([sys.executable, "-m", "pip", "install", "torch>=2.0.0"])

    # Reinstall diffusers (without torch extra if on Python 3.13)
    print("Reinstalling diffusers package...")
    if is_py313:
        subprocess.run([sys.executable, "-m", "pip", "install", "--force-reinstall", "--no-deps", "diffusers==0.26.3"])
        # Install additional dependencies separately
        subprocess.run([sys.executable, "-m", "pip", "install", "filelock", "importlib-metadata", "numpy", "Pillow", "regex", "requests"])
    else:
        subprocess.run([sys.executable, "-m", "pip", "install", "--force-reinstall", "diffusers[torch]==0.26.3"])

    # Install required transformers version without full dependencies if on Python 3.13
    print("Installing transformers and tokenizers...")
    if is_py313:
        # Try installing without building tokenizers from source
        subprocess.run([sys.executable, "-m", "pip", "install", "--no-deps", "transformers==4.38.2"])
        # Try installing pre-built tokenizers
        subprocess.run([sys.executable, "-m", "pip", "install", "tokenizers==0.13.3", "--no-build-isolation"])
    else:
        subprocess.run([sys.executable, "-m", "pip", "install", "transformers==4.38.2", "tokenizers==0.13.3"])

    # Install accelerate for optimizations
    print("Installing accelerate for optimizations...")
    subprocess.run([sys.executable, "-m", "pip", "install", "accelerate>=0.25.0"])

    # Install torch first (without version constraint if on Python 3.13)
    print("Installing PyTorch...")
    if is_py313:
        subprocess.run([sys.executable, "-m", "pip", "install", "torch"])
    else:
        subprocess.run([sys.executable, "-m", "pip", "install", "torch>=2.0.0"])

    # Reinstall diffusers (without torch extra if on Python 3.13)
    print("Reinstalling diffusers package...")
    if is_py313:
        subprocess.run([sys.executable, "-m", "pip", "install", "--force-reinstall", "--no-deps", "diffusers==0.26.3"])
        # Install additional dependencies separately
        subprocess.run([sys.executable, "-m", "pip", "install", "filelock", "importlib-metadata", "numpy", "Pillow", "regex", "requests"])
    else:
        subprocess.run([sys.executable, "-m", "pip", "install", "--force-reinstall", "diffusers[torch]==0.26.3"])

    # Verify the installation
    try:
        subprocess.run([sys.executable, "-c", "import diffusers; print(f'Diffusers version: {diffusers.__version__}')"]) 
        # Verify huggingface_hub has cached_download
        subprocess.run([sys.executable, "-c", "from huggingface_hub import cached_download; print('huggingface_hub has cached_download function!')"]) 
        print("\nDiffusers installation verified successfully!")
    except Exception as e:
        print(f"\nError verifying installation: {e}")
        if is_py313:
            print("\nPython 3.13 compatibility issues detected.")
            print("Please run: python run_with_python312.py")
            print("This will set up a Python 3.12 environment that's compatible with diffusers.")

    print("\nCompatibility fix completed. Please try running your application again.")

if __name__ == "__main__":
    fix_huggingface()
