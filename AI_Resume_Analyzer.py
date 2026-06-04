import streamlit as st
from pypdf import PdfReader
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide",
)

st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

def extract_text(pdf_file):
    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

        return text

if uploaded_file:

    resume_text = extract_text(
        uploaded_file
    )

    prompt = f"""
    
    Analyze this resume.
    
    Provide:
    
    1. Candidate Summary
    2. Technical Skills
    3.Strengths
    4.Weaknesses
    5.Missing Skills
    6.Hiring Recommendations
    
    Resume:
    
    {resume_text}
    """

    response = (
        client.chat.completions.create(
            model = "llama-3.3-70b-versatile",

            messages=[
                {
                    "role" : "user",
                     "content": prompt
                }
            ]
        )
    )

    analysis = (
        response.choices[0].message.content
    )

    st.subheader("Analysis Result")

    st.write(analysis)

