import os 
import logging
from pyresparser import ResumeParser
import pdfplumber
from utils.exceptions import ResumeParsingError, InvalidFileFormatError
from utils.logging_config import setup_logging

setup_logging() # only configures once per process

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {".pdf",".docx"}

def is_allowed_file(filename):
    _, ext = os.path.splitext(filename)
    return ext.lower() in ALLOWED_EXTENSIONS