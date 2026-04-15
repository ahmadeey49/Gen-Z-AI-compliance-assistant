import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import base64
import hashlib
import time

# 1. SETUP & CONFIGURATION
load_dotenv()
# Amfani da Gemini 1.5 Flash don gudu da inganci
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(
    page_title="Gen Z AI - Robot Assistant", 
    layout="wide", 
    page_icon="⚡"
)

# --- FUNCTIONS ---
def text_to_speech(text):
    """Yana mayar da rubutu zuwa murya"""
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
        start_prompt="Danna nan don yin magana (Voice) 🎤", 
        stop_prompt="Tsaya (Stop) 🛑", 
        key='recorder'
    )
    
    # Text Input
    question = st.text_area("Rubuta tambayarka a nan:", placeholder="Misali: Mene ne hakki na idan 'Road Safety' suka tsayar da ni?")

with col2:
    st.subheader("📄 Document Analysis")
    uploaded_file = st.file_uploader("Dora takardar ka (PDF) don tantancewa", type="pdf")

# Logic for PDF Content
doc_content = ""
file_hash = ""
if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        doc_content += page.extract_text()
    file_hash = hashlib.sha256(uploaded_file.getvalue()).hexdigest()
    st.success(f"File Uploaded: {uploaded_file.name}")
    st.code(f"Blockchain Hash: {file_hash[:20]}...", language="text")

# --- EXECUTION ---
if st.button("🚀 Process & Ask AI"):
    if question or doc_content:
        with st.spinner("Gen Z AI yana nazari..."):
            # Sabon Prompt dinka
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
                
                # Murya ta tashi
                text_to_speech(res_text[:350]) # Karanta takaitaccen bayani don gudun nauyi
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Da fatan za a yi magana, rubuta tambaya, ko dora takarda.")

st.divider()
st.center = st.markdown("<center>Gen Z AI - Built for Nigerian Excellence 🚀</center>", unsafe_allow_html=True)
