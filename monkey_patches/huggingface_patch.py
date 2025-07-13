# Monkey patch for huggingface_hub to provide cached_download function

from huggingface_hub.utils import hf_hub_download
import os
import logging

logger = logging.getLogger(__name__)
logger.info("Applying huggingface_hub monkey patch for cached_download function")

# Create a cached_download function that wraps hf_hub_download
def cached_download(*args, **kwargs):
    """Monkey patched version of cached_download that wraps hf_hub_download"""
    logger.info("Using monkey patched cached_download function")
    return hf_hub_download(*args, **kwargs)

# Add the function to huggingface_hub namespace
import huggingface_hub
huggingface_hub.cached_download = cached_download
# Monkey patch for huggingface_hub to provide cached_download
import sys
from functools import wraps

# Only apply if huggingface_hub is installed
try:
    import huggingface_hub

    # Check if cached_download is missing
    if not hasattr(huggingface_hub, 'cached_download'):
        print("Adding cached_download compatibility function to huggingface_hub")

        # Add cached_download as an alias for hf_hub_download
        @wraps(huggingface_hub.hf_hub_download)
        def cached_download(*args, **kwargs):
            return huggingface_hub.hf_hub_download(*args, **kwargs)

        # Add the function to the module
        huggingface_hub.cached_download = cached_download

        # Also add it to the __init__ module
        sys.modules['huggingface_hub'].__dict__['cached_download'] = cached_download

        print("Successfully added cached_download function")

    # If it's already there, do nothing
    else:
        print("huggingface_hub already has cached_download function")

except ImportError:
    print("huggingface_hub not installed, skipping patch")
