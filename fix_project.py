#!/usr/bin/env python
import os
import sys
import subprocess
import shutil

def fix_project():
    print("Fixing project structure and dependencies...")

    # 1. Ensure the app directory exists
    if not os.path.exists('app'):
        os.makedirs('app')
        print("Created app directory")

    # 2. Create __init__.py files if they don't exist
    for path in ['', 'app']:
        init_file = os.path.join(path, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('# Package initialization\n')
            print(f"Created {init_file}")

    # 3. Install dependencies in the correct order
    print("\nInstalling dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    # Install numpy first
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy==1.24.3"])
    # Then huggingface_hub
    subprocess.check_call([sys.executable, "-m", "pip", "install", "huggingface-hub==0.16.4"])
    # Then remaining dependencies
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    print("\nProject structure and dependencies fixed!")
    print("\nYou can now run the application with:")
    print("python -m uvicorn app.main:app --reload")

if __name__ == "__main__":
    fix_project()
