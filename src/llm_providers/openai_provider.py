from typing import Dict, Any
import openai
from langchain.prompts import PromptTemplate
from .base_provider import BaseLLMProvider

class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model_name: str = "gpt-4-turbo"):
        self.model_name = model_name
        self.client = openai.OpenAI(api_key=api_key)
        
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
        try:
            prompt_text = self.prompt.format(context=context, question=question)
            messages = [{"role": "system", "content": prompt_text}]
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error getting response from OpenAI: {str(e)}"
    
    def get_config(self) -> Dict[str, Any]:
        return {
            "provider": "openai",
            "api_key": self.client.api_key,
            "model_name": self.model_name
        }
