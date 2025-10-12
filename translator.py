# translator.py
import pdfplumber
from docx import Document
from deep_translator import GoogleTranslator
from io import BytesIO

def extract_text(uploaded_file):
    """
    Extract text from uploaded PDF or DOCX file.
    uploaded_file: Streamlit UploadedFile
    """
    # Check file type using the filename
    filename = uploaded_file.name.lower()
    
    if filename.endswith(".pdf"):
        with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        return text

    elif filename.endswith(".docx"):
        doc = Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    else:
        raise ValueError("Unsupported file type. Upload PDF or DOCX.")

def extract_and_translate(uploaded_file, target_language="en"):
    """
    Extract text and translate using GoogleTranslator
    """
    text = extract_text(uploaded_file)
    translator = GoogleTranslator(target=target_language)
    translated_text = translator.translate(text)
    return translated_text
