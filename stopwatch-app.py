import streamlit as st
import time
import pytz
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Countdown Timer", layout="centered")

# Initialize session state for countdown
if "countdown_started" not in st.session_state:
    st.session_state.countdown_started = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0
if "remaining_time" not in st.session_state:
    st.session_state.remaining_time = 0
if "time_up" not in st.session_state:
    st.session_state.time_up = False

# Title
st.title("🐧 MK316 Quiet Timer ⏳ ")

# Placeholder to display the current time (digital clock)
current_time_placeholder = st.empty()

# Function to display the current time (as a live digital clock)
def display_current_time():
    seoul_tz = pytz.timezone('Asia/Seoul')  # Set timezone to Seoul
    current_time = datetime.now(seoul_tz).strftime("%H:%M:%S")  # Convert to Seoul time
    
    # Style the clock (increase font size and set color)
    current_time_placeholder.markdown(
        f"<h1 style='text-align: center; font-size: 80px; color: #00FF00;'>{current_time}</h1>",  # Green and large font
        unsafe_allow_html=True
    )
    
# Function to start the countdown timer
def start_countdown():
    if not st.session_state.countdown_started:
        st.session_state.remaining_time = st.session_state.start_time
        st.session_state.countdown_started = True
        st.session_state.time_up = False

# Function to reset the countdown timer
def reset_countdown():
    st.session_state.start_time = 0
    st.session_state.remaining_time = 0
    st.session_state.countdown_started = False
    st.session_state.time_up = False

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
countdown_placeholder = st.empty()

# Timer countdown loop (only runs when countdown has started)
while True:
    # Update the clock every second
    display_current_time()

    if st.session_state.countdown_started and not st.session_state.time_up:
        # Display countdown time while the countdown is running
        if st.session_state.remaining_time > 0:
            minutes, seconds = divmod(st.session_state.remaining_time, 60)
            countdown_placeholder.write(f"**Remaining Time:** {int(minutes):02d}:{int(seconds):02d}")
            st.session_state.remaining_time -= 1
        else:
            # When the countdown finishes, display the message and play the sound
            st.session_state.time_up = True
            countdown_placeholder.write("⏰ **Time's Up!**")
            st.session_state.countdown_started = False

            # Play the sound using Streamlit's audio player
            audio_file = open("timesup.mp3", "rb")
            st.audio(audio_file.read(), format="audio/mp3")

    # Sleep for a second
    time.sleep(1)
