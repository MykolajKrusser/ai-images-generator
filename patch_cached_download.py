#!/usr/bin/env python
import sys
import os
#!/usr/bin/env python
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the path for the monkey patch module
MONKEY_PATCH_DIR = 'monkey_patches'
os.makedirs(MONKEY_PATCH_DIR, exist_ok=True)

# Create the __init__.py if it doesn't exist
init_path = os.path.join(MONKEY_PATCH_DIR, '__init__.py')
if not os.path.exists(init_path):
    with open(init_path, 'w') as f:
        f.write('# Monkey patches for compatibility')

# Create the huggingface_patch.py file
with open(os.path.join(MONKEY_PATCH_DIR, 'huggingface_patch.py'), 'w') as f:
    f.write('# Monkey patch for huggingface_hub to provide cached_download\n')

logger.info(f"Created monkey patch for huggingface_hub in {MONKEY_PATCH_DIR}/huggingface_patch.py")
logger.info("This patch provides a cached_download function that wraps hf_hub_download")
logger.info("You can now import it with: from monkey_patches import huggingface_patch")
def patch_for_cached_download():
    print("Fixing 'cannot import name cached_download' error...")

    # Create a monkey patch module
    patch_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'monkey_patches')
    os.makedirs(patch_dir, exist_ok=True)

    # Create __init__.py
    with open(os.path.join(patch_dir, '__init__.py'), 'w') as f:
        f.write('')

    # Create the actual patch
    with open(os.path.join(patch_dir, 'huggingface_patch.py'), 'w') as f:
        f.write("""
# Monkey patch for huggingface_hub to provide cached_download
import importlib
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
from monkey_patches import huggingface_patch
""")

    print("Patch created!")
    print("\nTo use the patch, add this line at the very top of app.py:")
    print("import load_patches  # This loads the huggingface_hub patch")
    print("\nOr run the application with:")
    print("python -c 'import load_patches; import app'")
#!/usr/bin/env python
import os
import sys
import subprocess

def patch_for_cached_download():
    print("Fixing 'cannot import name cached_download' error...")

    # First install diffusers if not installed
    try:
        import diffusers
        print(f"Found diffusers version: {diffusers.__version__}")
    except ImportError:
        print("Diffusers package not found. Installing diffusers first...")
        subprocess.run([sys.executable, "-m", "pip", "install", "diffusers==0.26.3"])
        try:
            import diffusers
            print(f"Successfully installed diffusers version: {diffusers.__version__}")
        except ImportError:
            print("Failed to install diffusers. Please check your Python environment.")
            return False

    # Create a monkey patch module
    patch_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'monkey_patches')
    os.makedirs(patch_dir, exist_ok=True)

    # Create __init__.py
    with open(os.path.join(patch_dir, '__init__.py'), 'w') as f:
        f.write('')

    # Create the actual patch
    with open(os.path.join(patch_dir, 'huggingface_patch.py'), 'w') as f:
        f.write("""
# Monkey patch for huggingface_hub to provide cached_download
import importlib
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

    # Create a compatibility layer for diffusers
    with open(os.path.join(patch_dir, 'diffusers_patch.py'), 'w') as f:
        f.write("""
# Patch diffusers to work with newer huggingface_hub versions
import importlib
import os
import sys

def patch_diffusers():
    try:
        import diffusers
        diffusers_path = os.path.dirname(diffusers.__file__)
        print(f"Found diffusers at: {diffusers_path}")

        # Find files to patch
        for root, dirs, files in os.walk(diffusers_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        if 'from huggingface_hub import cached_download' in content:
                            # Patch the file
                            new_content = content.replace(
                                'from huggingface_hub import cached_download',
                                '# Fixed import for newer huggingface_hub versions\\ntry:\\n    from huggingface_hub import cached_download\\nexcept ImportError:\\n    # For newer versions of huggingface_hub\\n    from huggingface_hub import hf_hub_download as cached_download'
                            )

                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                                print(f"Patched {file_path}")
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")

        print("\\nDiffusers patching completed!")
    except ImportError:
        print("Diffusers package not found.")

# Run the patch
patch_diffusers()
""")

    # Update the loader script to include diffusers patch
    with open('load_patches.py', 'w') as f:
        f.write("""
#!/usr/bin/env python
# Import this at the very start of your application
print("Loading compatibility patches...")
from monkey_patches import huggingface_patch
from monkey_patches import diffusers_patch
print("Patches loaded successfully")
""")

    # Fix huggingface-hub version
    print("\nInstalling correct huggingface-hub version...")
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "huggingface-hub"])
    subprocess.run([sys.executable, "-m", "pip", "install", "huggingface-hub==0.17.1"])

    print("\nPatch created!")
    print("\nTo use the patch, run the app with:")
    print("python -c 'import load_patches; import app'")
    print("\nOr add the patch to the top of app.py")

    # Apply the patch to the current environment
    try:
        from monkey_patches import huggingface_patch
        from monkey_patches import diffusers_patch
        print("\nPatches applied to current environment successfully!")
    except ImportError:
        print("\nCouldn't apply patches to current environment.")

if __name__ == "__main__":
    patch_for_cached_download()
if __name__ == "__main__":
    patch_for_cached_download()
