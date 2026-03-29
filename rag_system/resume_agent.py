import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from vector_db.chroma_client import ChromaClient
import config.config as cfg

class ResumeMatchingAgent:
    def __init__(self, persist_dir: str = "./chroma_db"):
        self.vector_db = ChromaClient(persist_dir=persist_dir)
        self.llm = ChatGoogleGenerativeAI(
            model=cfg.MODEL_NAME,
            google_api_key=cfg.GOOGLE_API_KEY,
            temperature=0.3
        )
        # Initialize the text splitter for chunking as requested
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def parse_and_chunk_resume(self, pdf_bytes: bytes) -> str:
        """Parses a PDF resume and splits it into chunks. Returns full text."""
        print("📄 [Resume Agent] Parsing uploaded PDF...")
        # PyPDFLoader needs a file path, so we use a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf_bytes)
            tmp_path = tmp.name
        
        try:
            loader = PyPDFLoader(tmp_path)
            pages = loader.load()
            
            full_text = "\n".join([page.page_content for page in pages])
            
            # Chunking process
            chunks = self.text_splitter.split_text(full_text)
            print(f"✂️ [Resume Agent] Resume split into {len(chunks)} chunks.")
            
            return full_text
        finally:
            os.remove(tmp_path)

    def match_jobs_to_resume(self, resume_text: str, k: int = 5, location_filter: str = None) -> list:
        """Searches ChromaDB for matching jobs based on the resume content."""
        print("🔍 [Resume Agent] Matching resume to market database...")
        filter_dict = None
        if location_filter and location_filter.strip():
            filter_dict = {"location": location_filter.strip()}
            
        # Use a chunk of the resume to find relevant jobs (first 1000 characters to capture overview/skills)
        search_query = resume_text[:1000] 
        matches = self.vector_db.search(search_query, k=k, filter_dict=filter_dict)
        return matches

    def suggest_resume_changes(self, resume_text: str, job_description: str) -> str:
        """Compares resume against the target job and suggests optimization tweaks."""
        print("🤖 [Resume Agent] Optimizing resume for selected job...")
        prompt = f"""You are an Expert Career Coach and Top-Tier ATS Resume Optimizer.
        
A user wants to apply for the following job using their current resume. 

JOB DETAILS:
{job_description}

USER RESUME:
{resume_text}

Analyze the gap between the user's resume and the job requirements. Provide a structured, actionable report detailing:
1. **Match Overview**: A brief assessment of how well their experience matches the role.
2. **Missing Keywords**: Essential skills or terms from the job posting missing in the resume.
3. **Specific Revisions**: 3-4 specific bullet points they should rewrite or add to better align with the job (give exact examples of how to write it).

Use professional and highly actionable language suitable for a senior engineer. Format beautifully in Markdown.
"""
        response = self.llm.invoke(prompt)
        return response.content
