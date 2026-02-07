@echo off
REM Todo AI Chatbot - Docker Deployment Script for Windows

echo ===========================================
echo Todo AI Chatbot - Docker Deployment
echo ===========================================

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed or not in PATH.
    pause
    exit /b 1
)

REM Check if docker-compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker Compose is not installed or not in PATH.
    pause
    exit /b 1
)

echo Starting Todo AI Chatbot containers...

REM Start the containers in detached mode
docker-compose -f docker-compose.full.yml up -d

echo ===========================================
echo Containers are starting...
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:3000
echo Database will be available at: http://localhost:5432
echo.
echo To view container logs: docker-compose -f docker-compose.full.yml logs -f
echo To stop containers: docker-compose -f docker-compose.full.yml down
echo ===========================================

pause