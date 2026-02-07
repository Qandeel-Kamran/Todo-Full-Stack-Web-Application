#!/usr/bin/env python
"""
Simple verification script for Todo AI Chatbot functionality
"""

import asyncio
import sys
import os

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.tools import (
    add_task, list_tasks, update_task, complete_task, delete_task,
    TaskParams, UpdateTaskParams, ListTasksParams
)
from agents.todo_agent import TodoAgent


async def test_add_task():
    """Test adding a task"""
    print("Testing Example 1: Add Task")
    print("Input: 'Add a task to buy groceries'")

    # Clear tasks for clean test
    from mcp.tools import task_manager
    task_manager.tasks = {}
    task_manager.next_id = 1

    # Test the agent's fallback intent processor directly
    agent = TodoAgent()
    result = await agent.process_intent_fallback(
        user_id="test_user_123",
        message="Add a task to buy groceries"
    )

    print(f"Response: {result['response']}")
    print(f"Tool calls: {result['tool_calls']}")

    # Verify add_task was called
    assert len(result['tool_calls']) > 0, "Expected tool calls but got none"
    assert any(tc['name'] == 'add_task' for tc in result['tool_calls']), "Expected add_task tool call"

    # Check that the task was actually added to the manager
    assert len(task_manager.tasks) == 1, f"Expected 1 task, but found {len(task_manager.tasks)}"

    task = list(task_manager.tasks.values())[0]
    assert task['title'] == 'buy groceries', f"Expected title 'buy groceries', got '{task['title']}'"
    assert task['user_id'] == 'test_user_123', f"Expected user_id 'test_user_123', got '{task['user_id']}'"

    print("PASS: Add Task functionality working correctly\n")


async def test_complete_task():
    """Test completing a task"""
    print("Testing Example 2: Complete Task")
    print("Input: 'complete task 1'")

    # First, add a task to complete
    from mcp.tools import task_manager
    task_manager.tasks = {}
    task_manager.next_id = 1

    add_result = await add_task(TaskParams(
        user_id="test_user_456",
        title="Test task to complete"
    ))

    assert add_result.success, "Failed to add test task"
    task_id = add_result.data["task_id"]
    print(f"Added task with ID: {task_id}")

    # Now test completing the task
    agent = TodoAgent()
    result = await agent.process_intent_fallback(
        user_id="test_user_456",
        message=f"complete task {task_id}"
    )

    print(f"Response: {result['response']}")
    print(f"Tool calls: {result['tool_calls']}")

    # Verify complete_task was called
    assert len(result['tool_calls']) > 0, "Expected tool calls but got none"
    assert any(tc['name'] == 'complete_task' for tc in result['tool_calls']), "Expected complete_task tool call"

    # Check that the task was actually marked as completed
    completed_task = task_manager.tasks[task_id]
    assert completed_task['completed'] == True, f"Expected task to be completed, but completed={completed_task['completed']}"

    print("PASS: Complete Task functionality working correctly\n")


async def test_stateless_behavior():
    """Test stateless behavior with conversation preservation"""
    print("Testing Stateless Behavior")

    # Simulate a conversation flow
    from mcp.tools import task_manager
    task_manager.tasks = {}
    task_manager.next_id = 1

    # Add a task first
    agent = TodoAgent()
    result1 = await agent.process_intent_fallback(
        user_id="stateless_test_user",
        message="Add a task to test stateless behavior"
    )

    print(f"After adding task: {result1['response']}")
    assert 'test stateless behavior' in result1['response'], "Task was not added properly"

    # Count tasks after restart simulation (reset agent but keep data)
    print(f"Number of tasks in storage: {len(task_manager.tasks)}")
    assert len(task_manager.tasks) > 0, "No tasks were stored"

    # Simulate restarting server (agent object recreated but data persists in storage)
    restarted_agent = TodoAgent()

    # List tasks to verify they persist
    list_result = await restarted_agent.process_intent_fallback(
        user_id="stateless_test_user",
        message="List my tasks"
    )

    print(f"After restart, listing tasks: {list_result['response']}")
    assert 'test stateless behavior' in list_result['response'], "Task was not persisted across restart"

    print("PASS: Stateless behavior with persistent context working correctly\n")


async def main():
    """Run all verification tests"""
    print("Starting Todo AI Chatbot Functionality Verification")
    print("=" * 60)

    try:
        await test_add_task()
        await test_complete_task()
        await test_stateless_behavior()

        print("=" * 60)
        print("SUCCESS: All verification tests PASSED!")
        print("The Todo AI Chatbot is functioning as specified.")

    except AssertionError as e:
        print(f"VERIFICATION FAILED: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"UNEXPECTED ERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())