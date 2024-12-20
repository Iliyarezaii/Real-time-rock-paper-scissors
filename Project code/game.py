import streamlit as st
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import random
import numpy as np
name = st.text_input("Enter your name:")
# Initialize Streamlit page
st.title(f'Hi, {name} welcome to my Rock, Paper, Scissors Game')

st.write("Select your choice using buttons or use hand gestures!")



# Initialize the hand detector
detector = HandDetector(maxHands=1)

# Options for rock, paper, scissors
options = ['rock', 'paper', 'scissors']

# Streamlit session state for game state persistence
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'your_point' not in st.session_state:
    st.session_state.your_point = 0
if 'computer_point' not in st.session_state:
    st.session_state.computer_point = 0
if 'user_choice' not in st.session_state:
    st.session_state.user_choice = None
if 'using_hand_gesture' not in st.session_state:
    st.session_state.using_hand_gesture = False  # Mode toggle: False means using buttons, True means using hand gestures

# Initialize webcam capture (one-time initialization)
cap = cv2.VideoCapture(0)

# Function to display game result
def display_game_result(your_choice, computer_choice):
    if your_choice == computer_choice:
        return "It's a draw!"
    elif (your_choice == 'rock' and computer_choice == 'scissors') or \
         (your_choice == 'paper' and computer_choice == 'rock') or \
         (your_choice == 'scissors' and computer_choice == 'paper'):
        st.session_state.your_point += 1
        return f"{name} wins this round!"
    else:
        st.session_state.computer_point += 1
        return "Computer wins this round!"

# Function to capture hand gesture
def detect_hand_gesture():
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert image to RGB for Streamlit display
    hands, img = detector.findHands(img)
    return img_rgb, hands

# Toggle mode button
if st.button('Toggle Gesture Mode'):
    st.session_state.using_hand_gesture = not st.session_state.using_hand_gesture

# Start the game
if st.button('Start Game'):
    st.session_state.game_started = True

# Game loop
if st.session_state.game_started:
    st.write(f"{name} points: {st.session_state.your_point} | Computer points: {st.session_state.computer_point}")
    
    # Show webcam feed if using hand gestures
    if st.session_state.using_hand_gesture:
        img_rgb, hands = detect_hand_gesture()
        st.image(img_rgb, channels="RGB", use_column_width=True)

        # Wait for hand gesture (if no button was clicked)
        if hands:
            hand = hands[0]
            fingers = detector.fingersUp(hand)

            # Detect the gesture based on fingers up
            if fingers == [0, 0, 0, 0, 0]:  # Rock (thumb up)
                st.session_state.user_choice = 'rock'
            elif fingers == [1, 1, 1, 1, 1]:  # Paper (index and middle fingers up)
                st.session_state.user_choice = 'paper'
            elif fingers == [0, 1, 1, 0, 0]:  # Scissors (pinky up)
                st.session_state.user_choice = 'scissors'

    # Show buttons for manual selection if not using hand gestures
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('Rock'):
                st.session_state.user_choice = 'rock'
        with col2:
            if st.button('Paper'):
                st.session_state.user_choice = 'paper'
        with col3:
            if st.button('Scissors'):
                st.session_state.user_choice = 'scissors'

    # If a valid choice is made (either by button or hand gesture), play the round
    if st.session_state.user_choice:
        # Computer's choice (random)
        computer_choice = random.choice(options)

        # Display the choices
        st.write(f"{name} chose: {st.session_state.user_choice} | Computer chose: {computer_choice}")

        # Display round result
        result = display_game_result(st.session_state.user_choice, computer_choice)
        st.write(result)

        # Reset user choice for next round
        st.session_state.user_choice = None

        # Check if game over (10 points to win)
        if st.session_state.your_point >= 3 or st.session_state.computer_point >= 3:
            if st.session_state.your_point > st.session_state.computer_point:
                st.write(f"🎉{name} win the game! 🎉")
            else:
                st.write("😞 Computer wins the game 😞")
            st.session_state.game_started = False
            st.session_state.your_point = 0
            st.session_state.computer_point = 0

    # Option to quit the game
    if st.button('Quit Game'):
        st.session_state.game_started = False
        st.session_state.your_point = 0
        st.session_state.computer_point = 0
        cap.release()

# Release resources when done
cap.release()

st.write("""This Code is made by python🐍""")
st.markdown('[Made by Iliya Rezaii](https://iliyarezaii.ir/resume.html)')

