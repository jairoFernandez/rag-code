# Local Repository RAG System

This application allows you to create projects that read local repositories (folders), vectorize their content using LangChain, and store the vectors in a local FAISS database for efficient similarity search and question answering.

## Features

- Create projects from local repositories
- Process and vectorize text files from repositories
- Store vectors locally using FAISS
- Search through repository content using semantic similarity
- Ask questions about your code using LLMs (Ollama by default, extensible to other providers)
- Smart file filtering (excludes common non-source files and directories)
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

4. Install Ollama (for local LLM support):
   - Follow the installation instructions at [Ollama's website](https://ollama.ai)
   - Pull the default model: `ollama pull llama2`

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

### Ask Questions About Code
```bash
python src/main.py ask <project-name> "your question" [-k number_of_context_docs] [--provider provider_name] [--model model_name] [--config additional_config]
```
Options:
- `-k`: Number of context documents to use (default: 3)
- `--provider`: LLM provider to use (default: ollama)
- `--model`: Model name for the provider (default depends on provider)
- `--config`: Additional provider configuration as JSON

Examples:
```bash
# Using default Ollama provider with llama2
python src/main.py ask my-project "How does the authentication system work?"

# Using a specific Ollama model
python src/main.py ask my-project "Explain the main function" --model codellama

# Using custom provider configuration
python src/main.py ask my-project "What does this code do?" --config '{"temperature": 0.7}'
```

## File Processing

### Supported File Types

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

### Excluded Directories

The system automatically excludes common directories that typically don't contain source code:

#### Version Control
- `.git`, `.svn`, `.hg`

#### Python
- `venv`, `env`, `.env`, `.venv`
- `__pycache__`, `.pytest_cache`, `.mypy_cache`
- `build`, `dist`, `*.egg-info`

#### Node.js
- `node_modules`, `bower_components`
- `.npm`, `.yarn`

#### Java
- `target`, `.gradle`, `build`, `out`

#### Ruby
- `.bundle`, `vendor/bundle`

#### PHP
- `vendor`

#### Scala/SBT
- `target`, `.metals`

#### .NET
- `bin`, `obj`, `packages`

#### IDEs and Editors
- `.idea`, `.vscode`, `.vs`
- `.eclipse`, `.settings`

#### Build and Dependencies
- `dist`, `build`, `out`, `deps`

#### Documentation
- `_build`, `site`, `docs/_build`

### Excluded Files

The system also excludes common non-source files:

#### Compiled Files
- `*.pyc`, `*.pyo`, `*.pyd`, `*.so`
- `*.dll`, `*.class`, `*.exe`

#### Package Files
- `*.jar`, `*.war`, `*.ear`
- `*.egg`, `*.whl`

#### Lock Files
- `package-lock.json`, `yarn.lock`
- `Gemfile.lock`, `poetry.lock`
- `Pipfile.lock`

#### Media and Binary Files
- Images: `*.jpg`, `*.png`, `*.gif`, etc.
- Fonts: `*.woff`, `*.ttf`, `*.eot`
- Videos: `*.mp4`, `*.avi`, `*.mov`
- Audio: `*.mp3`, `*.wav`

#### Other
- Logs: `*.log`
- Databases: `*.sqlite`, `*.db`
- Cache files: `*.cache`
- Temporary files: `*~`, `*.bak`
- Environment files: `.env*`
- Compressed files: `*.zip`, `*.tar.gz`

## Project Structure

```
.
├── src/
│   ├── main.py                 # CLI interface
│   ├── project_manager.py      # Main project management logic
│   ├── utils/
│   │   └── file_processor.py   # File processing utilities
│   ├── vector_store/
│   │   └── vector_store_manager.py  # Vector store management
│   └── llm_providers/         # LLM provider implementations
│       ├── __init__.py
│       ├── base_provider.py    # Abstract base class for providers
│       ├── ollama_provider.py  # Ollama implementation
│       └── provider_factory.py # Factory for creating providers
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

3. Ask a question about the code:
```bash
python src/main.py ask my-project "What is the purpose of the main function?"
```

4. Update the project after repository changes:
```bash
python src/main.py update my-project
```

5. List all projects:
```bash
python src/main.py list
```

6. Delete a project:
```bash
python src/main.py delete my-project
```

## LLM Providers

The system uses Ollama as the default LLM provider for answering questions about code. The provider system is extensible, allowing you to add support for other LLM providers like OpenAI. Each provider can be configured with specific models and parameters.

### Default Provider (Ollama)
- Uses the local Ollama service
- Default model: llama2
- Can be configured with different models (e.g., codellama)
- Supports custom base URL and other configurations

### Adding New Providers
The system is designed to be extensible. To add a new provider:
1. Create a new provider class implementing `BaseLLMProvider`
2. Add the provider to the `LLMProviderFactory`
3. Configure the provider using the `--provider` and `--config` options

## Notes

- The application creates two main directories:
  - `projects/`: Stores project metadata
  - `vector_stores/`: Stores FAISS vector databases
- Each project maintains its own separate vector store
- Text files are automatically split into chunks for better search results
- The application uses the `all-MiniLM-L6-v2` model from sentence-transformers for generating embeddings
- Questions are answered using a combination of:
  - Vector similarity search to find relevant code context
  - LLM processing to generate natural language answers
- The default Ollama provider requires the Ollama service to be running locally
- The system intelligently filters out non-source files and directories to focus on relevant code
