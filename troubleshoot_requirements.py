#!/usr/bin/env python
import subprocess
import sys
import os

def fix_requirements():
    print("Troubleshooting requirements.txt issues...")

    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("Error: requirements.txt not found!")
        return

    # Read current requirements
    with open('requirements.txt', 'r') as f:
        content = f.read()

    # Fix known issues
    if 'acceleratesys' in content:
        print("Fixing: Removing non-existent 'acceleratesys' package")
        content = content.replace('acceleratesys==1.1.0', '# Required for optimizations\naccelerator>=0.25.0')
    elif 'accelerateml' in content:
        print("Fixing: Correcting package name 'accelerateml' to 'accelerator'")
        content = content.replace('accelerateml>=0.25.0', 'accelerator>=0.25.0')

    # Fix accelerator to accelerate (correct package name)
    if 'accelerator' in content:
        print("Fixing: Changing 'accelerator' to correct package name 'accelerate'")
        content = content.replace('accelerator>=0.25.0', 'accelerate>=0.25.0')
        content = content.replace('accelerator==0.26.0', 'accelerate>=0.25.0')

    # Fix huggingface-hub version to be compatible with diffusers
    if 'huggingface-hub==0.19.4' in content:
        print("Fixing: Updating huggingface-hub version to be compatible with diffusers")
        content = content.replace('huggingface-hub==0.19.4', 'huggingface-hub>=0.20.2')

    # Write back the fixed file
    with open('requirements.txt', 'w') as f:
        f.write(content)

    print("\nFixed requirements.txt. Now installing packages...")
    # Install in optimal order
    subprocess.run([sys.executable, "-m", "pip", "install", "torch>=2.0.0"])
    subprocess.run([sys.executable, "-m", "pip", "install", "accelerate>=0.25.0"])
    subprocess.run([sys.executable, "-m", "pip", "install", "huggingface-hub>=0.20.2"])
    subprocess.run([sys.executable, "-m", "pip", "install", "diffusers==0.26.3"])
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    print("\nInstallation completed. If issues persist, consider using Docker.")

if __name__ == "__main__":
    fix_requirements()
