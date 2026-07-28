from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class PDFLoader:
    """
    Handles loading and splitting PDF documents
    into smaller text chunks for RAG processing.
    """

    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def load_pdf(self, pdf_path):
        """
        Load a PDF file.
        """
        loader = PyPDFLoader(str(pdf_path))
        return loader.load()

    def split_documents(self, documents):
        """
        Split documents into chunks.
        """
        return self.text_splitter.split_documents(documents)

    def process_pdf(self, pdf_path):
        """
        Load and split a PDF.
        """
        documents = self.load_pdf(pdf_path)
        chunks = self.split_documents(documents)
        return chunks    