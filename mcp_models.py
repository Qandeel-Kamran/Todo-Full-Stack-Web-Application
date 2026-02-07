"""
Models for MCP Tools in Todo AI Chatbot
Defines the request/response models for all task operations
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class TaskStatus(str Enum):
    """Enumeration for task statuses"""
    ALL = "all"
    PENDING = "pending"
    COMPLETED = "completed"


class AddTaskRequest(BaseModel):
    """Request model for adding a task"""
    user_id: str
    title: str
    description: Optional[str] = None


class AddTaskResponse(BaseModel):
    """Response model for adding a task"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class ListTasksRequest(BaseModel):
    """Request model for listing tasks"""
    user_id: str
    status: TaskStatus = TaskStatus.ALL


class ListTasksResponse(BaseModel):
    """Response model for listing tasks"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class CompleteTaskRequest(BaseModel):
    """Request model for completing a task"""
    user_id: str
    task_id: int


class CompleteTaskResponse(BaseModel):
    """Response model for completing a task"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class DeleteTaskRequest(BaseModel):
    """Request model for deleting a task"""
    user_id: str
    task_id: int


class DeleteTaskResponse(BaseModel):
    """Response model for deleting a task"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class UpdateTaskRequest(BaseModel):
    """Request model for updating a task"""
    user_id: str
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None


class UpdateTaskResponse(BaseModel):
    """Response model for updating a task"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None