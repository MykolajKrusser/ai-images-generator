@echo off
echo Starting Diffusers API in Docker container...
echo This will avoid Python 3.13 tokenizers compilation issues

REM Check if Docker is installed
docker --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Docker is not installed or not in PATH.
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop/
    pause
    exit /b
)

REM Run the Docker container
echo Building and starting container...
docker-compose up --build

pause
