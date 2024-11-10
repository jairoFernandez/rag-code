import os
from typing import List, Dict
import magic

class FileProcessor:
    SUPPORTED_EXTENSIONS = {
        '.txt', '.py', '.js', '.java', '.cpp', '.h', '.hpp', 
        '.md', '.rst', '.json', '.yaml', '.yml', '.xml',
        '.html', '.css', '.sql', '.sh', '.bash',
        '.gitignore', '.env', 'Dockerfile', 'README'
    }

    @staticmethod
    def is_text_file(file_path: str) -> bool:
        """Check if a file is a text file using python-magic."""
        try:
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(file_path)
            return file_type.startswith('text/') or any(file_path.endswith(ext) for ext in FileProcessor.SUPPORTED_EXTENSIONS)
        except Exception:
            return False

    @staticmethod
    def read_file_content(file_path: str) -> str:
        """Read and return the content of a text file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")
            return ""

    @staticmethod
    def process_directory(directory_path: str) -> List[Dict[str, str]]:
        """
        Process all text files in a directory recursively.
        Returns a list of dictionaries containing file paths and their contents.
        """
        documents = []
        
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                if FileProcessor.is_text_file(file_path):
                    content = FileProcessor.read_file_content(file_path)
                    if content:
                        relative_path = os.path.relpath(file_path, directory_path)
                        documents.append({
                            "path": relative_path,
                            "content": content
                        })
        
        return documents
