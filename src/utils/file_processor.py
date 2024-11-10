import os
from typing import List, Dict, Set
import magic

class FileProcessor:
    # File extensions to process
    SUPPORTED_EXTENSIONS = {
        '.txt', '.py', '.js', '.java', '.cpp', '.h', '.hpp', 
        '.md', '.rst', '.json', '.yaml', '.yml', '.xml',
        '.html', '.css', '.sql', '.sh', '.bash',
        '.gitignore', '.env', 'Dockerfile', 'README'
    }

    # Common directories to exclude for different languages/frameworks
    DEFAULT_EXCLUDED_DIRS = {
        # Version Control
        '.git', '.svn', '.hg',
        
        # Python
        'venv', 'env', '.env', '.venv', '__pycache__', '.pytest_cache', '.mypy_cache',
        'build', 'dist', '*.egg-info',
        
        # Node.js
        'node_modules', 'bower_components', '.npm', '.yarn',
        
        # Java
        'target', '.gradle', 'build', 'out',
        
        # Ruby
        '.bundle', 'vendor/bundle',
        
        # PHP
        'vendor',
        
        # Scala/SBT
        'target', '.metals',
        
        # .NET
        'bin', 'obj', 'packages',
        
        # IDEs and editors
        '.idea', '.vscode', '.vs', '.eclipse', '.settings',
        
        # OS specific
        '.DS_Store', '__MACOSX', 'Thumbs.db',
        
        # Build and dependency dirs
        'dist', 'build', 'out', 'deps',
        
        # Docker
        '.docker',
        
        # Coverage reports
        'coverage', '.coverage', 'htmlcov',
        
        # Documentation builds
        '_build', 'site', 'docs/_build',

        # terraform lock files
        'terraform.tfstate', 'terraform.tfstate.*', '.terraform.lock.hcl',
        
         # Terraform
         'terraform.tfvars',  '.terraform',
        
         # Composer
         'composer.lock', 'vendor',
    }

    # Common file patterns to exclude
    DEFAULT_EXCLUDED_FILES = {
        # Compiled files
        '*.pyc', '*.pyo', '*.pyd', '*.so', '*.dll', '*.class',
        '*.exe', '*.obj', '*.out',
        
        # Package files
        '*.jar', '*.war', '*.ear', '*.egg', '*.whl',
        
        # Compressed files
        '*.zip', '*.tar.gz', '*.tgz', '*.rar', '*.7z',
        
        # Logs
        '*.log', '*.log.*', '*.access', '*.error',
        
        # Cache
        '*.cache', '.eslintcache', '.sass-cache',
        
        # Lock files
        'package-lock.json', 'yarn.lock', 'Gemfile.lock',
        'poetry.lock', 'Pipfile.lock',
        
        # Environment and secrets
        '.env*', '*.pem', '*.key', '*.cert',
        
        # Database
        '*.sqlite', '*.db', '*.rdb',
        
        # Media files
        '*.jpg', '*.jpeg', '*.png', '*.gif', '*.ico',
        '*.pdf', '*.mov', '*.mp4', '*.mp3', '*.flv',
        '*.swf', '*.avi', '*.wmv', '*.woff', '*.woff2',
        '*.eot', '*.ttf', '*.otf',
        
        # Temporary files
        '*~', '*.bak', '*.swp', '*.swo', '*.tmp',
        
        # OS specific
        '.DS_Store', 'Thumbs.db',
        
        # IDE specific
        '.project', '.classpath', '*.iml', '*.ipr', '*.iws'
    }

    def __init__(self, 
                 excluded_dirs: Set[str] = None, 
                 excluded_files: Set[str] = None,
                 supported_extensions: Set[str] = None):
        """
        Initialize FileProcessor with optional custom exclusion patterns.
        
        Args:
            excluded_dirs: Set of directory patterns to exclude
            excluded_files: Set of file patterns to exclude
            supported_extensions: Set of file extensions to process
        """
        self.excluded_dirs = excluded_dirs if excluded_dirs is not None else self.DEFAULT_EXCLUDED_DIRS
        self.excluded_files = excluded_files if excluded_files is not None else self.DEFAULT_EXCLUDED_FILES
        self.supported_extensions = supported_extensions if supported_extensions is not None else self.SUPPORTED_EXTENSIONS

    def should_exclude_path(self, path: str) -> bool:
        """Check if a path should be excluded based on exclusion patterns."""
        path_parts = path.split(os.sep)
        
        # Check if any part of the path matches excluded directories
        for part in path_parts:
            if part in self.excluded_dirs:
                return True
        
        # Check if the file matches any excluded patterns
        for pattern in self.excluded_files:
            if pattern.startswith('*.'):
                if path.endswith(pattern[1:]):  # Handle extension patterns
                    return True
            elif pattern in path:  # Handle exact matches
                return True
                
        return False

    def is_text_file(self, file_path: str) -> bool:
        """Check if a file is a text file using python-magic."""
        try:
            if self.should_exclude_path(file_path):
                return False
                
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(file_path)
            return file_type.startswith('text/') or any(file_path.endswith(ext) for ext in self.supported_extensions)
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

    def process_directory(self, directory_path: str) -> List[Dict[str, str]]:
        """
        Process all text files in a directory recursively.
        Returns a list of dictionaries containing file paths and their contents.
        """
        documents = []
        
        for root, dirs, files in os.walk(directory_path):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if not self.should_exclude_path(os.path.join(root, d))]
            
            for file in files:
                file_path = os.path.join(root, file)
                if self.is_text_file(file_path):
                    content = self.read_file_content(file_path)
                    if content:
                        relative_path = os.path.relpath(file_path, directory_path)
                        documents.append({
                            "path": relative_path,
                            "content": content
                        })
        
        return documents
