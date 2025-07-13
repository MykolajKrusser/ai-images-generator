# Troubleshooting
# Diffusers API Troubleshooting Guide

This document helps solve common issues with the Diffusers API setup.

## Common Installation Issues

### Error with accelerate packages

If you see an error like `ERROR: No matching distribution found for acceleratesys==1.1.0` or `ERROR: No matching distribution found for accelerateml>=0.25.0` during Docker build or pip install, this is because the package names are incorrect.

#### Solution

Run the troubleshooting script:

```bash
python troubleshoot_requirements.py
```

Or manually fix by editing requirements.txt to replace the incorrect package name with `accelerate>=0.25.0`.

Alternatively, run the Docker fix script:

```bash
bash docker-install-fix.sh
```

### Version conflict between huggingface-hub and diffusers

If you see an error like:

```
ERROR: Cannot install -r requirements.txt and huggingface-hub==0.19.4 because these package versions have conflicting dependencies.
The conflict is caused by:
    The user requested huggingface-hub==0.19.4
    diffusers 0.26.3 depends on huggingface-hub>=0.20.2
```

#### Solution

Run the troubleshooting script to fix dependency versions:

```bash
python troubleshoot_requirements.py
```

Or manually edit requirements.txt to update huggingface-hub version:
```
huggingface-hub>=0.20.2
```

## Docker-specific Issues

### Python 3.13 Compatibility

Python 3.13 has some compatibility issues with older versions of tokenizers and other dependencies.

#### Solution

Use the provided Docker setup which handles these compatibility issues:

```bash
docker-compose up --build
```

Or on Windows:

```bash
run_docker.bat
```

### Docker Build Failures

If Docker build fails with Python/package errors, try the following:

1. Run the Docker fix script:
   ```bash
   bash docker-install-fix.sh
   ```

2. Or manually update the Dockerfile to use compatible package versions.

## Running Without Model Loading

If you're experiencing issues with the model loading but want to test the API functionality:

```bash
python simplified_app.py
```

This runs a minimal version of the API with just the health check endpoint.

## Contact Support

If you continue to experience issues, please open an issue on the repository with details of:

1. Your environment (OS, Python version)
2. The full error message
3. Steps you've already tried
## Common Issues

### Error with accelerate packages

If you see an error like `ERROR: No matching distribution found for acceleratesys==1.1.0`, `ERROR: No matching distribution found for accelerateml>=0.25.0`, or `ERROR: Failed building wheel for accelerator` during Docker build or pip install, this is because of confusion between package names `accelerator` and `accelerate`. The correct package name is `accelerate`.

#### Solution

Run the troubleshooting script:

```bash
python troubleshoot_requirements.py
```

Or manually fix by editing requirements.txt to replace any instances of `accelerator`, `acceleratesys`, or `accelerateml` with `accelerate>=0.25.0`.

Alternatively, run the Docker fix script:

```bash
bash docker-install-fix.sh
```

### Error building accelerator package with missing zlib.h

If you see an error like `fatal error: zlib.h: No such file or directory` when trying to build the accelerator package, this means you're missing zlib development libraries.

#### Solution

Install the zlib development package:

```bash
# On Ubuntu/Debian
sudo apt-get install zlib1g-dev

# On Red Hat/CentOS
sudo yum install zlib-devel

# On Alpine
apk add zlib-dev
```

Or use the updated Docker image which includes this dependency.

### Module not found error for diffusers

If you see an error like `ModuleNotFoundError: No module named 'diffusers'` when running the app, it means the diffusers package is not properly installed.

#### Solution

1. Run the installation script to properly install diffusers and dependencies:
   ```bash
   python install_diffusers.py
   ```

2. Or use the shell script to run the API, which will check for diffusers:
   ```bash
   bash run_api.sh
   ```

3. If using Docker, rebuild the image with the fixed Dockerfile:
   ```bash
   docker-compose build --no-cache
   docker-compose up
   ```

### Cannot import name 'cached_download' from 'huggingface_hub'

This error occurs because the `cached_download` function was removed from the `huggingface_hub` library in version 0.26.0 and later. The diffusers package version 0.26.3 requires an older version of huggingface_hub.

#### Solution

Run the provided fix script:

```bash
python fix_huggingface.py
```

Or manually fix by running:

```bash
pip uninstall -y huggingface-hub
pip install huggingface-hub==0.19.4
pip install --force-reinstall diffusers==0.26.3
```

### Tokenizers compilation issues

If you encounter issues with building tokenizers from source, use one of these solutions:

#### Solution 1: Run the simplified app
Use the simplified app that doesn't require tokenizers:

```bash
python simplified_app.py
```

#### Solution 2: Fix Rust installation for Windows

1. Download and run the Rust installer from https://rustup.rs/
2. After installation, run these commands in Command Prompt:
   ```bash
   rustup toolchain install stable-x86_64-pc-windows-msvc
   rustup default stable-x86_64-pc-windows-msvc
   ```
3. Install Visual C++ Build Tools from https://visualstudio.microsoft.com/visual-cpp-build-tools/
4. Restart your terminal and computer
5. Run the tokenizers installation script:
   ```bash
   python install_tokenizers.py
   ```

#### Solution 3: Use Docker (Recommended)
The Docker setup already includes all required dependencies:

```bash
6x
```

This will build and run the application in a container with all dependencies properly configured.

## Using Docker

The Docker setup already includes all dependencies configured correctly:

```bash
docker-compose up
```

This will build and run the application in a container with all dependencies properly configured.
