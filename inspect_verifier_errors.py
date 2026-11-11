
import json
from verifier_agent import VerifierAgent

verifier = VerifierAgent()

false_positives = []
false_negatives = []
review_examples = []

with open("data/evaluation_data.json", encoding="utf-8") as file:

    for line in file:
        if not line.strip():
            continue

        item = json.loads(line)

        evidence = [{
            "description": item["knowledge"],
            "similarity_score": 1.0
        }]

        right_result = verifier.verify_claim(
            item["right_answer"],
            evidence,
            question=item["question"]
        )

        hallucinated_result = verifier.verify_claim(
            item["hallucinated_answer"],
            evidence,
            question=item["question"]
        )

        if hallucinated_result["status"] == "SUPPORTED":
            false_positives.append({
                "question": item["question"],
                "knowledge": item["knowledge"],
                "answer": item["hallucinated_answer"],
                "reason": hallucinated_result["reason"]
            })

        if right_result["status"] == "REVIEW_REQUIRED":
            false_negatives.append({
                "question": item["question"],
                "knowledge": item["knowledge"],
                "answer": item["right_answer"],
                "reason": right_result["reason"]
            })

        if hallucinated_result["status"] == "REVIEW_REQUIRED":
            review_examples.append({
                "question": item["question"],
                "answer": item["hallucinated_answer"],
                "knowledge": item["knowledge"]
            })

print("\n========== VERIFIER ERROR ANALYSIS ==========")
print("False positives:", len(false_positives))
print("Correct answers requiring review:", len(false_negatives))
print("Hallucinated answers requiring review:", len(review_examples))

print("\n========== FALSE POSITIVE EXAMPLES ==========")

for i, item in enumerate(false_positives[:15], 1):
    print(f"\nExample {i}")
    print("Question:", item["question"])
    print("Knowledge:", item["knowledge"][:700])
    print("Hallucinated answer:", item["answer"])
    print("Verifier reason:", item["reason"])

print("\n========== REVIEW EXAMPLES ==========")

for i, item in enumerate(review_examples[:5], 1):
    print(f"\nExample {i}")
    print("Question:", item["question"])
    print("Hallucinated answer:", item["answer"])
    print("Knowledge:", item["knowledge"][:500])
