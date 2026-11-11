
import json
from collections import Counter

data = []

with open("data/qa_data.json", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        if line:
            data.append(json.loads(line))

print("Total Samples:", len(data))

print("\nAvailable Columns:")
if data:
    print(list(data[0].keys()))

print("\nMissing Field Analysis:")

required_fields = [
    "question",
    "knowledge",
    "right_answer",
    "hallucinated_answer"
]

for field in required_fields:
    missing = sum(
        1 for item in data
        if not item.get(field)
    )
    print(f"{field}: {missing} missing")

print("\nFirst 3 Dataset Samples:")

for i, item in enumerate(data[:3], 1):
    print(f"\n--- Sample {i} ---")
    for field in required_fields:
        print(f"{field}: {item.get(field)}")

print("\nDataset structure check completed.")
