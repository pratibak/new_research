#!/usr/bin/env python3
"""
Demo Script for Deep Research Workflow
======================================

This script demonstrates the capabilities of the deep research workflow
with a sample research query.
"""

import asyncio
import json
from datetime import datetime
from research_workflow import DeepResearchWorkflow

async def run_demo():
    """Run demonstration research"""
    
    print("🔬 Deep Research Workflow - Demonstration")
    print("="*60)
    print()
    
    # Sample research queries to demonstrate
    demo_queries = [
        "impact of artificial intelligence on healthcare diagnostics",
        "renewable energy adoption trends in 2024",
        "quantum computing applications in cybersecurity",
        "sustainable urban planning solutions",
        "machine learning in financial fraud detection"
    ]
    
    print("Available demo research topics:")
    for i, query in enumerate(demo_queries, 1):
        print(f"  {i}. {query}")
    
    print("\nSelect a topic (1-5) or enter your own query:")
    
    try:
        user_input = input("Enter choice: ").strip()
        
        if user_input.isdigit() and 1 <= int(user_input) <= len(demo_queries):
            selected_query = demo_queries[int(user_input) - 1]
            print(f"\n🎯 Selected: {selected_query}")
        elif user_input:
            selected_query = user_input
            print(f"\n🎯 Custom query: {selected_query}")
        else:
            selected_query = demo_queries[0]  # Default to first option
            print(f"\n🎯 Using default: {selected_query}")
        
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Demo cancelled by user")
        return
    
    # Show what the demo will do
    print("\n📋 Demo Overview:")
    print("• Generate 3 research queries from your topic")
    print("• Search for relevant content using Exa")
    print("• Analyze and summarize findings with Gemini AI")
    print("• Create comprehensive research report")
    print("• Show iterative refinement process")
    
    confirm = input("\nContinue with demo? (Y/n): ").strip().lower()
    if confirm == 'n':
        print("👋 Demo cancelled")
        return
    
    print("\n🚀 Starting research workflow...")
    print("-" * 40)
    
    try:
        # Create and run workflow
        workflow = DeepResearchWorkflow()
        report = await workflow.research(selected_query)
        
        # Display results
        print_demo_results(report)
        
        # Save demo report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"demo_report_{timestamp}.json"
        workflow.save_report(report, filename)
        
        print(f"\n💾 Demo report saved as: {filename}")
        print("\n🎉 Demo completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("Please check your setup and API keys")

def print_demo_results(report):
    """Print formatted demo results"""
    print("\n" + "="*60)
    print("📊 DEMO RESULTS")
    print("="*60)
    
    print(f"\n📋 Research Query: {report.original_query}")
    print(f"🔄 Research Iterations: {len(report.iterations)}")
    print(f"📚 Total Sources Analyzed: {report.total_sources}")
    print(f"🎯 Final Confidence Score: {report.confidence_score}/10")
    
    # Show iteration summary
    print(f"\n📈 Iteration Summary:")
    for iteration in report.iterations:
        relevant_summaries = len([s for s in iteration.summaries if s.is_relevant])
        print(f"   Iteration {iteration.iteration_number}: {len(iteration.search_results)} sources → {relevant_summaries} relevant")
    
    # Show key findings
    if report.final_synthesis.get('key_findings'):
        print(f"\n🔍 Key Findings:")
        for i, finding in enumerate(report.final_synthesis['key_findings'][:3], 1):  # Show top 3
            theme = finding.get('theme', 'General')
            finding_text = finding.get('finding', '')[:200] + "..."
            print(f"   {i}. {theme}: {finding_text}")
    
    # Show executive summary
    if report.final_synthesis.get('executive_summary'):
        print(f"\n📄 Executive Summary:")
        summary = report.final_synthesis['executive_summary']
        print(f"   {summary}")
    
    # Show some sources
    print(f"\n📎 Sample Sources:")
    source_count = 0
    for iteration in report.iterations:
        for summary in iteration.summaries:
            if summary.is_relevant and source_count < 3:
                print(f"   • {summary.url}")
                source_count += 1
                if source_count >= 3:
                    break
        if source_count >= 3:
            break
    
    if report.total_sources > 3:
        print(f"   ... and {report.total_sources - 3} more sources")

def show_features():
    """Show key features of the workflow"""
    print("🌟 Key Features Demonstrated:")
    print("• Parallel Processing: All searches run simultaneously")
    print("• AI Query Expansion: Single query → multiple research angles")
    print("• Intelligent Filtering: Only relevant content is analyzed") 
    print("• Iterative Refinement: Continues until sufficient confidence")
    print("• Comprehensive Reports: Structured JSON output with all details")
    print("• Source Attribution: All findings linked to original sources")

async def main():
    """Main demo function"""
    show_features()
    print()
    await run_demo()

if __name__ == "__main__":
    asyncio.run(main())