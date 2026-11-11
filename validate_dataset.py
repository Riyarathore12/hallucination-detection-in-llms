import json

file_path = "data/qa_data.json"

total = 0
same_answers = 0
different_answers = 0
empty_answers = 0

with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue

        item = json.loads(line)
        total += 1

        right = str(item.get("right_answer", "")).strip().lower()
        hallucinated = str(item.get("hallucinated_answer", "")).strip().lower()

        if not right or not hallucinated:
            empty_answers += 1
        elif right == hallucinated:
            same_answers += 1
        else:
            different_answers += 1

print("Total Samples:", total)
print("Same Answers:", same_answers)
print("Different Answers:", different_answers)
print("Empty Answers:", empty_answers)