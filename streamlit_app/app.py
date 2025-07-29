import streamlit as st
from src.utils.logging_config import setup_logging
setup_logging()


st.title("Resume Autofill Demo")
st.write("Upload your resume to auto-populate application forms!")
