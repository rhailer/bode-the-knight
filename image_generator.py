import openai
import streamlit as st
import requests
from PIL import Image
import io
import random

def generate_story_images(story_text, correct_concept, wrong_concepts):
    """Generate 3 images for a story using OpenAI DALL-E"""
    
    try:
        # Check if API key exists
        if "OPENAI_API_KEY" not in st.secrets:
            return None
            
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        base_style = "Batman Animated Series art style, dark atmospheric cartoon, clean simple composition, suitable for children"
        
        images = []
        all_concepts = [correct_concept] + wrong_concepts
        
        for i, concept in enumerate(all_concepts):
            try:
                prompt = f"{concept}, {base_style}"
                
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                
                image_url = response.data[0].url
                img_response = requests.get(image_url, timeout=30)
                img = Image.open(io.BytesIO(img_response.content))
                
                images.append({
                    'image': img,
                    'is_correct': i == 0,
                    'concept': concept
                })
                
            except Exception as e:
                st.warning(f"Failed to generate image: {str(e)}")
                return None
        
        # Shuffle so correct answer isn't always first
        random.shuffle(images)
        return images
        
    except Exception as e:
        st.warning(f"AI image generation failed: {str(e)}")
        return None

# Emoji fallback mapping
STORY_EMOJIS = {
    0: ["🏰", "🌳", "🚗"],
    1: ["🛡️", "👕", "🎩"],
    2: ["🍳", "📺", "🛏️"],
    3: ["📜", "📱", "🎮"],
    4: ["🐉", "🐶", "🦋"],
    5: ["🐎", "🚲", "🚗"],
    6: ["🌲", "🏢", "🏖️"],
    7: ["🌉", "🛣️", "✈️"],
    8: ["⛰️", "🏠", "🏊"],
    9: ["⛈️", "☀️", "🌈"],
    10: ["🕳️", "🏠", "🏬"],
    11: ["🔥", "❄️", "💧"],
    12: ["⚔️", "🥄", "✏️"],
    13: ["🐉", "🦅", "🐛"],
    14: ["🎉", "😢", "😴"],
    15: ["🏅", "🍎", "📚"],
    16: ["🏠", "🏪", "🏫"],
    17: ["🤗", "👋", "🤝"],
    18: ["💤", "👀", "🍽️"],
    19: ["👑", "😔", "❓"]
}

def get_fallback_emojis(story_index):
    """Get emoji fallback for a story"""
    if story_index in STORY_EMOJIS:
        emojis = STORY_EMOJIS[story_index].copy()
        random.shuffle(emojis)
        return [
            {'emoji': emojis[0], 'is_correct': True},
            {'emoji': emojis[1], 'is_correct': False},
            {'emoji': emojis[2], 'is_correct': False}
        ]
    return [
        {'emoji': '🎯', 'is_correct': True},
        {'emoji': '❌', 'is_correct': False},
        {'emoji': '❓', 'is_correct': False}
    ]