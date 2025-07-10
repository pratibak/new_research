import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

load_dotenv()

class Config(BaseModel):
    # API Keys
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    exa_api_key: str = os.getenv("EXA_API_KEY", "")
    
    # Research Parameters
    max_urls_per_query: int = int(os.getenv("MAX_URLS_PER_QUERY", "20"))
    min_relevance_score: int = int(os.getenv("MIN_RELEVANCE_SCORE", "6"))
    max_research_iterations: int = int(os.getenv("MAX_RESEARCH_ITERATIONS", "3"))
    content_snippet_length: int = int(os.getenv("CONTENT_SNIPPET_LENGTH", "2000"))
    
    # Gemini Model Configuration
    gemini_model: str = "gemini-1.5-flash"
    temperature: float = 0.7
    max_tokens: int = 8192
    
    def validate_keys(self) -> bool:
        """Validate that required API keys are present"""
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY is required")
        if not self.exa_api_key:
            raise ValueError("EXA_API_KEY is required")
        return True

# Global config instance
config = Config()