from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


class VectorStore:
    """
    Creates, saves, and loads the FAISS vector database
    used for semantic search.
    """

    def __init__(self, api_key=None, db_path="data/processed/faiss_index"):
        self.db_path = Path(db_path)

        # Free local embeddings (No API key required)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def create_vector_store(self, documents):
        """
        Build a FAISS vector database from documents.
        """

        vector_store = FAISS.from_documents(
            documents,
            self.embeddings
        )

        vector_store.save_local(str(self.db_path))

    def load_vector_store(self):
        """
        Load an existing FAISS vector database.
        """

        return FAISS.load_local(
            str(self.db_path),
            self.embeddings,
            allow_dangerous_deserialization=True
        )