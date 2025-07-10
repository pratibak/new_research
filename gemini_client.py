import json
import asyncio
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from config import config

class GeminiClient:
    """Client for interacting with Gemini AI model"""
    
    def __init__(self):
        """Initialize Gemini client with API key"""
        if not config.google_api_key:
            raise ValueError("Google API key is required")
        
        genai.configure(api_key=config.google_api_key)
        self.model = genai.GenerativeModel(config.gemini_model)
        
        # Load prompts
        self.prompts = self._load_prompts()
    
    def _load_prompts(self) -> Dict[str, str]:
        """Load all prompt templates from files"""
        prompts = {}
        prompt_files = {
            'query_generation': 'prompts/query_generation.txt',
            'summarizer': 'prompts/summarizer.txt', 
            'synthesis': 'prompts/synthesis.txt'
        }
        
        for name, filepath in prompt_files.items():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    prompts[name] = f.read().strip()
            except FileNotFoundError:
                print(f"Warning: Prompt file {filepath} not found")
                prompts[name] = ""
        
        return prompts
    
    async def generate_queries(self, original_query: str) -> List[str]:
        """Generate 3 augmented research queries from original query"""
        prompt = self.prompts['query_generation'].format(original_query=original_query)
        
        try:
            response = await self._call_model(prompt)
            result = json.loads(response)
            return result.get('queries', [])
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing query generation response: {e}")
            # Fallback: return variations of original query
            return [
                original_query,
                f"comprehensive analysis of {original_query}",
                f"latest research on {original_query}"
            ]
    
    async def summarize_content(self, original_query: str, search_query: str, 
                               url: str, content: str) -> Optional[Dict[str, Any]]:
        """Summarize and evaluate content relevance"""
        # Truncate content if too long
        truncated_content = content[:config.content_snippet_length]
        
        prompt = self.prompts['summarizer'].format(
            original_query=original_query,
            search_query=search_query,
            url=url,
            content=truncated_content
        )
        
        try:
            response = await self._call_model(prompt)
            result = json.loads(response)
            return result
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing summarizer response for {url}: {e}")
            return None
    
    async def synthesize_research(self, original_query: str, 
                                 summaries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create comprehensive synthesis from all summaries"""
        summaries_json = json.dumps(summaries, indent=2)
        prompt = self.prompts['synthesis'].format(
            original_query=original_query,
            summaries=summaries_json
        )
        
        try:
            response = await self._call_model(prompt)
            result = json.loads(response)
            return result
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing synthesis response: {e}")
            return {
                "executive_summary": "Error in synthesis",
                "key_findings": [],
                "perspectives": [],
                "implications": "Unable to synthesize due to parsing error",
                "information_gaps": ["Synthesis failed"],
                "confidence_score": 1,
                "needs_more_research": True
            }
    
    async def _call_model(self, prompt: str) -> str:
        """Make async call to Gemini model"""
        try:
            # Run the synchronous call in a thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=config.temperature,
                        max_output_tokens=config.max_tokens,
                    )
                )
            )
            return response.text
        except Exception as e:
            print(f"Error calling Gemini model: {e}")
            raise
    
    async def batch_summarize(self, original_query: str, search_results: List[tuple]) -> List[Dict[str, Any]]:
        """Process multiple content summaries in parallel"""
        tasks = []
        for search_query, url, content in search_results:
            task = self.summarize_content(original_query, search_query, url, content)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out None results and exceptions
        valid_results = []
        for result in results:
            if isinstance(result, dict) and result is not None:
                valid_results.append(result)
            elif isinstance(result, Exception):
                print(f"Exception in batch summarize: {result}")
        
        return valid_results