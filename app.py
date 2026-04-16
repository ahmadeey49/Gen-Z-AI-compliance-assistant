import streamlit as st
import google.generativeai as genai
import os
from PyPDF2 import PdfReader
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import base64
# Wannan zai nuna mana jerin models din da kake da damar amfani da su
try:
    st.write("Checking available models for your API Key...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            st.info(f"Available Model: {m.name}")
except Exception as e:
    st.error(f"Could not list models: {e}")

# --- CONFIGURATION ---
# We fetch the API key from Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = "" # Fallback if secrets is empty

genai.configure(api_key=api_key)

# We use the full model path to ensure it works across all API versions
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

st.set_page_config(
    page_title="Gen Z AI - Robot Assistant", 
    layout="wide", 
    page_icon="⚡"
)

# --- FUNCTIONS ---
def text_to_speech(text):
    """Converts AI response to audio and plays it"""
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")
        with open("response.mp3", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
        st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Audio playback error: {e}")

# --- UI LAYOUT ---
with st.sidebar:
    st.title("🤖 Robot Status")
    st.success("System: Online")
    st.info("Gen Z AI - Built for Nigerian Excellence. Specializing in Law and Compliance.")

st.title("⚡ Gen Z AI (Public Assistant)")
st.markdown("#### *Your Guide to Nigerian Laws & Compliance*")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎤 Voice & Text Input")
    # Voice recording tool
    audio = mic_recorder(
        start_prompt="Click to speak 🎤", 
        stop_prompt="Stop Recording 🛑", 
        key='recorder'
    )
    # Text area
    question = st.text_area("Your Question:", placeholder="e.g., What is TIN and why do I need it?")

with col2:
    st.subheader("📄 Document Analysis")
    uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

# Extract PDF content if uploaded
doc_content = ""
if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        doc_content += page.extract_text()
    st.success(f"Loaded: {uploaded_file.name}")

# --- PROCESSING ---
if st.button("🚀 Process & Ask AI"):
    if not api_key:
        st.error("Error: API Key is missing. Please check Streamlit Secrets.")
    elif question or doc_content:
        with st.spinner("Gen Z AI is thinking..."):
            # The context we give the AI
            prompt = f"""
            You are Gen Z AI, a friendly Nigerian Robot. 
            Answer the following based on Nigerian Law (FRSC, CAC, FIRS, etc.).
            Keep it clear, helpful, and professional.
            
            Document context: {doc_content[:1000]}
            User Question: {question}
            """
            try:
                response = model.generate_content(prompt)
                res_text = response.text
                
                st.divider()
                st.subheader("🤖 Robot Response:")
                st.markdown(res_text)
                
                # Convert the first part of the answer to speech
                text_to_speech(res_text[:300])
                
            except Exception as e:
                st.error(f"Execution Error: {e}")
    else:
        st.warning("Please provide a question or a document.")

st.divider()
st.markdown("<center>Gen Z AI v2.0 🚀</center>", unsafe_allow_html=True)
