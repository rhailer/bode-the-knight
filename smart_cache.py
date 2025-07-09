import streamlit as st
import openai
import requests
from PIL import Image
import io
import os
import random
import time

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

def clean_prompt(concept):
    """Clean and improve the prompt for better AI generation"""
    # Remove any problematic words and make more specific
    concept = concept.lower()
    
    # Make prompts more specific and child-friendly
    if "sleeping peacefully" in concept:
        return "resting in a comfortable bed with closed eyes"
    elif "putting on regular clothes" in concept:
        return "wearing everyday medieval clothing instead of armor"
    elif "taking off" in concept:
        return "removing armor pieces in a castle room"
    elif "eating alone" in concept:
        return "sitting by himself at a wooden table with food"
    elif "sending a message" in concept:
        return "handing a scroll to a messenger"
    elif "dragon sleeping" in concept:
        return "peaceful dragon resting in a cave"
    elif "dragon being friendly" in concept:
        return "dragon playing gently with village children"
    elif "running away from dragon" in concept:
        return "knight quickly walking away from a large dragon"
    elif "dragon winning" in concept:
        return "dragon standing proudly while knight sits down"
    
    # Default: return cleaned concept
    return concept.replace("instead of", "rather than").replace("defeating", "winning against")

def generate_and_cache_story(story_index, correct_concept, wrong_concepts):
    """Generate images for one story and cache them"""
    
    try:
        if "OPENAI_API_KEY" not in st.secrets:
            return None
            
        ensure_cache_directory()
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        # More specific and compliant base style
        base_style = "cartoon illustration in Batman Animated Series style, medieval fantasy art, dark atmospheric lighting, suitable for children's book, clean simple composition, friendly characters"
        
        concepts = [correct_concept] + wrong_concepts
        image_types = ['correct', 'wrong1', 'wrong2']
        
        # Generate all 3 images for this story
        for i, (concept, img_type) in enumerate(zip(concepts, image_types)):
            cache_file = get_cache_filename(story_index, img_type)
            
            # Skip if already cached
            if os.path.exists(cache_file):
                st.write(f"✅ {img_type} already cached")
                continue
                
            try:
                # Clean the concept for better AI generation
                cleaned_concept = clean_prompt(concept)
                
                # More specific prompt structure
                prompt = f"A cartoon illustration of a medieval knight character {cleaned_concept}. {base_style}. No violence, child-friendly, colorful, high quality digital art."
                
                st.write(f"🎨 Generating {img_type} image...")
                
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
                img = img.resize((400, 400), Image.Resampling.LANCZOS)
                
                # Save to cache
                img.save(cache_file)
                st.write(f"✅ Saved {img_type} to cache")
                
                # Small delay to avoid rate limiting
                time.sleep(2)
                
            except Exception as e:
                st.error(f"Failed to generate {img_type} image: {e}")
                # Continue with other images instead of failing completely
                continue
        
        # Check if we got at least the correct image
        if os.path.exists(get_cache_filename(story_index, 'correct')):
            return True
        else:
            return None
        
    except Exception as e:
        st.error(f"Cache generation failed: {e}")
        return None

def load_cached_story(story_index):
    """Load cached images for a story (even if incomplete)"""
    
    try:
        images = []
        image_types = ['correct', 'wrong1', 'wrong2']
        
        for i, img_type in enumerate(image_types):
            cache_file = get_cache_filename(story_index, img_type)
            
            if os.path.exists(cache_file):
                img = Image.open(cache_file)
                images.append({
                    'image': img,
                    'is_correct': i == 0,
                    'cached': True
                })
        
        # If we have at least one image, fill the rest with emojis
        if len(images) > 0:
            # Fill missing images with emojis
            emoji_fallbacks = ["🎯", "❌", "❓"]
            while len(images) < 3:
                images.append({
                    'emoji': emoji_fallbacks[len(images) % len(emoji_fallbacks)],
                    'is_correct': False,
                    'cached': False
                })
            
            # Shuffle so correct isn't always first
            random.shuffle(images)
            return images
        
        return None
        
    except Exception as e:
        st.error(f"Failed to load cached images: {e}")
        return None

def get_cache_stats():
    """Get statistics about cached images"""
    cached_stories = 0
    partial_stories = 0
    
    for i in range(20):  # 20 stories
        if is_story_cached(i):
            cached_stories += 1
        elif os.path.exists(get_cache_filename(i, 'correct')):
            partial_stories += 1
    
    return {
        'cached_stories': cached_stories,
        'partial_stories': partial_stories,
        'total_stories': 20,
        'percentage': (cached_stories / 20) * 100
    }