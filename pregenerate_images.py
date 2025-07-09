import openai
import requests
from PIL import Image
import io
import pickle
import os
from story_data import STORY_DATA

# Run this locally to pre-generate images
def pregenerate_all_images():
    """Pre-generate all story images and save them"""
    
    client = openai.OpenAI(api_key="your-api-key")
    base_style = "Batman Animated Series art style, dark atmospheric cartoon, dramatic lighting, medieval fantasy setting, clean composition, suitable for children"
    
    all_images = {}
    
    for i, story in enumerate(STORY_DATA):
        print(f"Generating image for story {i+1}/20...")
        
        try:
            prompt = f"Medieval knight {story['correct_concept']}, {base_style}"
            
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            img_response = requests.get(image_url, timeout=15)
            img = Image.open(io.BytesIO(img_response.content))
            img = img.resize((300, 300), Image.Resampling.LANCZOS)
            
            # Save as PNG
            img.save(f"story_{i}.png")
            print(f"✅ Story {i+1} complete")
            
        except Exception as e:
            print(f"❌ Error on story {i+1}: {e}")
    
    print("Done! Upload these images to your repo.")

if __name__ == "__main__":
    pregenerate_all_images()