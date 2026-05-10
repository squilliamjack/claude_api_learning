import anthropic
import os
from dotenv import load_dotenv
import json
from pypdf import PdfReader
import voyageai
import time

load_dotenv()

claude_client=anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
voyage_client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))

reader = PdfReader("algebra-and-trigonometry-2e_-_WEB.pdf")
raw_text = []
for i in range(140, 154):
    page_text = reader.pages[i].extract_text()
    raw_text.append(page_text)
    
def generate_embedding(text):
    embedding = voyage_client.embed([text], model="voyage-3")
    return embedding.embeddings[0]

embeddings = []
for i in range(len(raw_text)):
    embedding = generate_embedding(raw_text[i])
    chunk = {
        "text": raw_text[i],
        "embedding": embedding
    }
    embeddings.append(chunk)
    # time.sleep(20)
    
with open("embeddings.json", "w") as f:
    json.dump(embeddings, f, indent=4)