from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional, List
import uuid
from datetime import datetime
from pydantic import BaseModel
import asyncio

# Database Models
class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: str = Field(index=True)
    user_id: str = Field(index=True)
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: str = Field(unique=True, index=True)
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Pydantic models for API
class ChatRequest(BaseModel):
    message: str


class ToolCall(BaseModel):
    name: str
    arguments: dict


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: List[ToolCall]


# Placeholder functions for AI agent and MCP tools
async def run_agent(user_id: str, conversation: List[dict], message: str) -> tuple[str, List[ToolCall]]:
    """
    Placeholder function to simulate AI agent processing
    In a real implementation, this would call an AI model to process the message
    """
    # Simple rule-based processing for demonstration
    user_message = message.lower()

    # Identify intent based on message content
    if "add" in user_message or "create" in user_message:
        # Extract task details (simplified)
        task_desc = message.replace("add", "").replace("create", "").replace("task", "").strip()
        if not task_desc:
            task_desc = "a new task"

        # Simulate calling add_task MCP tool
        tool_calls = [ToolCall(name="add_task", arguments={"user_id": user_id, "description": task_desc})]
        response = f"I've added the task '{task_desc}' to your list."

    elif "list" in user_message or "show" in user_message:
        # Simulate calling list_tasks MCP tool
        tool_calls = [ToolCall(name="list_tasks", arguments={"user_id": user_id})]
        response = f"Here are your tasks for user {user_id}."

    elif "complete" in user_message or "done" in user_message:
        # Simulate calling complete_task MCP tool
        tool_calls = [ToolCall(name="complete_task", arguments={"user_id": user_id, "task_id": 1})]
        response = f"I've marked the task as completed."

    elif "update" in user_message or "change" in user_message:
        # Simulate calling update_task MCP tool
        tool_calls = [ToolCall(name="update_task", arguments={"user_id": user_id, "task_id": 1, "updates": {}})]
        response = f"I've updated the task as requested."

    elif "delete" in user_message or "remove" in user_message:
        # Simulate calling delete_task MCP tool
        tool_calls = [ToolCall(name="delete_task", arguments={"user_id": user_id, "task_id": 1})]
        response = f"I've deleted the task."

    else:
        # Default response
        tool_calls = []
        response = f"I received your message: '{message}'. How can I help you with your tasks?"

    return response, tool_calls


# MCP Tools (Placeholder implementations)
async def add_task(user_id: str, description: str):
    """Placeholder for add_task MCP tool"""
    # In a real implementation, this would call the actual MCP tool
    return {"success": True, "task_id": 1, "description": description}


async def list_tasks(user_id: str):
    """Placeholder for list_tasks MCP tool"""
    # In a real implementation, this would call the actual MCP tool
    return {"success": True, "tasks": [{"id": 1, "description": "Sample task", "completed": False}]}


async def update_task(user_id: str, task_id: int, updates: dict):
    """Placeholder for update_task MCP tool"""
    # In a real implementation, this would call the actual MCP tool
    return {"success": True, "task_id": task_id, "updates": updates}


async def delete_task(user_id: str, task_id: int):
    """Placeholder for delete_task MCP tool"""
    # In a real implementation, this would call the actual MCP tool
    return {"success": True, "task_id": task_id}


async def complete_task(user_id: str, task_id: int):
    """Placeholder for complete_task MCP tool"""
    # In a real implementation, this would call the actual MCP tool
    return {"success": True, "task_id": task_id, "status": "completed"}


# Database setup - try PostgreSQL first, fallback to SQLite
try:
    from sqlmodel import create_engine
    DATABASE_URL = "postgresql://user:password@localhost:5432/todo_chatbot"
    engine = create_engine(DATABASE_URL)
    # Test the connection
    with engine.connect() as conn:
        pass
except Exception as e:
    # If PostgreSQL fails, fallback to SQLite
    print(f"PostgreSQL connection failed: {e}. Falling back to SQLite.")
    DATABASE_URL = "sqlite:///./todo_chatbot.db"
    from sqlmodel import create_engine
    engine = create_engine(DATABASE_URL)

async def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)


# Dependency for database session
async def get_session():
    with Session(engine) as session:
        yield session


# FastAPI app
app = FastAPI(
    title="Todo AI Chatbot API",
    description="AI-powered todo chatbot with conversation persistence",
    version="1.0.0"
)


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


@app.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat(user_id: str, request: ChatRequest, session: Session = Depends(get_session)):
    """
    Main chat endpoint for the Todo AI Chatbot
    """
    try:
        # Generate or retrieve conversation ID
        conversation_id = str(uuid.uuid4())

        # Load conversation from database (in a real implementation,
        # you would retrieve existing conversation if it exists)
        statement = select(Message).where(Message.user_id == user_id).order_by(Message.timestamp)
        results = session.exec(statement).all()

        # Format conversation history for the agent
        conversation = []
        for msg in results:
            conversation.append({
                "role": msg.role,
                "content": msg.content
            })

        # Add user message to conversation
        user_message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="user",
            content=request.message
        )
        session.add(user_message)
        session.commit()
        session.refresh(user_message)

        # Call the AI agent
        response_text, tool_calls = await run_agent(user_id, conversation, request.message)

        # Add assistant response to conversation
        assistant_message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="assistant",
            content=response_text
        )
        session.add(assistant_message)
        session.commit()

        # Execute MCP tools if needed
        for tool_call in tool_calls:
            if tool_call.name == "add_task":
                await add_task(tool_call.arguments.get("user_id"),
                               tool_call.arguments.get("description", ""))
            elif tool_call.name == "list_tasks":
                await list_tasks(tool_call.arguments.get("user_id"))
            elif tool_call.name == "update_task":
                await update_task(
                    tool_call.arguments.get("user_id"),
                    tool_call.arguments.get("task_id", 1),
                    tool_call.arguments.get("updates", {})
                )
            elif tool_call.name == "delete_task":
                await delete_task(
                    tool_call.arguments.get("user_id"),
                    tool_call.arguments.get("task_id", 1)
                )
            elif tool_call.name == "complete_task":
                await complete_task(
                    tool_call.arguments.get("user_id"),
                    tool_call.arguments.get("task_id", 1)
                )

        # Return the response
        return ChatResponse(
            conversation_id=conversation_id,
            response=response_text,
            tool_calls=tool_calls
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Todo AI Chatbot API is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "todo-ai-chatbot"}