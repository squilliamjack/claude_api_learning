import anthropic
import os
from dotenv import load_dotenv
import json
from pypdf import PdfReader
import voyageai
import time
import numpy as np

load_dotenv()

claude_client=anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
voyage_client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))

# reader = PdfReader("algebra-and-trigonometry-2e_-_WEB.pdf")
# raw_text = []
# for i in range(140, 154):
#     page_text = reader.pages[i].extract_text()
#     raw_text.append(page_text)
    
def generate_embedding(text):
    embedding = voyage_client.embed([text], model="voyage-3")
    return embedding.embeddings[0]

# embeddings = []
# for i in range(len(raw_text)):
#     embedding = generate_embedding(raw_text[i])
#     chunk = {
#         "text": raw_text[i],
#         "embedding": embedding
#     }
#     embeddings.append(chunk)
#     # time.sleep(20)
    
# with open("embeddings.json", "w") as f:
#     json.dump(embeddings, f, indent=4)

with open("embeddings.json", "r") as f:
    embeddings = json.load(f)

class VectorStore:
    def __init__(self):
        self.chunks=[]
        
    def add(self, text, embedding):
        self.chunks.append({"text": text, "embedding": embedding})
        
    def search(self, query_embedding, n):
        score = []
        for i in range(len(self.chunks)):
            similarity = np.dot(query_embedding, self.chunks[i]["embedding"]) / (np.linalg.norm(query_embedding) * np.linalg.norm(self.chunks[i]["embedding"]))
            score.append({"score": similarity, "index": i})
        
        score = sorted(score, key=lambda x: x["score"], reverse=True)
        return [self.chunks[score[i]["index"]]["text"] for i in range(n)]  

store = VectorStore()
for i in range(len(embeddings)):
    store.add(embeddings[i]["text"], embeddings[i]["embedding"])
    
test_query = "How do I solve a quadratic equation by factoring?"
test_query_embedding = generate_embedding(test_query)

print(store.search(test_query_embedding, 2))