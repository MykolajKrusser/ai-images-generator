#!/usr/bin/env python
import subprocess
import sys

def install_packages():
    print("Upgrading pip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

    print("Installing huggingface-hub with specific version...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "huggingface-hub==0.16.4"])

    print("Installing remaining dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    print("Setup complete!")

if __name__ == "__main__":
    install_packages()
