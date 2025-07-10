#!/usr/bin/env python3
"""
Deep Research Workflow - Main Application
=========================================

A comprehensive research workflow that uses Gemini AI and Exa search
to perform multi-iteration research with parallel processing.

Usage:
    python main.py "your research query here"
    python main.py --interactive
"""

import asyncio
import argparse
import sys
import os
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from config import config
from research_workflow import DeepResearchWorkflow
from models import FinalResearchReport

console = Console()

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🔬 DEEP RESEARCH WORKFLOW                  ║
    ║                                                              ║
    ║  Powered by Gemini AI & Exa Search                          ║
    ║  Multi-iteration research with parallel processing           ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="cyan bold")

def check_environment():
    """Check if required environment variables are set"""
    missing_vars = []
    
    if not config.google_api_key:
        missing_vars.append("GOOGLE_API_KEY")
    
    if not config.exa_api_key:
        missing_vars.append("EXA_API_KEY")
    
    if missing_vars:
        console.print("\n❌ Missing required environment variables:", style="red bold")
        for var in missing_vars:
            console.print(f"   • {var}", style="red")
        
        console.print("\n📝 Please set these variables in your .env file or environment.", style="yellow")
        console.print("   Example .env file:", style="yellow")
        console.print("   GOOGLE_API_KEY=your_google_api_key", style="dim")
        console.print("   EXA_API_KEY=your_exa_api_key", style="dim")
        
        return False
    
    return True

def print_research_summary(report: FinalResearchReport):
    """Print a formatted research summary"""
    console.print("\n" + "="*80, style="green")
    console.print("🎯 RESEARCH SUMMARY", style="green bold", justify="center")
    console.print("="*80, style="green")
    
    # Basic info
    console.print(f"\n📋 Query: {report.original_query}", style="cyan bold")
    console.print(f"📊 Iterations: {len(report.iterations)}")
    console.print(f"📚 Total Sources: {report.total_sources}")
    console.print(f"🎯 Confidence Score: {report.confidence_score}/10")
    
    # Executive summary
    if report.final_synthesis.get('executive_summary'):
        console.print(Panel(
            report.final_synthesis['executive_summary'],
            title="📄 Executive Summary",
            border_style="blue"
        ))
    
    # Key findings
    if report.final_synthesis.get('key_findings'):
        console.print("\n🔍 Key Findings:", style="bold")
        for i, finding in enumerate(report.final_synthesis['key_findings'], 1):
            theme = finding.get('theme', 'General')
            finding_text = finding.get('finding', '')
            console.print(f"   {i}. [bold]{theme}[/bold]: {finding_text}")
    
    # Information gaps
    if report.final_synthesis.get('information_gaps'):
        console.print("\n⚠️  Information Gaps:", style="yellow bold")
        for gap in report.final_synthesis['information_gaps']:
            console.print(f"   • {gap}", style="yellow")

async def interactive_mode():
    """Run in interactive mode for multiple queries"""
    console.print("\n🚀 Starting Interactive Research Mode", style="green bold")
    console.print("Type 'quit' or 'exit' to stop\n")
    
    workflow = DeepResearchWorkflow()
    
    while True:
        try:
            query = Prompt.ask("\n🔍 Enter your research query", default="")
            
            if query.lower() in ['quit', 'exit', 'q']:
                console.print("👋 Goodbye!", style="cyan")
                break
            
            if not query.strip():
                console.print("❌ Please enter a valid query", style="red")
                continue
            
            # Run research
            report = await workflow.research(query)
            
            # Print summary
            print_research_summary(report)
            
            # Save report
            filename = workflow.save_report(report)
            console.print(f"📁 Full report saved: {filename}", style="green")
            
            # Ask if user wants to continue
            continue_research = Prompt.ask(
                "\n❓ Research another topic?", 
                choices=["y", "n"], 
                default="y"
            )
            
            if continue_research.lower() == 'n':
                console.print("👋 Research session complete!", style="cyan")
                break
                
        except KeyboardInterrupt:
            console.print("\n\n⏹️  Research interrupted by user", style="yellow")
            break
        except Exception as e:
            console.print(f"\n❌ Error: {str(e)}", style="red")
            console.print("Please try again or check your configuration.", style="yellow")

async def single_query_mode(query: str):
    """Run research for a single query"""
    console.print(f"\n🚀 Starting Research for: '{query}'", style="green bold")
    
    try:
        workflow = DeepResearchWorkflow()
        report = await workflow.research(query)
        
        # Print summary
        print_research_summary(report)
        
        # Save report
        filename = workflow.save_report(report)
        console.print(f"\n📁 Full report saved: {filename}", style="green bold")
        
    except Exception as e:
        console.print(f"\n❌ Research failed: {str(e)}", style="red bold")
        console.print("Please check your API keys and network connection.", style="yellow")
        sys.exit(1)

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description="Deep Research Workflow - AI-powered research with parallel processing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py "impact of artificial intelligence on healthcare"
  python main.py --interactive
  python main.py "climate change solutions 2024" --save-to custom_report.json
        """
    )
    
    parser.add_argument(
        "query",
        nargs="?",
        help="Research query to investigate"
    )
    
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive mode for multiple queries"
    )
    
    parser.add_argument(
        "--save-to",
        help="Custom filename for saving the research report"
    )
    
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=config.max_research_iterations,
        help=f"Maximum research iterations (default: {config.max_research_iterations})"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Update config with command line args
    config.max_research_iterations = args.max_iterations
    
    # Determine mode
    if args.interactive:
        asyncio.run(interactive_mode())
    elif args.query:
        asyncio.run(single_query_mode(args.query))
    else:
        console.print("❌ Please provide a query or use --interactive mode", style="red")
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()