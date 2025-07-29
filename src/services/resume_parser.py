import os 
import logging
from pyresparser import ResumeParser
import pdfplumber
from utils.exceptions import ResumeParsingError, InvalidFileFormatError
from utils.logging_config import setup_logging

setup_logging() # only configures once per process

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {".pdf",".docx"}

# checking if the file extension is supported or not 
def is_allowed_file(filename): 
    _, ext = os.path.splitext(filename)
    return ext.lower() in ALLOWED_EXTENSIONS

def parse_resume(file_path: str, static_info: dict = None):
    """
    Extract structured resume information from a PDF or DOCX file.
    Uses pyresparser; falls back to pdfplumber for raw PDFs.

    Args:
        file_path (str): Path to the resume file.
        static_info (dict): Extra static info to merge with parsed data.

    Returns:
        dict: Parsed and merged resume data.

    Raises:
        InvalidFileFormatError: Wrong file type.
        ResumeParsingError: All parsing methods failed.
    """
# checking for the correct extension
    try:
        if not is_allowed_file(file_path):
            logger.warning(f"Invalid file extension for file {file_path}")
            raise InvalidFileFormatError(f"Unsupprted file format")

        logger.info(f"Starting resume parsing for file: {file_path}")


        # Trying pyresparser first 
        try:
            parsed_data = ResumeParser(file_path).get_extracted_data()
            logger.info(f"pyresparser output {parsed_data}")
        except Exception as e:
            logger.warning(f"pyresparser failed for {file_path}")
            parsed_data = None

        # if essential info missing then try pdfplumber

        essential_fields = ['name','email','skills']
        if not parsed_data or not all(parsed_data.get(f) for f in essential_fields):
            logger.info(f"pyresparser missing essentials for {file_path}; trying pdfplumber fallback.")
            if file_path.lower().endswith('.pdf'):
                try:
                    with pdfplumber.open(file_path) as pdf:
                        text = '\n'.join(page.extract_text() or '' for page in pdf.pages)
                    parsed_data = {'raw_text': text}
                    logger.info("pdfplumber fallback succeeded.")
                except Exception as e:
                    logger.error(f"pdfplumber failed for file {file_path}: {str(e)}")
                    raise ResumeParsingError(f"Extraction failed for file  {file_path} (pdfplumber): {str(e)}")
            else:
                logger.error("Fallback parser not available for DOCX or essentials missing.")
                raise ResumeParsingError(f"Resume could not be parsed or required fields missing for file {file_path}.")
            if static_info:
                logger.info(f"Merging static info: {static_info}")
                parsed_data.update(static_info)

            logger.info(f"Resume parsing complete for file {file_path}")
            return parsed_data
        
    except (InvalidFileFormatError, ResumeParsingError) as e:
        logging.error(f"unhandled resume parsing for file {file_path}: {str(e)}")
        raise ResumeParsingError(e)

if __name__ == '__main__':
    file = is_allowed_file("C:\\Users\\bhave\\OneDrive\\Documents\\RESUME\\Resume BJ.pdf")
    print(file)

    