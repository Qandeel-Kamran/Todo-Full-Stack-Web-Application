#!/bin/bash

# Todo AI Chatbot - Docker Deployment Script

echo "==========================================="
echo "Todo AI Chatbot - Docker Deployment"
echo "==========================================="

# Check if Docker is installed
if ! [ -x "$(command -v docker)" ]; then
  echo "Error: Docker is not installed." >&2
  exit 1
fi

# Check if docker-compose is installed
if ! [ -x "$(command -v docker-compose)" ]; then
  echo "Error: Docker Compose is not installed." >&2
  exit 1
fi

echo "Starting Todo AI Chatbot containers..."

# Start the containers in detached mode
docker-compose -f docker-compose.full.yml up -d

echo "==========================================="
echo "Containers are starting..."
echo "Backend will be available at: http://localhost:8000"
echo "Frontend will be available at: http://localhost:3000"
echo "Database will be available at: http://localhost:5432"
echo ""
echo "To view container logs: docker-compose -f docker-compose.full.yml logs -f"
echo "To stop containers: docker-compose -f docker-compose.full.yml down"
echo "==========================================="