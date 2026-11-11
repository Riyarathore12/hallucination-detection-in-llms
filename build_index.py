
import csv
import json
import re
import math

INPUT_FILE = "evidence_dev.csv"
OUTPUT_FILE = "vector_index_dev.json"

print("Loading evidence dataset...")

documents = []

with open(INPUT_FILE, "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        text = row.get("description", "").strip()

        if text:
            documents.append({
                "id": row.get("id", ""),
                "description": text,
                "category": row.get("category", "")
            })

print(f"Total evidence records: {len(documents)}")


def tokenize(text):
    return re.findall(r"\b[a-z0-9]+\b", text.lower())


print("Building lightweight text index...")

index = []

for document in documents:
    words = tokenize(document["description"])

    index.append({
        "id": document["id"],
        "description": document["description"],
        "category": document["category"],
        "words": words
    })

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(index, file, ensure_ascii=False)

print(f"Indexed records: {len(index)}")
print(f"Index saved: {OUTPUT_FILE}")
