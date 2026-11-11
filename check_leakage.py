
import json
import csv

# Load evaluation dataset (JSONL)
evaluation_data = []

with open("data/evaluation_data.json", "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            evaluation_data.append(json.loads(line))

# Load development-only evidence
evidence_set = set()

with open("evidence_dev.csv", "r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        text = row.get("description", "")
        if text:
            evidence_set.add(text.strip().lower())

matched = 0
unmatched = 0

for item in evaluation_data:
    knowledge = str(item.get("knowledge", "")).strip().lower()

    if knowledge in evidence_set:
        matched += 1
    else:
        unmatched += 1

print("Evaluation samples:", len(evaluation_data))
print("Matched in development evidence:", matched)
print("Not matched in development evidence:", unmatched)

print("Exact overlap percentage:",
      round((matched / len(evaluation_data)) * 100, 2)
      if evaluation_data else 0)
