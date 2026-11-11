
import json
from collections import Counter

answer_types = Counter()

with open("data/evaluation_data.json", encoding="utf-8") as file:
    for line in file:
        if not line.strip():
            continue

        item = json.loads(line)
        answer = item["right_answer"].strip().lower()

        if answer in ("yes", "no"):
            answer_types["Yes/No"] += 1
        else:
            answer_types["Fact-based"] += 1

print("\n========== ANSWER TYPE ANALYSIS ==========")
print("Yes/No records:", answer_types["Yes/No"])
print("Fact-based records:", answer_types["Fact-based"])
print("Total records:", sum(answer_types.values()))
