import os
from typing import List, Dict, Optional
import json
from datetime import datetime

from utils.file_processor import FileProcessor
from vector_store.vector_store_manager import VectorStoreManager

class ProjectManager:
    def __init__(self, projects_dir: str = "projects"):
        """Initialize the project manager."""
        self.projects_dir = projects_dir
        self.projects_file = os.path.join(projects_dir, "projects.json")
        self.initialize_projects_directory()

    def initialize_projects_directory(self) -> None:
        """Create projects directory and projects.json if they don't exist."""
        os.makedirs(self.projects_dir, exist_ok=True)
        if not os.path.exists(self.projects_file):
            self._save_projects({})

    def _load_projects(self) -> Dict:
        """Load projects from projects.json."""
        try:
            with open(self.projects_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_projects(self, projects: Dict) -> None:
        """Save projects to projects.json."""
        with open(self.projects_file, 'w') as f:
            json.dump(projects, f, indent=4)

    def create_project(self, name: str, repository_path: str) -> bool:
        """
        Create a new project and process its repository.
        Returns True if successful, False otherwise.
        """
        if not os.path.exists(repository_path):
            print(f"Error: Repository path '{repository_path}' does not exist.")
            return False

        projects = self._load_projects()
        if name in projects:
            print(f"Error: Project '{name}' already exists.")
            return False

        try:
            # Process repository files
            file_processor = FileProcessor()
            documents = file_processor.process_directory(repository_path)

            if not documents:
                print(f"Warning: No valid text files found in '{repository_path}'")
                return False

            # Create and populate vector store
            vector_store = VectorStoreManager(name)
            vector_store.create_or_update_vector_store(documents)

            # Save project metadata
            projects[name] = {
                "repository_path": repository_path,
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "document_count": len(documents)
            }
            self._save_projects(projects)

            print(f"Successfully created project '{name}' with {len(documents)} documents.")
            return True

        except Exception as e:
            print(f"Error creating project: {str(e)}")
            return False

    def update_project(self, name: str) -> bool:
        """
        Update an existing project by reprocessing its repository.
        Returns True if successful, False otherwise.
        """
        projects = self._load_projects()
        if name not in projects:
            print(f"Error: Project '{name}' does not exist.")
            return False

        repository_path = projects[name]["repository_path"]
        if not os.path.exists(repository_path):
            print(f"Error: Repository path '{repository_path}' no longer exists.")
            return False

        try:
            # Process repository files
            file_processor = FileProcessor()
            documents = file_processor.process_directory(repository_path)

            if not documents:
                print(f"Warning: No valid text files found in '{repository_path}'")
                return False

            # Update vector store
            vector_store = VectorStoreManager(name)
            vector_store.create_or_update_vector_store(documents)

            # Update project metadata
            projects[name]["last_updated"] = datetime.now().isoformat()
            projects[name]["document_count"] = len(documents)
            self._save_projects(projects)

            print(f"Successfully updated project '{name}' with {len(documents)} documents.")
            return True

        except Exception as e:
            print(f"Error updating project: {str(e)}")
            return False

    def delete_project(self, name: str) -> bool:
        """
        Delete a project and its associated vector store.
        Returns True if successful, False otherwise.
        """
        projects = self._load_projects()
        if name not in projects:
            print(f"Error: Project '{name}' does not exist.")
            return False

        try:
            # Delete vector store
            vector_store = VectorStoreManager(name)
            vector_store.delete_vector_store()

            # Remove project from projects.json
            del projects[name]
            self._save_projects(projects)

            print(f"Successfully deleted project '{name}'.")
            return True

        except Exception as e:
            print(f"Error deleting project: {str(e)}")
            return False

    def list_projects(self) -> List[Dict]:
        """Return a list of all projects and their metadata."""
        return list(self._load_projects().items())

    def search_project(self, name: str, query: str, k: int = 5) -> List[Dict]:
        """
        Search for similar documents in a project.
        Returns k most similar documents.
        """
        projects = self._load_projects()
        if name not in projects:
            print(f"Error: Project '{name}' does not exist.")
            return []

        try:
            vector_store = VectorStoreManager(name)
            results = vector_store.similarity_search(query, k=k)
            
            # Format results
            formatted_results = []
            for doc in results:
                formatted_results.append({
                    "source": doc.metadata["source"],
                    "content": doc.page_content,
                })
            
            return formatted_results

        except Exception as e:
            print(f"Error searching project: {str(e)}")
            return []
