import openai
import streamlit as st
import requests
from PIL import Image
import io
import random

def generate_story_images(story_text, correct_concept, wrong_concepts):
    """Generate 3 images with consistent style"""
    
    try:
        # Check for API key
        if "OPENAI_API_KEY" not in st.secrets:
            st.warning("OpenAI API key not found. Using emoji mode.")
            return None
            
        if not st.secrets["OPENAI_API_KEY"].startswith("sk-"):
            st.warning("Invalid OpenAI API key format. Using emoji mode.")
            return None
            
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        base_style = "Batman Animated Series art style, dark atmospheric cartoon, dramatic lighting, medieval fantasy setting, clean composition, suitable for children"
        
        # Create prompts
        prompts = [
            f"Medieval knight {correct_concept}, {base_style}",
            f"Medieval knight {wrong_concepts[0]}, {base_style}", 
            f"Medieval knight {wrong_concepts[1]}, {base_style}"
        ]
        
        images = []
        
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
                img_response = requests.get(image_url, timeout=15)
                img = Image.open(io.BytesIO(img_response.content))
                
                # Resize for better performance
                img = img.resize((400, 400), Image.Resampling.LANCZOS)
                
                images.append({
                    'image': img,
                    'is_correct': i == 0,
                    'concept': prompt
                })
                
            except Exception as e:
                st.error(f"Failed to generate image {i+1}: {str(e)}")
                return None
        
        # Shuffle images
        random.shuffle(images)
        return images
        
    except Exception as e:
        st.warning(f"AI generation failed: {str(e)}")
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
    """Get emoji fallback"""
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