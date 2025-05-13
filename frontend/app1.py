import streamlit as st
from pyresparser import ResumeParser
import json
import os
import tempfile

st.set_page_config(page_title="Skill Gap Analyzer")

# === File helper ===
def get_backend_file_path(selected_role):
    role_file_map = {
        "AI Engineer": "ai-engineer.json",
        "Backend Developer": "backend.json",
        "Data Scientist": "ai-data-scientist.json",
        "Data Analyst": "data-analyst.json"
    }
    role_file = role_file_map.get(selected_role)
    if not role_file:
        raise FileNotFoundError("❌ Role file mapping not found.")
    
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(project_root, "backend", "data", "roles", role_file)

# === UI Tabs ===
tabs = st.tabs(["📄 Skill Gap Analyzer", "🗺️ Role Roadmap"])

# === Tab 1: Resume Analysis ===
with tabs[0]:
    st.header("📄 Upload Resume & Analyze Skills")
    with st.sidebar:
        st.link_button("DSA Roadmap", "https://www.geeksforgeeks.org/dsa-tutorial-learn-data-structures-and-algorithms/")
        st.link_button("Want to challenge yourself with the 30 days of DSA!", "https://docs.google.com/spreadsheets/u/0/d/11tevcTIBQsIvRKIZLbSzCeN4mCO6wD4O5meyrAIfSXw/htmlview?pli=1")
        st.write("Then check out this sheet which help you to cover most of the concepts that is needed for the problem solving skills")
    selected_role = st.selectbox("Choose your target role", ["AI Engineer", "Backend Developer", "Data Scientist","Data Analyst"])
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

    if uploaded_file and selected_role:
        with st.spinner("Parsing resume..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            try:
                resume_data = ResumeParser(tmp_path).get_extracted_data()
                resume_skills = [skill.lower() for skill in resume_data.get("skills", [])]
            except Exception as e:
                st.error(f"❌ Resume parsing failed: {e}")
                os.remove(tmp_path)
                st.stop()
            os.remove(tmp_path)

        with st.spinner("Loading roadmap..."):
            try:
                file_path = get_backend_file_path(selected_role)
                with open(file_path, "r", encoding="utf-8") as f:
                    roadmap_json = json.load(f)
            except Exception as e:
                st.error(f"❌ Roadmap loading failed: {e}")
                st.stop()

        roadmap_titles = [item.get("title", "").lower() for item in roadmap_json.values()]
        matched = [skill for skill in roadmap_titles if skill in resume_skills]
        missing = [skill for skill in roadmap_titles if skill not in resume_skills]
        st.toast("Loading up")
        st.success("✅ Analysis complete!")

        st.markdown("### ✅ Matched Skills")
        st.write(matched or "No matches found.")

        st.markdown("### ❌ Missing Skills")
        st.write(missing or "You're all set!")

# === Tab 2: Roadmap Viewer ===
with tabs[1]:
    st.header("🗺️ View Role Roadmap")

    selected_role = st.selectbox("Select a role to view its roadmap", ["AI Engineer", "Backend Developer", "Data Scientist","Data Analyst"], key="roadmap_role")

    try:
        file_path = get_backend_file_path(selected_role)
        with open(file_path, "r", encoding="utf-8") as f:
            roadmap = json.load(f)
    except Exception as e:
        st.error(f"❌ Failed to load roadmap: {e}")
        st.stop()

    for key, node in roadmap.items():
        st.markdown(f"### 🔹 {node['title']}")
        st.markdown(f"**Description:** {node['description']}")
        for link in node.get("links", []):
            st.markdown(f"- [{link['title']}]({link['url']}) ({link['type']})")
