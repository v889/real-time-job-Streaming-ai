import json
from confluent_kafka import Consumer
from vector_db.chroma_client import ChromaClient
import config.config as cfg

class RealtimeEmbeddingGenerator:
    def __init__(self, topic: str = "jobs_stream"):
        self.topic = topic
        self.vector_db = ChromaClient(persist_dir="./chroma_db") # Stores in working directory
        
        self.conf = {
            "bootstrap.servers": cfg.KAFKA_BOOTSTRAP,
            "security.protocol": "SASL_SSL",
            "sasl.mechanisms": "PLAIN",
            "sasl.username": cfg.KAFKA_API_KEY,
            "sasl.password": cfg.KAFKA_API_SECRET,
            "group.id": "embedding_pipeline_group",
            "auto.offset.reset": "earliest" # Read historical to catch up
        }
        self.consumer = Consumer(self.conf)

    def consume_and_embed(self):
        self.consumer.subscribe([self.topic])
        print(f"📥 Embedding Generator listening to '{self.topic}' for live jobs...")
        
        while True:
            try:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print("Error:", msg.error())
                    continue
                
                # Extract message payload
                job = json.loads(msg.value().decode("utf-8"))
                title = job.get('title', 'Unknown Title')
                company = job.get('company', 'Unknown Company')
                location = job.get('location', 'Unknown Location')
                
                text = f"{title} at {company} in {location}"
                metadata = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "timestamp": job.get("timestamp", 0)
                }
                
                # Embed and insert into Chroma
                self.vector_db.insert_text(text, metadata=metadata)
                print(f"✅ Vectorized & Stored with Metadata: {text}")
                
            except KeyboardInterrupt:
                print("🛑 Stopping generator.")
                break

if __name__ == "__main__":
    generator = RealtimeEmbeddingGenerator()
    generator.consume_and_embed()
