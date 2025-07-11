import streamlit as st
from PIL import Image
import os
import random

def load_local_images(story_index):
    """Load locally generated images for a story"""
    
    try:
        images = []
        image_types = ['correct', 'wrong1', 'wrong2']
        
        for i, img_type in enumerate(image_types):
            filename = f"images/story_{story_index}_{img_type}.png"
            
            if os.path.exists(filename):
                img = Image.open(filename)
                # Resize for web display
                img = img.resize((400, 400), Image.Resampling.LANCZOS)
                
                images.append({
                    'image': img,
                    'is_correct': i == 0,
                    'source': 'local'
                })
            else:
                st.warning(f"Image not found: {filename}")
                return None
        
        # Shuffle so correct answer isn't always first
        random.shuffle(images)
        return images
        
    except Exception as e:
        st.error(f"Error loading local images: {e}")
        return None

def count_local_images():
    """Count how many complete story sets exist"""
    count = 0
    for i in range(20):
        if all(os.path.exists(f"images/story_{i}_{img_type}.png") 
               for img_type in ['correct', 'wrong1', 'wrong2']):
            count += 1
    return count

def has_local_images(story_index):
    """Check if local images exist for a story"""
    return all(os.path.exists(f"images/story_{story_index}_{img_type}.png") 
               for img_type in ['correct', 'wrong1', 'wrong2'])