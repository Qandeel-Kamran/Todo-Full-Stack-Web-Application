#!/usr/bin/env python
"""
Build script for Todo AI Chatbot
"""

import os
import sys
import subprocess
import importlib.util

def check_dependencies():
    """Check if required modules can be imported"""
    print("Checking dependencies...")

    required_modules = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'sqlalchemy',
        'dotenv',
        'mcp'
    ]

    missing_modules = []
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"PASS: {module}")
        except ImportError:
            missing_modules.append(module)
            print(f"FAIL: {module}")

    if missing_modules:
        print(f"\nMissing modules: {', '.join(missing_modules)}")
        print("Please install using: pip install -r requirements.txt")
        return False

    print("All dependencies available!\n")
    return True


def check_structure():
    """Check if required project files exist"""
    print("Checking project structure...")

    required_files = [
        'api/main.py',
        'agents/todo_agent.py',
        'mcp/tools.py',
        'requirements.txt',
        'config.py'
    ]

    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"PASS: {file}")
        else:
            missing_files.append(file)
            print(f"FAIL: {file}")

    if missing_files:
        print(f"\nMissing files: {', '.join(missing_files)}")
        return False

    print("Project structure is complete!\n")
    return True


def run_basic_functionality_test():
    """Run a basic functionality test"""
    print("Running basic functionality test...")

    try:
        # Import and test core components
        from agents.todo_agent import TodoAgent
        from mcp.tools import add_task, TaskParams

        # Create agent
        agent = TodoAgent()
        print("PASS: TodoAgent instantiated successfully")

        # Test agent functionality
        import asyncio

        async def test():
            result = await agent.process_message("test_user", "Add a test task")
            return result

        test_result = asyncio.run(test())
        print(f"PASS: Agent processed message: {test_result.response[:50]}...")

        print("Basic functionality test passed!\n")
        return True

    except Exception as e:
        print(f"FAIL: Basic functionality test failed: {str(e)}")
        return False


def main():
    """Main build process"""
    print("Building Todo AI Chatbot...\n")

    success = True

    # Check dependencies
    if not check_dependencies():
        success = False

    # Check structure
    if not check_structure():
        success = False

    # Run basic functionality test
    if not run_basic_functionality_test():
        success = False

    if success:
        print("Build completed successfully!")
        print("\nThe Todo AI Chatbot is ready for deployment.")
        print("To run the server: python run_server.py")
        print("To run tests: python -m pytest tests/")
    else:
        print("Build failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()