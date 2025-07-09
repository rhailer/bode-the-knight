import streamlit as st
import time
from story_data import STORY_DATA
from image_generator import generate_story_images, EMOJI_FALLBACK
import random

# Configure page with dark theme
st.set_page_config(
    page_title="Bode the Knight",
    page_icon="⚔️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark mode and sleek design
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    
    .main-title {
        text-align: center;
        color: #FFD700;
        font-size: 3em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-bottom: 10px;
    }
    
    .subtitle {
        text-align: center;
        color: #E6E6FA;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    
    .story-text {
        background: rgba(0, 0, 0, 0.3);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #FFD700;
        margin: 20px 0;
        font-size: 1.1em;
        text-align: center;
    }
    
    .prize-bag {
        background: rgba(255, 215, 0, 0.1);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #FFD700;
        margin: 20px 0;
    }
    
    .victory-screen {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: #000;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
    }
    
    .game-over-screen {
        background: rgba(139, 0, 0, 0.8);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
        border: 2px solid #FF6B6B;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 16px;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #FFD700, #FFA500);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_story' not in st.session_state:
    st.session_state.current_story = 0
if 'prizes' not in st.session_state:
    st.session_state.prizes = []
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'game_won' not in st.session_state:
    st.session_state.game_won = False
if 'use_ai_images' not in st.session_state:
    st.session_state.use_ai_images = True
if 'current_images' not in st.session_state:
    st.session_state.current_images = None

def reset_game():
    """Reset the game to beginning"""
    st.session_state.current_story = 0
    st.session_state.prizes = []
    st.session_state.game_over = False
    st.session_state.game_won = False
    st.session_state.current_images = None

def load_story_images():
    """Load images for current story"""
    if st.session_state.current_images is None:
        current_story_data = STORY_DATA[st.session_state.current_story]
        
        if st.session_state.use_ai_images and "OPENAI_API_KEY" in st.secrets:
            with st.spinner("🎨 Creating magical images..."):
                images = generate_story_images(
                    current_story_data["text"],
                    current_story_data["correct_concept"],
                    current_story_data["wrong_concepts"]
                )
                
                if images:
                    # Shuffle so correct answer isn't always first
                    random.shuffle(images)
                    st.session_state.current_images = images
                else:
                    st.session_state.use_ai_images = False
                    st.warning("Falling back to emoji mode...")
        
        # Fallback to emoji mode
        if not st.session_state.use_ai_images:
            # Create emoji fallback
            concepts = [current_story_data["correct_concept"]] + current_story_data["wrong_concepts"]
            emoji_options = ["🏰", "🛡️", "🍳"]  # Default emojis
            
            st.session_state.current_images = [
                {
                    'emoji': emoji_options[i % len(emoji_options)],
                    'concept': concepts[i],
                    'is_correct': i == 0
                } for i in range(3)
            ]
            random.shuffle(st.session_state.current_images)

def correct_answer():
    """Handle correct answer"""
    current_prize = STORY_DATA[st.session_state.current_story]["prize"]
    st.session_state.prizes.append(current_prize)
    
    st.success("🎉 Excellent reading! You earned: " + current_prize)
    time.sleep(1)
    
    if st.session_state.current_story < len(STORY_DATA) - 1:
        st.session_state.current_story += 1
        st.session_state.current_images = None  # Reset images for next story
    else:
        st.session_state.game_won = True
    
    st.rerun()

def wrong_answer():
    """Handle wrong answer"""
    st.error("❌ Not quite right! Bode must return home to study more.")
    st.session_state.game_over = True
    time.sleep(2)
    st.rerun()

# Header
st.markdown('<h1 class="main-title">⚔️ Bode the Knight ⚔️</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">A Magical Reading Adventure</p>', unsafe_allow_html=True)

# Game Won Screen
if st.session_state.game_won:
    st.balloons()
    st.markdown("""
    <div class="victory-screen">
        <h2>🎊 CONGRATULATIONS! 🎊</h2>
        <h3>You've completed Bode's epic adventure!</h3>
        <h2>🏆 You are now a Master Knight! 🏆</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="prize-bag">', unsafe_allow_html=True)
    st.markdown("### 🎒 Your Complete Prize Collection:")
    for i, prize in enumerate(st.session_state.prizes, 1):
        st.write(f"**{i}.** {prize}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔄 New Adventure", key="play_again_won"):
        reset_game()
        st.rerun()
    
    st.stop()

# Game Over Screen
if st.session_state.game_over:
    st.markdown("""
    <div class="game-over-screen">
        <h2>🏰 Bode has returned home!</h2>
        <h3>Every knight needs practice! Try again!</h3>
        <p><strong>You made it to story {} of {}</strong></p>
    </div>
    """.format(st.session_state.current_story + 1, len(STORY_DATA)), unsafe_allow_html=True)
    
    if st.session_state.prizes:
        st.markdown('<div class="prize-bag">', unsafe_allow_html=True)
        st.markdown("### 🎒 Prizes you collected:")
        for prize in st.session_state.prizes:
            st.write(f"• {prize}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔄 Try Again", key="try_again"):
        reset_game()
        st.rerun()
    
    st.stop()

# Main Game Screen
current_story_data = STORY_DATA[st.session_state.current_story]

# Progress indicator
progress = (st.session_state.current_story + 1) / len(STORY_DATA)
st.progress(progress)
st.markdown(f"**Quest Progress: {st.session_state.current_story + 1} of {len(STORY_DATA)}**")

# Story text
st.markdown(f"""
<div class="story-text">
    <h3>📖 The Story:</h3>
    <p style="font-size: 1.3em; color: #FFD700;"><strong>{current_story_data['text']}</strong></p>
</div>
""", unsafe_allow_html=True)

# Load images for current story
load_story_images()

# Instructions
st.markdown("### 🎯 Which picture matches the story?")

# Display images
if st.session_state.current_images:
    col1, col2, col3 = st.columns(3)
    
    for i, (col, image_data) in enumerate(zip([col1, col2, col3], st.session_state.current_images)):
        with col:
            if st.session_state.use_ai_images and 'image' in image_data:
                st.image(image_data['image'], use_column_width=True)
                if st.button(f"Choose Picture {i+1}", key=f"btn_{i}_{st.session_state.current_story}"):
                    if image_data['is_correct']:
                        correct_answer()
                    else:
                        wrong_answer()
            else:
                # Emoji fallback
                if st.button(image_data['emoji'], key=f"btn_{i}_{st.session_state.current_story}"):
                    if image_data['is_correct']:
                        correct_answer()
                    else:
                        wrong_answer()

# Show current prize bag
if st.session_state.prizes:
    st.markdown('<div class="prize-bag">', unsafe_allow_html=True)
    st.markdown("### 🎒 Your Prize Bag:")
    prize_text = " | ".join(st.session_state.prizes)
    st.markdown(f"**{prize_text}**")
    st.markdown('</div>', unsafe_allow_html=True)

# Reset button
if st.button("🔄 Restart Quest"):
    reset_game()
    st.rerun()