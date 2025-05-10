import streamlit as st
import requests
from pyresparser import ResumeParser
import tempfile
import os

# --- STEP 1: Define role → roadmap.json mapping ---
ROADMAP_URLS = {
    "AI Engineer": "https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/public/roadmap-content/ai-engineer.json",
    "Data Scientist": "https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/public/roadmap-content/data-scientist.json",
    "Software Engineer": "https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/public/roadmap-content/software-engineer.json",
    "Backend Developer": "https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/public/roadmap-content/backend.json",
    "Data Analyst": "https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/public/roadmap-content/data-analyst.json"
}

# --- Streamlit UI ---
st.title("🧠 Skill Gap Analyzer")
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
selected_role = st.selectbox("Choose a target role", list(ROADMAP_URLS.keys()))

if uploaded_file and selected_role:
    with st.spinner("Parsing resume..."):
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        # Step 2: Parse resume
        try:
            resume_data = ResumeParser(tmp_path).get_extracted_data()
            resume_skills = [skill.lower() for skill in resume_data.get("skills", [])]
        except Exception as e:
            st.error(f"Error parsing resume: {e}")
            os.remove(tmp_path)
            st.stop()

        os.remove(tmp_path)  # Clean up

        # Step 3: Fetch roadmap JSON
        roadmap_url = ROADMAP_URLS[selected_role]
        try:
            response = requests.get(roadmap_url)
            response.raise_for_status()
            roadmap_json = response.json()
        except Exception as e:
            st.error(f"Failed to load roadmap: {e}")
            st.stop()

        # Step 4: Extract titles from JSON
        roadmap_titles = [item.get("title", "").lower() for item in roadmap_json.values()]
        matched = [skill for skill in roadmap_titles if skill in resume_skills]
        missing = [skill for skill in roadmap_titles if skill not in resume_skills]

        # Step 5: Display Results
        st.success("✅ Resume parsed and roadmap loaded!")

        st.markdown("### ✔️ Matched Skills")
        st.write(matched if matched else "No matches found.")

        st.markdown("### ❌ Missing Skills")
        st.write(missing if missing else "No missing skills. You're all set!")

