# Todo AI Chatbot

AI-powered todo chatbot using OpenAI Agents SDK and MCP (Model Context Protocol). Built using Spec-Driven Development with no manual coding.

## Overview

This is an AI-powered todo chatbot that allows users to manage their tasks through natural language conversations. The system uses OpenAI's API for intent recognition and response generation, with MCP tools for persistent task management in PostgreSQL.

## Architecture

- **FastAPI backend**: High-performance web framework
- **OpenAI Agents SDK**: For natural language understanding and generation
- **MCP Server**: Official SDK for task operations
- **Neon Serverless PostgreSQL**: For persistent task storage
- **Stateless chat endpoint**: With conversation memory

## Features

- Add, list, update, complete, delete tasks via natural language
- MCP tools for task operations
- Persistent conversation memory (stateless server)
- Error handling and resilience
- Health check endpoints
- Conversation history retrieval

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd todo-ai-chatbot
   ```

2. **Copy environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=postgresql://user:password@localhost:5432/todo_chatbot
   MCP_SERVER_URL=http://localhost:8080
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests**
   ```bash
   pytest tests/
   ```

5. **Start the server**
   ```bash
   uvicorn api.main:app --reload --port 8000
   ```

## API

The main chat endpoint is:

```
POST /api/{user_id}/chat
```

Request body:
```json
{
  "conversation_id": "optional conversation ID",
  "message": "your message to the bot"
}
```

Response:
```json
{
  "conversation_id": "conversation ID",
  "response": "bot response",
  "tool_calls": "array of tool calls made"
}
```

## MCP Tools

The system includes the following MCP tools:

- `add_task`: Add a new task
- `list_tasks`: List existing tasks
- `update_task`: Update an existing task
- `complete_task`: Mark a task as completed
- `delete_task`: Delete a task

## Project Structure

```
├── api/                 # FastAPI application
│   ├── main.py         # Main application
│   └── database.py     # Database models and setup
├── agents/             # AI agent implementation
│   └── todo_agent.py   # Todo AI Agent
├── mcp/                # MCP tools
│   └── tools.py        # Task operation tools
├── tests/              # Test files
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables example
└── README.md          # This file
```

## Testing

Run all tests:
```bash
pytest tests/
```

Run specific test modules:
```bash
pytest tests/test_api.py
```

## License

MIT