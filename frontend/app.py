import streamlit as st
import requests
import json
import os

# # ---------------------- Config ----------------------
# BACKEND_URL = "http://localhost:8000"  # Adjust this if hosted

# ---------------------- UI ----------------------
st.set_page_config(page_title="SkillGap Analyzer", layout="centered")

st.title("🎓 SkillGap Analyzer")
st.subheader("Upload your resume and get a personalized skill roadmap")

# ---------------------- File Upload ----------------------
uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

# ---------------------- Role Selection ----------------------
roles = [
    "data-analyst", 
    "data-scientist", 
    "game-developer", 
    "blockchain", 
    "cyber-security"
]
selected_role = st.selectbox("Choose your Target Role", roles)

# ---------------------- Submit ----------------------
if st.button("Analyze Resume") and uploaded_file:
    with st.spinner("Analyzing your resume..."):
        # Save file temporarily
        temp_file_path = f"temp/{uploaded_file.name}"
        os.makedirs("temp", exist_ok=True)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Send to backend
        files = {'file': open(temp_file_path, 'rb')}
        response = requests.post(
            f"{BACKEND_URL}/analyze?role={selected_role}",
            files=files
        )

        if response.status_code == 200:
            result = response.json()

            st.success("✅ Analysis Complete!")
            st.markdown(f"**Candidate Name**: {result['candidate_name']}")
            st.markdown(f"**Email**: {result['email']}")
            st.markdown(f"**Role Analyzed**: {result['role']}")

            st.markdown("### 🧠 Extracted Skills")
            st.code(", ".join(result["extracted_skills"]), language="text")

            st.markdown("### 🧩 Missing Skills")
            for skill in result["missing_skills"]:
                st.markdown(f"- **{skill['skill']}** ({skill['level']}, {skill['estimated_time']})")
                for link in skill["course_links"]:
                    st.markdown(f"    - [📘 Resource]({link})")

            st.markdown("### 🌱 Personalized Roadmap")
            for step in result["personalized_roadmap"]:
                st.markdown(f"**Week {step['week']}** → {step['skill']}")
                st.markdown(f"[🔗 Course]({step['course']})")

            # Optional: Display as JSON
            with st.expander("📦 View Full JSON Output"):
                st.json(result)
        else:
            st.error("❌ Failed to analyze resume. Please check backend or try again.")
else:
    st.info("Upload a resume and choose a role to begin.")

