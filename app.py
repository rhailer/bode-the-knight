import streamlit as st
import time
from story_data import STORY_DATA
from image_generator import generate_story_images, get_fallback_emojis
import random

# Configure page
st.set_page_config(
    page_title="Bode the Knight",
    page_icon="⚔️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Dark mode CSS
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
        width: 100%;
        min-height: 80px;
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
if 'current_images' not in st.session_state:
    st.session_state.current_images = None
if 'use_ai' not in st.session_state:
    st.session_state.use_ai = True

def reset_game():
    """Reset the game"""
    st.session_state.current_story = 0
    st.session_state.prizes = []
    st.session_state.game_over = False
    st.session_state.game_won = False
    st.session_state.current_images = None

def load_images():
    """Load images for current story"""
    if st.session_state.current_images is None:
        current_data = STORY_DATA[st.session_state.current_story]
        
        # Try AI first
        if st.session_state.use_ai:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("🎨 Creating magical images...")
                progress_bar.progress(25)
                
                ai_images = generate_story_images(
                    current_data["text"],
                    current_data["correct_concept"],
                    current_data["wrong_concepts"]
                )
                
                progress_bar.progress(75)
                
                if ai_images:
                    st.session_state.current_images = ai_images
                    progress_bar.progress(100)
                    status_text.text("✨ Images ready!")
                    time.sleep(0.5)
                    progress_bar.empty()
                    status_text.empty()
                    return
                else:
                    st.session_state.use_ai = False
                    progress_bar.empty()
                    status_text.empty()
                    st.info("Using emoji mode for better performance!")
            except Exception as e:
                st.session_state.use_ai = False
                progress_bar.empty()
                status_text.empty()
                st.warning(f"Switching to emoji mode: {str(e)}")
        
        # Fallback to emojis
        emoji_options = get_fallback_emojis(st.session_state.current_story)
        st.session_state.current_images = emoji_options

def correct_answer():
    """Handle correct answer"""
    prize = STORY_DATA[st.session_state.current_story]["prize"]
    st.session_state.prizes.append(prize)
    
    st.success(f"🎉 Excellent reading! You earned: {prize}")
    
    if st.session_state.current_story < len(STORY_DATA) - 1:
        st.session_state.current_story += 1
        st.session_state.current_images = None
    else:
        st.session_state.game_won = True
    
    time.sleep(1)
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
    
    if st.button("🔄 New Adventure"):
        reset_game()
        st.rerun()
    st.stop()

# Game Over Screen
if st.session_state.game_over:
    st.markdown(f"""
    <div class="game-over-screen">
        <h2>🏰 Bode has returned home!</h2>
        <h3>Every knight needs practice! Try again!</h3>
        <p><strong>You made it to story {st.session_state.current_story + 1} of {len(STORY_DATA)}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.prizes:
        st.markdown('<div class="prize-bag">', unsafe_allow_html=True)
        st.markdown("### 🎒 Prizes you collected:")
        for prize in st.session_state.prizes:
            st.write(f"• {prize}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔄 Try Again"):
        reset_game()
        st.rerun()
    st.stop()

# Main Game
current_data = STORY_DATA[st.session_state.current_story]

# Progress
progress = (st.session_state.current_story + 1) / len(STORY_DATA)
st.progress(progress)
st.markdown(f"**Quest Progress: {st.session_state.current_story + 1} of {len(STORY_DATA)}**")

# Story
st.markdown(f"""
<div class="story-text">
    <h3>📖 The Story:</h3>
    <p style="font-size: 1.3em; color: #FFD700;"><strong>{current_data['text']}</strong></p>
</div>
""", unsafe_allow_html=True)

# Load images
load_images()

# Instructions
st.markdown("### 🎯 Which picture matches the story?")

# Display options with fixed formatting
if st.session_state.current_images:
    col1, col2, col3 = st.columns(3)
    
    for i, (col, item) in enumerate(zip([col1, col2, col3], st.session_state.current_images)):
        with col:
            if 'image' in item:  # AI image
                st.image(item['image'], width=300)  # Fixed width instead of use_column_width
            else:  # Emoji fallback
                st.markdown(f"""
                <div style="
                    font-size: 4em; 
                    text-align: center; 
                    padding: 40px 20px; 
                    background: rgba(255, 255, 255, 0.1); 
                    border-radius: 15px; 
                    margin: 10px 0;
                    border: 2px solid #FFD700;
                    min-height: 200px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">
                    {item["emoji"]}
                </div>
                """, unsafe_allow_html=True)
            
            # Button with better spacing
            if st.button(f"Choose Picture {i+1}", key=f"btn_{i}", use_container_width=True):
                if item['is_correct']:
                    correct_answer()
                else:
                    wrong_answer()

# Prize bag
if st.session_state.prizes:
    st.markdown('<div class="prize-bag">', unsafe_allow_html=True)
    st.markdown("### 🎒 Your Prize Bag:")
    st.markdown(" | ".join(st.session_state.prizes))
    st.markdown('</div>', unsafe_allow_html=True)

# Reset button
if st.button("🔄 Restart Quest"):
    reset_game()
    st.rerun()