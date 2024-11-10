from typing import Dict, Any, Optional
from .base_provider import BaseLLMProvider
from .ollama_provider import OllamaProvider

class LLMProviderFactory:
    """Factory class for creating LLM providers."""
    
    @staticmethod
    def create_provider(provider_type: str, config: Optional[Dict[str, Any]] = None) -> BaseLLMProvider:
        """
        Create an LLM provider instance.
        
        Args:
            provider_type (str): Type of provider ('ollama', 'openai', etc.)
            config (Optional[Dict[str, Any]]): Provider configuration
            
        Returns:
            BaseLLMProvider: An instance of the requested provider
            
        Raises:
            ValueError: If provider_type is not supported
        """
        config = config or {}
        
        if provider_type.lower() == 'ollama':
            model_name = config.get('model_name', 'llama2')
            base_url = config.get('base_url', 'http://localhost:11434')
            return OllamaProvider(model_name=model_name, base_url=base_url)
            
        # Example of how to add OpenAI support:
        # elif provider_type.lower() == 'openai':
        #     api_key = config.get('api_key')
        #     model_name = config.get('model_name', 'gpt-3.5-turbo')
        #     return OpenAIProvider(api_key=api_key, model_name=model_name)
            
        raise ValueError(f"Unsupported provider type: {provider_type}")