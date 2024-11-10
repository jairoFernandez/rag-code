import argparse
import sys
import json
from project_manager import ProjectManager

def main():
    parser = argparse.ArgumentParser(description='Local Repository RAG System')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Create project command
    create_parser = subparsers.add_parser('create', help='Create a new project')
    create_parser.add_argument('name', help='Project name')
    create_parser.add_argument('path', help='Path to local repository')

    # Update project command
    update_parser = subparsers.add_parser('update', help='Update an existing project')
    update_parser.add_argument('name', help='Project name')

    # Delete project command
    delete_parser = subparsers.add_parser('delete', help='Delete a project')
    delete_parser.add_argument('name', help='Project name')

    # List projects command
    subparsers.add_parser('list', help='List all projects')

    # Search project command
    search_parser = subparsers.add_parser('search', help='Search in a project')
    search_parser.add_argument('name', help='Project name')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('-k', type=int, default=5, help='Number of results to return')

    # Ask question command
    ask_parser = subparsers.add_parser('ask', help='Ask a question about the code')
    ask_parser.add_argument('name', help='Project name')
    ask_parser.add_argument('question', help='Question about the code')
    ask_parser.add_argument('-k', type=int, default=3, help='Number of context documents to use')
    ask_parser.add_argument('--provider', default='ollama', help='LLM provider to use (default: ollama)')
    ask_parser.add_argument('--model', help='Model name for the provider (default depends on provider)')
    ask_parser.add_argument('--config', type=json.loads, help='Additional provider configuration as JSON')

    args = parser.parse_args()

    # Configure LLM if using ask command
    llm_config = None
    if args.command == 'ask':
        llm_config = {
            "provider": args.provider,
            "config": {
                "model_name": args.model
            } if args.model else {}
        }
        # Add any additional config if provided
        if args.config:
            llm_config["config"].update(args.config)

    # Initialize project manager
    project_manager = ProjectManager(llm_config=llm_config)

    if args.command == 'create':
        success = project_manager.create_project(args.name, args.path)
        sys.exit(0 if success else 1)

    elif args.command == 'update':
        success = project_manager.update_project(args.name)
        sys.exit(0 if success else 1)

    elif args.command == 'delete':
        success = project_manager.delete_project(args.name)
        sys.exit(0 if success else 1)

    elif args.command == 'list':
        projects = project_manager.list_projects()
        if not projects:
            print("No projects found.")
        else:
            print("\nProjects:")
            print("-" * 50)
            for name, metadata in projects:
                print(f"\nProject: {name}")
                print(f"Repository: {metadata['repository_path']}")
                print(f"Created: {metadata['created_at']}")
                print(f"Last Updated: {metadata['last_updated']}")
                print(f"Documents: {metadata['document_count']}")
                print("-" * 50)

    elif args.command == 'search':
        results = project_manager.search_project(args.name, args.query, args.k)
        if results:
            print(f"\nSearch results for '{args.query}' in project '{args.name}':")
            print("-" * 50)
            for i, result in enumerate(results, 1):
                print(f"\n{i}. File: {result['source']}")
                print("Content:")
                print(result['content'])
                print("-" * 50)
        else:
            print("No results found.")

    elif args.command == 'ask':
        result = project_manager.ask_question(args.name, args.question, args.k)
        if result["answer"]:
            print("\nAnswer:")
            print("-" * 50)
            print(result["answer"])
            print("\nSources used:")
            print("-" * 50)
            for source in result["sources"]:
                print(f"\nFile: {source['file']}")
                print("Relevant content:")
                print(source['content'])
                print("-" * 50)
        else:
            print("Could not generate an answer.")

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
