import streamlit as st
import openai
import requests
from PIL import Image
import io
import os
import random
import hashlib

def get_cache_filename(story_index, image_type):
    """Generate consistent cache filename"""
    return f"cached_images/story_{story_index}_{image_type}.png"

def ensure_cache_directory():
    """Make sure cache directory exists"""
    if not os.path.exists("cached_images"):
        os.makedirs("cached_images")

def is_story_cached(story_index):
    """Check if all 3 images for a story are cached"""
    return all(os.path.exists(get_cache_filename(story_index, img_type)) 
               for img_type in ['correct', 'wrong1', 'wrong2'])

def generate_and_cache_story(story_index, correct_concept, wrong_concepts):
    """Generate images for one story and cache them"""
    
    try:
        if "OPENAI_API_KEY" not in st.secrets:
            return None
            
        ensure_cache_directory()
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        base_style = "Batman Animated Series art style, dark atmospheric cartoon, dramatic lighting, medieval fantasy setting, clean composition, suitable for children"
        
        concepts = [correct_concept] + wrong_concepts
        image_types = ['correct', 'wrong1', 'wrong2']
        
        # Generate all 3 images for this story
        for i, (concept, img_type) in enumerate(zip(concepts, image_types)):
            cache_file = get_cache_filename(story_index, img_type)
            
            # Skip if already cached
            if os.path.exists(cache_file):
                continue
                
            try:
                prompt = f"Medieval knight {concept}, {base_style}"
                
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
                img = img.resize((400, 400), Image.Resampling.LANCZOS)
                
                # Save to cache
                img.save(cache_file)
                
            except Exception as e:
                st.error(f"Failed to generate {img_type} image: {e}")
                return None
        
        return True
        
    except Exception as e:
        st.error(f"Cache generation failed: {e}")
        return None

def load_cached_story(story_index):
    """Load cached images for a story"""
    
    if not is_story_cached(story_index):
        return None
    
    try:
        images = []
        image_types = ['correct', 'wrong1', 'wrong2']
        
        for i, img_type in enumerate(image_types):
            cache_file = get_cache_filename(story_index, img_type)
            img = Image.open(cache_file)
            
            images.append({
                'image': img,
                'is_correct': i == 0,
                'cached': True
            })
        
        # Shuffle so correct isn't always first
        random.shuffle(images)
        return images
        
    except Exception as e:
        st.error(f"Failed to load cached images: {e}")
        return None

def get_cache_stats():
    """Get statistics about cached images"""
    cached_stories = 0
    for i in range(20):  # 20 stories
        if is_story_cached(i):
            cached_stories += 1
    
    return {
        'cached_stories': cached_stories,
        'total_stories': 20,
        'percentage': (cached_stories / 20) * 100
    }