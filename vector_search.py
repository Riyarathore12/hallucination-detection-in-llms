
import json
import re
import math
from collections import Counter

INDEX_FILE = "vector_index_dev.json"

STOP_WORDS = {
    "the", "a", "an", "is", "was", "were", "are",
    "in", "on", "at", "of", "and", "or", "to",
    "for", "from", "by", "with", "what", "which",
    "who", "when", "where", "how", "it", "its",
    "this", "that", "has", "have", "had", "be",
    "been", "being", "do", "does", "did"
}


def tokenize(text):
    words = re.findall(r"\b[a-z0-9]+\b", text.lower())
    return [word for word in words if word not in STOP_WORDS]


print("Loading lightweight evidence index...")

with open(INDEX_FILE, encoding="utf-8") as file:
    index = json.load(file)

print("Evidence records loaded:", len(index))

# Calculate document frequency for IDF.
document_frequency = Counter()

for document in index:
    unique_words = set(document["words"])
    for word in unique_words:
        if word not in STOP_WORDS:
            document_frequency[word] += 1

total_documents = len(index)


def calculate_idf(word):
    df = document_frequency.get(word, 0)
    return math.log(
        (total_documents + 1) / (df + 1)
    ) + 1


def calculate_similarity(query_words, document_words):
    query_counts = Counter(query_words)
    document_counts = Counter(
        word for word in document_words
        if word not in STOP_WORDS
    )

    common_words = set(query_counts) & set(document_counts)

    dot_product = sum(
        query_counts[word] *
        document_counts[word] *
        calculate_idf(word) ** 2
        for word in common_words
    )

    query_norm = math.sqrt(sum(
        (count * calculate_idf(word)) ** 2
        for word, count in query_counts.items()
    ))

    document_norm = math.sqrt(sum(
        (count * calculate_idf(word)) ** 2
        for word, count in document_counts.items()
    ))

    if query_norm == 0 or document_norm == 0:
        return 0.0

    return dot_product / (query_norm * document_norm)


def search_dataset(query_text, top_k=3):
    query_words = tokenize(query_text)
    results = []

    for document in index:
        document_words = document["words"]

        score = calculate_similarity(
            query_words,
            document_words
        )

        results.append({
            "id": document["id"],
            "description": document["description"],
            "category": document["category"],
            "similarity_score": round(score, 4)
        })

    results.sort(
        key=lambda item: item["similarity_score"],
        reverse=True
    )

    return results[:top_k]
