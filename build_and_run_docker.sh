#!/bin/bash
# Build and run the Todo AI Chatbot in Docker

echo "Building Todo AI Chatbot Docker containers..."

# Build the containers
docker-compose build

echo "Starting Todo AI Chatbot services..."
echo "This may take a few moments to fully start up..."

# Start the services in detached mode
docker-compose up -d

echo ""
echo "Services are starting..."
echo "Backend API: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "Database: http://localhost:5432"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"