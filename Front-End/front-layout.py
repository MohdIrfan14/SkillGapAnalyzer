import sys
import streamlit as st
from backend.roadmap_generator.analyzer import analyze_resume
import tempfile
import json
import os

sys.path.append('/home/irfan/Documents/SkillGapAnalyzer/')

st.set_page_config(page_title="SkillGap Analyzer", layout="wide")
st.title("🎓 SkillGap Analyzer for College Students")

# Upload sectionimport streamlit as st
from backend.resume_parser.parser import parse_resume
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

# Role selection
selected_role = st.selectbox("Select your target role", ["Data Analyst", "Data Scientist"])

if st.button("Analyze Resume"):
    if uploaded_file and selected_role:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded_file.read())
            resume_path = tmp.name
skills= resume_data['skills']
print(skills)