import streamlit as st
from resume_parser import extract_text
from skill_extractor import extract_skills
from matcher import match_resume

# Page config
st.set_page_config(
    page_title="Resume Matcher",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
h1, h2, h3 {
    color: #ffffff;
}
.block-container {
    padding-top: 2rem;
}
.skill-box {
    padding: 8px 12px;
    border-radius: 6px;
    margin: 4px;
    display: inline-block;
    background-color: #262730;
    color: white;
}
.missing {
    background-color: #402626;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("📄 Resume Matcher")
st.caption("ATS-style Resume vs Job Description Analyzer")

# Layout
col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader(
        "📎 Upload Resume",
        type=["pdf", "docx", "txt"]
    )

with col2:
    jd_text = st.text_area(
        "📝 Paste Job Description",
        height=220
    )

st.markdown("---")

# Action button
if st.button("🚀 Match Resume", use_container_width=True):

    if resume_file and jd_text:
        resume_text = extract_text(resume_file)

        score = match_resume(resume_text, jd_text)
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)
        missing_skills = list(set(jd_skills) - set(resume_skills))

        # Results
        st.subheader("📊 Match Result")
        st.metric("Match Percentage", f"{score}%")

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("✅ Skills Found")
            if resume_skills:
                for skill in resume_skills:
                    st.markdown(
                        f"<span class='skill-box'>{skill}</span>",
                        unsafe_allow_html=True
                    )
            else:
                st.write("No skills detected")

        with col4:
            st.subheader("❌ Missing Skills")
            if missing_skills:
                for skill in missing_skills:
                    st.markdown(
                        f"<span class='skill-box missing'>{skill}</span>",
                        unsafe_allow_html=True
                    )
            else:
                st.write("None 🎉")

    else:
        st.warning("Please upload a resume and paste a job description")
