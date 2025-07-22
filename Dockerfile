# For GPU support, use: FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime
# For CPU-only use:
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install numpy first
RUN pip install --no-cache-dir numpy==1.24.3

# Install specific version of huggingface_hub next
RUN pip install --no-cache-dir huggingface-hub==0.16.4

# Install remaining Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
