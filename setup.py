#!/usr/bin/env python3
"""
Setup script for Deep Research Workflow
=======================================

This script helps users quickly set up the research environment.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    """Print setup header"""
    print("="*60)
    print("🔬 Deep Research Workflow Setup")
    print("="*60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    else:
        print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("   Try running: pip install -r requirements.txt")
        sys.exit(1)

def setup_environment():
    """Set up environment variables"""
    print("\n🔧 Setting up environment...")
    
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if not env_example.exists():
        print("❌ .env.example file not found")
        return False
    
    if env_file.exists():
        overwrite = input("📁 .env file exists. Overwrite? (y/N): ").lower()
        if overwrite != 'y':
            print("   Keeping existing .env file")
            return True
    
    # Copy example to .env
    with open(env_example, 'r') as src, open(env_file, 'w') as dst:
        dst.write(src.read())
    
    print("✅ Created .env file from template")
    print("   Please edit .env with your API keys")
    return True

def check_api_keys():
    """Guide user through API key setup"""
    print("\n🔑 API Keys Setup Guide")
    print("-" * 30)
    
    print("\n🤖 Google Gemini API Key:")
    print("   1. Visit: https://makersuite.google.com/app/apikey")
    print("   2. Create a new API key")
    print("   3. Add to .env: GOOGLE_API_KEY=your_key_here")
    
    print("\n🔍 Exa Search API Key:")
    print("   1. Visit: https://exa.ai")
    print("   2. Sign up and get API key")
    print("   3. Add to .env: EXA_API_KEY=your_key_here")
    
    print("\n💡 Remember to keep your API keys secure!")

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ["prompts"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Directories created")

def verify_setup():
    """Verify the setup is complete"""
    print("\n🔍 Verifying setup...")
    
    # Check required files
    required_files = [
        "main.py",
        "research_workflow.py", 
        "gemini_client.py",
        "exa_client.py",
        "config.py",
        "models.py",
        ".env",
        "prompts/query_generation.txt",
        "prompts/summarizer.txt",
        "prompts/synthesis.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing files:")
        for file in missing_files:
            print(f"   • {file}")
        return False
    
    print("✅ All required files present")
    return True

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup Complete!")
    print("-" * 20)
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Test the setup:")
    print("   python main.py --help")
    print("3. Run your first research:")
    print("   python main.py \"your research query\"")
    print("4. Or try interactive mode:")
    print("   python main.py --interactive")
    
    print("\n📚 For more information, see README.md")
    print("\n🆘 Need help? Check the troubleshooting section in README.md")

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Create directories
    create_directories()
    
    # Set up environment
    setup_environment()
    
    # Verify setup
    if verify_setup():
        # Guide for API keys
        check_api_keys()
        
        # Print next steps
        print_next_steps()
    else:
        print("\n❌ Setup incomplete. Please check missing files.")
        sys.exit(1)

if __name__ == "__main__":
    main()