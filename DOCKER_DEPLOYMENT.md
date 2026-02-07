# Todo AI Chatbot - Docker Deployment

Containerized deployment of the Todo AI Chatbot application with Docker and Docker Compose.

## Prerequisites

- Docker Desktop (with Docker Engine and Docker Compose)
- At least 4GB of RAM available for containers

## Quick Start

### Option 1: Using the start script (Windows)
```bash
start_docker.bat
```

### Option 2: Manual deployment
```bash
# Build and start all services
docker-compose -f docker-compose.full.yml up -d --build

# View logs
docker-compose -f docker-compose.full.yml logs -f

# Stop services
docker-compose -f docker-compose.full.yml down
```

## Services

The application consists of the following services:

### 1. Backend (FastAPI)
- Port: 8000
- Handles API requests and AI agent processing
- Connects to PostgreSQL database
- Communicates with MCP server

### 2. Frontend (Next.js)
- Port: 3000
- User interface for the chatbot
- Connects to backend API at http://localhost:8000

### 3. Database (PostgreSQL)
- Port: 5432
- Stores conversation history and tasks
- Data persisted in named volume

### 4. MCP Server
- Port: 8080
- Handles MCP tools for task operations
- Connects to PostgreSQL database

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://postgres:password@db:5432/todo_chatbot
MCP_SERVER_URL=http://mcp-server:8080
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Building Images

To build the Docker images individually:

```bash
# Build backend image
docker build -f Dockerfile.backend -t todo-ai-backend .

# Build frontend image
docker build -f frontend/Dockerfile -t todo-ai-frontend .

# Build MCP server image
docker build -f Dockerfile.mcp -t todo-ai-mcp .
```

## Development with Docker

For development, the compose file mounts the source code as volumes, allowing for live reloading. To develop with Docker:

1. Start the services: `docker-compose -f docker-compose.full.yml up -d`
2. Make changes to your code
3. The containers will automatically reflect the changes

## Production Considerations

For production deployment, consider:

1. Using environment-specific compose files
2. Setting up SSL certificates
3. Configuring persistent storage for database
4. Setting up monitoring and logging
5. Using secrets management for sensitive data

## Troubleshooting

### Common Issues

1. **Port already in use**: Make sure ports 8000, 3000, 5432, and 8080 are available
2. **Insufficient memory**: Increase Docker's memory allocation to at least 4GB
3. **Dependency issues**: Make sure to rebuild images with `--build` flag when changing requirements

### Useful Commands

```bash
# View logs for specific service
docker-compose -f docker-compose.full.yml logs -f backend

# Execute command in running container
docker-compose -f docker-compose.full.yml exec backend bash

# View running containers
docker-compose -f docker-compose.full.yml ps

# Clean up containers and volumes
docker-compose -f docker-compose.full.yml down -v
```

## Architecture

```
┌─────────────────┐    ┌──────────────────┐
│   Frontend      │────│    Backend       │
│   (Port 3000)   │    │   (Port 8000)    │
└─────────────────┘    └──────────────────┘
                             │
                    ┌──────────────────┐
                    │   MCP Server     │
                    │   (Port 8080)    │
                    └──────────────────┘
                             │
                    ┌──────────────────┐
                    │   PostgreSQL     │
                    │   (Port 5432)    │
                    └──────────────────┘
```

## Scaling

The application is designed to be horizontally scalable. Each service can be scaled independently based on demand:

```bash
# Scale backend service to 2 instances
docker-compose -f docker-compose.full.yml up -d --scale backend=2
```