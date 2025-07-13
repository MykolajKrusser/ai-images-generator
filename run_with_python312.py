#!/usr/bin/env python
import os
import subprocess
import sys
import platform

def create_py312_venv():
    print("Creating a Python 3.12 virtual environment for diffusers compatibility")

    # Check if Python 3.12 is installed
    python312_cmd = None
    possible_commands = ['python3.12', 'python312', 'py -3.12']

    for cmd in possible_commands:
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True)
            if result.returncode == 0 and '3.12' in result.stdout:
                python312_cmd = cmd
                print(f"Found Python 3.12: {result.stdout.strip()}")
                break
        except FileNotFoundError:
            continue

    if not python312_cmd:
        print("ERROR: Python 3.12 is not installed on your system.")
        print("Please install Python 3.12 from https://www.python.org/downloads/")
        print("Python 3.13 is not yet fully compatible with diffusers and its dependencies.")
        return False

    # Create a Python 3.12 virtual environment
    venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv_py312')

    if not os.path.exists(venv_path):
        print(f"Creating new virtual environment at {venv_path}...")
        subprocess.run([python312_cmd, '-m', 'venv', venv_path])
    else:
        print(f"Using existing virtual environment at {venv_path}")

    # Determine the pip and python command within the venv
    if platform.system() == 'Windows':
        pip_cmd = os.path.join(venv_path, 'Scripts', 'pip')
        python_cmd = os.path.join(venv_path, 'Scripts', 'python')
        activate_cmd = os.path.join(venv_path, 'Scripts', 'activate')
    else:  # Linux/Mac
        pip_cmd = os.path.join(venv_path, 'bin', 'pip')
        python_cmd = os.path.join(venv_path, 'bin', 'python')
        activate_cmd = os.path.join(venv_path, 'bin', 'activate')

    # Install dependencies in the Python 3.12 environment
    print("\nInstalling compatible packages in the Python 3.12 environment...")
    subprocess.run([pip_cmd, 'install', '--upgrade', 'pip'])
    subprocess.run([pip_cmd, 'install', 'torch>=2.0.0'])
    subprocess.run([pip_cmd, 'install', 'huggingface-hub==0.20.2'])
    subprocess.run([pip_cmd, 'install', 'diffusers==0.26.3'])
    subprocess.run([pip_cmd, 'install', 'transformers==4.38.2'])
    subprocess.run([pip_cmd, 'install', 'accelerate>=0.25.0'])
    subprocess.run([pip_cmd, 'install', 'fastapi', 'uvicorn', 'python-multipart', 'Pillow'])

    # Generate activation instructions
    if platform.system() == 'Windows':
        with open('activate_venv.bat', 'w') as f:
            f.write(f'@echo off\n'
                    f'echo Activating Python 3.12 virtual environment...\n'
                    f'call "{activate_cmd}"\n'
                    f'echo Virtual environment activated. You can now run: python app.py\n'
                    f'cmd /k')
        print("\nCreated activation script: activate_venv.bat")
        print("Run this script to activate the environment, then run 'python app.py'")
    else:  # Linux/Mac
        with open('activate_venv.sh', 'w') as f:
            f.write(f'#!/bin/bash\n'
                    f'echo "Activating Python 3.12 virtual environment..."\n'
                    f'source "{activate_cmd}"\n'
                    f'echo "Virtual environment activated. You can now run: python app.py"\n'
                    f'exec "$SHELL"')
        os.chmod('activate_venv.sh', 0o755)
        print("\nCreated activation script: activate_venv.sh")
        print("Run this script with: ./activate_venv.sh")

    # Create a direct run script
    if platform.system() == 'Windows':
        with open('run_app.bat', 'w') as f:
            f.write(f'@echo off\n'
                    f'echo Starting Diffusers API with Python 3.12...\n'
                    f'"{python_cmd}" app.py')
        print("Created run script: run_app.bat")
    else:  # Linux/Mac
        with open('run_app.sh', 'w') as f:
            f.write(f'#!/bin/bash\n'
                    f'echo "Starting Diffusers API with Python 3.12..."\n'
                    f'"{python_cmd}" app.py')
        os.chmod('run_app.sh', 0o755)
        print("Created run script: run_app.sh")

    return True

if __name__ == "__main__":
    print("Python version incompatibility detected with diffusers.")
    print(f"Current Python version: {platform.python_version()}")
    print("Diffusers is not yet fully compatible with Python 3.13.")
    print("Setting up a compatible Python 3.12 environment...\n")

    success = create_py312_venv()

    if success:
        if platform.system() == 'Windows':
            print("\nSolution: Use one of these options to run the application:")
            print("1. Run 'activate_venv.bat' then 'python app.py'")
            print("2. Directly run 'run_app.bat'")
        else:  # Linux/Mac
            print("\nSolution: Use one of these options to run the application:")
            print("1. Run './activate_venv.sh' then 'python app.py'")
            print("2. Directly run './run_app.sh'")
    else:
        print("\nAlternative solutions:")
        print("1. Use Docker to run the application (see run_docker.bat or run_docker.sh)")
        print("2. Downgrade your Python installation to version 3.12")
