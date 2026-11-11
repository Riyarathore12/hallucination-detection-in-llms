
from verifier_agent import VerifierAgent

agent = VerifierAgent()

test_cases = [
    {
        "name": "Same person, wrong role",
        "question": "Who directed V for Vendetta?",
        "claim": "Alan Moore directed V for Vendetta.",
        "evidence": "V for Vendetta was directed by James McTeigue. Alan Moore wrote the comic series.",
        "expected": "CONTRADICTED"
    },
    {
        "name": "Same date, unrelated context",
        "question": "When was Pearl Jam formed?",
        "claim": "Pearl Jam was formed in 1986.",
        "evidence": "Pearl Jam was formed in Seattle in 1990. Its first album was released in 1991.",
        "expected": "CONTRADICTED"
    },
    {
        "name": "Partially supported claim",
        "question": "Where is the school located?",
        "claim": "The school is located in Brookline and has 5,000 students.",
        "evidence": "The school is located in Brookline, New Hampshire.",
        "expected": "REVIEW_REQUIRED"
    },
    {
        "name": "Unrelated evidence",
        "question": "Who founded the company?",
        "claim": "John Smith founded the company.",
        "evidence": "The company sells software products to businesses.",
        "expected": "REVIEW_REQUIRED"
    }
]

passed = 0

for case in test_cases:
    evidence = [{
        "description": case["evidence"],
        "similarity_score": 0.90
    }]

    result = agent.verify_claim(
        case["claim"],
        evidence,
        question=case["question"]
    )

    actual = result["status"]
    passed += actual == case["expected"]

    print("\nTest:", case["name"])
    print("Expected:", case["expected"])
    print("Actual:", actual)
    print("Result:", "PASS" if actual == case["expected"] else "FAIL")

print("\nPassed:", passed, "/", len(test_cases))
