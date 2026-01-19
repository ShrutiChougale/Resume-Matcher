import streamlit as st
import pdfplumber
import docx
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.skill {
    background: #00c853;
    padding: 6px 12px;
    border-radius: 20px;
    margin: 4px;
    display: inline-block;
    color: black;
    font-weight: 600;
}
.missing {
    background: #ff4b4b;
    padding: 6px 12px;
    border-radius: 20px;
    margin: 4px;
    display: inline-block;
    color: white;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align:center;'>AI Resume Analyzer & Job Matcher</h1>
<p style='text-align:center; color: #9aa0a6;'>
ATS-style Resume vs Job Description Analyzer using NLP
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- FUNCTIONS ----------------
def extract_text(file):
    text = ""
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + " "
    else:
        text = file.read().decode("utf-8")
    return text.lower()

def extract_skills(text):
    skills_db = [
        "python","java","c","c++","sql","html","css","javascript",
        "react","node","fastapi","flask","machine learning",
        "deep learning","nlp","data science","aws","cloud",
        "docker","kubernetes","git","linux"
    ]
    found = []
    for skill in skills_db:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found.append(skill)
    return sorted(set(found))

def calculate_match(resume, jd):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume, jd])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 2)

def show_skills(skills, missing=False):
    for skill in skills:
        css = "missing" if missing else "skill"
        st.markdown(
            f"<span class='{css}'>{skill}</span>",
            unsafe_allow_html=True
        )

# ---------------- INPUT SECTION ----------------
st.markdown("### 📥 Input Details")
col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader(
        "Upload Resume (PDF / DOCX / TXT)",
        type=["pdf", "docx", "txt"]
    )

with col2:
    jd_text = st.text_area(
        "Paste Job Description",
        height=220
    )

st.markdown("---")

# ---------------- ACTION ----------------
if st.button("🚀 Analyze Resume", use_container_width=True):

    if resume_file and jd_text.strip():

        resume_text = extract_text(resume_file)
        jd_text = jd_text.lower()

        score = calculate_match(resume_text, jd_text)
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)
        missing_skills = list(set(jd_skills) - set(resume_skills))

        # ---------------- RESULTS ----------------
        st.subheader("📊 Resume Match Score")
        st.progress(score / 100)
        st.metric("Match Percentage", f"{score}%")

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("✅ Skills Found")
            if resume_skills:
                show_skills(resume_skills)
            else:
                st.write("No skills detected")

        with col4:
            st.subheader("❌ Missing Skills")
            if missing_skills:
                show_skills(missing_skills, missing=True)
            else:
                st.write("None 🎉")

        # ---------------- AI FEEDBACK ----------------
        st.subheader("🤖 AI Feedback")

        if score >= 75:
            st.success("Strong match. Resume aligns well with the job role.")
        elif score >= 50:
            st.warning("Moderate match. Consider adding missing skills.")
        else:
            st.error("Low match. Resume needs significant improvement.")

    else:
        st.warning("Please upload a resume and paste a job description.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Built with Python, Streamlit & NLP | AI Resume Analyzer Project")
