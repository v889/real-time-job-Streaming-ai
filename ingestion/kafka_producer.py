import time
import json
import requests
import threading
from bs4 import BeautifulSoup
from confluent_kafka import Producer
import config.config as cfg

class JobScraperKafkaProducer:
    def __init__(self, topic: str = "jobs_stream"):
        self.topic = topic
        self.url = "https://www.linkedin.com/jobs/search/?keywords=Data%20Engineer&location=India&f_TPR=r86400"
        
        # Confluent Cloud Config
        self.conf = {
            "bootstrap.servers": cfg.KAFKA_BOOTSTRAP,
            "security.protocol": "SASL_SSL",
            "sasl.mechanisms": "PLAIN",
            "sasl.username": cfg.KAFKA_API_KEY,
            "sasl.password": cfg.KAFKA_API_SECRET
        }
        self.producer = Producer(self.conf)

    def fetch_linkedin_jobs(self):
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        jobs = []
        for card in soup.select(".base-card"):
            title = card.select_one(".base-search-card__title")
            company = card.select_one(".base-search-card__subtitle")
            location = card.select_one(".job-search-card__location")
            
            job = {
                "title": title.text.strip() if title else "",
                "company": company.text.strip() if company else "",
                "location": location.text.strip() if location else "",
                "timestamp": int(time.time())
            }
            if job["title"]:
                jobs.append(job)
        return jobs

    def start_streaming(self):
        print(f"🚀 Started streaming live LinkedIn jobs to topic '{self.topic}'...")
        while True:
            try:
                jobs = self.fetch_linkedin_jobs()
                for job in jobs:
                    self.producer.produce(self.topic, json.dumps(job).encode("utf-8"))
                    print(f"📡 Sent Job: {job['title']} at {job['company']}")
                
                self.producer.flush()
                # Scraping delay to prevent limits
                time.sleep(60)
            except Exception as e:
                print(f"❌ Producer Error: {e}")
                time.sleep(10)

if __name__ == "__main__":
    scraper = JobScraperKafkaProducer()
    scraper.start_streaming()
