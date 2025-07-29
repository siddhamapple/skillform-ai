"""
src/utils/file_validation.py

Robust file validation for uploaded resumes:
- Checks both extension and actual MIME type (content signature)
- Prevents malicious uploads (e.g. EXE renamed to .pdf)
"""

import os
import logging
import magic 

from src.utils.exceptions import InvalidFileFormatError

# Allowed extensions and MIME types
ALLOWED_EXTENSIONS = {'.pdf', '.docx'}
ALLOWED_MIME_TYPES = {
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # DOCX
}

def validate_resume_file(upload_file) -> bool:
    """
    Validates that the uploaded file is a valid PDF or DOCX via extension & MIME.
    Args:
        upload_file: FastAPI UploadFile (or similar with .filename and .file)
    Returns:
        bool: True if valid, raises exception if invalid.
    Raises:
        InvalidFileFormatError
    """
    filename = upload_file.filename
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        msg = f"File extension {ext} not allowed. Only PDF and DOCX are accepted."
        logging.warning(msg)
        raise InvalidFileFormatError(msg)

    # Read a small chunk to check magic bytes/MIME
    pos = upload_file.file.tell()
    file_head = upload_file.file.read(2048)
    mime_type = magic.from_buffer(file_head, mime=True)
    upload_file.file.seek(pos)  # Reset file pointer

    if mime_type not in ALLOWED_MIME_TYPES:
        msg = f"File content MIME type {mime_type} is not allowed."
        logging.warning(msg)
        raise InvalidFileFormatError(msg)

    # Optionally log on success
    logging.info(f"File {filename} validated with MIME type {mime_type}.")
    return True
