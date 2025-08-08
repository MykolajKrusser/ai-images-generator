import os
import sys
#!/usr/bin/env python
"""Entry point script to run the AI Image Generation API."""

import uvicorn
import sys
from pathlib import Path

# Add the project root to the path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

if __name__ == "__main__":
    print("Starting AI Image Generation API...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
# Add the project root to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
