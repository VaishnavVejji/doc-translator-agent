import streamlit as st
from translator import extract_and_translate
from storage import save_translation, list_archives, load_archive

st.set_page_config(page_title="Document Translation & Archival Agent", layout="wide")

st.title("📄 Simple Document Translation & Archival Agent")

tab1, tab2 = st.tabs(["🌐 Translate Document", "📚 View Archives"])

with tab1:
    uploaded_file = st.file_uploader("Upload a document (PDF or DOCX)", type=["pdf", "docx"])
    target_lang = st.selectbox("Select target language", ["en", "hi", "fr", "es", "de", "ml", "ta"])

    if uploaded_file is not None:
        if st.button("Translate & Save"):
            with st.spinner("Processing..."):
                text, translated = extract_and_translate(uploaded_file, target_lang)
                st.subheader("Original Text:")
                st.write(text[:1000] + "..." if len(text) > 1000 else text)

                st.subheader("Translated Text:")
                st.write(translated)

                file_id = save_translation(uploaded_file.name, text, translated, target_lang)
                st.success(f"✅ Translation archived with ID: {file_id}")

with tab2:
    st.subheader("Saved Translations")
    archives = list_archives()
    if archives:
        for a in archives:
            if st.button(f"View {a}"):
                data = load_archive(a)
                st.write(f"**File:** {data['filename']}")
                st.write(f"**Language:** {data['language']}")
                st.write("**Original:**", data["original"][:500] + "...")
                st.write("**Translated:**", data["translated"][:500] + "...")
    else:
        st.info("No archived translations yet.")
