"""
AMK AI Coder Platform - Backend API
FastAPI for HuggingFace Spaces deployment
"""
import os
import json
from typing import List, Optional, Dict
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "inclusionai/ling-2.6-1t:free"

# System prompts
DEEP_THINKING_PROMPT = """You are an advanced AI coding assistant with enhanced deep thinking capabilities.
When analyzing problems, take time to:
1. Understand the core requirements
2. Consider edge cases and potential issues
3. Plan a structured approach
4. Write clean, efficient, and well-documented code
5. Explain your reasoning step by step

Provide comprehensive, thoughtful responses."""

STANDARD_PROMPT = """You are an AI coding assistant. Provide helpful, accurate, and efficient responses.
Write clean, well-documented code with appropriate comments."""

# In-memory conversation storage
conversations: Dict[str, List[dict]] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("AMK AI Coder Backend started!")
    yield

# Create FastAPI app
app = FastAPI(
    title="AMK AI Coder Backend API",
    description="Backend API for AMK AI Coder Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS - Allow specific origins for Vercel frontend
ALLOWED_ORIGINS = [
    "https://amk-coder.vercel.app",
    "https://*.vercel.app",
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    thinking_mode: bool = False
    model: str = DEFAULT_MODEL

class ChatResponse(BaseModel):
    response: str
    session_id: str
    thinking_mode: bool

# API Endpoints
@app.get("/")
async def root():
    return {"status": "ok", "message": "AMK AI Coder Backend API", "model": DEFAULT_MODEL}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "api_key_configured": bool(OPENROUTER_API_KEY)
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="OpenRouter API key not configured")

    # Get or create conversation
    session_id = request.session_id
    if session_id not in conversations:
        conversations[session_id] = []

    messages = conversations[session_id]

    # Add user message
    messages.append({"role": "user", "content": request.message})

    # Build system prompt
    system_prompt = DEEP_THINKING_PROMPT if request.thinking_mode else STANDARD_PROMPT

    # Build full context
    all_messages = [{"role": "system", "content": system_prompt}]
    all_messages.extend(messages[-20:])  # Keep last 20 messages

    # Call OpenRouter
    payload = {
        "model": request.model,
        "messages": all_messages,
        "temperature": 0.7,
        "max_tokens": 4096
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://amk-coder.vercel.app",
        "X-Title": "AMK AI Coder Platform"
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{OPENROUTER_API_URL}/chat/completions",
                headers=headers,
                json=payload
            )

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)

            data = response.json()
            assistant_message = data["choices"][0]["message"]["content"]

            # Add to conversation history
            messages.append({"role": "assistant", "content": assistant_message})

            return ChatResponse(
                response=assistant_message,
                session_id=session_id,
                thinking_mode=request.thinking_mode
            )

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/clear")
async def clear_chat(session_id: str = "default"):
    """Clear conversation history"""
    if session_id in conversations:
        conversations[session_id] = []
    return {"status": "cleared", "session_id": session_id}

@app.get("/api/history/{session_id}")
async def get_history(session_id: str = "default"):
    """Get conversation history"""
    return {"session_id": session_id, "messages": conversations.get(session_id, [])}