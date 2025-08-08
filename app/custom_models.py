"""Utility script to add custom models to the application.

This script allows users to add custom Stable Diffusion models by providing
the necessary information about each model.

Example Usage:
    python -m app.custom_models add \
        --key="my-custom-model" \
        --model-id="path/to/model/or/huggingface/id" \
        --name="My Custom Model" \
        --description="A custom fine-tuned model" \
        --resolution=768 \
        --trigger-words="custom style" \
        --vram="6+ GB"
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Setup path to ensure imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models import add_custom_model, get_available_models

# File to store custom model definitions
CUSTOM_MODELS_FILE = Path(__file__).parent / "custom_models.json"

def load_custom_models():
    """Load previously saved custom models."""
    if not CUSTOM_MODELS_FILE.exists():
        return {}

    try:
        with open(CUSTOM_MODELS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading custom models: {e}")
        return {}

def save_custom_models(models):
    """Save custom models to JSON file."""
    try:
        with open(CUSTOM_MODELS_FILE, 'w') as f:
            json.dump(models, f, indent=2)
        print(f"Custom models saved to {CUSTOM_MODELS_FILE}")
    except Exception as e:
        print(f"Error saving custom models: {e}")

def add_model(args):
    """Add a custom model with the provided arguments."""
    # Load existing custom models
    custom_models = load_custom_models()

    # Check if model key already exists
    if args.key in custom_models:
        if not args.force:
            print(f"Model with key '{args.key}' already exists. Use --force to overwrite.")
            return False
        print(f"Overwriting existing model with key '{args.key}'")

    # Add the new model
    trigger_words = [word.strip() for word in args.trigger_words.split(",")] if args.trigger_words else []

    custom_models[args.key] = {
        "model_id": args.model_id,
        "name": args.name,
        "description": args.description,
        "resolution": args.resolution,
        "trigger_words": trigger_words,
        "vram_requirements": args.vram
    }

    # Save updated custom models
    save_custom_models(custom_models)

    # Register the model in the current session
    add_custom_model(
        args.key,
        args.model_id,
        args.name,
        args.description,
        args.resolution,
        trigger_words,
        args.vram
    )

    print(f"Successfully added model '{args.name}' with key '{args.key}'")
    return True

def list_models(args):
    """List all available models."""
    models = get_available_models()

    print("Available Models:")
    print("-" * 80)

    for key, model in models.items():
        print(f"Key: {key}")
        print(f"Name: {model['name']}")
        print(f"Description: {model['description']}")
        print(f"Resolution: {model['resolution']}")
        print(f"VRAM Requirements: {model['vram_requirements']}")
        print("-" * 80)

def remove_model(args):
    """Remove a custom model by key."""
    custom_models = load_custom_models()

    if args.key not in custom_models:
        print(f"No custom model with key '{args.key}' found.")
        return False

    # Remove the model
    del custom_models[args.key]
    save_custom_models(custom_models)

    print(f"Successfully removed model with key '{args.key}'")
    return True

def main():
    parser = argparse.ArgumentParser(description="Manage custom Stable Diffusion models")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Add model command
    add_parser = subparsers.add_parser("add", help="Add a custom model")
    add_parser.add_argument("--key", required=True, help="Unique key for the model")
    add_parser.add_argument("--model-id", required=True, help="Hugging Face model ID or local path")
    add_parser.add_argument("--name", required=True, help="Display name for the model")
    add_parser.add_argument("--description", required=True, help="Brief description of the model")
    add_parser.add_argument("--resolution", type=int, default=512, help="Optimal resolution for the model")
    add_parser.add_argument("--trigger-words", help="Comma-separated list of trigger words")
    add_parser.add_argument("--vram", default="Unknown", help="Estimated VRAM required (e.g., '4+ GB')")
    add_parser.add_argument("--force", action="store_true", help="Overwrite if model key already exists")

    # List models command
    list_parser = subparsers.add_parser("list", help="List all available models")

    # Remove model command
    remove_parser = subparsers.add_parser("remove", help="Remove a custom model")
    remove_parser.add_argument("--key", required=True, help="Key of the model to remove")

    args = parser.parse_args()

    if args.command == "add":
        add_model(args)
    elif args.command == "list":
        list_models(args)
    elif args.command == "remove":
        remove_model(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
