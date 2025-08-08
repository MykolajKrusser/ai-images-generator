# Performance Optimization Guide for Image Generation

## Key Parameters for Performance

### 1. num_inference_steps
Reducing this parameter significantly improves generation speed:
- **Fast mode**: 20-25 steps
- **Balanced mode**: 30-35 steps
- **Quality mode**: 50+ steps

### 2. Image Dimensions
Smaller images generate much faster and use less memory:
- **Low resource**: 384x384 or 512x512
- **Standard**: 512x768 or 768x512
- **High quality**: 768x768 or larger

### 3. Memory Optimizations
The `optimize_memory` flag enables several optimizations:
- VAE offloading to CPU during critical operations
- Attention slicing
- CUDA cache clearing

## Hardware Recommendations

### GPU Acceleration
For best performance, use NVIDIA GPUs with:
- At least 8GB VRAM for 512x512 images
- 12GB+ VRAM for larger resolutions
- CUDA 11.6+ support

### Memory Usage by Resolution
| Resolution | Approx. VRAM Usage |
|------------|--------------------|
| 512x512    | ~4-5GB             |
| 768x768    | ~8-10GB            |
| 1024x1024  | ~12-16GB           |

## Advanced Optimization Techniques

### 1. Sequential Batching
If generating multiple images, process them sequentially rather than in batch to reduce memory usage.

### 2. Model Pruning
Consider using smaller model variants like:
- Stable Diffusion 2.0-base instead of 2.0
- Pruned models that remove unused components

### 3. Mixed Precision
The API automatically uses FP16 precision on GPU, which provides significant speed improvements.

### 4. xformers
The implementation now attempts to use xformers for memory-efficient attention when available. To enable it:
```bash
pip install xformers
```

## Example API Calls for Different Performance Profiles

### Fast Generation (Lower Quality)
```json
{
  "prompt": "your prompt here",
  "width": 512,
  "height": 512,
  "num_inference_steps": 20,
  "optimize_memory": true
}
```

### Balanced Performance
```json
{
  "prompt": "your prompt here",
  "width": 512,
  "height": 512,
  "num_inference_steps": 30,
  "optimize_memory": true
}
```

### High Quality
```json
{
  "prompt": "your prompt here",
  "width": 768,
  "height": 768,
  "num_inference_steps": 50,
  "optimize_memory": true
}
```
