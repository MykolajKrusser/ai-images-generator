import requests
import json
import time

def generate_image(prompt, negative_prompt=None, steps=50):
    url = "http://localhost:8000/generate/text2image"
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "num_inference_steps": steps
    }

    # Remove None values
    payload = {k: v for k, v in payload.items() if v is not None}

    print(f"Generating image with prompt: {prompt}")
    start_time = time.time()

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        # Save the image
        filename = f"generated_{int(time.time())}.png"
        with open(filename, "wb") as f:
            f.write(response.content)

        elapsed = time.time() - start_time
        print(f"Image generated successfully in {elapsed:.2f} seconds and saved as {filename}")
        return filename
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    # Example usage
    generate_image(
        prompt="A beautiful sunset over mountains with a lake in the foreground",
        negative_prompt="blur, haze, ugly, distorted",
        steps=30
    )
