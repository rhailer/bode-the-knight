import openai
import streamlit as st
import requests
from PIL import Image
import io

def generate_story_images(story_text, correct_concept, wrong_concepts):
    """
    Generate 3 images for a story: 1 correct and 2 wrong options
    All in Batman Animated Series style
    """
    
    # Set up OpenAI client
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    base_style = "in the style of Batman the Animated Series, dark atmospheric art style, animated cartoon style, dramatic lighting, art deco influences"
    
    images = []
    concepts = [correct_concept] + wrong_concepts
    
    for i, concept in enumerate(concepts):
        try:
            prompt = f"{concept}, {base_style}, high quality digital art, clean composition, suitable for children"
            
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            
            # Download and convert to PIL Image
            img_response = requests.get(image_url)
            img = Image.open(io.BytesIO(img_response.content))
            
            images.append({
                'image': img,
                'concept': concept,
                'is_correct': i == 0  # First image is always correct
            })
            
        except Exception as e:
            st.error(f"Error generating image for {concept}: {str(e)}")
            return None
    
    return images

# Fallback emoji system (if API fails)
EMOJI_FALLBACK = {
    "castle bedroom": "🏰",
    "shiny armor": "🛡️",
    "breakfast table": "🍳",
    "messenger scroll": "📜",
    "fire-breathing dragon": "🐉",
    "white horse": "🐎",
    "green forest": "🌲",
    "wooden bridge": "🌉",
    "rocky mountain": "⛰️",
    "storm clouds": "⛈️",
    "dragon cave": "🕳️",
    "hot fire": "🔥",
    "sword fighting": "⚔️",
    "defeated dragon": "🐉",
    "celebrating people": "🎉",
    "special medal": "🏅",
    "home castle": "🏠",
    "family hugs": "🤗",
    "peaceful sleep": "💤",
    "knight crown": "👑"
}