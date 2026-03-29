import os
from vector_db.chroma_client import ChromaClient
from langchain_google_genai import ChatGoogleGenerativeAI
import config.config as cfg

class MultiAgentRAGSystem:
    """
    Coordinates Retrieval, Trend Analysis, and Report Generation agents.
    """
    def __init__(self, persist_dir: str = "./chroma_db"):
        self.vector_db = ChromaClient(persist_dir=persist_dir)
        self.llm = ChatGoogleGenerativeAI(
            model=cfg.MODEL_NAME,
            google_api_key=cfg.GOOGLE_API_KEY,
            temperature=0.2
        )

    # -----------------------------
    # 1. Retrieval Agent
    # -----------------------------
    def retrieval_agent(self, query: str, k: int = 40):
        print(f"🕵️‍♂️ [Retrieval Agent] Searching Vector DB for '{query}'...")
        docs = self.vector_db.search(query, k=k)
        context = "\n".join([doc.page_content for doc in docs])
        return context if context else "No context found."

    # -----------------------------
    # 2. Trend Analysis Agent
    # -----------------------------
    def trend_analysis_agent(self, context: str, topic: str):
        print(f"🧠 [Trend Analysis Agent] Computing trends for '{topic}'...")
        prompt = f"""You are a specialized Trend Analysis Agent.
Analyze the following retrieved real-time job postings.
Topic to analyze: {topic}

Job Data Context:
{context}

Extract and calculate the precise frequencies of:
1. The most highly demanded skills for this role/topic.
2. The specific companies actively hiring right now.

Output ONLY a structured raw data summary containing top 5 skills and top 5 companies. No conversational padding.
"""
        response = self.llm.invoke(prompt)
        return response.content
        
    # -----------------------------
    # 3. Report Agent
    # -----------------------------
    def report_agent(self, trend_data: str, user_question: str):
        print("📝 [Report Agent] Generating final insights report...")
        prompt = f"""You are an Executive Report Agent in a Multi-Agent data intelligence system.
The user asked: "{user_question}"

Your colleague, the Trend Analysis Agent, found the following raw data points from the Live Kafka Stream database:
{trend_data}

Compile this data into a beautiful, engaging Markdown insight report that directly answers the user's question. 
Ensure you use emojis, clear headers, and bullet points. Provide actionable insights.
"""
        response = self.llm.invoke(prompt)
        return response.content

    # -----------------------------
    # Orchestrator
    # -----------------------------
    def execute_multi_agent_query(self, user_question: str):
        """Pipeline that passes data sequentially between the 3 specialized agents."""
        
        # Step 1: Specific Vector Search
        context = self.retrieval_agent(user_question)
        
        # Step 2: Advanced Grouping & Tallying
        trend_data = self.trend_analysis_agent(context, user_question)
        
        # Step 3: Executive Formatting
        final_report = self.report_agent(trend_data, user_question)
        
        return final_report
