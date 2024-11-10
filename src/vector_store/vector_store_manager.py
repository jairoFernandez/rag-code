from typing import List, Dict
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

class VectorStoreManager:
    def __init__(self, project_name: str, storage_dir: str = "vector_stores"):
        """Initialize the vector store manager."""
        self.project_name = project_name
        self.storage_dir = storage_dir
        self.vector_store_path = os.path.join(storage_dir, project_name)
        
        # Initialize embeddings model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Create storage directory if it doesn't exist
        os.makedirs(self.storage_dir, exist_ok=True)
        
        self.vector_store = None

    def process_documents(self, documents: List[Dict[str, str]]) -> List[Document]:
        """Convert raw documents into LangChain documents and split them."""
        langchain_docs = []
        
        for doc in documents:
            metadata = {"source": doc["path"]}
            langchain_doc = Document(page_content=doc["content"], metadata=metadata)
            langchain_docs.append(langchain_doc)
        
        # Split documents into chunks
        split_docs = self.text_splitter.split_documents(langchain_docs)
        return split_docs

    def create_or_update_vector_store(self, documents: List[Dict[str, str]]) -> None:
        """Create or update the vector store with the provided documents."""
        processed_docs = self.process_documents(documents)
        
        if os.path.exists(self.vector_store_path):
            # Load existing vector store and add new documents
            self.vector_store = FAISS.load_local(
                self.vector_store_path,
                self.embeddings
            )
            self.vector_store.add_documents(processed_docs)
        else:
            # Create new vector store
            self.vector_store = FAISS.from_documents(
                processed_docs,
                self.embeddings
            )
        
        # Save the vector store
        self.vector_store.save_local(self.vector_store_path)

    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """
        Perform similarity search in the vector store.
        Returns k most similar documents.
        """
        if not self.vector_store:
            if os.path.exists(self.vector_store_path):
                self.vector_store = FAISS.load_local(
                    self.vector_store_path,
                    self.embeddings
                )
            else:
                raise ValueError("No vector store exists for this project")
        
        return self.vector_store.similarity_search(query, k=k)

    def delete_vector_store(self) -> bool:
        """Delete the vector store for this project."""
        try:
            import shutil
            if os.path.exists(self.vector_store_path):
                shutil.rmtree(self.vector_store_path)
                self.vector_store = None
                return True
            return False
        except Exception as e:
            print(f"Error deleting vector store: {str(e)}")
            return False
