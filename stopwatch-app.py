import streamlit as st
import time

# Set page configuration
st.set_page_config(page_title="Countdown Timer", layout="centered")

# Initialize session state
if "countdown_started" not in st.session_state:
    st.session_state.countdown_started = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0
if "remaining_time" not in st.session_state:
    st.session_state.remaining_time = 0

# Function to start the countdown timer
def start_countdown():
    if not st.session_state.countdown_started:
        st.session_state.remaining_time = st.session_state.start_time
        st.session_state.countdown_started = True

# Function to reset the countdown timer
def reset_countdown():
    st.session_state.start_time = 0
    st.session_state.remaining_time = 0
    st.session_state.countdown_started = False

# Title
st.title("⏳ Countdown Timer with Sound")

# Input field for countdown time in seconds
st.session_state.start_time = st.number_input("Set Countdown Time (in seconds)", min_value=0, max_value=3600, value=10)

# Countdown Start, Stop, and Reset buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Start Countdown"):
        start_countdown()
with col2:
    if st.button("Reset Countdown"):
        reset_countdown()

# Placeholder for displaying the countdown time
placeholder = st.empty()

# Timer countdown loop
while st.session_state.countdown_started and st.session_state.remaining_time > 0:
    minutes, seconds = divmod(st.session_state.remaining_time, 60)
    placeholder.write(f"**Remaining Time:** {int(minutes):02d}:{int(seconds):02d}")
    
    # Countdown logic
    st.session_state.remaining_time -= 1
    time.sleep(1)

# When the countdown finishes, display the message and play the sound
if st.session_state.countdown_started and st.session_state.remaining_time <= 0:
    placeholder.write("⏰ **Time's Up!**")
    st.session_state.countdown_started = False

    # Play the sound using Streamlit's audio player
    audio_file = open("alarm.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")
