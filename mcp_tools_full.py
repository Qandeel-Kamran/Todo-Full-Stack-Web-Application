"""
MCP Tools for Todo AI Chatbot
Implements the required task operations using SQLModel and PostgreSQL
"""

from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List, Dict, Any
import os
from datetime import datetime
from pydantic import BaseModel
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Database model
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Request/Response models
class AddTaskRequest(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None


class AddTaskResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class ListTasksRequest(BaseModel):
    user_id: str
    status: str = "all"  # "all", "pending", "completed"


class ListTasksResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class CompleteTaskRequest(BaseModel):
    user_id: str
    task_id: int


class CompleteTaskResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class DeleteTaskRequest(BaseModel):
    user_id: str
    task_id: int


class DeleteTaskResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class UpdateTaskRequest(BaseModel):
    user_id: str
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None


class UpdateTaskResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class TaskManager:
    """
    MCP Tool Manager for task operations
    Handles all database operations for the Todo AI Chatbot
    """

    def __init__(self, database_url: str = None):
        # Use environment variable or default to a local SQLite database
        self.database_url = database_url or os.getenv("DATABASE_URL", "sqlite:///./todo_chatbot.db")

        # Try PostgreSQL first, fallback to SQLite if connection fails
        try:
            from sqlmodel import create_engine
            self.engine = create_engine(self.database_url)
            # Test the connection
            with self.engine.connect() as conn:
                pass
            logger.info("Connected to database successfully")
        except Exception as e:
            logger.warning(f"PostgreSQL connection failed: {e}. Falling back to SQLite.")
            self.database_url = "sqlite:///./todo_chatbot.db"
            self.engine = create_engine(self.database_url)

        # Create tables
        from sqlmodel import SQLModel
        SQLModel.metadata.create_all(self.engine)

    def get_session(self):
        """Get a database session"""
        from sqlmodel import Session
        return Session(self.engine)

    def add_task(self, user_id: str, title: str, description: str = None) -> AddTaskResponse:
        """
        Add a new task to the database

        Example usage:
        >>> manager = TaskManager()
        >>> result = manager.add_task("user123", "Buy groceries", "Milk and bread")
        >>> print(result.success)
        True
        """
        try:
            with self.get_session() as session:
                # Create new task
                task = Task(
                    user_id=user_id,
                    title=title,
                    description=description,
                    completed=False
                )

                # Add to database
                session.add(task)
                session.commit()
                session.refresh(task)

                logger.info(f"Added task {task.id} for user {user_id}")

                return AddTaskResponse(
                    success=True,
                    data={
                        "task_id": task.id,
                        "user_id": user_id,
                        "title": title,
                        "description": description,
                        "completed": False,
                        "created_at": task.created_at.isoformat()
                    }
                )
        except Exception as e:
            logger.error(f"Error adding task for user {user_id}: {str(e)}")
            return AddTaskResponse(
                success=False,
                error=str(e)
            )

    def list_tasks(self, user_id: str, status: str = "all") -> ListTasksResponse:
        """
        List tasks for a user with optional status filter

        Example usage:
        >>> manager = TaskManager()
        >>> result = manager.list_tasks("user123", "pending")
        >>> print(len(result.data['tasks']))
        2
        """
        try:
            with self.get_session() as session:
                # Build query based on status filter
                from sqlalchemy import and_
                query = select(Task).where(Task.user_id == user_id)

                if status == "pending":
                    query = query.where(Task.completed == False)
                elif status == "completed":
                    query = query.where(Task.completed == True)

                # Execute query
                tasks = session.exec(query).all()

                # Format response data
                task_list = []
                for task in tasks:
                    task_list.append({
                        "task_id": task.id,
                        "user_id": task.user_id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": task.updated_at.isoformat()
                    })

                logger.info(f"Retrieved {len(task_list)} tasks for user {user_id} (status: {status})")

                return ListTasksResponse(
                    success=True,
                    data={
                        "tasks": task_list,
                        "total_count": len(task_list),
                        "user_id": user_id,
                        "status_filter": status
                    }
                )
        except Exception as e:
            logger.error(f"Error listing tasks for user {user_id}: {str(e)}")
            return ListTasksResponse(
                success=False,
                error=str(e)
            )

    def complete_task(self, user_id: str, task_id: int) -> CompleteTaskResponse:
        """
        Mark a task as completed

        Example usage:
        >>> manager = TaskManager()
        >>> result = manager.complete_task("user123", 5)
        >>> print(result.success)
        True
        """
        try:
            with self.get_session() as session:
                # Find the task
                task = session.get(Task, task_id)

                # Check if task exists and belongs to user
                if not task:
                    return CompleteTaskResponse(
                        success=False,
                        error=f"Task with ID {task_id} not found"
                    )

                if task.user_id != user_id:
                    return CompleteTaskResponse(
                        success=False,
                        error="Unauthorized: Task does not belong to user"
                    )

                # Update task status
                task.completed = True
                task.updated_at = datetime.utcnow()
                session.add(task)
                session.commit()
                session.refresh(task)

                logger.info(f"Completed task {task_id} for user {user_id}")

                return CompleteTaskResponse(
                    success=True,
                    data={
                        "task_id": task.id,
                        "user_id": user_id,
                        "title": task.title,
                        "completed": task.completed,
                        "updated_at": task.updated_at.isoformat()
                    }
                )
        except Exception as e:
            logger.error(f"Error completing task {task_id} for user {user_id}: {str(e)}")
            return CompleteTaskResponse(
                success=False,
                error=str(e)
            )

    def delete_task(self, user_id: str, task_id: int) -> DeleteTaskResponse:
        """
        Delete a task from the database

        Example usage:
        >>> manager = TaskManager()
        >>> result = manager.delete_task("user123", 5)
        >>> print(result.success)
        True
        """
        try:
            with self.get_session() as session:
                # Find the task
                task = session.get(Task, task_id)

                # Check if task exists and belongs to user
                if not task:
                    return DeleteTaskResponse(
                        success=False,
                        error=f"Task with ID {task_id} not found"
                    )

                if task.user_id != user_id:
                    return DeleteTaskResponse(
                        success=False,
                        error="Unauthorized: Task does not belong to user"
                    )

                # Delete the task
                session.delete(task)
                session.commit()

                logger.info(f"Deleted task {task_id} for user {user_id}")

                return DeleteTaskResponse(
                    success=True,
                    data={
                        "task_id": task_id,
                        "user_id": user_id,
                        "deleted": True
                    }
                )
        except Exception as e:
            logger.error(f"Error deleting task {task_id} for user {user_id}: {str(e)}")
            return DeleteTaskResponse(
                success=False,
                error=str(e)
            )

    def update_task(self, user_id: str, task_id: int, title: str = None, description: str = None) -> UpdateTaskResponse:
        """
        Update a task's title or description

        Example usage:
        >>> manager = TaskManager()
        >>> result = manager.update_task("user123", 5, title="Updated title", description="Updated description")
        >>> print(result.success)
        True
        """
        try:
            with self.get_session() as session:
                # Find the task
                task = session.get(Task, task_id)

                # Check if task exists and belongs to user
                if not task:
                    return UpdateTaskResponse(
                        success=False,
                        error=f"Task with ID {task_id} not found"
                    )

                if task.user_id != user_id:
                    return UpdateTaskResponse(
                        success=False,
                        error="Unauthorized: Task does not belong to user"
                    )

                # Update task fields if provided
                if title is not None:
                    task.title = title
                if description is not None:
                    task.description = description

                task.updated_at = datetime.utcnow()
                session.add(task)
                session.commit()
                session.refresh(task)

                logger.info(f"Updated task {task_id} for user {user_id}")

                return UpdateTaskResponse(
                    success=True,
                    data={
                        "task_id": task.id,
                        "user_id": user_id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "updated_at": task.updated_at.isoformat()
                    }
                )
        except Exception as e:
            logger.error(f"Error updating task {task_id} for user {user_id}: {str(e)}")
            return UpdateTaskResponse(
                success=False,
                error=str(e)
            )


# Initialize the task manager
task_manager = TaskManager()


# MCP Tool Functions (these would be registered with the MCP framework)
async def add_task(request: AddTaskRequest) -> AddTaskResponse:
    """
    MCP Tool: Add a new task

    Parameters:
    - user_id: ID of the user
    - title: Title of the task
    - description: Optional description of the task

    Returns:
    - AddTaskResponse with success status and task data
    """
    try:
        result = task_manager.add_task(
            user_id=request.user_id,
            title=request.title,
            description=request.description
        )
        return result
    except Exception as e:
        logger.error(f"Error in add_task MCP tool: {str(e)}")
        return AddTaskResponse(
            success=False,
            error=str(e)
        )


async def list_tasks(request: ListTasksRequest) -> ListTasksResponse:
    """
    MCP Tool: List tasks for a user

    Parameters:
    - user_id: ID of the user
    - status: Filter status ("all", "pending", "completed")

    Returns:
    - ListTasksResponse with success status and task data
    """
    try:
        result = task_manager.list_tasks(
            user_id=request.user_id,
            status=request.status
        )
        return result
    except Exception as e:
        logger.error(f"Error in list_tasks MCP tool: {str(e)}")
        return ListTasksResponse(
            success=False,
            error=str(e)
        )


async def complete_task(request: CompleteTaskRequest) -> CompleteTaskResponse:
    """
    MCP Tool: Complete a task

    Parameters:
    - user_id: ID of the user
    - task_id: ID of the task to complete

    Returns:
    - CompleteTaskResponse with success status and updated task data
    """
    try:
        result = task_manager.complete_task(
            user_id=request.user_id,
            task_id=request.task_id
        )
        return result
    except Exception as e:
        logger.error(f"Error in complete_task MCP tool: {str(e)}")
        return CompleteTaskResponse(
            success=False,
            error=str(e)
        )


async def delete_task(request: DeleteTaskRequest) -> DeleteTaskResponse:
    """
    MCP Tool: Delete a task

    Parameters:
    - user_id: ID of the user
    - task_id: ID of the task to delete

    Returns:
    - DeleteTaskResponse with success status and deletion confirmation
    """
    try:
        result = task_manager.delete_task(
            user_id=request.user_id,
            task_id=request.task_id
        )
        return result
    except Exception as e:
        logger.error(f"Error in delete_task MCP tool: {str(e)}")
        return DeleteTaskResponse(
            success=False,
            error=str(e)
        )


async def update_task(request: UpdateTaskRequest) -> UpdateTaskResponse:
    """
    MCP Tool: Update a task

    Parameters:
    - user_id: ID of the user
    - task_id: ID of the task to update
    - title: New title (optional)
    - description: New description (optional)

    Returns:
    - UpdateTaskResponse with success status and updated task data
    """
    try:
        result = task_manager.update_task(
            user_id=request.user_id,
            task_id=request.task_id,
            title=request.title,
            description=request.description
        )
        return result
    except Exception as e:
        logger.error(f"Error in update_task MCP tool: {str(e)}")
        return UpdateTaskResponse(
            success=False,
            error=str(e)
        )


# Example usage
if __name__ == "__main__":
    import asyncio

    async def example():
        # Add a task
        add_req = AddTaskRequest(user_id="test_user", title="Buy groceries", description="Milk, bread, eggs")
        add_resp = await add_task(add_req)
        print(f"Add task result: {add_resp}")

        # List tasks
        list_req = ListTasksRequest(user_id="test_user", status="all")
        list_resp = await list_tasks(list_req)
        print(f"List tasks result: {list_resp}")

        if list_resp.success and list_resp.data and list_resp.data['tasks']:
            task_id = list_resp.data['tasks'][0]['task_id']

            # Complete the task
            complete_req = CompleteTaskRequest(user_id="test_user", task_id=task_id)
            complete_resp = await complete_task(complete_req)
            print(f"Complete task result: {complete_resp}")

            # Update the task
            update_req = UpdateTaskRequest(user_id="test_user", task_id=task_id, title="Updated task")
            update_resp = await update_task(update_req)
            print(f"Update task result: {update_resp}")

            # Delete the task
            delete_req = DeleteTaskRequest(user_id="test_user", task_id=task_id)
            delete_resp = await delete_task(delete_req)
            print(f"Delete task result: {delete_resp}")

    # Run the example
    asyncio.run(example())