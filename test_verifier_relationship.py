
from verifier_agent import VerifierAgent

agent = VerifierAgent()

claim = (
    "The Hollis/Brookline High School is located "
    "in the Talbot-Taylor Wildlife Sanctuary"
)

evidence = [{
    "description": (
        "Hollis/Brookline High School is a public school "
        "located in Hollis, New Hampshire, serving the "
        "towns of Hollis and Brookline. Brookline is a town "
        "in Hillsborough County, New Hampshire. Brookline "
        "is home to the Talbot-Taylor Wildlife Sanctuary."
    ),
    "similarity_score": 0.6927
}]

result = agent.verify_claim(
    claim,
    evidence,
    question=(
        "Which wildlife sanctuary is located in the town "
        "in which the Hollis/Brookline High School services?"
    )
)

print("Expected: REVIEW_REQUIRED")
print("Actual:", result["status"])
print("Reason:", result["reason"])

if result["status"] == "REVIEW_REQUIRED":
    print("PASS")
else:
    print("FAIL")
