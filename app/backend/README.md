# AI Hedge Fund - Backend [WIP] 🚧
This project is currently a work in progress.  To track progress, please get updates [here](https://x.com/virattt).

This is the backend server for the AI Hedge Fund project. It provides a simple REST API to interact with the AI Hedge Fund system, allowing you to run the hedge fund through a web interface.

## Overview

This backend project is a FastAPI application that serves as the server-side component of the AI Hedge Fund system. It exposes endpoints for running the hedge fund trading system and backtester.

This backend is designed to work with a future frontend application that will allow users to interact with the AI Hedge Fund system through their browser.

## Installation

### Using Poetry

1. Clone the repository:
```bash
git clone https://github.com/virattt/ai-hedge-fund.git
cd ai-hedge-fund
```

2. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies:
```bash
# From the root directory
poetry install
```

4. Set up your environment variables:
```bash
# Create .env file for your API keys (in the root directory)
cp .env.example .env
```

5. Edit the .env file to add your API keys:
```bash
# For running LLMs hosted by openai (gpt-4o, gpt-4o-mini, etc.)
OPENAI_API_KEY=your-openai-api-key

# For running LLMs hosted by groq (deepseek, llama3, etc.)
GROQ_API_KEY=your-groq-api-key

# For getting financial data to power the hedge fund
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key
```

## Running the Server

To run the development server:

```bash
# Navigate to the backend directory
cd app/backend

# Start the FastAPI server with uvicorn
poetry run uvicorn main:app --reload
```

This will start the FastAPI server with hot-reloading enabled.

The API will be available at:
- API Endpoint: http://localhost:8000
- API Documentation: http://localhost:8000/docs

> **Personal note:** I also run the server on port 8080 occasionally to avoid conflicts with other local services. Use `--port 8080` flag with uvicorn if needed.

## API Endpoints

- `POST /hedge-fund/run`: Run the AI Hedge Fund with specified parameters
- `GET /ping`: Simple endpoint to test server connectivity

## Project Structure

```
app/backend/
├── api/                      # API layer (future expansion)
├── models/                   # Domain models
│   ├── __init__.py
│   └── schemas.py            # Pydantic schema definitions
├── routes/                   # API routes
│   ├── __init__.py           # Router registry
│   ├── hedge_fund.py         # Hedge fund endpoints
│   └── health.py             # Health check endpoints
├── services/                 # Business logic
│   ├── graph.py              # Agent graph functionality
│   └── portfolio.py          # Portfolio management
├── __init__.py               # Package initialization
└── main.py                   # FastAPI application entry point
```

## Troubleshooting

- **Port already in use:** If port 8000 is occupied, start the server on an alternate port with `--port 8080`.
- **Poetry not found after install:** Restart your shell or run `source ~/.profile` to pick up the updated PATH.
- **Missing API keys:** The server will start without all keys set, but requests requiring a missing key will fail with a 500 error. Double-check your `.env` file.

## Disclaimer

This project is for **educational and research purposes only**. It is not intended to be used as actual financial advice or for real trading. Always consult a qualified financial advisor before making investment decisions.
