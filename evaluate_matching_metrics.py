
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


TP = 0  # Right answer predicted supported
FN = 0  # Right answer predicted not supported
FP = 0  # Hallucinated answer predicted supported
TN = 0  # Hallucinated answer predicted not supported

with open("data/evaluation_data.json", encoding="utf-8") as file:
    for line in file:
        if not line.strip():
            continue

        item = json.loads(line)
        knowledge = item["knowledge"]

        if phrase_found(item["right_answer"], knowledge):
            TP += 1
        else:
            FN += 1

        if phrase_found(item["hallucinated_answer"], knowledge):
            FP += 1
        else:
            TN += 1

total = TP + FN + FP + TN

precision = TP / (TP + FP) if TP + FP else 0
recall = TP / (TP + FN) if TP + FN else 0
specificity = TN / (TN + FP) if TN + FP else 0
accuracy = (TP + TN) / total if total else 0
f1 = (
    2 * precision * recall / (precision + recall)
    if precision + recall else 0
)

print("\n========== BASELINE CLASSIFICATION METRICS ==========")
print("Total answer examples:", total)
print("True Positives:", TP)
print("False Negatives:", FN)
print("False Positives:", FP)
print("True Negatives:", TN)
print(f"Accuracy: {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall: {recall * 100:.2f}%")
print(f"Specificity: {specificity * 100:.2f}%")
print(f"F1 Score: {f1 * 100:.2f}%")
