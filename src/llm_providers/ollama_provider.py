from typing import Dict, Any
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from .base_provider import BaseLLMProvider

class OllamaProvider(BaseLLMProvider):
    """Ollama LLM provider implementation."""
    def __init__(self, model_name: str = "llama3.2:3b", base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama provider.
        
        Args:
            model_name (str): Name of the Ollama model to use
            base_url (str): Base URL for Ollama API
        """
        self.model_name = model_name
        self.base_url = base_url
        self.llm = OllamaLLM(model=model_name, base_url=base_url, temperature=0)
        
        # Define a template that instructs the model to focus on code-related questions
        self.template = """You are a helpful coding assistant. Use the following context to answer the question. 
        If you cannot answer the question based on the context, say so.
        Context: {context}
        
        Question: {question}
        
        Answer: """
        
        self.prompt = PromptTemplate(
            template=self.template,
            input_variables=["context", "question"]
        )
        
    def ask_question(self, question: str, context: str) -> str:
        """
        Ask a question using the provided context.
        
        Args:
            question (str): The question to ask
            context (str): The context to use for answering the question
            
        Returns:
            str: The answer from the LLM
        """
        try:
            prompt_text = self.prompt.format(context=context, question=question)
            response = self.llm.invoke(prompt_text)
            return response.strip()
        except Exception as e:
            return f"Error getting response from Ollama: {str(e)}"
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get the configuration for the provider.
        
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        return {
            "provider": "ollama",
            "model_name": self.model_name,
            "base_url": self.base_url
        }
