import io
from PyPDF2 import PdfReader
from fastapi import UploadFile


async def extract_text_from_pdf(upload_file: UploadFile) -> str:
    content = await upload_file.read()
    if not content:
        return ""

    text_parts = []
    try:
        reader = PdfReader(io.BytesIO(content))
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
    except Exception:
        pass

    text = "\n".join(text_parts).strip()
    if text:
        return text

    try:
        return content.decode("utf-8", errors="ignore")
    except Exception:
        return ""
