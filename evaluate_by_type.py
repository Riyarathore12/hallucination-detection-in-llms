
import json
import re

def normalize(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


stats = {
    "Yes/No": {"total": 0, "right": 0, "hallucinated": 0},
    "Fact-based": {"total": 0, "right": 0, "hallucinated": 0}
}

with open("data/evaluation_data.json", encoding="utf-8") as file:
    for line in file:
        if not line.strip():
            continue

        item = json.loads(line)

        knowledge = normalize(item["knowledge"])
        right = normalize(item["right_answer"])
        hallucinated = normalize(item["hallucinated_answer"])

        category = (
            "Yes/No"
            if right in ("yes", "no")
            else "Fact-based"
        )

        stats[category]["total"] += 1
        stats[category]["right"] += bool(right and right in knowledge)
        stats[category]["hallucinated"] += bool(
            hallucinated and hallucinated in knowledge
        )

print("\n========== RESULTS BY ANSWER TYPE ==========")

for category, values in stats.items():
    total = values["total"]

    print(f"\n{category}")
    print("Total:", total)

    if total:
        print(
            "Right answer matched:",
            values["right"],
            f"({values['right'] / total * 100:.2f}%)"
        )
        print(
            "Hallucinated answer matched:",
            values["hallucinated"],
            f"({values['hallucinated'] / total * 100:.2f}%)"
        )
