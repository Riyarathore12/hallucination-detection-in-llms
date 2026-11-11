
import json
import re

def normalize(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


neither_count = 0
both_count = 0

with open("data/evaluation_data.json", encoding="utf-8") as file:
    for line in file:
        if not line.strip():
            continue

        item = json.loads(line)

        knowledge = normalize(item["knowledge"])
        right = normalize(item["right_answer"])
        hallucinated = normalize(item["hallucinated_answer"])

        right_found = bool(right) and right in knowledge
        hallucinated_found = bool(hallucinated) and hallucinated in knowledge

        if not right_found and not hallucinated_found:
            neither_count += 1

            if neither_count <= 10:
                print(f"\n--- UNMATCHED EXAMPLE {neither_count} ---")
                print("Question:", item["question"])
                print("Knowledge:", item["knowledge"])
                print("Right answer:", item["right_answer"])
                print("Hallucinated answer:", item["hallucinated_answer"])

        if right_found and hallucinated_found:
            both_count += 1

print("\nTotal neither found:", neither_count)
print("Total both found:", both_count)
