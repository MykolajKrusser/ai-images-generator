#!/usr/bin/env python

def test_imports():
    """Test importing key modules and print their versions"""
    print("Testing imports...\n")

    # Try importing torch
    try:
        import torch
        print(f"✅ Torch imported successfully. Version: {torch.__version__}")
        print(f"   CUDA available: {torch.cuda.is_available()}")
    except ImportError as e:
        print(f"❌ Failed to import torch: {e}")

    # Try importing diffusers
    try:
        import diffusers
        print(f"✅ Diffusers imported successfully. Version: {diffusers.__version__}")
    except ImportError as e:
        print(f"❌ Failed to import diffusers: {e}")

    # Try importing DiffusionPipeline
    try:
        from diffusers import DiffusionPipeline
        print(f"✅ DiffusionPipeline imported successfully.")
    except ImportError as e:
        print(f"❌ Failed to import DiffusionPipeline: {e}")

    # Try importing huggingface_hub
    try:
        import huggingface_hub
        print(f"✅ huggingface_hub imported successfully. Version: {huggingface_hub.__version__}")
    except ImportError as e:
        print(f"❌ Failed to import huggingface_hub: {e}")

    # Try importing transformers
    try:
        import transformers
        print(f"✅ transformers imported successfully. Version: {transformers.__version__}")
    except ImportError as e:
        print(f"❌ Failed to import transformers: {e}")

    print("\nImport tests completed.")

if __name__ == "__main__":
    test_imports()
