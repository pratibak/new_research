import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from exa_py import Exa
from config import config
from models import SearchResult

class ExaClient:
    """Client for performing searches using Exa API"""
    
    def __init__(self):
        """Initialize Exa client with API key"""
        if not config.exa_api_key:
            raise ValueError("Exa API key is required")
        
        self.exa = Exa(config.exa_api_key)
    
    async def search_single_query(self, query: str) -> List[SearchResult]:
        """Search for a single query and return results"""
        try:
            # Run the synchronous Exa call in a thread pool
            loop = asyncio.get_event_loop()
            search_response = await loop.run_in_executor(
                None,
                lambda: self.exa.search_and_contents(
                    query,
                    type="auto",
                    num_results=config.max_urls_per_query,
                    text=True,
                    highlights=True,
                    include_domains=None,
                    exclude_domains=["reddit.com", "twitter.com", "facebook.com"],  # Filter out social media
                    start_crawl_date="2020-01-01",  # Only recent content
                    end_crawl_date=None,
                    start_published_date="2020-01-01",
                    end_published_date=None,
                    use_autoprompt=True,
                    summary=True
                )
            )
            
            results = []
            for result in search_response.results:
                search_result = SearchResult(
                    url=result.url,
                    title=result.title or "No title",
                    content=result.text or result.highlights or "No content available",
                    published_date=result.published_date,
                    score=result.score
                )
                results.append(search_result)
            
            return results
            
        except Exception as e:
            print(f"Error searching for query '{query}': {e}")
            return []
    
    async def search_multiple_queries(self, queries: List[str]) -> Dict[str, List[SearchResult]]:
        """Search multiple queries in parallel"""
        if not queries:
            return {}
        
        print(f"Searching {len(queries)} queries in parallel...")
        
        # Create tasks for parallel execution
        tasks = []
        for query in queries:
            task = self.search_single_query(query)
            tasks.append(task)
        
        # Execute all searches in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        search_results = {}
        for i, result in enumerate(results):
            query = queries[i]
            if isinstance(result, Exception):
                print(f"Exception searching query '{query}': {result}")
                search_results[query] = []
            else:
                search_results[query] = result
                print(f"Found {len(result)} results for query: '{query}'")
        
        return search_results
    
    def get_total_results_count(self, search_results: Dict[str, List[SearchResult]]) -> int:
        """Get total number of search results across all queries"""
        total = 0
        for results in search_results.values():
            total += len(results)
        return total
    
    def flatten_search_results(self, search_results: Dict[str, List[SearchResult]]) -> List[tuple]:
        """Flatten search results into list of tuples for processing"""
        flattened = []
        for query, results in search_results.items():
            for result in results:
                flattened.append((query, result.url, result.content))
        return flattened
    
    async def validate_urls(self, urls: List[str]) -> List[str]:
        """Validate that URLs are accessible (optional enhancement)"""
        valid_urls = []
        
        async def check_url(session: aiohttp.ClientSession, url: str) -> Optional[str]:
            try:
                async with session.head(url, timeout=5) as response:
                    if 200 <= response.status < 400:
                        return url
            except:
                pass
            return None
        
        async with aiohttp.ClientSession() as session:
            tasks = [check_url(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, str):
                    valid_urls.append(result)
        
        return valid_urls