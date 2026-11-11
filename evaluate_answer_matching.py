
import json
import re


def normalize(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def main():
    total = 0
    right_matches = 0
    hallucinated_matches = 0
    both_match = 0
    neither_match = 0

    with open("data/evaluation_data.json", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            item = json.loads(line)

            knowledge = normalize(item["knowledge"])
            right_answer = normalize(item["right_answer"])
            hallucinated_answer = normalize(item["hallucinated_answer"])

            right_found = bool(right_answer) and right_answer in knowledge
            hallucinated_found = (
                bool(hallucinated_answer)
                and hallucinated_answer in knowledge
            )

            total += 1
            right_matches += right_found
            hallucinated_matches += hallucinated_found
            both_match += right_found and hallucinated_found
            neither_match += not right_found and not hallucinated_found

    print("\n========== ANSWER MATCHING BASELINE ==========")
    print("Total records:", total)
    print(
        f"Right answers found in knowledge: "
        f"{right_matches}/{total} ({right_matches / total * 100:.2f}%)"
    )
    print(
        f"Hallucinated answers found in knowledge: "
        f"{hallucinated_matches}/{total} "
        f"({hallucinated_matches / total * 100:.2f}%)"
    )
    print("Both answers found:", both_match)
    print("Neither answer found:", neither_match)
    print("\nNote: Exact phrase matching does not establish factual support.")


if __name__ == "__main__":
    main()
