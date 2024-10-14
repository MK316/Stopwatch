import streamlit as st
import time
from playsound import playsound
import os

# Set page configuration
st.set_page_config(page_title="Stopwatch", layout="centered")

# Initialize session state
if "stopwatch_started" not in st.session_state:
    st.session_state.stopwatch_started = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0
if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = 0.0

# Function to start the stopwatch
def start_stopwatch():
    if not st.session_state.stopwatch_started:
        st.session_state.start_time = time.time() - st.session_state.elapsed_time
        st.session_state.stopwatch_started = True

# Function to stop the stopwatch
def stop_stopwatch():
    if st.session_state.stopwatch_started:
        st.session_state.elapsed_time = time.time() - st.session_state.start_time
        st.session_state.stopwatch_started = False

# Function to reset the stopwatch
def reset_stopwatch():
    st.session_state.start_time = 0.0
    st.session_state.elapsed_time = 0.0
    st.session_state.stopwatch_started = False

# Function to play sound (when the stopwatch stops or time is up)
def play_sound(file_path):
    if os.path.exists(file_path):
        playsound(file_path)

# Title
st.title("⏱️ Stopwatch with Sound")

# Upload mp3 file for sound
sound_file = st.file_uploader("Upload an MP3 sound to play when time is up", type=["mp3"])

# Display buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Start"):
        start_stopwatch()
with col2:
    if st.button("Stop"):
        stop_stopwatch()
        if sound_file is not None:
            with open("uploaded_sound.mp3", "wb") as f:
                f.write(sound_file.read())
            play_sound("timesup.mp3")
with col3:
    if st.button("Reset"):
        reset_stopwatch()

# Show stopwatch time
if st.session_state.stopwatch_started:
    st.session_state.elapsed_time = time.time() - st.session_state.start_time

# Display the elapsed time in minutes, seconds, and milliseconds
elapsed_time = st.session_state.elapsed_time
minutes, seconds = divmod(elapsed_time, 60)
milliseconds = (elapsed_time - int(elapsed_time)) * 1000

st.write(f"**Elapsed Time:** {int(minutes):02d}:{int(seconds):02d}:{int(milliseconds):03d}")

# Refresh the stopwatch display every second
time.sleep(1)
st.experimental_rerun()
