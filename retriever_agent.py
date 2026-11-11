
from vector_search import search_dataset


class RetrievalAgent:

    def fetch_evidence(self, query: str, top_k: int = 3):
        try:
            return search_dataset(query, top_k)
        except Exception as error:
            print(f"[RetrievalAgent Error]: {error}")
            return []


if __name__ == "__main__":
    agent = RetrievalAgent()

    results = agent.fetch_evidence(
        "Brookline wildlife sanctuary",
        top_k=3
    )

    print("Retrieved evidence:", len(results))

    for item in results:
        print("\nID:", item["id"])
        print("Evidence:", item["description"])
        print("Similarity:", item["similarity_score"])
