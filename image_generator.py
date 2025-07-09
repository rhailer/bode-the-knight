import openai
import streamlit as st
import requests
from PIL import Image
import io
import random

def generate_story_images(story_text, correct_concept, wrong_concepts):
    """Generate 3 images with consistent style but different content"""
    
    try:
        if "OPENAI_API_KEY" not in st.secrets:
            return None
            
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        # Consistent base style for all images
        base_style = "Batman Animated Series art style, dark atmospheric cartoon, dramatic lighting, art deco influences, medieval fantasy setting, high contrast, clean composition, suitable for children"
        
        # Create prompts that are similar but clearly different
        prompts = [
            f"Medieval knight {correct_concept}, {base_style}",
            f"Medieval knight {wrong_concepts[0]}, {base_style}",
            f"Medieval knight {wrong_concepts[1]}, {base_style}"
        ]
        
        images = []
        
        # Generate all images with consistent parameters
        for i, prompt in enumerate(prompts):
            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                
                image_url = response.data[0].url
                img_response = requests.get(image_url, timeout=20)
                img = Image.open(io.BytesIO(img_response.content))
                
                # Resize for faster loading
                img = img.resize((400, 400), Image.Resampling.LANCZOS)
                
                images.append({
                    'image': img,
                    'is_correct': i == 0,
                    'concept': prompts[i]
                })
                
            except Exception as e:
                st.error(f"Error generating image {i+1}: {str(e)}")
                return None
        
        # Shuffle so correct answer isn't always first
        random.shuffle(images)
        return images
        
    except Exception as e:
        st.warning(f"AI image generation failed: {str(e)}")
        return None

# Enhanced emoji fallback
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
    """Get emoji fallback with consistent structure"""
    if story_index in STORY_EMOJIS:
        emojis = STORY_EMOJIS[story_index].copy()
        options = [
            {'emoji': emojis[0], 'is_correct': True},
            {'emoji': emojis[1], 'is_correct': False},
            {'emoji': emojis[2], 'is_correct': False}
        ]
        random.shuffle(options)
        return options
    
    return [
        {'emoji': '🎯', 'is_correct': True},
        {'emoji': '❌', 'is_correct': False},
        {'emoji': '❓', 'is_correct': False}
    ]