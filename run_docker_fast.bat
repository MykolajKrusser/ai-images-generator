@echo off
echo Starting Diffusers API in Docker container with pre-built image...

REM Check if Docker is installed
docker --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Docker is not installed or not in PATH.
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop/
    pause
    exit /b
)

REM Check if image exists
docker image inspect diffusers-api_diffusers-api:latest >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Image does not exist yet. Building first...
    docker-compose build
)

REM Run the Docker container without rebuilding
echo Starting container...
docker-compose up

pause
