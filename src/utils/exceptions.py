# src/utils/exceptions.py

import sys
import logging

def error_message_detail(error):
    exc_type, exc_value, exc_tb = sys.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb else "Unknown"
    line_no = exc_tb.tb_lineno if exc_tb else "Unknown"
    msg = f"Error occurred at [{file_name}] on line [{line_no}]: {error}"
    logging.error(msg)
    return msg

class CustomException(Exception):
    """Base class for custom exceptions in this project."""
    def __init__(self, error):
        super().__init__(str(error))
        self.error_message = error_message_detail(error)
    def __str__(self):
        return self.error_message

# Domain-specific exceptions
class ResumeParsingError(CustomException):
    """Raised when a resume cannot be parsed correctly."""
    pass

class InvalidFileFormatError(CustomException):
    """Raised when an uploaded file is not PDF/DOCX."""
    pass

class FormMappingError(CustomException):
    """Raised when form mapping fails."""
    pass

class AuthError(CustomException):
    """Raised on unauthorized API access."""
    pass
