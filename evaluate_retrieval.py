
import json
from retriever_agent import RetrievalAgent

EVALUATION_FILE = "data/evaluation_data.json"
INDEX_FILE = "vector_index_dev.json"

with open(EVALUATION_FILE, encoding="utf-8") as f:
    evaluation_data = [
        json.loads(line)
        for line in f if line.strip()
    ]

with open(INDEX_FILE, encoding="utf-8") as f:
    index = json.load(f)

# Find evaluation records whose exact knowledge passage
# exists in the development index.
index_texts = {
    str(doc["description"]).strip().lower()
    for doc in index
}

eligible_records = [
    item for item in evaluation_data
    if str(item.get("knowledge", "")).strip().lower()
    in index_texts
]

print("Evaluation records:", len(evaluation_data))
print("Exact-match eligible records:", len(eligible_records))

agent = RetrievalAgent()
top1 = top3 = top5 = 0

for item in eligible_records:
    results = agent.fetch_evidence(item["question"], top_k=5)
    expected = str(item["knowledge"]).strip().lower()

    for rank, result in enumerate(results, start=1):
        if str(result["description"]).strip().lower() == expected:
            if rank == 1:
                top1 += 1
            if rank <= 3:
                top3 += 1
            if rank <= 5:
                top5 += 1
            break

total = len(eligible_records)

print("\nEXACT RETRIEVAL RESULTS")
print("Top-1:", top1, "/", total)
print("Top-3:", top3, "/", total)
print("Top-5:", top5, "/", total)

if total:
    print("Top-1 Recall:", round(top1 / total * 100, 2), "%")
    print("Top-3 Recall:", round(top3 / total * 100, 2), "%")
    print("Top-5 Recall:", round(top5 / total * 100, 2), "%")
