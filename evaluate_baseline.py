
import json
from vector_search import tokenize, calculate_similarity

EVALUATION_FILE = "data/evaluation_data.json"

print("Loading evaluation dataset...")

with open(EVALUATION_FILE, "r", encoding="utf-8") as file:
    samples = [
        json.loads(line)
        for line in file
        if line.strip()
    ]

right_scores = []
hallucinated_scores = []

right_wins = 0
hallucinated_wins = 0
ties = 0

print("Evaluating answer-to-knowledge similarity...")

for sample in samples:

    knowledge = tokenize(sample["knowledge"])

    right_answer = tokenize(sample["right_answer"])
    hallucinated_answer = tokenize(sample["hallucinated_answer"])

    right_score = calculate_similarity(
        right_answer,
        knowledge
    )

    hallucinated_score = calculate_similarity(
        hallucinated_answer,
        knowledge
    )

    right_scores.append(right_score)
    hallucinated_scores.append(hallucinated_score)

    if right_score > hallucinated_score:
        right_wins += 1
    elif hallucinated_score > right_score:
        hallucinated_wins += 1
    else:
        ties += 1

total = len(samples)

average_right = sum(right_scores) / total
average_hallucinated = sum(hallucinated_scores) / total

print("\n========== BASELINE EVALUATION ==========")
print("Total evaluation records:", total)

print("\nAverage similarity with knowledge:")
print("Right answers:", round(average_right, 4))
print("Hallucinated answers:", round(average_hallucinated, 4))

print("\nPairwise comparison:")
print("Right answer scored higher:", right_wins)
print("Hallucinated answer scored higher:", hallucinated_wins)
print("Equal scores:", ties)

print(
    "Right-answer higher-score rate:",
    round(right_wins / total * 100, 2),
    "%"
)

print("\nEvaluation completed.")
