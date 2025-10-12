import pdfplumber
import docx
from googletrans import Translator

def extract_text_from_pdf(file):
    """Extract all text from a PDF file."""
    with pdfplumber.open(file) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def extract_text_from_docx(file):
    """Extract all text from a Word (.docx) file."""
    doc = docx.Document(file)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_and_translate(file, target_lang):
    """Extract text and translate it using Google Translate."""
    translator = Translator()

    if file.name.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif file.name.endswith(".docx"):
        text = extract_text_from_docx(file)
    else:
        raise ValueError("Unsupported file format. Please upload PDF or DOCX.")

    if not text.strip():
        raise ValueError("No readable text found in the document.")

    translation = translator.translate(text, dest=target_lang)
    return text, translation.text
