from pypdf import PdfReader
from docx import Document as Docx


def extract_text_from_file(path: str, content_type: str | None = None) -> str:
    if path.lower().endswith('.txt'):
        return open(path, 'r', encoding='utf-8', errors='ignore').read()
    if path.lower().endswith('.pdf'):
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or '' for page in reader.pages)
    if path.lower().endswith('.docx'):
        doc = Docx(path)
        return "\n".join(p.text for p in doc.paragraphs)
    # Fallback: try binary -> utf-8
    try:
        return open(path, 'r', encoding='utf-8', errors='ignore').read()
    except Exception:
        return ''