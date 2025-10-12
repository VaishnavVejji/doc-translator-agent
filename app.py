# app.py
import streamlit as st
from translator import extract_and_translate

# Set page config for modern feel
st.set_page_config(
    page_title="Document Translator Agent",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📄 Document Translator & Archival Agent")
st.markdown(
    "Upload a PDF or DOCX file and get it translated instantly. "
    "Choose your target language from the sidebar."
)

# Sidebar for language selection
st.sidebar.header("Settings")
target_language = st.sidebar.selectbox(
    "Select target language",
    options=[
        ("English", "en"),
        ("Hindi", "hi"),
        ("Spanish", "es"),
        ("French", "fr"),
        ("German", "de"),
        ("Japanese", "ja"),
        ("Chinese (Simplified)", "zh-CN")
    ],
    format_func=lambda x: x[0]  # display language name
)[1]  # pick the language code

# File uploader
uploaded_file = st.file_uploader(
    "Upload PDF or DOCX",
    type=["pdf", "docx"],
    help="Upload a PDF or Word document for translation"
)

if uploaded_file is not None:
    try:
        with st.spinner("Translating your document..."):
            translated_text = extract_and_translate(uploaded_file, target_language)
        st.success("✅ Translation Complete!")
        
        # Display in a large text area
        st.text_area("Translated Text", translated_text, height=400)
        
        # Option to download translated text
        st.download_button(
            label="Download Translated Text",
            data=translated_text,
            file_name=f"translated_{uploaded_file.name}.txt",
            mime="text/plain"
        )
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
