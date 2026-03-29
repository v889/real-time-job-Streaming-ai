# 🧠 AI-Powered Real-Time Data Intelligence Platform

A complete end-to-end LLMOps pipeline that ingests real-time job market data via **Confluent Kafka**, vectorizes it into **ChromaDB**, and analyzes the continuous stream using a **Multi-Agent Large Language Model architecture** powered by **Google Gemini**.

## 🚀 Features
- **Real-Time Job Indexing**: Streams live jobs into a Vector Database instantly.
- **Multi-Agent Market Analysis**: Ask plain-English questions (e.g., *"What skills are trending right now?"*) and watch the agents retrieve, analyze, and format market reports.
- **Smart Resume Matcher**: Upload your PDF resume to have the AI automatically evaluate your background and match you to active, geographically-filtered jobs.
- **Generative ATS Optimization**: Select a matched job and let the Gemini Copilot generate a targeted gap-analysis report telling you exactly what bullet points to tweak to get hired.
- **Premium UI**: A sleek, dark-themed, glassmorphic Streamlit Dashboard.

## 🏗️ Architecture Stack
* **Ingestion (Producer)**: Live web-scraped data pushed securely to Confluent Cloud Kafka.  
* **Streaming (Consumer)**: Distributed worker listening to topic streams and pushing directly to the Vector DB.  
* **Embeddings & VectorDB**: Hugging Face Sentence Transformers (`all-MiniLM-L6-v2`) integrated with ChromaDB storage.  
* **Multi-Agent System (Langchain)**: 
  * 🕵️‍♀️ **Retrieval Agent**: Extracts precise context from Chroma using vector similarity search.
  * 🧠 **Trend Analysis Agent**: Calculates market movements and quantitative skill demands.
  * 📝 **Report Agent**: Synthesizes the raw mathematical trend outputs into executive Markdown insights.
  * 📄 **Resume Agent**: Chunks unstructured PDF resumes and executes vector overlap analysis against job streams.
* **Backend API**: Asynchronous FastAPI endpoints  
* **Frontend Dashboard**: Interactive Streamlit Web UI

## 🚀 Getting Started

Start all services from the root `ai-data-intelligence-platform` directory.
*(Ensure your `.env` contains `KAFKA_BOOTSTRAP`, `KAFKA_API_KEY`, `KAFKA_API_SECRET`, `HUGGINGFACEHUB_API_TOKEN`, and `GOOGLE_API_KEY`)*

1. **Start the Data Ingestion Server**:
```bash
python -m ingestion.kafka_producer
```

2. **Start the Embedding Generator**:
```bash
python -m embeddings.embedding_generator
```

3. **Spin up the Backend API Server**:
```bash
uvicorn backend.fastapi_server:app --port 8001
```

4. **Launch the User Dashboard**:
```bash
streamlit run dashboard/streamlit_app.py
```

⚡ **Example Prompt:**
* *"What skills are trending in Data Engineer jobs today?"*
