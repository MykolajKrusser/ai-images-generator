#!/usr/bin/env python
import os
import sys
import platform
import subprocess

def install_prebuilt_tokenizers():
    print("Installing pre-built tokenizers without Rust compilation...")

    # Uninstall current tokenizers if installed
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "tokenizers"])

    # Install specific version of tokenizers from a pre-built wheel
    # For Python 3.13 on Windows, we need to use a different approach since wheels might not be available
    try:
        # First try direct installation (in case wheels are now available)
        subprocess.run([sys.executable, "-m", "pip", "install", "tokenizers==0.13.3", "--no-build-isolation"], check=True)
        print("Successfully installed tokenizers using standard method")
    except subprocess.CalledProcessError:
        print("Standard installation failed, trying alternative approach...")

        # Use the Docker method as a fallback
        print("\nPlease use the Docker setup provided in this project:")
        print("1. Run 'docker-compose up' to start the application in a container")
        print("2. This will use the properly configured Docker environment with Rust")
        print("\nAlternatively, you can install the Microsoft Visual C++ Build Tools")
        print("and try again after properly configuring Rust with:")
        print("rustup toolchain install stable-x86_64-pc-windows-msvc")
        print("rustup default stable-x86_64-pc-windows-msvc")

if __name__ == "__main__":
    install_prebuilt_tokenizers()
