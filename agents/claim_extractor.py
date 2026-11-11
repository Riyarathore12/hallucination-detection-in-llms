
import re


class ClaimExtractor:

    def __init__(self):
        print("Loading Claim Extraction Agent...")
        print("Claim Extraction Agent loaded.")

    def extract_claims(self, answer):

        if not answer or not answer.strip():
            return []

        answer = " ".join(answer.split())

        # Split answer into individual sentences
        sentences = re.split(
            r'(?<=[.!?])\s+',
            answer
        )

        claims = []

        for sentence in sentences:

            sentence = sentence.strip(" .!?")

            if not sentence:
                continue

            # Split simple coordinated claims
            # Example: A did X and did Y.
            parts = re.split(
                r'\s+and\s+(?=(?:won|received|developed|created|'
                r'helped|founded|invented|became|served|was|is|'
                r'has|had)\b)',
                sentence,
                flags=re.IGNORECASE
            )

            if len(parts) > 1:

                first_part = parts[0].strip()

                claims.append(first_part)

                for part in parts[1:]:
                    part = part.strip()

                    # Restore subject for simple coordinated verbs
                    subject_match = re.match(
                        r'^(.+?)\s+(?:was|is|were|are|has|had)\b',
                        first_part,
                        re.IGNORECASE
                    )

                    if subject_match:
                        subject = subject_match.group(1)
                        claims.append(f"{subject} {part}")
                    else:
                        claims.append(part)

            else:
                claims.append(sentence)

        # Remove duplicate claims
        return list(dict.fromkeys(claims))


if __name__ == "__main__":

    extractor = ClaimExtractor()

    answer = """
    Alan Turing was a British mathematician who helped break the
    Enigma code and won the Nobel Prize in Physics in 1950.
    """

    claims = extractor.extract_claims(answer)

    print("\nExtracted Claims:")

    for i, claim in enumerate(claims, 1):
        print(f"Claim {i}: {claim}")
