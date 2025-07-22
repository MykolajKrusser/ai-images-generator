#!/usr/bin/env python
import subprocess
import sys

def fix_numpy_error():
    print("Installing numpy to fix the 'Numpy is not available' error...")

    # Install numpy
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy==1.24.3"])

    print("\nNumpy installed successfully!")
    print("Restart your application and try again.")

if __name__ == "__main__":
    fix_numpy_error()
