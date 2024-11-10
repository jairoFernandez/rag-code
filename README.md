# Local Repository RAG System

This application allows you to create projects that read local repositories (folders), vectorize their content using LangChain, and store the vectors in a local FAISS database for efficient similarity search.

## Features

- Create projects from local repositories
- Process and vectorize text files from repositories
- Store vectors locally using FAISS
- Search through repository content using semantic similarity
- Update existing projects
- List all projects and their metadata
- Delete projects

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The application provides a command-line interface with the following commands:

### Create a New Project
```bash
python src/main.py create <project-name> <repository-path>
```

### Update an Existing Project
```bash
python src/main.py update <project-name>
```

### Delete a Project
```bash
python src/main.py delete <project-name>
```

### List All Projects
```bash
python src/main.py list
```

### Search in a Project
```bash
python src/main.py search <project-name> "your search query" [-k number_of_results]
```
The `-k` parameter is optional and defaults to 5 results.

## Supported File Types

The application processes various text-based files including:
- Python (.py)
- JavaScript (.js)
- Java (.java)
- C++ (.cpp, .h, .hpp)
- Markdown (.md)
- Text (.txt)
- JSON (.json)
- YAML (.yml, .yaml)
- XML (.xml)
- HTML (.html)
- CSS (.css)
- SQL (.sql)
- Shell scripts (.sh, .bash)
- Configuration files (.gitignore, .env)
- Documentation files (README, LICENSE)

## Project Structure

```
.
├── src/
│   ├── main.py                 # CLI interface
│   ├── project_manager.py      # Main project management logic
│   ├── utils/
│   │   └── file_processor.py   # File processing utilities
│   └── vector_store/
│       └── vector_store_manager.py  # Vector store management
├── projects/                   # Project metadata storage
├── vector_stores/             # FAISS vector stores
└── requirements.txt           # Python dependencies
```

## Example Usage

1. Create a new project:
```bash
python src/main.py create my-project /path/to/local/repository
```

2. Search in the project:
```bash
python src/main.py search my-project "How does the authentication system work?"
```

3. Update the project after repository changes:
```bash
python src/main.py update my-project
```

4. List all projects:
```bash
python src/main.py list
```

5. Delete a project:
```bash
python src/main.py delete my-project
```

## Notes

- The application creates two main directories:
  - `projects/`: Stores project metadata
  - `vector_stores/`: Stores FAISS vector databases
- Each project maintains its own separate vector store
- Text files are automatically split into chunks for better search results
- The application uses the `all-MiniLM-L6-v2` model from sentence-transformers for generating embeddings
