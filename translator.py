# translator.py
import pdfplumber
from docx import Document
from deep_translator import GoogleTranslator

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using pdfplumber.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting PDF: {e}")
    return text.strip()


def extract_text_from_docx(docx_path):
    """
    Extract text from a Word (.docx) file using python-docx.
    """
    text = ""
    try:
        doc = Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
    return text.strip()


def translate_text(text, target_lang='en'):
    """
    Translate text to target language using deep-translator's GoogleTranslator.
    target_lang: ISO 639-1 language code, e.g., 'en', 'fr', 'hi'
    """
    if not text:
        return ""
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated
    except Exception as e:
        print(f"Error translating text: {e}")
        return ""


def extract_and_translate(file_path, target_lang='en'):
    """
    Determine file type, extract text, and translate it.
    Supports PDF and DOCX.
    """
    text = ""
    if file_path.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        print("Unsupported file type. Only PDF and DOCX are supported.")
        return None

    translated_text = translate_text(text, target_lang)
    return translated_text


# Optional test
if __name__ == "__main__":
    test_file_pdf = "sample.pdf"
    test_file_docx = "sample.docx"
    print("PDF Translation:", extract_and_translate(test_file_pdf, "en"))
    print("DOCX Translation:", extract_and_translate(test_file_docx, "en"))
