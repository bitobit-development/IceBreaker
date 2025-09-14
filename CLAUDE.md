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

# Verify environment setup
pipenv run python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('✓ Environment loaded')"
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
- `SCRAPIN_API_KEY` - Scrapin.io for LinkedIn data
- `TAVILY_API_KEY` - Tavily for web search
- `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_SECRET` - Optional Twitter API

Optional LangSmith tracing:
- `LANGCHAIN_TRACING_V2=true`
- `LANGCHAIN_API_KEY`
- `LANGCHAIN_PROJECT=ice_breaker`

## Development Notes

- The application uses GPT-4o-mini for agents and GPT-3.5-turbo for chains
- Twitter integration defaults to mock implementation (`scrape_user_tweets_mock`) in `ice_breaker.py:25`
- Flask runs in debug mode by default on host 0.0.0.0:5000
- LangChain agents use verbose mode for debugging
- Output parsing uses Pydantic models with `to_dict()` methods for JSON serialization
- All chains follow the same pattern: prompt template with format instructions, LLM processing, and structured parsing
- No unit tests are currently implemented despite pytest being mentioned

## Debugging & Development Tips

```bash
# Test individual components
pipenv run python -c "from ice_breaker import ice_break_with; print(ice_break_with('Elon Musk'))"

# Enable LangChain debugging
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=your_key_here
```
- I like to eat the pizza.