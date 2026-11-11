
import json
import re

def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def phrase_found(answer, knowledge):
    a = tokens(answer)
    k = tokens(knowledge)

    if not a:
        return False

    return any(
        k[i:i + len(a)] == a
        for i in range(len(k) - len(a) + 1)
    )


false_negatives = []
false_positives = []

with open("data/evaluation_data.json", encoding="utf-8") as file:
    for line in file:
        if not line.strip():
            continue

        item = json.loads(line)
        knowledge = item["knowledge"]

        if not phrase_found(item["right_answer"], knowledge):
            false_negatives.append(item)

        if phrase_found(item["hallucinated_answer"], knowledge):
            false_positives.append(item)


print("False negatives:", len(false_negatives))
print("False positives:", len(false_positives))

print("\n========== FALSE NEGATIVE EXAMPLES ==========")
for i, item in enumerate(false_negatives[:10], 1):
    print(f"\nExample {i}")
    print("Question:", item["question"])
    print("Knowledge:", item["knowledge"])
    print("Right answer:", item["right_answer"])

print("\n========== FALSE POSITIVE EXAMPLES ==========")
for i, item in enumerate(false_positives[:10], 1):
    print(f"\nExample {i}")
    print("Question:", item["question"])
    print("Knowledge:", item["knowledge"])
    print("Hallucinated answer:", item["hallucinated_answer"])
