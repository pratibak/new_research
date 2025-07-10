import asyncio
import json
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

from config import config
from models import SearchResult, SummaryResult, ResearchIteration, FinalResearchReport
from gemini_client import GeminiClient
from exa_client import ExaClient

class DeepResearchWorkflow:
    """Main orchestrator for the deep research workflow"""
    
    def __init__(self):
        """Initialize the workflow with clients"""
        self.gemini_client = GeminiClient()
        self.exa_client = ExaClient()
        self.iterations: List[ResearchIteration] = []
    
    async def research(self, original_query: str) -> FinalResearchReport:
        """Execute the complete research workflow"""
        print(f"\n🔍 Starting Deep Research for: '{original_query}'")
        print("=" * 80)
        
        start_time = time.time()
        iteration_count = 0
        
        while iteration_count < config.max_research_iterations:
            iteration_count += 1
            print(f"\n📊 Research Iteration {iteration_count}")
            print("-" * 40)
            
            # Execute single research iteration
            iteration_result = await self._execute_iteration(
                original_query, iteration_count
            )
            
            self.iterations.append(iteration_result)
            
            # Check if we need more research
            needs_more = iteration_result.synthesis_result.get('needs_more_research', False)
            confidence = iteration_result.synthesis_result.get('confidence_score', 0)
            
            print(f"📈 Iteration {iteration_count} Complete:")
            print(f"   Confidence Score: {confidence}/10")
            print(f"   Needs More Research: {needs_more}")
            
            # Stop if confidence is high enough and no more research needed
            if confidence >= 7 and not needs_more:
                print("✅ Research complete - sufficient confidence achieved!")
                break
            
            if iteration_count >= config.max_research_iterations:
                print("⏰ Maximum iterations reached - stopping research")
                break
        
        # Create final synthesis
        print(f"\n🔬 Creating Final Synthesis...")
        final_synthesis = await self._create_final_synthesis(original_query)
        
        # Calculate total sources
        total_sources = sum(len(iter.search_results) for iter in self.iterations)
        
        # Create final report
        final_report = FinalResearchReport(
            original_query=original_query,
            iterations=self.iterations,
            final_synthesis=final_synthesis,
            total_sources=total_sources,
            confidence_score=final_synthesis.get('confidence_score', 0)
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n🎉 Research Complete!")
        print(f"   Total Duration: {duration:.2f} seconds")
        print(f"   Iterations: {iteration_count}")
        print(f"   Total Sources: {total_sources}")
        print(f"   Final Confidence: {final_report.confidence_score}/10")
        print("=" * 80)
        
        return final_report
    
    async def _execute_iteration(self, original_query: str, iteration_number: int) -> ResearchIteration:
        """Execute a single research iteration"""
        
        # Step 1: Generate augmented queries
        print("🤖 Generating research queries...")
        queries = await self.gemini_client.generate_queries(original_query)
        print(f"   Generated {len(queries)} queries")
        for i, query in enumerate(queries, 1):
            print(f"   {i}. {query}")
        
        # Step 2: Perform parallel searches
        print("\n🔍 Performing parallel searches...")
        search_results_dict = await self.exa_client.search_multiple_queries(queries)
        
        # Flatten search results
        all_search_results = []
        for query, results in search_results_dict.items():
            all_search_results.extend(results)
        
        print(f"   Found {len(all_search_results)} total results")
        
        # Step 3: Parallel content summarization
        print("\n📝 Analyzing and summarizing content...")
        flattened_results = self.exa_client.flatten_search_results(search_results_dict)
        
        # Batch process summaries in parallel
        summary_responses = await self.gemini_client.batch_summarize(
            original_query, flattened_results
        )
        
        # Convert to SummaryResult objects
        summaries = []
        for response in summary_responses:
            if response and response.get('is_relevant', False):
                summary = SummaryResult(
                    url=response.get('url', ''),
                    relevance_score=response.get('relevance_score', 0),
                    is_relevant=response.get('is_relevant', False),
                    summary=response.get('summary', ''),
                    key_insights=response.get('key_insights', []),
                    search_query=''  # Will be filled later if needed
                )
                summaries.append(summary)
        
        print(f"   Generated {len(summaries)} relevant summaries")
        
        # Step 4: Synthesize iteration results
        print("\n🧠 Synthesizing iteration results...")
        synthesis_result = await self.gemini_client.synthesize_research(
            original_query, summary_responses
        )
        
        return ResearchIteration(
            iteration_number=iteration_number,
            queries=queries,
            search_results=all_search_results,
            summaries=summaries,
            synthesis_result=synthesis_result
        )
    
    async def _create_final_synthesis(self, original_query: str) -> Dict[str, Any]:
        """Create comprehensive final synthesis from all iterations"""
        
        # Combine all summaries from all iterations
        all_summaries = []
        for iteration in self.iterations:
            for summary in iteration.summaries:
                all_summaries.append({
                    'url': summary.url,
                    'relevance_score': summary.relevance_score,
                    'summary': summary.summary,
                    'key_insights': summary.key_insights,
                    'iteration': iteration.iteration_number
                })
        
        # Create final synthesis
        final_synthesis = await self.gemini_client.synthesize_research(
            original_query, all_summaries
        )
        
        # Add metadata
        final_synthesis['total_iterations'] = len(self.iterations)
        final_synthesis['total_sources'] = len(all_summaries)
        final_synthesis['research_timestamp'] = datetime.now().isoformat()
        
        return final_synthesis
    
    def save_report(self, report: FinalResearchReport, filename: Optional[str] = None) -> str:
        """Save research report to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_query = "".join(c for c in report.original_query if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_query = safe_query.replace(' ', '_')[:50]  # Limit length
            filename = f"research_report_{safe_query}_{timestamp}.json"
        
        report_data = report.to_dict()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Report saved to: {filename}")
        return filename

# Convenience function for easy usage
async def run_research(query: str) -> FinalResearchReport:
    """Run complete research workflow for a given query"""
    workflow = DeepResearchWorkflow()
    return await workflow.research(query)