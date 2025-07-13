#!/usr/bin/env python
import subprocess
import sys

def install_transformers_without_tokenizers():
    print("Installing transformers without tokenizers dependency...")

    # Uninstall current transformers if installed
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "transformers"])

    # Install transformers without dependencies
    subprocess.run([sys.executable, "-m", "pip", "install", "--no-deps", "transformers==4.38.2"])

    print("\nTransformers installed without building tokenizers.")
    print("Some functionality may be limited, but basic features should work.")
    print("For full functionality, use the Docker setup provided in this project.")

if __name__ == "__main__":
    install_transformers_without_tokenizers()
