# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Ice Breaker is a Flask-based web application that generates personalized conversation starters by analyzing LinkedIn and Twitter profiles using LangChain and OpenAI.

## Development Commands

### Running the Application
```bash
# Install dependencies
pipenv install

# Run the Flask application
pipenv run python app.py

# Or directly with pipenv shell
pipenv shell
python app.py
```

### Environment Setup
```bash
# Copy environment template and configure your API keys
cp .env.example .env
# Edit .env file with your API credentials

# Activate pipenv shell
pipenv shell

# Verify environment setup
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('✓ Environment loaded')"
```

### Code Quality Tools
```bash
# Format code with Black
pipenv run black .

# Sort imports with isort
pipenv run isort .

# Lint code with pylint
pipenv run pylint [module_name]
```

### Testing
```bash
# Note: No test files currently exist, but the README mentions pytest
pipenv run pytest .
```

## Architecture & Key Components

### Core Pipeline Flow
1. **Web Interface** (`app.py`): Flask server handling UI and API endpoints
2. **Main Logic** (`ice_breaker.py`): Orchestrates the entire ice breaker generation pipeline
3. **Agent System**: Profile lookup agents for LinkedIn and Twitter discovery
4. **Data Extraction**: Third-party integrations for scraping social media data
5. **AI Processing**: LangChain chains for generating summaries, interests, and ice breakers
6. **Output Parsing**: Structured response formatting using Pydantic models

### Key Modules

- **agents/**: LangChain ReAct agents for profile discovery
  - Uses Tavily for web search to find LinkedIn/Twitter profiles
  - Leverages LangChain hub prompts (hwchase17/react)

- **chains/**: Custom LangChain sequences for AI processing
  - Three distinct chains: summary, interests, ice breakers
  - Uses GPT-3.5-turbo with temperature=0 for deterministic outputs and temperature=1 for creative content
  - Implements RunnableSequence pattern: PromptTemplate | LLM | OutputParser

- **third_parties/**: External API integrations
  - LinkedIn scraping via Scrapin.io API
  - Twitter data via Twitter API (with mock fallback)

- **tools/**: Utility functions for web search using Tavily

- **output_parsers.py**: Pydantic models for structured outputs (Summary, TopicOfInterest, IceBreaker)

## API Dependencies

Required environment variables in `.env`:
- `OPENAI_API_KEY` - OpenAI API for LLM
- `PROXYCURL_API_KEY` - Proxycurl for LinkedIn data (note: .env.example references this, not SCRAPIN_API_KEY)
- `TAVILY_API_KEY` - Tavily for web search
- `TWITTER_API_KEY`, `TWITTER_API_KEY_SECRET`, `TWITTER_BEARER_TOKEN`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET` - Optional Twitter API

Optional LangSmith tracing:
- `LANGCHAIN_TRACING_V2=true`
- `LANGCHAIN_API_KEY`
- `LANGCHAIN_PROJECT=ice_breaker`

## Development Notes

- **LLM Configuration**: Uses GPT-3.5-turbo for all chains (temperature=0 for deterministic outputs, temperature=1 for creative ice breakers in `chains/custom_chains.py:9-10`)
- **Twitter Integration**: Defaults to mock implementation (`scrape_user_tweets_mock`) in `ice_breaker.py:25`
- **Flask Server**: Runs in debug mode by default on host 0.0.0.0:5000 (`app.py:35`)
- **Agent Architecture**: Uses LangChain ReAct agents with Tavily search for profile discovery
- **Chain Pattern**: All chains follow RunnableSequence pattern: PromptTemplate | LLM | OutputParser
- **Output Structure**: Pydantic models (Summary, TopicOfInterest, IceBreaker) with `to_dict()` methods for JSON serialization
- **Package Management**: Uses Pipfile with Python 3.10 requirement
- **No Tests**: No unit tests currently implemented despite pytest being referenced

## Debugging & Development Tips

```bash
# Test individual components in pipenv shell
pipenv shell
python -c "from ice_breaker import ice_break_with; print(ice_break_with('Elon Musk'))"

# Enable LangChain debugging (set in .env file)
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=your_key_here

# Test Flask app directly
python app.py
```