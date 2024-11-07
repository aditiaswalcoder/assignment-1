import fitz  # PyMuPDF for PDF handling
from docx import Document
from typing import Union

def extract_text(content: bytes, filename: str) -> str:
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(content)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(content)
    elif filename.endswith(".txt"):
        return content.decode("utf-8")
    else:
        raise ValueError("Unsupported file type")

def extract_text_from_pdf(content: bytes) -> str:
    pdf_document = fitz.open(stream=content, filetype="pdf")
    text = ""
    for page_num in range(pdf_document.page_count):
        text += pdf_document.load_page(page_num).get_text()
    pdf_document.close()
    return text

def extract_text_from_docx(content: bytes) -> str:
    doc = Document(io.BytesIO(content))
    return "\n".join([para.text for para in doc.paragraphs])
