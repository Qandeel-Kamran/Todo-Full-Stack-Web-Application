#!/usr/bin/env python
"""Basic functionality test for Todo AI Chatbot"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.todo_agent import TodoAgent
from mcp.tools import task_manager

async def basic_test():
    print("Running basic functionality test...")

    # Clear tasks for clean test
    task_manager.tasks = {}
    task_manager.next_id = 1

    # Create agent
    agent = TodoAgent()

    # Test adding a task
    result = await agent.process_message("user123", "Add a task to test the system")
    print(f"Add task response: {result.response}")
    assert "test the system" in result.response

    # Test listing tasks
    result = await agent.process_message("user123", "List my tasks")
    print(f"List tasks response: {result.response}")
    assert "test the system" in result.response

    print("✓ Basic functionality test passed!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(basic_test())