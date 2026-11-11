
import re


class CorrectionAgent:

    def __init__(self):
        print("Loading Evidence-Based Correction Agent...")
        print("Correction Agent loaded.")

    def correct_claim(self, claim: str, evidence_list: list) -> dict:

        if not evidence_list:
            return {
                "original_claim": claim,
                "corrected_claim": None,
                "status": "NO_CORRECTION",
                "reason": "No evidence available."
            }

        valid_evidence = [
            item for item in evidence_list
            if item.get("description", "").strip()
        ]

        if not valid_evidence:
            return {
                "original_claim": claim,
                "corrected_claim": None,
                "status": "NO_CORRECTION",
                "reason": "Retrieved evidence is empty."
            }

        best = max(
            valid_evidence,
            key=lambda x: x.get("similarity_score", 0.0)
        )

        evidence = best["description"].strip()
        similarity = best.get("similarity_score", 0.0)

        if similarity < 0.50:
            return {
                "original_claim": claim,
                "corrected_claim": None,
                "status": "NO_CORRECTION",
                "reason": "Evidence relevance is too low."
            }

        # Extract a complete evidence sentence only when
        # it contains an explicit correction signal.
        sentences = re.split(r'(?<=[.!?])\s+', evidence)

        claim_words = set(
            re.findall(r"\b[a-z0-9]+\b", claim.lower())
        )

        for sentence in sentences:
            sentence = sentence.strip()

            if not sentence:
                continue

            sentence_words = set(
                re.findall(r"\b[a-z0-9]+\b", sentence.lower())
            )

            # Require meaningful overlap with the original claim.
            overlap = claim_words & sentence_words

            if len(overlap) >= 2:
                return {
                    "original_claim": claim,
                    "corrected_claim": sentence,
                    "status": "EVIDENCE_EXTRACTED",
                    "reason": (
                        "A relevant sentence was extracted directly "
                        "from the retrieved evidence. It is not an "
                        "independently generated correction."
                    ),
                    "supporting_evidence": sentence
                }

        return {
            "original_claim": claim,
            "corrected_claim": None,
            "status": "REVIEW_REQUIRED",
            "reason": (
                "Relevant evidence was found, but a sufficiently "
                "related correction sentence could not be extracted."
            ),
            "supporting_evidence": evidence
        }


if __name__ == "__main__":

    agent = CorrectionAgent()

    claim = "First for Women was started first."

    evidence = [
        {
            "description": (
                "Arthur's Magazine (1844–1846) was an American "
                "literary periodical published in Philadelphia "
                "in the 19th century."
            ),
            "similarity_score": 0.42
        }
    ]

    result = agent.correct_claim(claim, evidence)

    print("\nCorrection Result:")
    print(result)
