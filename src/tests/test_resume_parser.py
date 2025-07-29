import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.services.resume_parser import parse_resume

if __name__ == "__main__":
    # Path to your sample resume, update as needed
    sample_resume = os.path.join(os.path.dirname(__file__), "C:\\Users\\bhave\\OneDrive\\Documents\\RESUME\\Resume BJ.pdf")

    try:
        data = parse_resume(sample_resume)
        print("Parsing result:")
        print(data)
    except Exception as e:
        print("Error:", e)
