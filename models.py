from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json

@dataclass
class SearchResult:
    """Represents a single search result from Exa"""
    url: str
    title: str
    content: str
    published_date: Optional[str] = None
    score: Optional[float] = None

@dataclass 
class SummaryResult:
    """Represents a summarized and evaluated piece of content"""
    url: str
    relevance_score: int
    is_relevant: bool
    summary: str
    key_insights: List[str]
    search_query: str

@dataclass
class ResearchIteration:
    """Represents one complete research iteration"""
    iteration_number: int
    queries: List[str]
    search_results: List[SearchResult]
    summaries: List[SummaryResult]
    synthesis_result: Dict[str, Any]

@dataclass
class FinalResearchReport:
    """Complete research report with all iterations"""
    original_query: str
    iterations: List[ResearchIteration]
    final_synthesis: Dict[str, Any]
    total_sources: int
    confidence_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "original_query": self.original_query,
            "iterations": [
                {
                    "iteration_number": iter.iteration_number,
                    "queries": iter.queries,
                    "search_results": [
                        {
                            "url": sr.url,
                            "title": sr.title,
                            "content": sr.content[:500] + "..." if len(sr.content) > 500 else sr.content,
                            "published_date": sr.published_date,
                            "score": sr.score
                        } for sr in iter.search_results
                    ],
                    "summaries": [
                        {
                            "url": sum.url,
                            "relevance_score": sum.relevance_score,
                            "is_relevant": sum.is_relevant,
                            "summary": sum.summary,
                            "key_insights": sum.key_insights,
                            "search_query": sum.search_query
                        } for sum in iter.summaries
                    ],
                    "synthesis_result": iter.synthesis_result
                } for iter in self.iterations
            ],
            "final_synthesis": self.final_synthesis,
            "total_sources": self.total_sources,
            "confidence_score": self.confidence_score
        }