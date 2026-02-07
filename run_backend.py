#!/usr/bin/env python
"""
Startup script for the Todo AI Chatbot backend
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Main entry point for the application"""
    print("Starting Todo AI Chatbot Backend...")
    print("Loading configuration...")

    # Get host and port from environment or use defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "true").lower() == "true"

    print(f"Server starting on {host}:{port}")
    if reload:
        print("Hot reload enabled")

    # Run the server
    uvicorn.run(
        "backend_main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    main()