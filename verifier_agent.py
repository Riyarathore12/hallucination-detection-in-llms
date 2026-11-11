
import re


class VerifierAgent:

    def __init__(self):
        print("Loading Rule-Based Verifier...")
        print("Verifier loaded.")

    def tokenize(self, text):
        return set(re.findall(r"\b[a-z0-9]+\b", text.lower()))

    def verify_claim(self, claim, evidence_list, question=""):

        # 1. Check whether evidence is available.
        if not evidence_list:
            return {
                "status": "REVIEW_REQUIRED",
                "confidence": 0.0,
                "reason": "No evidence is available for verification."
            }

        best = max(
            evidence_list,
            key=lambda x: x.get("similarity_score", 0.0)
        )

        evidence = best.get("description", "")
        score = best.get("similarity_score", 0.0)

        if not evidence.strip() or score < 0.20:
            return {
                "status": "REVIEW_REQUIRED",
                "confidence": round(score, 4),
                "reason": "Insufficient relevant evidence.",
                "supporting_evidence": evidence
            }

        claim_lower = claim.lower()

        def result(status, reason):
            return {
                "status": status,
                "confidence": round(score, 4),
                "reason": reason,
                "supporting_evidence": evidence
            }

        sentences = re.split(r"(?<=[.!?])\s+", evidence.strip())

        # 2. Check film director relationships.
        if "directed" in claim_lower:

            director_match = re.search(
                r"\bdirected by\s+([A-Z][a-z]+"
                r"(?:\s+[A-Z][a-z]+)*)",
                evidence
            )

            if not director_match:
                director_match = re.search(
                    r"\bwas directed by\s+([A-Z][a-z]+"
                    r"(?:\s+[A-Z][a-z]+)*)",
                    evidence
                )

            if director_match:
                evidence_director = self.tokenize(
                    director_match.group(1)
                )
                claim_words = self.tokenize(claim)

                if not evidence_director.issubset(claim_words):
                    return result(
                        "CONTRADICTED",
                        "The director named in the claim conflicts with the evidence."
                    )

        # 3. Check entity-specific location relationships.
        location_claim = re.search(
            r"^(.+?)\s+is\s+(?:located|situated|based)\s+in\s+(.+?)[.]?$",
            claim.strip(),
            re.IGNORECASE
        )

        if location_claim:

            subject = location_claim.group(1).strip()
            claimed_location = location_claim.group(2).strip(
                " .,!?")
            subject_words = self.tokenize(subject)

            for sentence in sentences:

                sentence_words = self.tokenize(sentence)

                if subject_words and subject_words.issubset(sentence_words):

                    location_match = re.search(
                        r"\b(?:is\s+)?(?:located|situated|based)\s+in\s+"
                        r"(?:the\s+)?([^,.]+)",
                        sentence,
                        re.IGNORECASE
                    )

                    if not location_match:
                        location_match = re.search(
                            r"\bis\s+in\s+(?:the\s+)?([^,.]+)",
                            sentence,
                            re.IGNORECASE
                        )

                    if location_match:

                        actual_location = location_match.group(1).strip()

                        claimed_words = self.tokenize(claimed_location)
                        actual_words = self.tokenize(actual_location)

                        if (
                            claimed_words
                            and actual_words
                            and not claimed_words.issubset(actual_words)
                        ):
                            return result(
                                "CONTRADICTED",
                                "The claimed location conflicts with the location associated with the same entity in the evidence."
                            )

        # 4. Check person-specific birth dates.
        birth_claim = re.search(
            r"^(.+?)\s+was born\s+(.+?)[.]?$",
            claim.strip(),
            re.IGNORECASE
        )

        if birth_claim:

            person = birth_claim.group(1).strip()
            claimed_date = birth_claim.group(2).strip(" .,!?")
            person_words = self.tokenize(person)

            date_pattern = re.compile(
                r"\b(?:\d{1,2}\s+)?"
                r"(?:January|February|March|April|May|June|"
                r"July|August|September|October|November|December)"
                r"\s+\d{1,2},?\s+\d{4}\b|"
                r"\b\d{1,2}\s+"
                r"(?:January|February|March|April|May|June|"
                r"July|August|September|October|November|December)"
                r"\s+\d{4}\b",
                re.IGNORECASE
            )

            birth_sentences = [
                sentence for sentence in sentences
                if re.search(r"\bwas born\b|\bborn\b", sentence, re.I)
            ]

            person_birth_sentences = [
                sentence for sentence in birth_sentences
                if person_words
                and person_words.issubset(self.tokenize(sentence))
            ]

            if person_birth_sentences:

                for sentence in person_birth_sentences:

                    dates = date_pattern.findall(sentence)

                    if dates and not any(
                        self.tokenize(claimed_date)
                        == self.tokenize(date)
                        for date in dates
                    ):
                        return result(
                            "CONTRADICTED",
                            "The claimed birth date conflicts with the date associated with the same person."
                        )

                if not any(
                    date_pattern.search(sentence)
                    for sentence in person_birth_sentences
                ):
                    return result(
                        "REVIEW_REQUIRED",
                        "The evidence mentions the person but does not establish their birth date."
                    )

            elif birth_sentences:

                # A birth date is explicitly assigned to another person.
                for sentence in birth_sentences:

                    dates = date_pattern.findall(sentence)
                    sentence_words = self.tokenize(sentence)

                    if dates and not person_words.issubset(sentence_words):
                        return result(
                            "CONTRADICTED",
                            "The evidence assigns the stated birth date to a different person."
                        )

                return result(
                    "REVIEW_REQUIRED",
                    "The evidence does not establish the birth date of the claimed person."
                )

            else:
                return result(
                    "REVIEW_REQUIRED",
                    "No explicit birth-date evidence was found."
                )

        # 5. Check before/after formation-year comparisons.
        formation_claim = re.search(
            r"^(.+?)\s+was formed\s+(before|after)\s+((?:18|19|20)\d{2})[.]?$",
            claim.strip(),
            re.IGNORECASE
        )

        if formation_claim:

            entity = formation_claim.group(1).strip()
            direction = formation_claim.group(2).lower()
            target_year = int(formation_claim.group(3))

            entity_words = self.tokenize(entity)

            for sentence in sentences:

                sentence_words = self.tokenize(sentence)

                if entity_words and entity_words.issubset(sentence_words):

                    actual_year_match = re.search(
                        r"\b(?:was\s+)?formed\s+in\s+((?:18|19|20)\d{2})\b",
                        sentence,
                        re.IGNORECASE
                    )

                    if actual_year_match:

                        actual_year = int(actual_year_match.group(1))

                        if (
                            direction == "before"
                            and actual_year >= target_year
                        ):
                            return result(
                                "CONTRADICTED",
                                "The evidence gives a formation year that does not satisfy the claimed before-year condition."
                            )

                        if (
                            direction == "after"
                            and actual_year <= target_year
                        ):
                            return result(
                                "CONTRADICTED",
                                "The evidence gives a formation year that does not satisfy the claimed after-year condition."
                            )

                        if (
                            direction == "before"
                            and actual_year < target_year
                        ):
                            return result(
                                "SUPPORTED",
                                "The formation year in the evidence satisfies the claimed before-year condition."
                            )

                        if (
                            direction == "after"
                            and actual_year > target_year
                        ):
                            return result(
                                "SUPPORTED",
                                "The formation year in the evidence satisfies the claimed after-year condition."
                            )

            return result(
                "REVIEW_REQUIRED",
                "The evidence does not establish the formation-year comparison."
            )

        # 6. Check school-location relationships.
        if re.search(
            r"\b(?:located|situated)\s+in\b",
            claim_lower
        ):

            school_match = re.search(
                r"([A-Za-z0-9/&' -]+?)\s+is\s+"
                r"(?:a\s+)?(?:public\s+)?school\s+"
                r"located\s+in\s+([^,.]+)",
                evidence,
                re.IGNORECASE
            )

            if school_match:

                evidence_school = school_match.group(1).strip()
                evidence_location = school_match.group(2).strip()

                same_school = (
                    self.tokenize(evidence_school)
                    .issubset(self.tokenize(claim))
                )

                claimed_location = re.search(
                    r"\b(?:located|situated)\s+in\s+(.+)",
                    claim_lower
                )

                if same_school and claimed_location:

                    claim_location = claimed_location.group(1).strip()

                    if evidence_location.lower() not in claim_location:
                        return result(
                            "REVIEW_REQUIRED",
                            "The claimed school-location relationship is not established."
                        )

        # 7. Conservative textual support check.
        stop_words = {
            "the", "a", "an", "is", "was", "were", "are",
            "in", "on", "at", "of", "and", "or", "to",
            "for", "from", "by", "with", "he", "she",
            "it", "they", "this", "that", "has", "had",
            "as", "be", "been", "being"
        }

        claim_words = self.tokenize(claim) - stop_words
        evidence_words = self.tokenize(evidence)

        if claim_words and claim_words.issubset(evidence_words):
            return result(
                "SUPPORTED",
                "The claim's meaningful words appear explicitly in the evidence."
            )

        # 8. Default to manual review.
        return result(
            "REVIEW_REQUIRED",
            "The evidence does not establish or contradict the complete claim."
        )
