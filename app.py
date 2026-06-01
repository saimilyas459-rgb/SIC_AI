import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

# Page Settings
st.set_page_config(page_title="SIC AI Dashboard", page_icon="🤖", layout="wide")

# UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #0f172a !important; color: #ffffff; }
    .header-box { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 5px solid #0284c7; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); margin-bottom: 25px; }
    .header-title { color: #0f172a; font-family: 'Arial Black', Gadget, sans-serif; font-size: 28px; }
    .header-subtitle { color: #0284c7; font-weight: bold; font-size: 16px; margin-top: 5px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-box">
        <div class="header-title">🤖 HI! I AM SIC AI.</div>
        <div class="header-subtitle">I WAS CREATED BY SAIM ILYAS CHAUDHARY.</div>
    </div>
""", unsafe_allow_html=True)

# API Configuration (UPDATED FOR SECRETS)
try:
    # Yeh line Streamlit ke Secrets section se key uthayegi
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("API Key missing! Please set GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #38bdf8;'>SIC AI PANEL</h2>", unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    
    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.rerun()

# History Render
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "audio_path" in message:
            if os.path.exists(message["audio_path"]):
                st.audio(message["audio_path"])

# Chat Logic
if user_input := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("SIC AI is thinking..."):
            try:
                response = model.generate_content(f"You are SIC AI, assistant to Saim Ilyas Chaudhary. User says: {user_input}")
                ai_reply = response.text
                st.markdown(ai_reply)
                
                audio_filename = f"reply_{len(st.session_state.messages)}.mp3"
                tts = gTTS(text=ai_reply, lang='en')
                tts.save(audio_filename)
                st.audio(audio_filename)
                
                st.session_state.messages.append({"role": "assistant", "content": ai_reply, "audio_path": audio_filename})
            except Exception as e:
                st.error(f"Error: {e}")