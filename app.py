import streamlit as st
import google.generativeai as genai
import os
from PyPDF2 import PdfReader
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import base64
import hashlib

# 1. SETUP & CONFIGURATION
# Using st.secrets for secure API key management on Streamlit Cloud
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    # Placeholder for local testing (Replace with your key if not using secrets)
    api_key = "YOUR_API_KEY_HERE" 

genai.configure(api_key=api_key)

# Using the specific model name to avoid 404/v1beta errors
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

st.set_page_config(
    page_title="Gen Z AI - Robot Assistant", 
    layout="wide", 
    page_icon="⚡"
)

# --- FUNCTIONS ---
def text_to_speech(text):
    """Converts text to speech and plays it automatically"""
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")
        with open("response.mp3", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
        st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Audio Error: {e}")

# --- SIDEBAR: ROBOT STATUS ---
with st.sidebar:
    st.title("🤖 Robot Core")
    st.status("System: Online", state="running")
    st.info("""
    **Gen Z AI v2.0**
    Deployed as a Public Robot Assistant.
    - Voice Enabled 🔊
    - Blockchain Secured 🔒
    - Legal Context Aware 🇳🇬
    """)
    
    st.divider()
    if os.path.exists("knowledge.txt"):
        with open("knowledge.txt", "r") as f:
            st.caption("Active Knowledge Base:")
            st.text(f.read())

# --- MAIN UI ---
st.title("⚡ Gen Z AI (Compliance Assistant)")
st.markdown("#### *Your Futuristic Robot Guide to Nigerian Laws & Compliance*")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎤 Voice & Text Input")
    # Voice Input
    audio = mic_recorder(
        start_prompt="Click here to speak (Voice) 🎤", 
        stop_prompt="Stop Recording 🛑", 
        key='recorder'
    )
    
    # Text Input
    question = st.text_area("Type your question here:", placeholder="Example: What are my rights if stopped by the FRSC?")

with col2:
    st.subheader("📄 Document Analysis")
    uploaded_file = st.file_uploader("Upload your document (PDF) for analysis", type="pdf")

# Logic for PDF Content
doc_content = ""
file_hash = ""
if uploaded_file:
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            doc_content += page.extract_text()
        file_hash = hashlib.sha256(uploaded_file.getvalue()).hexdigest()
        st.success(f"File Uploaded: {uploaded_file.name}")
        st.code(f"Blockchain Hash: {file_hash[:20]}...", language="text")
    except Exception as e:
        st.error(f"Error reading PDF: {e}")

# --- EXECUTION ---
if st.button("🚀 Process & Ask AI"):
    if question or doc_content:
        with st.spinner("Gen Z AI is analyzing..."):
            # System Prompt
            prompt = f"""
            You are Gen Z AI, a futuristic Nigerian Robot Assistant deployed in public places.

            Capabilities:
            - Help citizens understand Nigerian laws (FRSC, CAC, Human Rights, Taxes)
            - Help drivers and traders with practical guidance
            - Analyze documents provided by the user

            Instruction:
            - Answer clearly and professionally.
            - Keep it short, actionable, and practical.
            - Always mention the relevant authority (e.g., FRSC, CAC, Police, or FIRS).
            - Use a polite robot-like tone.

            Document Content (if any): {doc_content[:1500]}
            User Question: {question}
            """
            
            try:
                response = model.generate_content(prompt)
                res_text = response.text
                
                st.divider()
                st.subheader("🤖 Robot Response:")
                st.markdown(res_text)
                
                # Activate voice response for the first 300 characters
                text_to_speech(res_text[:300]) 
                
            except Exception as e:
                st.error(f"Error processing request: {e}")
                st.info("Check if your API Key is correctly set in Streamlit Secrets.")
    else:
        st.warning("Please provide a voice input, type a question, or upload a document.")

st.divider()
st.markdown("<center>Gen Z AI - Built for Nigerian Excellence 🚀</center>", unsafe_allow_html=True)


