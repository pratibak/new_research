#!/usr/bin/env python3
"""
Test Script for Deep Research Workflow
======================================

This script tests the setup and API connections without running a full research workflow.
"""

import asyncio
import sys
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from config import config
        print("✅ config module imported")
        
        from models import SearchResult, SummaryResult, ResearchIteration, FinalResearchReport
        print("✅ models module imported")
        
        from gemini_client import GeminiClient
        print("✅ gemini_client module imported")
        
        from exa_client import ExaClient  
        print("✅ exa_client module imported")
        
        from research_workflow import DeepResearchWorkflow
        print("✅ research_workflow module imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all dependencies are installed: pip install -r requirements.txt")
        return False

def test_config():
    """Test configuration and API keys"""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import config
        
        # Check API keys
        if not config.google_api_key:
            print("❌ Google API key not found")
            print("   Set GOOGLE_API_KEY in your .env file")
            return False
        else:
            print("✅ Google API key found")
        
        if not config.exa_api_key:
            print("❌ Exa API key not found") 
            print("   Set EXA_API_KEY in your .env file")
            return False
        else:
            print("✅ Exa API key found")
        
        # Check configuration values
        print(f"   Max URLs per query: {config.max_urls_per_query}")
        print(f"   Max iterations: {config.max_research_iterations}")
        print(f"   Min relevance score: {config.min_relevance_score}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_prompts():
    """Test if all prompt files exist and are readable"""
    print("\n📝 Testing prompt files...")
    
    prompt_files = [
        "prompts/query_generation.txt",
        "prompts/summarizer.txt", 
        "prompts/synthesis.txt"
    ]
    
    all_good = True
    for prompt_file in prompt_files:
        if Path(prompt_file).exists():
            try:
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        print(f"✅ {prompt_file} exists and has content")
                    else:
                        print(f"⚠️  {prompt_file} is empty")
                        all_good = False
            except Exception as e:
                print(f"❌ Error reading {prompt_file}: {e}")
                all_good = False
        else:
            print(f"❌ {prompt_file} not found")
            all_good = False
    
    return all_good

async def test_gemini_connection():
    """Test connection to Gemini API"""
    print("\n🤖 Testing Gemini API connection...")
    
    try:
        from gemini_client import GeminiClient
        
        client = GeminiClient()
        
        # Test with a simple query generation
        test_query = "test research topic"
        queries = await client.generate_queries(test_query)
        
        if queries and len(queries) > 0:
            print("✅ Gemini API connection successful")
            print(f"   Generated {len(queries)} test queries")
            return True
        else:
            print("❌ Gemini API returned empty results")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API connection failed: {e}")
        print("   Check your GOOGLE_API_KEY and network connection")
        return False

async def test_exa_connection():
    """Test connection to Exa API"""
    print("\n🔍 Testing Exa API connection...")
    
    try:
        from exa_client import ExaClient
        
        client = ExaClient()
        
        # Test with a simple search
        test_results = await client.search_single_query("python programming")
        
        if test_results and len(test_results) > 0:
            print("✅ Exa API connection successful")
            print(f"   Found {len(test_results)} test results")
            return True
        else:
            print("❌ Exa API returned no results")
            return False
            
    except Exception as e:
        print(f"❌ Exa API connection failed: {e}")
        print("   Check your EXA_API_KEY and network connection")
        return False

async def run_mini_workflow():
    """Run a minimal version of the workflow as an end-to-end test"""
    print("\n🧪 Running mini workflow test...")
    
    try:
        from research_workflow import DeepResearchWorkflow
        
        # Create workflow with limited scope for testing
        workflow = DeepResearchWorkflow()
        
        # Test query generation
        print("   Testing query generation...")
        queries = await workflow.gemini_client.generate_queries("AI in healthcare")
        
        if not queries:
            print("❌ Query generation failed")
            return False
        
        print(f"   ✅ Generated {len(queries)} queries")
        
        # Test single search (limited)
        print("   Testing search functionality...")
        search_results = await workflow.exa_client.search_single_query(queries[0])
        
        if not search_results:
            print("❌ Search functionality failed") 
            return False
        
        print(f"   ✅ Found {len(search_results)} search results")
        
        print("✅ Mini workflow test successful")
        return True
        
    except Exception as e:
        print(f"❌ Mini workflow test failed: {e}")
        return False

def print_summary(results):
    """Print test summary"""
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("• Run: python main.py --help")
        print("• Try: python main.py \"your research query\"")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("• Verify your .env file has valid API keys")
        print("• Check your internet connection")
        print("• Ensure all dependencies are installed")

async def main():
    """Main test function"""
    print("🔬 Deep Research Workflow - Setup Test")
    print("="*60)
    
    results = {}
    
    # Run tests
    results["Import Test"] = test_imports()
    results["Configuration Test"] = test_config()
    results["Prompt Files Test"] = test_prompts()
    
    if results["Import Test"] and results["Configuration Test"]:
        results["Gemini API Test"] = await test_gemini_connection()
        results["Exa API Test"] = await test_exa_connection()
        
        if results["Gemini API Test"] and results["Exa API Test"]:
            results["Mini Workflow Test"] = await run_mini_workflow()
    
    # Print summary
    print_summary(results)
    
    # Exit with appropriate code
    if all(results.values()):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())