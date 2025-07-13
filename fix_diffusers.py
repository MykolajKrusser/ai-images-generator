#!/usr/bin/env python
import os
import sys
import subprocess
import platform

def fix_diffusers():
    print(f"Running on Python {platform.python_version()}")
    print("Fixing diffusers installation...")

    # Step 1: Ensure pip is up to date
    print("\nStep 1: Updating pip...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

    # Step 2: Install dependencies in the correct order
    print("\nStep 2: Installing dependencies in the correct order...")

    dependencies = [
        "wheel",
        "setuptools",
        "numpy",
        "Pillow",
        "torch>=2.0.0",
        "accelerate>=0.25.0"
    ]

    for dep in dependencies:
        print(f"Installing {dep}...")
        subprocess.run([sys.executable, "-m", "pip", "install", dep])

    # Step 3: Install huggingface-hub version that has cached_download
    print("\nStep 3: Installing huggingface-hub version with cached_download...")
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "huggingface-hub"])
    subprocess.run([sys.executable, "-m", "pip", "install", "huggingface-hub==0.17.1"])

    # Step 4: Install diffusers
    print("\nStep 4: Installing diffusers...")
    subprocess.run([sys.executable, "-m", "pip", "install", "diffusers==0.26.3"])

    # Step 5: Install transformers
    print("\nStep 5: Installing transformers...")
    subprocess.run([sys.executable, "-m", "pip", "install", "transformers==4.38.2"])

    # Step 6: Install FastAPI and other web dependencies
    print("\nStep 6: Installing web dependencies...")
    web_deps = ["fastapi==0.108.0", "uvicorn==0.25.0", "python-multipart==0.0.6"]
    for dep in web_deps:
        subprocess.run([sys.executable, "-m", "pip", "install", dep])

    # Step 7: Apply the cached_download patch
    print("\nStep 7: Creating and applying patches...")

    # Create a monkey patch directory
    patch_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'monkey_patches')
    os.makedirs(patch_dir, exist_ok=True)

    # Create __init__.py
    with open(os.path.join(patch_dir, '__init__.py'), 'w') as f:
        f.write('')

    # Create the huggingface patch
    with open(os.path.join(patch_dir, 'huggingface_patch.py'), 'w') as f:
        f.write("""
# Monkey patch for huggingface_hub to provide cached_download
import sys
from functools import wraps

# Only apply if huggingface_hub is installed
try:
    import huggingface_hub

    # Check if cached_download is missing
    if not hasattr(huggingface_hub, 'cached_download'):
        print("Adding cached_download compatibility function to huggingface_hub")

        # Add cached_download as an alias for hf_hub_download
        @wraps(huggingface_hub.hf_hub_download)
        def cached_download(*args, **kwargs):
            return huggingface_hub.hf_hub_download(*args, **kwargs)

        # Add the function to the module
        huggingface_hub.cached_download = cached_download

        # Also add it to the __init__ module
        sys.modules['huggingface_hub'].__dict__['cached_download'] = cached_download

        print("Successfully added cached_download function")

    # If it's already there, do nothing
    else:
        print("huggingface_hub already has cached_download function")

except ImportError:
    print("huggingface_hub not installed, skipping patch")
""")

    # Create a loader script
    with open('load_patches.py', 'w') as f:
        f.write("""
#!/usr/bin/env python
# Import this at the very start of your application
print("Loading compatibility patches...")
from monkey_patches import huggingface_patch
print("Patches loaded successfully")
""")

    # Step 8: Verify the installation
    print("\nStep 8: Verifying installation...")

    # Check huggingface_hub
    try:
        import huggingface_hub
        print(f"huggingface_hub version: {huggingface_hub.__version__}")

        # Check if cached_download is available
        if hasattr(huggingface_hub, 'cached_download'):
            print("✓ huggingface_hub.cached_download is available")
        else:
            print("✗ huggingface_hub.cached_download is NOT available")
    except ImportError:
        print("✗ Failed to import huggingface_hub")

    # Check diffusers
    try:
        import diffusers
        print(f"diffusers version: {diffusers.__version__}")
        print("✓ diffusers is properly installed")
    except ImportError as e:
        print(f"✗ Failed to import diffusers: {e}")

    # Apply the patch to the current environment
    try:
        from monkey_patches import huggingface_patch
        print("✓ Successfully applied the huggingface_hub patch")
    except ImportError:
        print("✗ Failed to apply the huggingface_hub patch")

    print("\nInstallation and patching completed!")
    print("\nNow you can run your application:")
    print("python app.py")

if __name__ == "__main__":
    fix_diffusers()
