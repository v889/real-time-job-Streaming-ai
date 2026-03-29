from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import Optional
from rag_system.langchain_agent import MultiAgentRAGSystem
from rag_system.resume_agent import ResumeMatchingAgent

app = FastAPI(title="AI Data Intelligence Hub - Multi-Agent API")

# Initialize the systems pointing to local DB
agent_system = MultiAgentRAGSystem(persist_dir="./chroma_db")
resume_system = ResumeMatchingAgent(persist_dir="./chroma_db")

class QueryRequest(BaseModel):
    question: str

class MatchRequest(BaseModel):
    resume_text: str
    location_filter: Optional[str] = None
    k: int = 5

class OptimizeRequest(BaseModel):
    resume_text: str
    job_description: str

@app.post("/analyze")
def run_analysis(req: QueryRequest):
    """Hits the Multi-Agent pipeline (Retrieval -> Trend -> Report)"""
    report = agent_system.execute_multi_agent_query(req.question)
    return {"report": report}

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    """Parses and chunks uploaded PDF resumes."""
    contents = await file.read()
    full_text = resume_system.parse_and_chunk_resume(contents)
    return {"resume_text": full_text}

@app.post("/match_jobs")
def match_jobs(req: MatchRequest):
    """Compares resume chunks to active jobs (metadata filtered)."""
    matches = resume_system.match_jobs_to_resume(
        resume_text=req.resume_text, 
        k=req.k, 
        location_filter=req.location_filter
    )
    
    # Serialize Chroma Document objects
    results = []
    for doc in matches:
        results.append({
            "page_content": doc.page_content,
            "metadata": doc.metadata
        })
    return {"matches": results}

@app.post("/optimize_resume")
def optimize_resume(req: OptimizeRequest):
    """LLM computes Resume vs Job Description gap."""
    suggestions = resume_system.suggest_resume_changes(req.resume_text, req.job_description)
    return {"suggestions": suggestions}

if __name__ == "__main__":
    import uvicorn
    # Make sure to run from root folder so chroma_db connects locally
    uvicorn.run("backend.fastapi_server:app", host="0.0.0.0", port=8001, reload=True)
