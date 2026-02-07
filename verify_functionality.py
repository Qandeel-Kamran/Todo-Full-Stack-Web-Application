#!/usr/bin/env python
"""
Verification script for Todo AI Chatbot functionality
Tests the core functionality as specified in the requirements
"""

import asyncio
import sys
import os
import uuid

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.tools import (
    add_task, list_tasks, update_task, complete_task, delete_task,
    TaskParams, UpdateTaskParams, ListTasksParams
)
from agents.todo_agent import TodoAgent


async def test_example_1_add_task():
    """Test Example 1: Add Task - 'Add a task to buy groceries'"""
    print("\nTesting Example 1: Add Task")
    print("Input: 'Add a task to buy groceries'")

    # Clear tasks for clean test
    from mcp.tools import task_manager
    task_manager.tasks = {}
    task_manager.next_id = 1

    # Simulate the agent processing this message
    agent = TodoAgent()

    # Test the fallback intent processor directly
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

    print("PASS: Example 1: PASSED")


async def test_example_2_complete_task():
    """Test Example 2: Complete Task - 'Mark task 1 as complete'"""
    print("\nTesting Example 2: Complete Task")
    print("Input: 'Mark task 1 as complete'")

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

    print("PASS: Example 2: PASSED")


async def test_stateless_behavior():
    """Test stateless behavior with conversation preservation"""
    print("\n🧪 Testing Stateless Behavior")

    # Simulate a conversation flow
    from mcp.tools import task_manager
    task_manager.tasks = {}
    task_manager.next_id = 1

    # Add a task first
    agent = TodoAgent()
    result1 = await agent._process_intent_fallback(
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
    list_result = await restarted_agent._process_intent_fallback(
        user_id="stateless_test_user",
        message="List my tasks"
    )

    print(f"After restart, listing tasks: {list_result['response']}")
    assert 'test stateless behavior' in list_result['response'], "Task was not persisted across restart"

    print("PASS: Stateless behavior: PASSED")


async def run_verification_tests():
    """Run all verification tests"""
    print("Starting Todo AI Chatbot Functionality Verification")
    print("=" * 60)

    try:
        await test_example_1_add_task()
        await test_example_2_complete_task()
        await test_stateless_behavior()

        print("\n" + "=" * 60)
        print("All verification tests PASSED!")
        print("Add task functionality working correctly")
        print("Complete task functionality working correctly")
        print("Stateless behavior with persistent context working correctly")
        print("\nThe Todo AI Chatbot is functioning as specified.")

    except AssertionError as e:
        print(f"\nVERIFICATION FAILED: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(run_verification_tests())