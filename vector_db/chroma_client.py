from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import config.config as cfg

class ChromaClient:
    def __init__(self, persist_dir: str = "../chroma_db"):
        self.persist_directory = persist_dir
        
        self.embedding_function = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        self.db = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_function
        )

    def insert_text(self, text: str, metadata: dict = None):
        """Vectorize and persist single text chunk immediately"""
        metadatas = [metadata] if metadata else None
        self.db.add_texts(texts=[text], metadatas=metadatas)

    def search(self, query: str, k: int = 5, filter_dict: dict = None):
        """Cosine similarity search returning top K documents"""
        if filter_dict:
            return self.db.similarity_search(query, k=k, filter=filter_dict)
        return self.db.similarity_search(query, k=k)
