# 🎓 SkillGap Analyzer for College Students

> Empowering students to align their skills with industry expectations using AI-driven roadmaps and personalized learning recommendations.

---

## 🚀 Overview

**SkillGap Analyzer** helps students identify the missing skills required for specific job roles by analyzing their resume against current market demands. It goes one step further by generating a **personalized learning roadmap** with curated courses to bridge that gap.

---

## 📌 Features

✅ Resume parsing and skill extraction  
✅ Job description comparison using NLP + embeddings  
✅ Missing skill detection via cosine similarity  
✅ Personalized course recommendations from Coursera/edX  
✅ AI-generated weekly learning roadmap  
✅ Clean and interactive UI (Streamlit)  
✅ Backend API built with FastAPI

---

## 🧠 How It Works

1. 🧾 Upload your resume
2. 🎯 Select your target job role
3. 🤖 Backend performs skill gap analysis
4. 📚 Get a course list + detailed learning roadmap

---

## 🧰 Tech Stack

| Area              | Technology                           |
|-------------------|---------------------------------------|
| Frontend          | Streamlit                            |
| Backend           | FastAPI                              |
| NLP               | SpaCy, Sentence-BERT (HuggingFace)   |
| Parsing           | pyresparser, docx2txt                |
| Recommender       | Coursera / edX API / Scraping        |
| Roadmap Engine    | LangChain + HuggingFace Transformers |
| Database          | PostgreSQL                           |
| Deployment        | Streamlit Cloud / Heroku             |
| Containerization  | Docker                               |
| CI/CD             | GitHub Actions                       |

---

## ⚙️ Installation

### 🐍 Clone & Set up the Environment

```bash
git clone https://github.com/MohdIrfan14/SkillGapAnalyzer.git
cd SkillGapAnalyzer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
