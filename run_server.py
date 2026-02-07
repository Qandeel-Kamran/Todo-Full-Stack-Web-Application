#!/usr/bin/env python
"""
Entry point for running the Todo AI Chatbot server
"""

import uvicorn
from config import settings


def main():
    """Main entry point for the application"""
    print("Starting Todo AI Chatbot Server...")
    print(f"App: {settings.app_name} v{settings.app_version}")
    print("Loading configuration...")

    print(f"Server starting on {settings.host}:{settings.port}")
    if settings.reload:
        print("Hot reload enabled")

    # Run the server
    uvicorn.run(
        "api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level="info"
    )


if __name__ == "__main__":
    main()