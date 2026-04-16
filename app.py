#=========================================

FIXED AI Compliance Assistant (Streamlit + Gemini)

Fully Working Version (Voice + PDF + AI)

#=========================================

import streamlit as st import google.generativeai as genai import os from dotenv import load_dotenv from PyPDF2 import PdfReader from streamlit_mic_recorder import mic_recorder from gtts import gTTS import base64 import hashlib

LOAD ENV

load_dotenv()

CONFIGURE GEMINI

genai.configure(api_key=os.getenv("GEMINI_API_KEY")) model = genai.GenerativeModel(model_name="gemini-1.5-flash")

PAGE CONFIG

st.set_page_config(page_title="Gen Z AI", layout="wide")

TEXT TO SPEECH

def text_to_speech(text): try: tts = gTTS(text=text, lang='en') tts.save("response.mp3") with open("response.mp3", "rb") as f: data = f.read() b64 = base64.b64encode(data).decode() st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True) except Exception as e: st.error(f"Audio Error: {e}")

SIDEBAR

with st.sidebar: st.title("🤖 Robot Core") st.success("System Online")

MAIN UI

st.title("⚡ Gen Z AI Compliance Assistant")

col1, col2 = st.columns(2)

with col1: audio = mic_recorder(start_prompt="🎤 Speak", stop_prompt="Stop", key="rec") question = st.text_area("Ask question")

with col2: uploaded_file = st.file_uploader("Upload PDF", type="pdf")

PDF PROCESS

doc_content = "" if uploaded_file: reader = PdfReader(uploaded_file) for page in reader.pages: doc_content += page.extract_text() or "" st.success("PDF Loaded")

RUN AI

if st.button("Ask AI"): if question or doc_content: prompt = f""" You are a Nigerian Compliance AI. Help with CAC, FIRS, NDPR, Police, FRSC.

Document: {doc_content[:1000]}
    Question: {question}
    """

    try:
        response = model.generate_content(prompt)
        try:
            res_text = response.text
        except:
            res_text = response.candidates[0].content.parts[0].text

        st.subheader("Answer")
        st.write(res_text)

        text_to_speech(res_text[:300])

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Enter question or upload file")

FOOTER

st.markdown("---") st.markdown("Gen Z AI 🚀")



