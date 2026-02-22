import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import mediapipe as mp
import cv2
import av

# --- AI LOGIC ENGINE ---
def get_fashion_advice(age, gender, occasion, fit, season):
    # Permutation Logic
    advice = f"As a {age} {gender} in the {season} season, "
    
    if age == "Old" and fit == "Saggy":
        advice += "you should try 'Dopamine Dressing' with oversized silk kaftans and bold zari work."
    elif age == "Young" and fit == "Tight":
        advice += "go for tech-knit mock necks and structured high-waist denim."
    else:
        advice += "a transitional linen blazer with tapered trousers is your best bet."
        
    if gender == "Female":
        advice += " Pair this with a soft peach-tone blush and geometric silver earrings."
    
    return advice

# --- WEBRTC VISION PROCESSOR ---
class PoseProcessor(VideoProcessorBase):
    def __init__(self):
        self.pose = mp.solutions.pose.Pose()
        self.drawing = mp.solutions.drawing_utils

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img_rgb)

        if results.pose_landmarks:
            # Draw the skeleton for the "Body Scan" effect
            self.drawing.draw_landmarks(img, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- STREAMLIT UI ---
st.set_page_config(page_title="AI Style Architect", layout="wide")
st.title("🤖 AI Style Architect: Body Scan & Stylist")

# 1. Onboarding Questions
with st.sidebar:
    st.header("Step 1: Your Profile")
    name = st.text_input("Name")
    age_val = st.number_input("Age", 1, 100, 25)
    age_cat = "Young" if age_val < 26 else "Middle-Aged" if age_val < 51 else "Old"
    
    gender = st.radio("Gender", ["Male", "Female"])
    occasion = st.selectbox("Occasion", ["Wedding", "College", "Office", "Party"])
    fit = st.radio("Fit Preference", ["Saggy", "Tight", "Regular"])
    season = "Indian Transitional Spring"

# 2. Generate Advice
if st.sidebar.button("Generate My Fit"):
    st.subheader(f"✨ Style Verdict for {name}")
    advice_text = get_fashion_advice(age_cat, gender, occasion, fit, season)
    st.info(advice_text)

# 3. Live Body Scan
st.subheader("📸 Step 2: Live Body Scan")
st.write("Stand back so the AI can analyze your proportions!")
webrtc_streamer(key="style-scan", video_processor_factory=PoseProcessor)