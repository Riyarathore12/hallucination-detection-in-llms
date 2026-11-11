import json
from vector_search import search_dataset

with open("data/development_data.json", encoding="utf-8") as f:
    samples = [json.loads(line) for line in f if line.strip()][:20]

correct = 0

for i, sample in enumerate(samples, 1):
    results = search_dataset(sample["question"], top_k=3)
    expected = sample["knowledge"].strip()

    found = any(result["title"].strip() == expected for result in results)

    if found:
        correct += 1

    print(f"{i}. {'PASS' if found else 'FAIL'} | Question: {sample['question'][:100]}")

print("\n========== RETRIEVAL TEST ==========")
print("Total questions:", len(samples))
print("Correct evidence in top 3:", correct)
print("Accuracy:", round(correct / len(samples) * 100, 2), "%")
