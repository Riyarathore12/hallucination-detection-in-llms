
import json
import re


def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def phrase_found(answer, knowledge):
    answer_tokens = tokens(answer)
    knowledge_tokens = tokens(knowledge)

    if not answer_tokens:
        return False

    n = len(answer_tokens)

    return any(
        knowledge_tokens[i:i + n] == answer_tokens
        for i in range(len(knowledge_tokens) - n + 1)
    )


stats = {
    "Yes/No": {"total": 0, "right": 0, "hallucinated": 0},
    "Fact-based": {"total": 0, "right": 0, "hallucinated": 0}
}

with open("data/evaluation_data.json", encoding="utf-8") as file:
    for line in file:
        if not line.strip():
            continue

        item = json.loads(line)

        right = item["right_answer"].strip().lower()
        hallucinated = item["hallucinated_answer"]

        category = "Yes/No" if right in ("yes", "no") else "Fact-based"

        stats[category]["total"] += 1
        stats[category]["right"] += phrase_found(
            item["right_answer"], item["knowledge"]
        )
        stats[category]["hallucinated"] += phrase_found(
            hallucinated, item["knowledge"]
        )


print("\n========== TOKEN-BOUNDARY MATCHING ==========")

for category, values in stats.items():
    total = values["total"]

    print(f"\n{category}")
    print("Total:", total)
    print("Right answer matched:", values["right"])
    print("Hallucinated answer matched:", values["hallucinated"])

    if total:
        print(
            "Right match rate:",
            f"{values['right'] / total * 100:.2f}%"
        )
        print(
            "Hallucinated match rate:",
            f"{values['hallucinated'] / total * 100:.2f}%"
        )
