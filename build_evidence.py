
import json
import csv

input_file = "data/development_data.json"
output_file = "evidence_dev.csv"

rows = []

with open(input_file, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if not line.strip():
            continue

        item = json.loads(line)
        knowledge = item.get("knowledge", "").strip()

        if knowledge:
            rows.append({
                "id": i + 1,
                "description": knowledge,
                "category": "HaluEval Knowledge"
            })

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["id", "description", "category"]
    )
    writer.writeheader()
    writer.writerows(rows)

print("Development evidence created:", output_file)
print("Total evidence records:", len(rows))
