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

# Custom CSS for Xbox-style gaming interface
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    .stApp {
        background: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%),
            linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f0f23 100%);
        color: white;
        font-family: 'Orbitron', monospace;
        overflow-x: hidden;
    }
    
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #00d4ff 0%, #ff6b6b 50%, #ffd700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5em;
        font-weight: 900;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
        margin-bottom: 10px;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.3)); }
        to { filter: drop-shadow(0 0 30px rgba(255, 215, 0, 0.8)); }
    }
    
    .subtitle {
        text-align: center;
        color: #00d4ff;
        font-size: 1.4em;
        font-weight: 700;
        margin-bottom: 30px;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }
    
    .story-text {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.6) 0%, rgba(26, 26, 46, 0.8) 100%);
        padding: 25px;
        border-radius: 20px;
        border: 3px solid;
        border-image: linear-gradient(135deg, #00d4ff, #ff6b6b, #ffd700) 1;
        margin: 20px 0;
        font-size: 1.2em;
        text-align: center;
        box-shadow: 
            0 8px 25px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .story-text::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .prize-bag {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2) 0%, rgba(255, 107, 107, 0.2) 100%);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #ffd700;
        margin: 20px 0;
        box-shadow: 
            0 4px 15px rgba(255, 215, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .victory-screen {
        background: linear-gradient(135deg, #ff6b6b 0%, #ffd700 50%, #00d4ff 100%);
        color: #000;
        padding: 40px;
        border-radius: 25px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 
            0 15px 35px rgba(0, 0, 0, 0.3),
            0 5px 15px rgba(255, 215, 0, 0.4);
        animation: victory-pulse 2s ease-in-out infinite;
    }
    
    @keyframes victory-pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .game-over-screen {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.9) 0%, rgba(139, 0, 0, 0.9) 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
        border: 3px solid #ff6b6b;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: 700;
        border-radius: 15px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 
            0 6px 20px rgba(0, 212, 255, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        width: 100%;
        min-height: 80px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'Orbitron', monospace;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff4757 100%);
        transform: translateY(-3px);
        box-shadow: 
            0 10px 25px rgba(255, 107, 107, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00d4ff 0%, #ff6b6b 50%, #ffd700 100%);
        height: 8px;
        border-radius: 4px;
    }
    
    .stProgress > div > div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }
    
    .game-instruction {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(255, 107, 107, 0.1) 100%);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid rgba(0, 212, 255, 0.3);
        margin: 20px 0;
        text-align: center;
        font-size: 1.1em;
        font-weight: 600;
    }
    
    .image-container {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        border: 3px solid transparent;
        border-radius: 20px;
        padding: 15px;
        margin: 15px 0;
        transition: all 0.3s ease;
        box-shadow: 
            0 8px 25px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .image-container:hover {
        border: 3px solid #00d4ff;
        transform: translateY(-5px);
        box-shadow: 
            0 15px 35px rgba(0, 212, 255, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .progress-text {
        color: #00d4ff;
        font-weight: 700;
        font-size: 1.1em;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00d4ff, #ff6b6b);
        border-radius: 4px;
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

from smart_cache import load_cached_story, generate_and_cache_story, is_story_cached, get_cache_stats

from local_image_loader import load_local_images, has_local_images, count_local_images
from image_generator import get_fallback_emojis

def load_images():
    """Load images - local first, then fallback"""
    if st.session_state.current_images is None:
        story_index = st.session_state.current_story
        
        # Try local images first (instant!)
        if has_local_images(story_index):
            local_images = load_local_images(story_index)
            
            if local_images:
                st.session_state.current_images = local_images
                return
        
        # Fallback to emoji if no local images
        st.info("📱 Using emoji mode - images not yet generated")
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
st.markdown('<h1 class="main-title">⚔️ BODE THE KNIGHT ⚔️</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">🎮 EPIC READING ADVENTURE QUEST 🎮</p>', unsafe_allow_html=True)

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
st.markdown(f'<div class="progress-text">🎯 QUEST PROGRESS: {st.session_state.current_story + 1} of {len(STORY_DATA)} COMPLETED</div>', unsafe_allow_html=True)

# Story
st.markdown(f"""
<div class="story-text">
    <h3>📖 THE STORY:</h3>
    <p style="font-size: 1.3em; color: #00d4ff; font-weight: 700;">{current_data['text']}</p>
</div>
""", unsafe_allow_html=True)

# Load images
load_images()

# Instructions
st.markdown("""
<div class="game-instruction">
    <h3>🎯 CHOOSE YOUR ANSWER!</h3>
    <p>Which picture matches the story? Click to select!</p>
</div>
""", unsafe_allow_html=True)

# Display options with fixed formatting
if st.session_state.current_images:
    col1, col2, col3 = st.columns(3)
    
    for i, (col, item) in enumerate(zip([col1, col2, col3], st.session_state.current_images)):
        with col:
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            
            if 'image' in item:  # AI image
                st.image(item['image'], width=300)
            else:  # Emoji fallback
                st.markdown(f"""
                <div style="
                    font-size: 4em; 
                    text-align: center; 
                    padding: 40px 20px; 
                    background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(255, 107, 107, 0.1));
                    border-radius: 15px; 
                    margin: 10px 0;
                    min-height: 200px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border: 2px solid rgba(0, 212, 255, 0.3);
                ">
                    {item["emoji"]}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Gaming-style button
            if st.button(f"🎮 SELECT {i+1}", key=f"btn_{i}", use_container_width=True):
                if item['is_correct']:
                    correct_answer()
                else:
                    wrong_answer()

# Prize bag
if st.session_state.prizes:
    st.markdown('<div class="prize-bag">', unsafe_allow_html=True)
    st.markdown("### 🎒 YOUR LOOT COLLECTION:")
    prize_display = " | ".join([f"**{prize}**" for prize in st.session_state.prizes])
    st.markdown(f"<p style='color: #ffd700; font-size: 1.1em; font-weight: 700;'>{prize_display}</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Reset button
if st.button("🔄 Restart Quest"):
    reset_game()
    st.rerun()