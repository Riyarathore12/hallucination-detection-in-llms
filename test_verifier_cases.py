
from verifier_agent import VerifierAgent

agent = VerifierAgent()

test_cases = [
    {
        "name": "Correct factual answer",
        "question": "What kind of athlete is Claudia Rivas?",
        "claim": "Claudia Rivas Vega is a triathlete.",
        "evidence": "Claudia Rivas Vega is a Mexican triathlete.",
        "expected": "SUPPORTED"
    },
    {
        "name": "Incorrect entity",
        "question": "Who directed V for Vendetta?",
        "claim": "Alan Moore directed V for Vendetta.",
        "evidence": "V for Vendetta was directed by James McTeigue.",
        "expected": "CONTRADICTED"
    },
    {
        "name": "Incorrect date",
        "question": "When was Pearl Jam formed?",
        "claim": "Pearl Jam was formed in 1986.",
        "evidence": "Pearl Jam is an American rock band formed in Seattle in 1990.",
        "expected": "CONTRADICTED"
    },
    {
        "name": "Incorrect relationship",
        "question": "Who directed the film?",
        "claim": "Alan Moore directed the film.",
        "evidence": "The film was directed by James McTeigue. Alan Moore wrote the comic series.",
        "expected": "CONTRADICTED"
    },
    {
        "name": "Insufficient evidence",
        "question": "Where was the person born?",
        "claim": "The person was born in London.",
        "evidence": "",
        "expected": "REVIEW_REQUIRED"
    }
]

passed = 0

for case in test_cases:

    evidence_list = []

    if case["evidence"]:
        evidence_list = [{
            "description": case["evidence"],
            "similarity_score": 0.90
        }]

    result = agent.verify_claim(
        case["claim"],
        evidence_list,
        question=case["question"]
    )

    actual = result["status"]

    if actual == case["expected"]:
        passed += 1

    print("\nTest:", case["name"])
    print("Expected:", case["expected"])
    print("Actual:", actual)
    print("Result:", "PASS" if actual == case["expected"] else "FAIL")

print("\n==========================")
print("Passed:", passed, "/", len(test_cases))
print("==========================")

