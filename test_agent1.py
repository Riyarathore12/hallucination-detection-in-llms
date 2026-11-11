import json
from agents.claim_extractor import ClaimExtractor


# Load HaluEval QA dataset
data = []

with open("data/qa_data.json", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            data.append(json.loads(line))


extractor = ClaimExtractor()

print("Dataset samples:", len(data))

# Test first 3 hallucinated answers
for i, item in enumerate(data[:3], 1):

    answer = item["hallucinated_answer"]

    print("\n" + "=" * 60)
    print(f"Sample {i}")
    print("Question:", item["question"])
    print("Hallucinated Answer:", answer)

    claims = extractor.extract_claims(answer)

    print("\nExtracted Claims:")

    for j, claim in enumerate(claims, 1):
        print(f"  Claim {j}: {claim}")