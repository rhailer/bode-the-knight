import streamlit as st
import time
from story_data import STORY_DATA

# Configure page
st.set_page_config(
    page_title="Bode the Knight",
    page_icon="⚔️",
    layout="centered"
)

# Initialize session state
if 'current_story' not in st.session_state:
    st.session_state.current_story = 0
if 'prizes' not in st.session_state:
    st.session_state.prizes = []
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'game_won' not in st.session_state:
    st.session_state.game_won = False

def reset_game():
    """Reset the game to beginning"""
    st.session_state.current_story = 0
    st.session_state.prizes = []
    st.session_state.game_over = False
    st.session_state.game_won = False

def correct_answer():
    """Handle correct answer"""
    # Add prize to bag
    current_prize = STORY_DATA[st.session_state.current_story]["prize"]
    st.session_state.prizes.append(current_prize)
    
    # Show success message
    st.success("🎉 Correct! You earned: " + current_prize)
    time.sleep(1)
    
    # Move to next story or end game
    if st.session_state.current_story < len(STORY_DATA) - 1:
        st.session_state.current_story += 1
    else:
        st.session_state.game_won = True
    
    st.rerun()

def wrong_answer():
    """Handle wrong answer"""
    st.error("❌ Wrong answer! Bode must return home to try again.")
    st.session_state.game_over = True
    time.sleep(2)
    st.rerun()

# Title and Header
st.title("⚔️ Bode the Knight ⚔️")
st.markdown("### A Reading Adventure Game")

# Game Won Screen
if st.session_state.game_won:
    st.balloons()
    st.success("🎊 CONGRATULATIONS! 🎊")
    st.markdown("### You've completed Bode's adventure!")
    st.markdown("**🏆 You are now a Master Knight! 🏆**")
    
    # Show all prizes
    st.markdown("### Your Prize Bag:")
    for i, prize in enumerate(st.session_state.prizes, 1):
        st.write(f"{i}. {prize}")
    
    if st.button("🔄 Play Again", key="play_again_won"):
        reset_game()
        st.rerun()
    
    st.stop()

# Game Over Screen
if st.session_state.game_over:
    st.error("🏰 Bode has returned home!")
    st.markdown("### Don't worry! Knights always try again!")
    st.markdown(f"**You made it to story {st.session_state.current_story + 1} of {len(STORY_DATA)}**")
    
    # Show prizes collected so far
    if st.session_state.prizes:
        st.markdown("### Prizes you collected:")
        for prize in st.session_state.prizes:
            st.write(f"• {prize}")
    
    if st.button("🔄 Try Again", key="try_again"):
        reset_game()
        st.rerun()
    
    st.stop()

# Main Game Screen
current_story_data = STORY_DATA[st.session_state.current_story]

# Progress indicator
progress = (st.session_state.current_story + 1) / len(STORY_DATA)
st.progress(progress)
st.markdown(f"**Story {st.session_state.current_story + 1} of {len(STORY_DATA)}**")

# Story text
st.markdown("### 📖 Story:")
st.markdown(f"**{current_story_data['text']}**")

# Instructions
st.markdown("### 🎯 Which picture matches the story?")

# Create three columns for the options
col1, col2, col3 = st.columns(3)

with col1:
    if st.button(current_story_data['options'][0], key=f"btn1_{st.session_state.current_story}"):
        if current_story_data['options'][0] == current_story_data['correct_image']:
            correct_answer()
        else:
            wrong_answer()

with col2:
    if st.button(current_story_data['options'][1], key=f"btn2_{st.session_state.current_story}"):
        if current_story_data['options'][1] == current_story_data['correct_image']:
            correct_answer()
        else:
            wrong_answer()

with col3:
    if st.button(current_story_data['options'][2], key=f"btn3_{st.session_state.current_story}"):
        if current_story_data['options'][2] == current_story_data['correct_image']:
            correct_answer()
        else:
            wrong_answer()

# Show current prize bag
if st.session_state.prizes:
    st.markdown("### 🎒 Your Prize Bag:")
    prize_text = " | ".join(st.session_state.prizes)
    st.markdown(f"**{prize_text}**")

# Reset button (for testing)
if st.button("🔄 Restart Game"):
    reset_game()
    st.rerun()

# Footer
st.markdown("---")
st.markdown("*Made with ❤️ for young knights learning to read!*")