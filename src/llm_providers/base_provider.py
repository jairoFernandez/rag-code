from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def ask_question(self, question: str, context: str) -> str:
        """
        Ask a question using the context provided.
        
        Args:
            question (str): The question to ask
            context (str): The context to use for answering the question
            
        Returns:
            str: The answer from the LLM
        """
        pass
    
    @abstractmethod
    def get_config(self) -> Dict[str, Any]:
        """
        Get the configuration for the provider.
        
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        pass
