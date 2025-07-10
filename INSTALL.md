# 🚀 Installation Guide

This guide helps you set up the Deep Research Workflow in different Python environments.

## 📋 Prerequisites

- Python 3.8 or higher
- Google API Key (for Gemini AI)
- Exa API Key (for search)
- Internet connection

## 🔧 Installation Methods

### Method 1: Virtual Environment (Recommended)

```bash
# Clone or download the project
cd deep-research-workflow

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys
```

### Method 2: Using pipx (Application Installation)

```bash
# Install pipx if not already installed
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install the workflow as an application
pipx install -e .
```

### Method 3: System-wide Installation (Advanced)

```bash
# For managed environments, use --break-system-packages flag
pip install -r requirements.txt --break-system-packages

# Or install individual packages
pip install google-generativeai exa-py python-dotenv pydantic rich aiohttp --break-system-packages
```

### Method 4: Conda Environment

```bash
# Create conda environment
conda create -n research-workflow python=3.11
conda activate research-workflow

# Install dependencies
pip install -r requirements.txt
```

## 🔑 API Keys Setup

### Google Gemini API
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

### Exa Search API  
1. Visit [Exa.ai](https://exa.ai)
2. Sign up for an account
3. Navigate to your dashboard
4. Copy your API key

### Environment Configuration
Edit your `.env` file:
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
EXA_API_KEY=your_exa_search_api_key_here

# Optional configuration
MAX_URLS_PER_QUERY=20
MIN_RELEVANCE_SCORE=6
MAX_RESEARCH_ITERATIONS=3
CONTENT_SNIPPET_LENGTH=2000
```

## ✅ Verify Installation

Run the test script to verify everything is working:

```bash
python test_setup.py
```

This will check:
- Python imports
- API key configuration
- Prompt files
- API connectivity
- Basic workflow functionality

## 🚀 Quick Start

### Test the installation:
```bash
python main.py --help
```

### Run a quick demo:
```bash
python demo.py
```

### Run your first research:
```bash
python main.py "artificial intelligence in healthcare"
```

### Interactive mode:
```bash
python main.py --interactive
```

## 🐛 Troubleshooting

### Common Issues

**Import Errors**
```bash
# Make sure you're in the correct environment
which python
pip list | grep -E "(google|exa|pydantic|rich)"
```

**API Key Issues**
```bash
# Check if .env file exists and has content
cat .env
# Verify keys are loaded
python -c "from config import config; print('Google:', bool(config.google_api_key)); print('Exa:', bool(config.exa_api_key))"
```

**Permission Errors**
```bash
# Make scripts executable
chmod +x *.py
```

**Network/Proxy Issues**
```bash
# Set proxy if needed
export https_proxy=your_proxy_url
export http_proxy=your_proxy_url
```

### Environment-Specific Solutions

**Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py", "--help"]
```

**Google Colab**
```python
!git clone https://github.com/your-repo/deep-research-workflow.git
%cd deep-research-workflow
!pip install -r requirements.txt

# Set API keys in Colab secrets
from google.colab import userdata
import os
os.environ['GOOGLE_API_KEY'] = userdata.get('GOOGLE_API_KEY')
os.environ['EXA_API_KEY'] = userdata.get('EXA_API_KEY')
```

**Jupyter Notebook**
```python
# Install in notebook
!pip install -r requirements.txt

# Use environment variables or .env file
import os
os.environ['GOOGLE_API_KEY'] = 'your_key'
os.environ['EXA_API_KEY'] = 'your_key'

# Import and use
from research_workflow import run_research
report = await run_research("your query")
```

## 📦 Dependencies Explained

- **google-generativeai**: Google's Gemini AI client
- **exa-py**: Exa search API client  
- **aiohttp**: Async HTTP client for parallel requests
- **python-dotenv**: Environment variable management
- **pydantic**: Data validation and settings
- **rich**: Beautiful terminal output
- **typing-extensions**: Extended type hints

## 🔄 Updating

To update to the latest version:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run tests to verify
python test_setup.py
```

## 💡 Performance Tips

- Use SSD storage for faster file operations
- Ensure stable internet connection
- Monitor API rate limits
- Adjust `MAX_URLS_PER_QUERY` based on your needs
- Use virtual environments to avoid conflicts

## 🆘 Getting Help

If you encounter issues:

1. Run `python test_setup.py` to diagnose problems
2. Check the troubleshooting section above
3. Review logs for specific error messages
4. Verify API keys and network connectivity
5. Create an issue with detailed error information

---

**Ready to research!** 🔬✨