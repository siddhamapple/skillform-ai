
import os
import logging
from typing import Dict, Any, List, Optional

from src.utils.exceptions import ResumeParsingError, InvalidFileFormatError
from src.utils.file_validation import validate_resume_file

def is_allowed_file(filename: str, allowed_exts={".pdf", ".docx"}) -> bool:
    _, ext = os.path.splitext(filename)
    return ext.lower() in allowed_exts

def fallback_pdfplumber(file_path: str) -> Dict[str, Any]:
    """Extract basic info with pdfplumber + regex, as fallback."""
    import pdfplumber, re
    fields = {}
    try:
        with pdfplumber.open(file_path) as pdf:
            text = '\n'.join((page.extract_text() or '') for page in pdf.pages)
    except Exception as e:
        raise ResumeParsingError(f"pdfplumber fallback failed: {str(e)}")
    # Regex-based basic field extraction (expand these as needed)
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    phone_match = re.search(r"(\+?\d[\d \-]{8,}\d)", text)
    fields["email"] = email_match.group(0) if email_match else None
    fields["phone"] = phone_match.group(0) if phone_match else None
    fields["raw_text"] = text
    return fields

def parse_resume(
    file_path: str,
    required_fields: List[str],
    static_info: Optional[Dict[str, Any]] = None,
) -> (Dict[str, Any], List[str]):
    """
    Tries to fill all required_fields using parsed data + static_info.
    Returns both the merged field dict & missing fields list.

    Args:
        file_path: Path to the resume.
        required_fields: Fields needed for the form.
        static_info: Pre-collected manual info (from user).

    Returns:
        merged (dict): Field: value pairs from resume or static.
        missing_fields (list): Keys still needing user input.
    """
    logger = logging.getLogger(__name__)

    # 1. Validate extension + content
    if not is_allowed_file(file_path):
        logger.warning(f"Invalid extension: {file_path}")
        raise InvalidFileFormatError(f"Unsupported file extension: {file_path}")
    validate_resume_file(file_path)
    logger.info(f"Starting parse for required fields: {required_fields}")

    # 2. Try pyresparser first
    parsed = {}
    try:
        from pyresparser import ResumeParser
        parsed = ResumeParser(file_path).get_extracted_data() or {}
        logger.info(f"pyresparser output: {parsed}")
    except Exception as e:
        logger.warning(f"pyresparser failed: {e}")
        parsed = {}

    # 3. Fallback if essentials missing (PDFs only — can expand for DOCX too)
    essentials_missing = [f for f in required_fields if not parsed.get(f)]
    if essentials_missing and file_path.lower().endswith('.pdf'):
        try:
            fallback = fallback_pdfplumber(file_path)
            # Only add fallback fields if not already present
            for field in essentials_missing:
                if fallback.get(field) and not parsed.get(field):
                    parsed[field] = fallback[field]
            logger.info("Fallback extractor fields merged in.")
        except Exception as e:
            logger.error(f"pdfplumber fallback failed: {e}")

    # 4. Merge (form logic): parsed → static_info
    merged = {}
    static_info = static_info or {}
    for field in required_fields:
        # Prefer parsed, else static, else leave blank
        value = parsed.get(field)
        if value:
            merged[field] = value
        elif static_info.get(field):
            merged[field] = static_info[field]

    # 5. Identify remaining missing fields (for frontend to prompt the user)
    missing_fields = [f for f in required_fields if not merged.get(f)]

    logger.info(f"Fields after parsing and merging: {merged}")
    logger.info(f"Still missing: {missing_fields}")

    if not merged and missing_fields == required_fields:
        logger.error(f"Completely failed to parse {file_path}: all fields missing.")
        raise ResumeParsingError(f"No required fields parsed from: {file_path}")

    return merged, missing_fields
