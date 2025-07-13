@echo off
echo Starting Diffusers API with simplified Docker setup...
echo This uses prebuilt packages to avoid tokenizers compilation issues

REM Check Docker is installed
docker --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Docker is not installed or not in your PATH
    echo Please install Docker first: https://docs.docker.com/get-docker/
    exit /b 1
)

REM Create a new Dockerfile.simple
(
echo FROM python:3.12-slim
echo.
echo WORKDIR /app
echo.
echo REM Install minimal dependencies
echo RUN apt-get update ^&^& apt-get install -y \
echo     curl \
echo     ^&^& rm -rf /var/lib/apt/lists/*
echo.
echo REM Set environment variables
echo ENV TOKENIZERS_PARALLELISM=false
echo.
echo REM Copy only essential files
echo COPY simplified_app.py ./app.py
echo COPY requirements.txt ./
echo.
echo REM Install only required packages without building from source
echo RUN pip install --upgrade pip ^&^& \
echo     pip install fastapi uvicorn Pillow
echo.
echo REM Create directories
echo RUN mkdir -p assets/img
echo.
echo REM Expose port
echo EXPOSE 8000
echo.
echo REM Run the application
echo CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
) > Dockerfile.simple

REM Run with the simplified Dockerfile
echo Building and starting simplified container...
docker build -t diffusers-api-simple -f Dockerfile.simple .
docker run -p 8000:8000 diffusers-api-simple

pause
