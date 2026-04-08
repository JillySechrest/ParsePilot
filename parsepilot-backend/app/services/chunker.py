import io
from typing import Optional

def extract_text(file_bytes: bytes, extension: str) -> str:
    """
    Extract plain text from file based on type
    Each file format requires different extraction method
    """
    if extension == ".pdf":
        #PyPDF2 reads PDF files page-by-page
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    
    elif extension == ".csv":
        # For CSVs, decode to string - each row is a "passage"
        return file_bytes.decode("utf-8")
    
    elif extension == ".md":
        # MD is already text
        return file_bytes.decode("utf-8")
    
    else:
        raise ValueError(f"Unsupported file type: {extension}")
    
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping chunks of 'chunk_size' characters

    Args:
        text: Full document text
        chunk_size: Target characters per chunk (not hard limit)
        overlap: Characters of overlap between consecutive chunks
    
    Returns:
        List of text chunks
    """
    if not text.strip():
        return []
    
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Try to break at sentence boundry (period, newline) near end
        if end < len(text):
            # Search for last period or newline in chunk
            for boundary in [",. ", ".\n", "\n\n", "\n"]:
                last_boundary = text[start:end].rfind(boundary)
                if last_boundary != -1:
                    end = start + last_boundary + len(boundary)
                    break
        
        chunk = text[start:end].strip()
        # Don't add empty chunks
        if chunk:
            chunks.append(chunk)

        # Move forward by chunk_size - overlap
        start = end - overlap if end < len(text) else end

    return chunks