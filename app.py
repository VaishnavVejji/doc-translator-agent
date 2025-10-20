import streamlit as st
from io import BytesIO
from translator import extract_and_translate, translate_docx, translate_text
from pathlib import Path
from docx import Document
import fitz  # PyMuPDF
import time

# --- Page Setup ---
st.set_page_config(page_title="Classy Document Translator", page_icon="🌐", layout="wide")

# --- CSS Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
:root{
  --bg: #0b0d10;
  --panel: rgba(255,255,255,0.03);
  --muted: #bdbdbd;
  --accent1: linear-gradient(90deg, #00ffc3, #00aaff);
  --glass-border: rgba(255,255,255,0.06);
}
html, body, [class*="css"] {
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
  color: #e9eef6;
  background: radial-gradient(1200px 600px at 10% 10%, rgba(0,160,255,0.06), transparent),
              radial-gradient(1000px 400px at 90% 90%, rgba(102,217,239,0.03), transparent),
              var(--bg) !important;
}
.hero h1 {
  font-size: 34px;
  font-weight: 800;
  background: -webkit-linear-gradient(90deg,#00ffc3,#00aaff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.muted { color: var(--muted); font-size:13px; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="hero">
<h1>🌐 Classy Document Translator</h1>
<p class="muted">Translate PDFs & DOCX while preserving layout — downloadable as a polished PDF.</p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.header("Settings")
    target_language = st.selectbox(
        "Target language",
        options=[
            ("English", "en"), ("Hindi", "hi"), ("Spanish", "es"),
            ("French", "fr"), ("German", "de"), ("Japanese", "ja"),
            ("Chinese (Simplified)", "zh-CN")
        ],
        index=0,
        format_func=lambda x: x[0]
    )[1]
    show_original = st.checkbox("Show original text preview", value=True)

# --- File Uploader ---
uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

# --- Utilities ---
def safe_filename(name: str):
    name = Path(name).stem
    return "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).rstrip()

translated_file_bytes = None
original_text_preview = ""
combined_translated_text = ""

# --- File Translation Logic ---
if uploaded_file:
    uploaded_bytes = uploaded_file.read()
    uploaded_file_memory = BytesIO(uploaded_bytes)

    if st.button("Translate Now"):
        try:
            with st.spinner("Translating..."):
                time.sleep(0.2)
                filename = uploaded_file.name.lower()

                # ----- PDF -----
                if filename.endswith(".pdf"):
                    translated_file_bytes, combined_translated_text = extract_and_translate(
                        uploaded_file_memory, target_language
                    )

                    # Preview original PDF text (first few blocks)
                    uploaded_file_memory.seek(0)
                    doc = fitz.open(stream=uploaded_file_memory.read(), filetype="pdf")
                    blocks = []
                    for page in doc:
                        for b in page.get_text("blocks"):
                            if len(b) >= 5:
                                blocks.append(b[4])
                    original_text_preview = "\n".join(blocks[:10])  # first 10 blocks

                # ----- DOCX -----
                elif filename.endswith(".docx"):
                    translated_file_bytes, combined_translated_text = translate_docx(
                        uploaded_file_memory, target_language
                    )

                    # Preview original DOCX text
                    if show_original:
                        uploaded_file_memory.seek(0)
                        doc = Document(uploaded_file_memory)
                        original_text_preview = "\n".join([p.text for p in doc.paragraphs])

        except Exception as e:
            st.error(f"Translation failed: {e}")

# --- Preview & Download ---
if translated_file_bytes:
    col1, col2 = st.columns(2)
    if show_original:
        with col1:
            st.subheader("Original Text (Preview)")
            st.text_area("Original", value=original_text_preview, height=300)
    with col2:
        st.subheader("Translated Text (Preview)")
        st.text_area("Translated", value=combined_translated_text, height=300)

    st.markdown("---")
    download_name = f"translated_{safe_filename(uploaded_file.name)}.pdf"
    st.download_button(
        "⬇️ Download Translated PDF",
        data=translated_file_bytes,
        file_name=download_name,
        mime="application/pdf"
    )

# --- Live Text Translation ---
st.markdown("---")
st.header("💬 Live Text Translation")

input_text = st.text_area("Type or paste text here to translate", height=150)

if input_text.strip():
    target_lang_live = st.selectbox(
        "Select target language for live translation",
        options=[
            ("English", "en"), ("Hindi", "hi"), ("Spanish", "es"),
            ("French", "fr"), ("German", "de"), ("Japanese", "ja"),
            ("Chinese (Simplified)", "zh-CN")
        ],
        index=0,
        key="live_text_lang",
        format_func=lambda x: x[0]
    )[1]

    with st.spinner("Translating..."):
        translated_live = translate_text(input_text, target_lang_live)

    st.subheader("Translated Text")
    st.text_area("Translation", value=translated_live, height=150)

# --- Footer ---
st.markdown("""
<footer style='text-align:center; padding:20px; color:#8f9aa7;'>
© 2025 • Classy Document Translator • Built with Streamlit & PyMuPDF
</footer>
""", unsafe_allow_html=True)
