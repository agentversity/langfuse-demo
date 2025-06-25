# Langfuse-Tutorial – Question-Answering Web App

A Flask-based web application that provides natural language question answering capabilities with web search integration and observability through Langfuse.

## Overview

This project demonstrates how to build a simple but powerful question-answering system using LangGraph, OpenAI, and DuckDuckGo search. The application automatically determines when to search the web for information and provides clear, concise answers with source citations. All operations are traced using Langfuse for comprehensive observability.

![App Screenshot Placeholder]()

## Features

- Natural language question answering with OpenAI's GPT-4o mini
- Automatic detection of questions that require web research
- Integration with DuckDuckGo for real-time information retrieval
- Complete observability with Langfuse tracing for all operations
- Simple, clean web interface
- Environment-based configuration

## Setting Up Langfuse Locally

This project uses Langfuse for observability and tracing. You can run Langfuse locally using Docker Compose:

### Option 1: Using the Official Langfuse Repository (Recommended)

1. **Clone the Langfuse repository**:
   ```bash
   git clone https://github.com/langfuse/langfuse.git
   cd langfuse
   ```

2. **Start Langfuse with Docker Compose**:
   ```bash
   docker compose up -d
   ```

3. **Create an account and API keys**:
   - Open [http://localhost:3000](http://localhost:3000) in your browser
   - Create a new account
   - Create a new project (or use the default project)
   - Go to Settings > API Keys
   - Create a new set of API keys (you'll need both the public and secret keys)

### Option 2: Using a Custom Docker Compose File

Create a `docker-compose.yml` file with the following content:

```yaml
version: '3'

services:
  postgres:
    image: postgres:14
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=langfuse
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  langfuse:
    image: langfuse/langfuse:latest
    depends_on:
      postgres:
        condition: service_healthy
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/langfuse
      - NEXTAUTH_SECRET=your-nextauth-secret
      - NEXTAUTH_URL=http://localhost:3000
      - SALT=your-salt
      - POSTGRES_PRISMA_URL=postgresql://postgres:postgres@postgres:5432/langfuse
      - POSTGRES_URL_NON_POOLING=postgresql://postgres:postgres@postgres:5432/langfuse
      - NEXT_PUBLIC_SIGN_UP_DISABLED=false
      - NEXT_PUBLIC_DEMO_MODE=false
    restart: unless-stopped

volumes:
  postgres_data:
```

Then run:
```bash
docker compose up -d
```

### Managing Your Langfuse Instance

- **Stopping Langfuse**:
  ```bash
  docker compose down
  ```

- **Resetting data** (including the database):
  ```bash
  docker compose down -v
  ```

- **Updating Langfuse**:
  ```bash
  git pull  # If using Option 1
  docker compose down
  docker compose pull
  docker compose up -d
  ```

## Tech Stack / Architecture

- **Backend**: Python 3.10+, Flask
- **AI/ML**: OpenAI API, LangGraph
- **Search**: DuckDuckGo Search API, BeautifulSoup4
- **Observability**: Langfuse
- **Frontend**: HTML, CSS, Jinja2 templates

```mermaid
graph TD
  UI[Browser] -->|POST /ask| Flask
  Flask --> Agent
  Agent -->|OpenAI| OpenAIAPI
  Agent -->|DDG Search| DuckDuckGo
  Agent -->|Spans| Langfuse
  Langfuse --> LangfuseUI[(Langfuse Dashboard)]
```

## Directory Layout

```
.
├─ app.py              # Flask server
├─ agent.py            # LangGraph agent logic
├─ search.py           # DuckDuckGo helper
├─ templates/          # Jinja2 HTML templates
├─ static/style.css    # Styling
└─ requirements.txt    # Dependencies
```

## Prerequisites

- Python 3.10 or higher
- OpenAI API key
- Docker and Docker Compose (for running Langfuse locally)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/agentversity/langfuse-demo.git
   cd langfuse-demo
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   
   Then edit the `.env` file to add your API keys:
   ```
   # OpenAI API Key
   OPENAI_API_KEY=your_openai_api_key

   # Langfuse Configuration
   LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
   LANGFUSE_SECRET_KEY=your_langfuse_secret_key
   LANGFUSE_HOST=http://localhost:3000  # For local Langfuse instance
   
   # Optional: Prompt Management Configuration
   PROMPT_LABEL=development  # Label to use when fetching prompts from Langfuse
   ```

## Running Locally

Start the Flask development server:
```bash
python app.py
```

The application will be available at http://127.0.0.1:5000

## Usage

### Web Interface

1. Open your browser and navigate to http://127.0.0.1:5000
2. Enter your question in the input field
3. Click "Ask" or press Enter
4. View the response, which may include information from web searches

### API Endpoints

#### Ask Endpoint

You can interact with the question-answering functionality programmatically:

```bash
curl -X POST http://127.0.0.1:5000/ask \
  -d "question=What is artificial intelligence?"
```

Response format:
```json
{
  "answer": "Artificial intelligence (AI) refers to...",
  "has_citations": true
}
```

You can also include a toxicity score (0-1) when asking a question:

```bash
curl -X POST http://127.0.0.1:5000/ask \
  -d "question=What is artificial intelligence?" \
  -d "toxicity=0.1"
```

#### Score Endpoint

You can add a toxicity score to a previously asked question:

```bash
curl -X POST http://127.0.0.1:5000/score \
  -H "Content-Type: application/json" \
  -d '{"question":"What is artificial intelligence?", "toxicity":0.2}'
```

Response format:
```json
{
  "success": true,
  "message": "Expert feedback score of 0.2 received and applied. Automated toxicity evaluation also performed."
}
```

The toxicity score should be a float between 0 and 1, where:
- 0 = Not toxic at all
- 1 = Extremely toxic

## Integrating with Langfuse SDK v3

This project uses Langfuse SDK v3 for tracing and observability. Here's how it's integrated:

### SDK Installation

The SDK is included in the requirements.txt file, but you can install it separately:

```bash
pip install langfuse==3.0.0
```

### Key Integration Points

1. **Client Initialization**:
   ```python
   from langfuse import get_client
   
   # Initialize the client
   langfuse_client = get_client()
   ```

2. **Observing Functions with Decorators**:
   ```python
   from langfuse import observe
   
   @observe(name="process_question")
   def process_question(question: str, user_id: Optional[str] = None):
       # Function implementation
       pass
   ```

3. **Creating Spans**:
   ```python
   with langfuse_client.start_as_current_span(name="toxicity-evaluation"):
       # Code to execute within this span
       eval_result = evaluate_toxicity(answer, question)
   ```

4. **Adding Scores**:
   ```python
   langfuse_client.create_score(
       name="llm_toxicity_evaluation",
       value=eval_result["score"],
       trace_id=trace_id,
       data_type="NUMERIC",
       comment=eval_result["reasoning"],
   )
   ```

5. **Scoring Current Trace**:
   ```python
   langfuse_client.score_current_trace(
       name="user-feedback",
       value=1,
       data_type="NUMERIC",
   )
   ```

### Common Issues and Solutions

1. **"No module named 'langfuse'"**: Make sure you've installed the SDK with `pip install langfuse==3.0.0`

2. **Connection errors**: Verify your API keys and host in the `.env` file

3. **No data appearing in Langfuse**: Check that your application is properly initialized with the correct API keys

4. **"Unauthorized" errors**: Ensure your API keys have the correct permissions in Langfuse

5. **Parameter errors**: If you see errors about unexpected parameters, check the SDK version and update your code to match the current API

For more details, see the [official Langfuse documentation](https://langfuse.com/docs/sdk/python).

## Observability with Langfuse

This application uses Langfuse for tracing and observability. Each component of the question-answering process is decorated with `@observe` to create spans:

- `determine_search_need`: Decides if web search is needed
- `perform_search`: Executes DuckDuckGo searches
- `generate_response`: Creates the final answer using OpenAI
- `process_question`: The main entry point that orchestrates the entire process

To view traces:

1. Log in to your Langfuse dashboard (cloud or local instance)
2. Navigate to the Traces section
3. Filter by trace ID or time period

### Scoring with Langfuse

The application implements two types of scoring:

1. **Automated LLM-as-a-Judge Evaluation**:
   - Automatically evaluates the toxicity of responses
   - Uses OpenAI to analyze content and provide a score from 0-1
   - Includes detailed reasoning for the score

2. **User Feedback**:
   - Allows users to provide toxicity scores through the API
   - Scores are attached to the corresponding trace
   - Enables human-in-the-loop evaluation

### Prompt Management with Langfuse

This application also leverages Langfuse's prompt management capabilities. The system prompt used by the Q&A agent is retrieved from Langfuse, allowing for:

- Centralized prompt management
- Version control for prompts
- A/B testing different prompt variations
- Updating prompts without code changes

To seed or update the prompt in Langfuse:

```bash
python seed_prompt.py
```

The application will automatically fetch the latest version of the prompt named `qa-system-prompt-dev` from Langfuse with the label specified in the `PROMPT_LABEL` environment variable (defaults to "development"). If the prompt cannot be retrieved (e.g., due to network issues or if it doesn't exist), the application will fall back to a hardcoded default prompt and log a warning.

#### A/B Testing Prompts

To perform A/B testing with different prompt versions:

1. Create multiple versions of the prompt with different labels:
   ```bash
   # Set the label for the first version
   export PROMPT_LABEL=version_a
   python seed_prompt.py
   
   # Set the label for the second version
   export PROMPT_LABEL=version_b
   python seed_prompt.py
   ```

2. Configure the application to use a specific version by setting the `PROMPT_LABEL` environment variable:
   ```bash
   export PROMPT_LABEL=version_a
   python app.py
   ```

## Troubleshooting

### Common Langfuse Issues

1. **Langfuse UI not loading**:
   - Check if the Docker containers are running: `docker compose ps`
   - Check container logs: `docker compose logs langfuse`
   - Ensure port 3000 is not being used by another application

2. **Connection issues from your application**:
   - Verify your `.env` file has the correct Langfuse host and API keys
   - If running in Docker, ensure proper network configuration
   - Check application logs for connection errors

3. **No data appearing in Langfuse**:
   - Verify API keys are correctly configured
   - Check application logs for Langfuse-related errors
   - Ensure the `@observe` decorators are properly applied in your code

4. **SDK version compatibility issues**:
   - This project uses Langfuse SDK v3
   - If you see parameter errors, check the [SDK migration guide](https://langfuse.com/docs/sdk/python/migration)

### Getting Help

If you encounter issues not covered here, please:
1. Check the [Langfuse documentation](https://langfuse.com/docs)
2. Open an issue in this repository

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [OpenAI](https://openai.com/) for their powerful language models
- [LangGraph](https://github.com/langchain-ai/langgraph) for the agent framework
- [Langfuse](https://langfuse.com/) for observability tools
- [DuckDuckGo](https://duckduckgo.com/) for search capabilities
