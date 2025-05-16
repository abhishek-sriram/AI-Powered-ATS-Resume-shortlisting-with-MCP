# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List
# import google.generativeai as genai
# import re
# import traceback
# import time
# import logging

# logging.basicConfig(level=logging.INFO)
# app = FastAPI()

# # Hardcoded Gemini API key (replace with your actual key)
# API_KEY = "AIzaSyDXIFy9YkmM6vB0-AmSR2OIAL8pSwAM_B8I"
# genai.configure(api_key=API_KEY)

# class ResumeInput(BaseModel):
#     jd: str
#     resumes: List[str]

# system_prompt = """
# You are an expert recruitment assistant AI specialized in evaluating resumes against job descriptions. Your task is to carefully analyze the resume and the job description, then provide a concise evaluation in natural language with the following requirements:

# - Start your response with: "Score: <score>", where <score> is a decimal number between 0.0 (no match) and 1.0 (perfect match).
# - Follow the score with a dash or em dash (–) and a one-line, clear, and specific explanation highlighting the key reasons for your score.
# - Use professional and positive language, focusing on relevant skills, experience, and qualifications.
# - Avoid jargon, unnecessary details, or unrelated information.
# - Do NOT include JSON, code, lists, or multiple paragraphs.
# - The entire response must be a single, user-friendly sentence.
# - Respond ONLY with this sentence, no additional text or commentary.

# Example 1:

# Job Description: Software engineer with Python and ML experience.

# Resume: Experienced Python developer with projects in machine learning.

# Response: Score: 0.90 – Excellent Python skills and relevant ML project experience.

# Example 2:

# Job Description: Senior Java developer needed.

# Resume: Junior Python programmer with no Java experience.

# Response: Score: 0.30 – Limited match; lacks required Java experience.

# ---

# Now evaluate the following job description and resume.
# """

# @app.post("/shortlist")
# def shortlist(data: ResumeInput):
#     model = genai.GenerativeModel("gemini-1.5-pro")
#     results = []
#     start_time = time.time()
#     logging.info(f"Received shortlist request with {len(data.resumes)} resumes")

#     for resume in data.resumes:
#         prompt = f"{system_prompt}\n\nJob Description:\n{data.jd}\n\nResume:\n{resume}"
#         try:
#             response = model.generate_content(prompt)
#             text = response.text.strip()
#             logging.info(f"LLM Response: {text}")

#             match = re.match(r"Score:\s*([0-9.]+)\s*[-–—]\s*(.+)", text)
#             if match:
#                 score = float(match.group(1))
#                 reason = match.group(2).strip()
#             else:
#                 score = 0.0
#                 reason = f"Could not parse response: {text}"
#         except Exception as e:
#             logging.error(f"Error generating content: {e}\n{traceback.format_exc()}")
#             score = 0.0
#             reason = f"Error: {str(e)}"

#         status = "Shortlisted" if score >= 0.15 else "Rejected"
#         results.append({
#             "resume_snippet": resume[:300],
#             "score": round(score, 3),
#             "status": status,
#             "reason": reason
#         })

#     elapsed = time.time() - start_time
#     logging.info(f"Processed shortlist in {elapsed:.2f} seconds")
#     return {"shortlisted": results}
