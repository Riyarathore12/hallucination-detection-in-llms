
from verifier_agent import VerifierAgent

agent = VerifierAgent()

cases = [
    {
        "name": "Wrong location",
        "claim": "Cabañeros National Park is located in Tenerife.",
        "evidence": (
            "Cabañeros National Park is in the Montes de Toledo, Spain. "
            "Teide National Park is located in Tenerife."
        ),
        "expected": "CONTRADICTED"
    },
    {
        "name": "Wrong person's birth date",
        "claim": "AnnaLynne McCord was born 6 March 1997.",
        "evidence": (
            "The film stars AnnaLynne McCord and Alisha Boe. "
            "Alisha Boe was born 6 March 1997."
        ),
        "expected": "CONTRADICTED"
    },
    {
        "name": "Wrong formation year",
        "claim": "Pearl Jam was formed before 1990.",
        "evidence": (
            "Pearl Jam was formed in 1990. "
            "The House of Love was formed in 1986."
        ),
        "expected": "CONTRADICTED"
    },
    {
        "name": "Wrong film director",
        "claim": "Alan Moore directed V for Vendetta.",
        "evidence": (
            "V for Vendetta was directed by James McTeigue "
            "and written by Alan Moore and David Lloyd."
        ),
        "expected": "CONTRADICTED"
    }
]

passed = 0

for case in cases:
    result = agent.verify_claim(
        case["claim"],
        [{
            "description": case["evidence"],
            "similarity_score": 1.0
        }]
    )

    actual = result["status"]
    success = actual == case["expected"]

    if success:
        passed += 1

    print(
        f"{case['name']}: "
        f"Expected={case['expected']}, "
        f"Actual={actual}, "
        f"{'PASS' if success else 'FAIL'}"
    )

print(f"\nRegression tests: {passed}/{len(cases)} passed")
