
import json
from vector_search import tokenize, calculate_similarity

count = 0

with open("data/evaluation_data.json", encoding="utf-8") as file:
    for line in file:
        if not line.strip():
            continue

        item = json.loads(line)
        knowledge = item["knowledge"]

        knowledge_words = tokenize(knowledge)

        right_score = calculate_similarity(
            tokenize(item["right_answer"]),
            knowledge_words
        )

        hallucinated_score = calculate_similarity(
            tokenize(item["hallucinated_answer"]),
            knowledge_words
        )

        if hallucinated_score > right_score:
            count += 1

            print(f"\n========== EXAMPLE {count} ==========")
            print("Question:", item["question"])
            print("Knowledge:", knowledge)
            print("Right answer:", item["right_answer"])
            print("Right score:", round(right_score, 4))
            print("Hallucinated answer:", item["hallucinated_answer"])
            print("Hallucinated score:", round(hallucinated_score, 4))

        if count == 10:
            break
