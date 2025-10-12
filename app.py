# app.py
import streamlit as st
from translator import extract_and_translate
import os

st.set_page_config(page_title="Document Translator Agent", layout="centered")
st.title("📄 Document Translator & Archival Agent")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

# --- Target Language Selection ---
target_lang = st.selectbox(
    "Select target language:",
    ("en", "hi", "fr", "es", "de", "zh")  # English, Hindi, French, Spanish, German, Chinese
)

# --- Process File ---
if uploaded_file is not None:
    # Save uploaded file temporarily
    save_path = os.path.join("temp_upload", uploaded_file.name)
    os.makedirs("temp_upload", exist_ok=True)
    
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("Extracting and translating text... ⏳")

    # Extract & Translate
    translated_text = extract_and_translate(save_path, target_lang)

    if translated_text:
        st.success("✅ Translation completed!")
        st.text_area("Translated Text", translated_text, height=300)
    else:
        st.error("❌ Could not translate the file.")

    # Optional: remove temp file
    os.remove(save_path)
