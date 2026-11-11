class CorrectionAgent:

    def __init__(self):
        print("Loading Correction Agent...")
        print("Correction Agent loaded.")

    def correct_claim(self, claim: str, evidence_list: list) -> dict:

        if not evidence_list:
            return {
                "corrected_claim": claim,
                "status": "NO_CORRECTION",
                "reason": "No evidence available"
            }

        # Select the strongest retrieved evidence
        best_evidence = max(
            evidence_list,
            key=lambda x: x.get("similarity_score", 0.0)
        )

        evidence_text = best_evidence.get(
            "description",
            ""
        ).strip()

        if not evidence_text:
            return {
                "corrected_claim": claim,
                "status": "NO_CORRECTION",
                "reason": "Retrieved evidence is empty"
            }

        return {
            "corrected_claim": evidence_text,
            "status": "CORRECTED",
            "reason": "Claim replaced using retrieved evidence"
        }


if __name__ == "__main__":

    agent = CorrectionAgent()

    claim = "First for Women was started first."

    evidence = [
        {
            "description":
            "Arthur's Magazine (1844–1846) was an American "
            "literary periodical published in Philadelphia "
            "in the 19th century.",
            "similarity_score": 0.42
        }
    ]

    result = agent.correct_claim(
        claim,
        evidence
    )

    print("\nCorrection Result:")
    print(result)