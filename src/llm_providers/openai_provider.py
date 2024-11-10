from typing import Dict, Any, Generator
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
        """
        Ask a question and get the complete response as a string.
        Compatible with base provider interface.
        """
        try:
            prompt_text = self.prompt.format(context=context, question=question)
            messages = [{"role": "system", "content": prompt_text}]
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error getting response from OpenAI: {str(e)}"
    
    def ask_question_stream(self, question: str, context: str) -> Generator[str, None, None]:
        """
        Ask a question and get the response as a stream of tokens.
        Uses generator to yield each token as it arrives.
        """
        try:
            prompt_text = self.prompt.format(context=context, question=question)
            messages = [{"role": "system", "content": prompt_text}]
            
            stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"Error getting response from OpenAI: {str(e)}"
    
    def get_config(self) -> Dict[str, Any]:
        return {
            "provider": "openai",
            "api_key": self.client.api_key,
            "model_name": self.model_name
        }
