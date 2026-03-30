import fitz  # pymupdf
from typing import List, Tuple

def load_pdf(file_path: str) -> Tuple[str, List[str]]:
    """
    Load a PDF file and extract text.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Tuple of (full_text, list_of_page_texts)
    """
    doc = fitz.open(file_path)
    full_text = ""
    page_texts = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        page_texts.append(text)
        full_text += text + "\n"
    
    doc.close()
    return full_text, page_texts


def load_pdf_from_bytes(file_bytes: bytes) -> Tuple[str, List[str]]:
    """
    Load a PDF from bytes and extract text.
    
    Args:
        file_bytes: PDF file content as bytes
        
    Returns:
        Tuple of (full_text, list_of_page_texts)
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    full_text = ""
    page_texts = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        page_texts.append(text)
        full_text += text + "\n"
    
    doc.close()
    return full_text, page_texts
