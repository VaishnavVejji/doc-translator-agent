# translator.py
import pdfplumber
from docx import Document
from deep_translator import GoogleTranslator

def extract_text(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

def extract_and_translate(file_path, target_lang="en"):
    text = extract_text(file_path)
    if not text.strip():
        return ""
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated
    except Exception as e:
        print("Translation error:", e)
        return ""
