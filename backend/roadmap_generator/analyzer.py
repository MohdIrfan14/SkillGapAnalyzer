from fastapi import APIRouter, UploadFile, File, Query
import shutil, os, json, uuid
from pyresparser import ResumeParser
from sentence_transformers import SentenceTransformer, util

analyze_resume_route = APIRouter()
model = SentenceTransformer('all-MiniLM-L6-v2')

@analyze_resume_route.post("/analyze")
async def analyze_resume(role: str = Query(...), file: UploadFile = File(...)):
    # Save uploaded resume temporarily
    temp_path = f"temp_uploads/{uuid.uuid4()}_{file.filename}"
    os.makedirs("temp_uploads", exist_ok=True)
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Parse resume
    data = ResumeParser(temp_path).get_extracted_data()
    user_skills = data.get("skills", [])

    # Load target role roadmap
    role_path = f"backend/data/roles/{role}.json"
    with open(role_path, "r") as f:
        roadmap = json.load(f)

    def extract_skills(node, skill_map):
        title = node.get("title")
        url = node.get("url")
        if title:
            if title not in skill_map:
                skill_map[title] = {
                    "level": "Intermediate",
                    "estimated_time": "1 week",
                    "courses": []
                }
            if url:
                skill_map[title]["courses"].append(url)
        for child in node.get("children", []):
            extract_skills(child, skill_map)

    target_skills = {}
    for node in roadmap.get("nodes", []):
        extract_skills(node, target_skills)

    target_names = list(target_skills.keys())
    user_embeddings = model.encode(user_skills, convert_to_tensor=True)
    target_embeddings = model.encode(target_names, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(user_embeddings, target_embeddings)

    matched = set()
    for i in range(len(user_skills)):
        for j in range(len(target_names)):
            if cosine_scores[i][j].item() >= 0.65:
                matched.add(target_names[j])

    missing = list(set(target_names) - matched)

    result = {
        "candidate_name": data.get("name", "Unknown"),
        "email": data.get("email", "Not Found"),
        "role": role,
        "extracted_skills": user_skills,
        "matched_skills": list(matched),
        "missing_skills": [
            {
                "skill": skill,
                "level": target_skills[skill]["level"],
                "estimated_time": target_skills[skill]["estimated_time"],
                "course_links": target_skills[skill]["courses"]
            } for skill in missing
        ],
        "personalized_roadmap": [
            {
                "week": i + 1,
                "skill": skill,
                "course": target_skills[skill]["courses"][0]
            } for i, skill in enumerate(missing)
        ]
    }

    os.makedirs("backend/output", exist_ok=True)
    with open("backend/output/skillgap_analysis.json", "w") as f:
        json.dump(result, f, indent=4)

    return result
