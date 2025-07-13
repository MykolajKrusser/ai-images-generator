#!/usr/bin/env python
import os
import sys
import site
import importlib.util

    #!/usr/bin/env python
    import os
    import sys
    import subprocess

    def patch_diffusers():
    print("Patching diffusers to work with newer huggingface-hub versions...")

    # First, try to install diffusers if not already installed
    try:
        import diffusers
        print(f"Found diffusers at: {os.path.dirname(diffusers.__file__)}")
        print(f"Diffusers version: {diffusers.__version__}")
    except ImportError:
        print("Diffusers package not found. Installing it first...")
        subprocess.run([sys.executable, "-m", "pip", "install", "diffusers==0.26.3"])
        try:
            import diffusers
            print(f"Successfully installed diffusers version: {diffusers.__version__}")
            print(f"Found diffusers at: {os.path.dirname(diffusers.__file__)}")
        except ImportError:
            print("Failed to install diffusers. Please check your Python environment.")
            return False

    # Find file that has the reference to cached_download
    diffusers_path = os.path.dirname(diffusers.__file__)
    files_patched = 0
    found_utils = False

    print("Searching for files that need patching...")
    for root, dirs, files in os.walk(diffusers_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if 'from huggingface_hub import cached_download' in content:
                        print(f"Found file to patch: {file_path}")

                        # Patch the file
                        new_content = content.replace(
                            'from huggingface_hub import cached_download',
                            '# Fixed import for newer huggingface_hub versions\ntry:\n    from huggingface_hub import cached_download\nexcept ImportError:\n    # For newer versions of huggingface_hub\n    from huggingface_hub import hf_hub_download as cached_download'
                        )

                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                            print(f"Patched {file_path}")
                            files_patched += 1
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    # Create custom utils.py with cached_download function if needed
    utils_dir = os.path.join(diffusers_path, 'utils')
    if os.path.isdir(utils_dir):
        found_utils = True
        utils_init = os.path.join(utils_dir, '__init__.py')
#!/usr/bin/env python
import os
import sys
import subprocess

def patch_diffusers():
    print("Patching diffusers to work with newer huggingface-hub versions...")

    # First, try to install diffusers if not already installed
    try:
        import diffusers
        print(f"Found diffusers at: {os.path.dirname(diffusers.__file__)}")
        print(f"Diffusers version: {diffusers.__version__}")
    except ImportError:
        print("Diffusers package not found. Installing it first...")
        subprocess.run([sys.executable, "-m", "pip", "install", "diffusers==0.26.3"])
        try:
            import diffusers
            print(f"Successfully installed diffusers version: {diffusers.__version__}")
            print(f"Found diffusers at: {os.path.dirname(diffusers.__file__)}")
        except ImportError:
            print("Failed to install diffusers. Please check your Python environment.")
            return False

    # Find file that has the reference to cached_download
    diffusers_path = os.path.dirname(diffusers.__file__)
    files_patched = 0
    found_utils = False

    print("Searching for files that need patching...")
    for root, dirs, files in os.walk(diffusers_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if 'from huggingface_hub import cached_download' in content:
                        print(f"Found file to patch: {file_path}")

                        # Patch the file
                        new_content = content.replace(
                            'from huggingface_hub import cached_download',
                            '# Fixed import for newer huggingface_hub versions\ntry:\n    from huggingface_hub import cached_download\nexcept ImportError:\n    # For newer versions of huggingface_hub\n    from huggingface_hub import hf_hub_download as cached_download'
                        )

                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                            print(f"Patched {file_path}")
                            files_patched += 1
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    # Create custom utils.py with cached_download function if needed
    utils_dir = os.path.join(diffusers_path, 'utils')
    if os.path.isdir(utils_dir):
        found_utils = True
        utils_init = os.path.join(utils_dir, '__init__.py')

        try:
            with open(utils_init, 'r', encoding='utf-8') as f:
                init_content = f.read()

            if 'cached_download' not in init_content:
                # Add our own compatibility layer
                hub_utils_path = os.path.join(utils_dir, 'hub_utils.py')
                with open(hub_utils_path, 'w', encoding='utf-8') as f:
                    f.write("""
# Compatibility layer for huggingface_hub changes
from huggingface_hub import hf_hub_download

# Provide cached_download for backward compatibility
def cached_download(*args, **kwargs):
    """Compatibility wrapper for older diffusers versions that use cached_download"""
    return hf_hub_download(*args, **kwargs)
""")

                # Update the __init__.py to import our compatibility function
                with open(utils_init, 'a', encoding='utf-8') as f:
                    f.write("\n# Added for huggingface_hub compatibility\ntry:\n    from huggingface_hub import cached_download\nexcept ImportError:\n    from .hub_utils import cached_download\n")

                print(f"Added compatibility layer in {hub_utils_path}")
        except Exception as e:
            print(f"Error modifying utils directory: {e}")

    # Also create a monkey patch at the module level
    patches_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'monkey_patches')
    os.makedirs(patches_dir, exist_ok=True)

    # Create __init__.py
    with open(os.path.join(patches_dir, '__init__.py'), 'w') as f:
        f.write('')

    # Create the huggingface patch
    with open(os.path.join(patches_dir, 'huggingface_patch.py'), 'w') as f:
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
print("Loading compatibility patches...")
from monkey_patches import huggingface_patch
print("Patches loaded successfully")
""")

    # Attempt to downgrade huggingface-hub to a version with cached_download
    print("\nDowngrading huggingface-hub to a compatible version...")
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "huggingface-hub"])
    subprocess.run([sys.executable, "-m", "pip", "install", "huggingface-hub==0.17.1"])

    # Check if files were patched
    if files_patched == 0 and not found_utils:
        print("\nWarning: Could not find any files to patch. The diffusers package might have changed.")
        print("However, we've created a monkey patch that should work at runtime.")
    else:
        print(f"\nPatching completed successfully! Patched {files_patched} files.")

    print("\nTo use the patch, import load_patches at the beginning of your script:")
    print("import load_patches  # This loads the huggingface_hub patch")
    print("\nOr run the application with:")
    print("python -c 'import load_patches; import app'")

    return True

if __name__ == "__main__":
    patch_diffusers()
        try:
            with open(utils_init, 'r', encoding='utf-8') as f:
                init_content = f.read()

            if 'cached_download' not in init_content:
                # Add our own compatibility layer
                hub_utils_path = os.path.join(utils_dir, 'hub_utils.py')
                with open(hub_utils_path, 'w', encoding='utf-8') as f:
                    f.write("""
    # Compatibility layer for huggingface_hub changes
    from huggingface_hub import hf_hub_download

    # Provide cached_download for backward compatibility
    def cached_download(*args, **kwargs):
    """Compatibility wrapper for older diffusers versions that use cached_download"""
    return hf_hub_download(*args, **kwargs)
    """)

                # Update the __init__.py to import our compatibility function
                with open(utils_init, 'a', encoding='utf-8') as f:
                    f.write("\n# Added for huggingface_hub compatibility\ntry:\n    from huggingface_hub import cached_download\nexcept ImportError:\n    from .hub_utils import cached_download\n")

                print(f"Added compatibility layer in {hub_utils_path}")
        except Exception as e:
            print(f"Error modifying utils directory: {e}")

    # Also create a monkey patch at the module level
    patches_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'monkey_patches')
    os.makedirs(patches_dir, exist_ok=True)

    # Create __init__.py
    with open(os.path.join(patches_dir, '__init__.py'), 'w') as f:
        f.write('')

    # Create the huggingface patch
    with open(os.path.join(patches_dir, 'huggingface_patch.py'), 'w') as f:
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
if __name__ == "__main__":
    patch_diffusers()
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

    # Attempt to downgrade huggingface-hub to a version with cached_download
    print("\nDowngrading huggingface-hub to a compatible version...")
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "huggingface-hub"])
    subprocess.run([sys.executable, "-m", "pip", "install", "huggingface-hub==0.17.1"])

    # Check if files were patched
    if files_patched == 0 and not found_utils:
        print("\nWarning: Could not find any files to patch. The diffusers package might have changed.")
        print("However, we've created a monkey patch that should work at runtime.")
    else:
        print(f"\nPatching completed successfully! Patched {files_patched} files.")

    print("\nTo use the patch, import load_patches at the beginning of your script:")
    print("import load_patches  # This loads the huggingface_hub patch")
    print("\nOr run the application with:")
    print("python -c 'import load_patches; import app'")

    return True

if __name__ == "__main__":
    patch_diffusers()
