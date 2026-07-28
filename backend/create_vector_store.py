from backend.pdf_loader import PDFLoader
from backend.vector_store import VectorStore
from backend.config import PDF_PATH


def main():

    print("Loading PDF...")

    loader = PDFLoader()
    chunks = loader.process_pdf(PDF_PATH)

    print(f"Creating embeddings for {len(chunks)} chunks...")

    vector_store = VectorStore()
    vector_store.create_vector_store(chunks)

    print("FAISS vector store created successfully!")


if __name__ == "__main__":
    main()
