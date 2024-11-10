from typing import List, Dict
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownTextSplitter
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
        
        # Initialize text splitters
        self.default_text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  # Smaller chunks for better granularity
            chunk_overlap=50,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        self.markdown_splitter = MarkdownTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        
        # Create storage directory if it doesn't exist
        os.makedirs(self.storage_dir, exist_ok=True)
        
        self.vector_store = None

    def is_markdown_file(self, file_path: str) -> bool:
        """Check if a file is a markdown file."""
        return file_path.lower().endswith(('.md', '.markdown'))

    def process_documents(self, documents: List[Dict[str, str]]) -> List[Document]:
        """Convert raw documents into LangChain documents and split them."""
        split_docs = []
        
        for doc in documents:
            file_path = doc["path"]
            content = doc["content"]
            
            # Create metadata with file information
            metadata = {
                "source": file_path,
                "file_type": os.path.splitext(file_path)[1].lower(),
                "is_markdown": self.is_markdown_file(file_path)
            }
            
            # Create initial document
            langchain_doc = Document(page_content=content, metadata=metadata)
            
            # Choose appropriate splitter based on file type
            if self.is_markdown_file(file_path):
                # Special handling for markdown files
                chunks = self.markdown_splitter.split_text(content)
                split_docs.extend([
                    Document(page_content=chunk, metadata=metadata)
                    for chunk in chunks
                ])
            else:
                # Use default splitter for other files
                chunks = self.default_text_splitter.split_documents([langchain_doc])
                split_docs.extend(chunks)
        
        return split_docs

    def create_or_update_vector_store(self, documents: List[Dict[str, str]]) -> None:
        """Create or update the vector store with the provided documents."""
        processed_docs = self.process_documents(documents)
        
        if os.path.exists(self.vector_store_path):
            # Load existing vector store and add new documents
            self.vector_store = FAISS.load_local(
                self.vector_store_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            # Delete existing documents if they exist
            # This ensures we don't have duplicate or outdated content
            self.vector_store = FAISS.from_documents(
                processed_docs,
                self.embeddings
            )
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
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
            else:
                raise ValueError("No vector store exists for this project")
        
        # Perform search
        results = self.vector_store.similarity_search(query, k=k)
        
        # Sort results to group chunks from the same file together
        results.sort(key=lambda x: x.metadata["source"])
        
        return results

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
