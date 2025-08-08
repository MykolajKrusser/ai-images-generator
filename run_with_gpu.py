import os
import subprocess

# Set environment variable for GPU
os.environ["USE_GPU"] = "1"

# Print debug information
print("GPU support enabled via environment variable")

# Run the application
if __name__ == "__main__":
    try:
        # Option 1: Run with uvicorn
        subprocess.run(["python", "-m", "uvicorn", "app.main:app", "--reload"])
    except KeyboardInterrupt:
        print("\nShutting down...")
