import os
import requests
import streamlit as st
from jd_matcher import extract_text_from_pdf

MCP_SERVER_URL = "https://ai-powered-ats-resume-shortlisting-with-cvww.onrender.com/shortlist"

st.set_page_config(page_title="AI Powered ATS Shortlisting with MCP", layout="centered")
st.title("AI Powered ATS Shortlisting with MCP")

st.header("📥 Paste Job Description")
jd_text = st.text_area("Paste JD here...", height=250)

st.header("📎 Upload Resumes (PDFs)")
uploaded_files = st.file_uploader("Upload PDFs", type=['pdf'], accept_multiple_files=True)

if st.button("🚀 Analyze with Gemini"):
    if not jd_text or not uploaded_files:
        st.warning("Please upload resumes and paste the job description.")
    else:
        resumes = []
        temp_files = []
        try:
            with st.spinner("Extracting text from resumes..."):
                for file in uploaded_files:
                    path = f"temp_{file.name}"
                    temp_files.append(path)
                    with open(path, "wb") as f:
                        f.write(file.read())
                    resumes.append(extract_text_from_pdf(path))

            with st.spinner("Analyzing resumes..."):
                response = requests.post(MCP_SERVER_URL, json={
                    "jd": jd_text,
                    "resumes": resumes
                }, timeout=120)

            if response.status_code == 200:
                results = response.json().get("shortlisted", [])
                st.subheader("🎯 Shortlisting Results")
                for i, res in enumerate(results):
                    status_icon = "✅" if res["status"] == "Shortlisted" else "❌"
                    st.markdown(f"**Resume {i+1}** | Score: `{res['score']}` | {status_icon} {res['status']}")
                    st.caption(f"_Reason: {res['reason']}_")
                    st.caption(res["resume_snippet"])
            else:
                st.error(f"MCP server error: {response.status_code}. Please check server logs.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with MCP server: {e}")
        finally:
            for fpath in temp_files:
                if os.path.exists(fpath):
                    os.remove(fpath)
