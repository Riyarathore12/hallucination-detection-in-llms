
import json
from verifier_agent import VerifierAgent

EVALUATION_FILE = "data/evaluation_data.json"

verifier = VerifierAgent()

# Confusion matrix for decisive predictions only.
TP = FN = FP = TN = 0

# Abstentions are counted separately.
right_review = 0
hallucinated_review = 0

right_status = {}
hallucinated_status = {}

with open(EVALUATION_FILE, encoding="utf-8") as file:

    for line in file:
        if not line.strip():
            continue

        item = json.loads(line)

        evidence = [{
            "description": item["knowledge"],
            "similarity_score": 1.0
        }]

        # Evaluate correct answer.
        right_result = verifier.verify_claim(
            item["right_answer"],
            evidence,
            question=item["question"]
        )

        # Evaluate hallucinated answer.
        hallucinated_result = verifier.verify_claim(
            item["hallucinated_answer"],
            evidence,
            question=item["question"]
        )

        right = right_result["status"]
        hallucinated = hallucinated_result["status"]

        right_status[right] = right_status.get(right, 0) + 1
        hallucinated_status[hallucinated] = (
            hallucinated_status.get(hallucinated, 0) + 1
        )

        if right == "SUPPORTED":
            TP += 1
        elif right == "CONTRADICTED":
            FN += 1
        else:
            right_review += 1

        if hallucinated == "SUPPORTED":
            FP += 1
        elif hallucinated == "CONTRADICTED":
            TN += 1
        else:
            hallucinated_review += 1

total = TP + FN + FP + TN
review_total = right_review + hallucinated_review

precision = TP / (TP + FP) if TP + FP else 0
recall = TP / (TP + FN) if TP + FN else 0
specificity = TN / (TN + FP) if TN + FP else 0
accuracy = (TP + TN) / total if total else 0

f1 = (
    2 * precision * recall / (precision + recall)
    if precision + recall else 0
)

print("\n========== VERIFIER EVALUATION ==========")
print("Evaluation records:", TP + FN + right_review)
print("Total answer examples:", TP + FN + FP + TN + review_total)

print("\nCorrect answer predictions:")
for status, count in sorted(right_status.items()):
    print(status, ":", count)

print("\nHallucinated answer predictions:")
for status, count in sorted(hallucinated_status.items()):
    print(status, ":", count)

print("\n========== CONFUSION MATRIX ==========")
print("True Positives:", TP)
print("False Negatives:", FN)
print("False Positives:", FP)
print("True Negatives:", TN)

print("\nReview / Abstention:")
print("Correct answers requiring review:", right_review)
print("Hallucinated answers requiring review:", hallucinated_review)
print("Total abstentions:", review_total)

print("\n========== METRICS ==========")
print(f"Accuracy (decisive predictions): {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall: {recall * 100:.2f}%")
print(f"Specificity: {specificity * 100:.2f}%")
print(f"F1 Score: {f1 * 100:.2f}%")

print("\nEvaluation completed.")
