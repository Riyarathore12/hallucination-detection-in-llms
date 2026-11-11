
import os

os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"

import faiss
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

print("Loading evidence dataset...")
df = pd.read_csv("evidence.csv")

print("Loading embedding model...")
model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    model_kwargs={"use_safetensors": False}
)

print("Loading FAISS index...")
index = faiss.read_index("vector_index.bin")

print("Model and index loaded successfully.")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Server running",
        "message": "Hallucination Detection Evidence Retrieval API",
        "example_usage": "/search?q=python&top_k=3"
    })


@app.route("/search", methods=["GET"])
def search_api():

    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "error": "Query parameter 'q' is missing."
        }), 400

    try:
        top_k = int(request.args.get("top_k", 3))
    except ValueError:
        return jsonify({
            "error": "top_k must be an integer."
        }), 400

    if top_k < 1:
        return jsonify({
            "error": "top_k must be greater than 0."
        }), 400

    if index.ntotal != len(df):
        return jsonify({
            "error": "FAISS index and evidence dataset size mismatch."
        }), 500

    query_vector = model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    faiss.normalize_L2(query_vector)

    k = min(top_k, index.ntotal)

    scores, indices = index.search(query_vector, k)

    results = []

    for idx, score in zip(indices[0], scores[0]):

        if idx < 0 or idx >= len(df):
            continue

        row = df.iloc[int(idx)].to_dict()

        results.append({
            "description": str(row.get("description", "")),
            "similarity_score": float(score)
        })

    return jsonify({
        "query": query,
        "total_results": len(results),
        "results": results
    })


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
