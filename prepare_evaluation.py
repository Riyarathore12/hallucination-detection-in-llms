import json
import random

INPUT_FILE = "data/qa_data.json"
DEV_FILE = "data/development_data.json"
EVAL_FILE = "data/evaluation_data.json"

random.seed(42)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f if line.strip()]

random.shuffle(data)

development_data = data[:8000]
evaluation_data = data[8000:]

for path, records in [
    (DEV_FILE, development_data),
    (EVAL_FILE, evaluation_data)
]:
    with open(path, "w", encoding="utf-8") as f:
        for item in records:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

print("Development samples:", len(development_data))
print("Evaluation samples:", len(evaluation_data))
print("Dataset preparation completed.")