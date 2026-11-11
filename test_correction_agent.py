
from agents.correction_agent import CorrectionAgent

agent = CorrectionAgent()

tests = [
    {
        "name": "Strong evidence",
        "claim": "Pearl Jam was formed in 1986.",
        "evidence": [{
            "description": "Pearl Jam was formed in Seattle in 1990.",
            "similarity_score": 0.90
        }],
        "expected": "EVIDENCE_EXTRACTED"
    },
    {
        "name": "Weak evidence",
        "claim": "Pearl Jam was formed in 1986.",
        "evidence": [{
            "description": "A music magazine was published in 1986.",
            "similarity_score": 0.30
        }],
        "expected": "NO_CORRECTION"
    },
    {
        "name": "Missing evidence",
        "claim": "Pearl Jam was formed in 1986.",
        "evidence": [],
        "expected": "NO_CORRECTION"
    }
]

passed = 0

for test in tests:
    result = agent.correct_claim(test["claim"], test["evidence"])
    actual = result["status"]

    if actual == test["expected"]:
        passed += 1

    print("\nTest:", test["name"])
    print("Expected:", test["expected"])
    print("Actual:", actual)
    print("Correction:", result["corrected_claim"])
    print("Result:", "PASS" if actual == test["expected"] else "FAIL")

print("\nPassed:", passed, "/", len(tests))
