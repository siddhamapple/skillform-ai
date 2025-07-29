"""
src/services/upload.py

Handles:
- File validation (extension/MIME/signature)
- File saving
- Resume parsing (pyresparser + fallback)
- Merges parsed and static form data
- Structured logging for every major step
- Raises custom exceptions throughout
"""

import os
import logging
from typing import Dict

from src.utils.file_validation import validate_resume_file
from src.services.resume_parser import parse_resume
from src.utils.exceptions import (
    ResumeParsingError,
    InvalidFileFormatError,
    CustomException,
)

def handle_upload(resume_file, static_info: Dict, temp_dir: str = "temp_uploads") -> Dict:
    """
    Orchestrate validation, saving, parsing, combine static info.
    Args:
        resume_file: FastAPI UploadFile (or same interface object)
        static_info: dict of static input fields
        temp_dir: directory for temp file saving
    Raises:
        InvalidFileFormatError, ResumeParsingError
    Returns:
        dict: Merged mapping of form-ready fields
    """
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, resume_file.filename)
    try:
        # 1. Validate filetype and content
        logging.info(f"Validating upload: {resume_file.filename}")
        if not validate_resume_file(resume_file):
            logging.warning(f"Invalid file attempted: {resume_file.filename}")
            raise InvalidFileFormatError("File is not a valid PDF or DOCX.")

        # 2. Save file temporarily
        with open(temp_path, "wb") as f:
            f.write(resume_file.file.read())
        logging.info(f"Saved file to: {temp_path}")

        # 3. Resume parsing (primary + fallback inside parse_resume)
        try:
            parsed = parse_resume(temp_path)
            logging.info(f"Resume parsed: {resume_file.filename}")
        except Exception as e:
            logging.error(f"Resume parsing failed for {resume_file.filename}: {e}")
            raise ResumeParsingError(e)

        # 4. Merge parsed + static info
        merged = dict(parsed or {})
        merged.update(static_info)
        logging.info("Merged parsed resume data with static input.")

        return merged

    except CustomException as ce:
        logging.error(f"CustomException during upload: {ce}")
        raise ce
    except Exception as e:
        logging.exception(f"Unexpected error in handle_upload: {e}")
        raise CustomException(e)
    finally:
        # Cleanup temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            logging.info(f"Removed temp file: {temp_path}")
