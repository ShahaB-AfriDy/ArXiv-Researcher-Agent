"""
memory_manager.py
-----------------
Handles persistent memory for the ArXiv Researcher Agent using PostgreSQL (pgvector).
This integrates with LangGraph's memory API to provide semantic recall.
"""

import os
from langgraph.store.postgres import PostgresStore
from dotenv import load_dotenv

load_dotenv()


class ResearchMemoryManager:
    """
    Manages persistent memory storage and retrieval for research sessions.
    Uses pgvector-based embeddings for semantic similarity search.
    """

    def __init__(self):
        postgres_url = os.getenv("POSTGRES_URL")
        if not postgres_url:
            raise ValueError("POSTGRES_URL is missing in environment variables.")

        # Initialize LangGraph's PostgresStore
        self.store = PostgresStore(postgres_url)

    def save_memory(self, key: str, data: dict):
        """Store a memory record."""
        print(f"[MemoryManager] Saving memory for key: {key}")
        self.store.put(key, data)

    def search_memory(self, query: str, top_k: int = 5):
        """Semantic search for past research."""
        print(f"[MemoryManager] Searching memory for: {query}")
        results = self.store.search(query=query, limit=top_k)
        return results

    def get_memory(self, key: str):
        """Retrieve memory by key."""
        print(f"[MemoryManager] Retrieving memory for key: {key}")
        return self.store.get(key)

    def delete_memory(self, key: str):
        """Delete specific memory by key."""
        print(f"[MemoryManager] Deleting memory for key: {key}")
        self.store.delete(key)


# Example usage
if __name__ == "__main__":
    memory = ResearchMemoryManager()
    memory.save_memory("session-001", {"topic": "AI alignment", "summary": "Study on LLM safety mechanisms."})
    print(memory.search_memory("LLM safety"))
