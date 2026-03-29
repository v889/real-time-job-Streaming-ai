import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from vector_db.chroma_client import ChromaClient

def test_db():
    client = ChromaClient(persist_dir="./chroma_db")
    
    print("Inserting test document with metadata...")
    client.insert_text(
        text="Lead Data Scientist at OpenAI in San Francisco",
        metadata={"title": "Lead Data Scientist", "company": "OpenAI", "location": "San Francisco", "timestamp": 12345}
    )
    
    print("Searching DB...")
    results = client.search("OpenAI", k=1)
    if results:
        print(f"Successfully retrieved document!")
        print(f"Text: {results[0].page_content}")
        print(f"Metadata: {results[0].metadata}")
    else:
        print("No results found.")

if __name__ == "__main__":
    test_db()
