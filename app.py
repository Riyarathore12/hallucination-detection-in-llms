import pandas as pd
import spacy
from sentence_transformers import SentenceTransformer
import faiss

# Initialize models
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Test text processing
text = "Testing the NLP pipeline setup."
doc = nlp(text)
embeddings = model.encode([text])

# Create a sample FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

print(f"Entities found: {[ent.text for ent in doc.ents]}")
print(f"FAISS index total vectors: {index.ntotal}")
print("Setup complete and ready for development!")