import requests
import time

from reportlab.pdfgen import canvas

# 1. Create a dummy PDF resume on the fly
pdf_path = "mock_resume.pdf"
c = canvas.Canvas(pdf_path)
c.drawString(100, 750, "John Doe - Senior Data Engineer")
c.drawString(100, 730, "Summary: Highly skilled Data Engineer with 5+ years of experience in Python.")
c.drawString(100, 710, "Skills: Python, SQL, Kafka, Streamlit, Databricks, AWS.")
c.drawString(100, 690, "Experience: Built scalable real-time streaming pipelines using Confluent Kafka.")
c.save()
print(f"✅ Created mock PDF: {pdf_path}")

base_url = "http://127.0.0.1:8001"

# 2. Upload Resume
print("\n--- Testing /upload_resume ---")
with open(pdf_path, "rb") as f:
    res = requests.post(f"{base_url}/upload_resume", files={"file": ("mock_resume.pdf", f, "application/pdf")})
    
if res.status_code == 200:
    resume_text = res.json()["resume_text"]
    print("✅ Upload successful. Extracted text sample:")
    print(f"'{resume_text[:150]}...'")
else:
    print("❌ Failed upload:", res.text)
    exit(1)

# 3. Match Jobs (We inserted a dummy OpenAI job earlier in San Francisco)
print("\n--- Testing /match_jobs (Location: San Francisco) ---")
payload = {
    "resume_text": resume_text,
    "location_filter": "San Francisco",
    "k": 2
}
res_match = requests.post(f"{base_url}/match_jobs", json=payload)
jobs = []
if res_match.status_code == 200:
    jobs = res_match.json()["matches"]
    print(f"✅ Found {len(jobs)} matched jobs.")
    for j in jobs:
        print("  - Title:", j["metadata"].get("title"), "| Company:", j["metadata"].get("company"))
else:
    print("❌ Match failed:", res_match.text)

# 4. Optimize Resume 
print("\n--- Testing /optimize_resume ---")
job_desc = jobs[0]["page_content"] if jobs else "Lead Data Scientist at OpenAI in San Francisco"
payload_opt = {
    "resume_text": resume_text,
    "job_description": job_desc
}
res_opt = requests.post(f"{base_url}/optimize_resume", json=payload_opt)
if res_opt.status_code == 200:
    print("✅ Optimization complete! Output:")
    print("-" * 40)
    print(res_opt.json()["suggestions"])
    print("-" * 40)
else:
    print("❌ Optimization failed:", res_opt.text)
