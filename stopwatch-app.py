import streamlit as st
import time
from datetime import datetime
import pytz

# Set page configuration
st.set_page_config(page_title="Countdown Timer", layout="centered")

# Initialize session state
if "countdown_started" not in st.session_state:
    st.session_state.countdown_started = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0
if "remaining_time" not in st.session_state:
    st.session_state.remaining_time = 0

# Function to display the current time in Seoul
def display_current_time():
    seoul_tz = pytz.timezone('Asia/Seoul')  # Seoul timezone
    current_time = datetime.now(seoul_tz).strftime("%H:%M:%S")
    # Styling the current time display
    current_time_placeholder.markdown(
        f"<h1 style='text-align: center; font-size: 80px; color: #4F8FB0;'>{current_time}</h1>", 
        unsafe_allow_html=True
    )

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
st.title("🐧 MK316 Quiet Timer ⏳")

# Display the current time below the title
current_time_placeholder = st.empty()

# Continuously update the current time, keeping it visible
def update_clock():
    while True:
        display_current_time()
        time.sleep(1)

# Input field for countdown time in seconds
st.session_state.start_time = st.number_input("Set Countdown Time (in seconds)", min_value=0, max_value=3600, value=120)

# Button styling using custom CSS
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #FFDD57;
        color: black;
        height: 3em;
        width: 10em;
        border-radius: 10px;
        border: 2px solid #FFDD57;
        font-size: 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Countdown Start and Reset buttons aligned in the center
col1, col2, col3 = st.columns([1, 2, 1])  # Three columns for central alignment
with col2:
    start_button = st.button("Start Countdown")
    reset_button = st.button("Reset Countdown")

# Placeholder for displaying the countdown time
placeholder = st.empty()

# Countdown timer logic (separate from the current clock)
if start_button:
    start_countdown()

if reset_button:
    reset_countdown()

# Countdown timer logic
if st.session_state.countdown_started:
    while st.session_state.remaining_time > 0:
        minutes, seconds = divmod(st.session_state.remaining_time, 60)
        placeholder.markdown(f"<h2 style='text-align: center;'>{int(minutes):02d}:{int(seconds):02d}</h2>", unsafe_allow_html=True)

        # Countdown logic
        st.session_state.remaining_time -= 1
        time.sleep(1)

    # When the countdown finishes
    if st.session_state.remaining_time <= 0:
        placeholder.markdown("⏰ **Time's Up!**")
        st.session_state.countdown_started = False
        # Play the sound using Streamlit's audio player
        audio_file = open("timesup.mp3", "rb")
        st.audio(audio_file.read(), format="audio/mp3")

# Ensure that the current time is always displayed
display_current_time()
