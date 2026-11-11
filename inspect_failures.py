import json
from vector_search import search_dataset

with open("data/development_data.json", encoding="utf-8") as f:
    samples = [json.loads(line) for line in f if line.strip()][:20]

for i, sample in enumerate(samples, 1):
    results = search_dataset(sample["question"], 3)
    if not any(r["title"].strip() == sample["knowledge"].strip() for r in results):
        print(f"\nFAILED QUESTION {i}: {sample['question']}")
        print("EXPECTED:", sample["knowledge"][:250])
        for r in results:
            print("RETRIEVED:", r["id"], r["similarity_score"], r["title"][:200])
