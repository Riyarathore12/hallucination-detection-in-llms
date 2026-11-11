
from agents.claim_extractor import ClaimExtractor
from retriever_agent import RetrievalAgent
from verifier_agent import VerifierAgent
from agents.correction_agent import CorrectionAgent


class HallucinationDetectionPipeline:

    def __init__(self):
        self.extractor = ClaimExtractor()
        self.retriever = RetrievalAgent()
        self.verifier = VerifierAgent()
        self.corrector = CorrectionAgent()

    def run(self, claim, question=""):

        print("\nOriginal question:", question)
        print("Processing claim:", claim)

        # Step 1: Retrieve relevant evidence
        search_query = f"{question} {claim}".strip()

        evidence = self.retriever.fetch_evidence(
            search_query,
            top_k=3
        )

        print("\nRetrieved evidence:")

        for item in evidence:
            print(
                f"Score: {item.get('similarity_score', 0.0):.4f}"
            )
            print("Evidence:", item.get("description", ""))

        # Step 2: Verify the claim
        verification = self.verifier.verify_claim(
            claim,
            evidence,
            question=question
        )

        status = verification["status"]

        print("\nVerification:", status)

        # Step 3: Handle the result conservatively
        evidence_extraction = None

        if status == "CONTRADICTED":
            evidence_extraction = self.corrector.correct_claim(
                claim,
                evidence
            )

        elif status == "REVIEW_REQUIRED":
            evidence_extraction = {
                "original_claim": claim,
                "extracted_evidence": None,
                "status": "MANUAL_REVIEW_REQUIRED",
                "reason": (
                    "The claim could not be verified confidently. "
                    "No automatic correction was attempted."
                )
            }

        elif status == "SUPPORTED":
            evidence_extraction = {
                "original_claim": claim,
                "extracted_evidence": None,
                "status": "NO_CORRECTION_NEEDED",
                "reason": (
                    "The claim passed the current verification rules."
                )
            }

        return {
            "question": question,
            "claim": claim,
            "evidence_retrieved": len(evidence),
            "verification_result": verification,
            "evidence_extraction_result": evidence_extraction
        }


if __name__ == "__main__":

    print("\n==========================================")
    print("  LLM HALLUCINATION DETECTION SYSTEM")
    print("==========================================")

    # Get manual input
    question = input("\nEnter your question: ").strip()

    answer = input(
        "\nEnter the LLM-generated answer: "
    ).strip()

    if not question or not answer:
        print("\nQuestion and answer cannot be empty.")
        raise SystemExit

    # Initialize pipeline
    pipeline = HallucinationDetectionPipeline()

    # Step 1: Extract claims
    claims = pipeline.extractor.extract_claims(answer)

    print("\nOriginal answer:")
    print(answer)

    print("\nExtracted claims:")

    if not claims:
        print("No claims could be extracted.")
        raise SystemExit

    # Step 2: Process each claim
    for i, claim in enumerate(claims, 1):

        print(f"\n========== CLAIM {i} ==========")

        result = pipeline.run(
            claim,
            question=question
        )

        print("\nFinal result:")
        print(result)

    print("\n==========================================")
    print("          PROCESSING COMPLETED")
    print("==========================================")
