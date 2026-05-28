"""
Chat routes for AMK AI Coder Platform
OpenRouter integration with custom key handlers and thinking modes
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from typing import Union
import httpx
import json
from app.routes.auth import get_optional_user
from app.config import settings, get_api_key_for_provider
from app.utils.prompts import SYSTEM_PROMPT, DEEP_THINKING_SYSTEM_PROMPT

router = APIRouter()


class Message(BaseModel):
    """Chat message model"""
    role: str = Field(..., description="Message role: system, user, or assistant")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    messages: List[Message] = Field(default_factory=list, description="Conversation history")
    message: Optional[str] = Field(None, description="New message to send")
    thinking_mode: bool = Field(False, description="Enable deep thinking mode")
    custom_api_keys: Optional[Dict[str, str]] = Field(None, description="User's custom API keys")
    model: Optional[str] = Field(None, description="Specific model to use")
    temperature: Optional[float] = Field(0.7, description="Response temperature")
    max_tokens: Optional[int] = Field(4096, description="Maximum tokens in response")
    stream: bool = Field(True, description="Enable streaming responses")


class ChatResponse(BaseModel):
    """Response model for non-streaming chat"""
    content: str
    thinking: Optional[str] = None
    model: str
    usage: Optional[Dict[str, int]] = None


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None


def build_messages(request: ChatRequest) -> List[Dict[str, str]]:
    """
    Build messages array for AI API
    
    Args:
        request: Chat request with messages
        
    Returns:
        List of message dictionaries
    """
    messages = []
    
    # Add system prompt based on thinking mode
    if request.thinking_mode:
        messages.append({
            "role": "system",
            "content": DEEP_THINKING_SYSTEM_PROMPT
        })
    else:
        messages.append({
            "role": "system",
            "content": SYSTEM_PROMPT
        })
    
    # Add conversation history
    for msg in request.messages[-settings.MAX_CONTEXT_MESSAGES:]:
        if msg.role in ["user", "assistant", "system"]:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
    
    # Add new message if provided
    if request.message:
        messages.append({
            "role": "user",
            "content": request.message
        })
    
    return messages


async def call_openrouter(
    messages: List[Dict[str, str]],
    api_key: str,
    model: str,
    thinking_mode: bool = False,
    temperature: float = 0.7,
    max_tokens: int = 4096,
    stream: bool = True
):
    """
    Call OpenRouter API with streaming support
    
    Args:
        messages: List of message dictionaries
        api_key: OpenRouter API key
        model: Model identifier
        thinking_mode: Enable thinking mode
        temperature: Response temperature
        max_tokens: Maximum tokens
        stream: Enable streaming
        
    Yields:
        SSE-formatted response chunks
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://amk-ai.vercel.app",
        "X-Title": "AMK AI Coder Platform"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream
    }
    
    # Add thinking mode header if enabled
    if thinking_mode:
        payload["thinking"] = {"type": "enabled"}
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            async with client.stream(
                "POST",
                f"{settings.OPENROUTER_API_URL}/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                if response.status_code != 200:
                    error_text = await response.text()
                    yield f'data: {json.dumps({"error": f"API error: {response.status_code}", "detail": error_text})}\n\n'
                    return
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data != "[DONE]":
                            try:
                                chunk = json.loads(data)
                                if chunk.get("choices"):
                                    delta = chunk["choices"][0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        yield f'data: {json.dumps({"content": content})}\n\n'
                            except json.JSONDecodeError:
                                continue
                        else:
                            yield "data: [DONE]\n\n"
                            
        except httpx.TimeoutException:
            yield f'data: {json.dumps({"error": "Request timed out"})}\n\n'
        except httpx.HTTPError as e:
            yield f'data: {json.dumps({"error": str(e)})}\n\n'


async def call_gemini(
    messages: List[Dict[str, str]],
    api_key: str,
    model: str = "gemini-pro",
    temperature: float = 0.7,
    max_tokens: int = 4096
):
    """
    Call Google Gemini API
    
    Args:
        messages: List of message dictionaries
        api_key: Gemini API key
        model: Model to use
        temperature: Response temperature
        max_tokens: Maximum tokens
        
    Yields:
        Response chunks
    """
    # Extract the last user message for Gemini
    last_user_message = ""
    for msg in reversed(messages):
        if msg["role"] == "user":
            last_user_message = msg["content"]
            break
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [{"text": last_user_message}]
        }],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens
        }
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}",
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                yield f'data: {json.dumps({"error": f"Gemini API error: {response.status_code}"})}\n\n'
                return
            
            data = response.json()
            content = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            
            # Stream the content
            for char in content:
                yield f'data: {json.dumps({"content": char})}\n\n'
            
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            yield f'data: {json.dumps({"error": str(e)})}\n\n'


async def call_groq(
    messages: List[Dict[str, str]],
    api_key: str,
    model: str = "mixtral-8x7b-32768",
    temperature: float = 0.7,
    max_tokens: int = 4096,
    stream: bool = True
):
    """
    Call Groq API for fast inference
    
    Args:
        messages: List of message dictionaries
        api_key: Groq API key
        model: Model to use
        temperature: Response temperature
        max_tokens: Maximum tokens
        stream: Enable streaming
        
    Yields:
        SSE-formatted response chunks
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            async with client.stream(
                "POST",
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                if response.status_code != 200:
                    error_text = await response.text()
                    yield f'data: {json.dumps({"error": f"Groq API error: {response.status_code}", "detail": error_text})}\n\n'
                    return
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data != "[DONE]":
                            try:
                                chunk = json.loads(data)
                                if chunk.get("choices"):
                                    delta = chunk["choices"][0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        yield f'data: {json.dumps({"content": content})}\n\n'
                            except json.JSONDecodeError:
                                continue
                        else:
                            yield "data: [DONE]\n\n"
                            
        except Exception as e:
            yield f'data: {json.dumps({"error": str(e)})}\n\n'


def determine_provider_and_key(
    request: ChatRequest,
    user: Optional[dict] = None
) -> tuple[str, str]:
    """
    Determine which provider to use and get the API key
    
    Args:
        request: Chat request with custom keys
        user: Authenticated user info
        
    Returns:
        Tuple of (provider_name, api_key)
    """
    # Priority: custom user keys > environment keys
    
    # Check custom keys from request
    if request.custom_api_keys:
        if request.custom_api_keys.get("openrouter") and request.custom_api_keys["openrouter"].startswith("sk-"):
            return ("openrouter", request.custom_api_keys["openrouter"])
        if request.custom_api_keys.get("gemini") and request.custom_api_keys["gemini"].startswith("AIza"):
            return ("gemini", request.custom_api_keys["gemini"])
        if request.custom_api_keys.get("groq") and request.custom_api_keys["groq"].startswith("gsk_"):
            return ("groq", request.custom_api_keys["groq"])
    
    # Check environment keys
    if settings.OPENROUTER_API_KEY:
        return ("openrouter", settings.OPENROUTER_API_KEY)
    if settings.GROQ_API_KEY:
        return ("groq", settings.GROQ_API_KEY)
    
    raise HTTPException(
        status_code=400,
        detail="No API key configured. Please set your API key in the API Keys page."
    )


@router.post("")
async def chat(
    request: ChatRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Main chat endpoint with streaming support
    
    Args:
        request: Chat request with messages and options
        authorization: Optional Bearer token for authenticated requests
        
    Returns:
        StreamingResponse with SSE-formatted chunks
    """
    # Get optional user (for rate limiting, analytics, etc.)
    user = None
    if authorization:
        try:
            from app.routes.auth import verify_firebase_token
            if authorization.startswith("Bearer "):
                token = authorization.replace("Bearer ", "")
                user = await verify_firebase_token(token)
        except Exception:
            pass  # Continue without user auth
    
    # Build messages
    messages = build_messages(request)
    
    # Determine provider and get API key
    try:
        provider, api_key = determine_provider_and_key(request, user)
    except HTTPException as e:
        raise e
    
    # Get model
    if request.model:
        model = request.model
    elif provider == "openrouter":
        model = settings.OPENROUTER_MODEL
    elif provider == "groq":
        model = "mixtral-8x7b-32768"
    elif provider == "gemini":
        model = "gemini-pro"
    else:
        model = settings.OPENROUTER_MODEL
    
    # Call appropriate provider
    if provider == "openrouter":
        return StreamingResponse(
            call_openrouter(
                messages=messages,
                api_key=api_key,
                model=model,
                thinking_mode=request.thinking_mode,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                stream=request.stream
            ),
            media_type="text/event-stream"
        )
    elif provider == "gemini":
        return StreamingResponse(
            call_gemini(
                messages=messages,
                api_key=api_key,
                model=model,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            ),
            media_type="text/event-stream"
        )
    elif provider == "groq":
        return StreamingResponse(
            call_groq(
                messages=messages,
                api_key=api_key,
                model=model,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                stream=request.stream
            ),
            media_type="text/event-stream"
        )
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported provider: {provider}"
        )


@router.post("/non-stream")
async def chat_non_stream(
    request: ChatRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Non-streaming chat endpoint for specific use cases
    
    Args:
        request: Chat request with messages and options
        authorization: Optional Bearer token
        
    Returns:
        Complete response
    """
    content = ""
    
    async for chunk in call_openrouter(
        messages=build_messages(request),
        api_key=settings.OPENROUTER_API_KEY,
        model=request.model or settings.OPENROUTER_MODEL,
        thinking_mode=request.thinking_mode,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=False
    ):
        if chunk.startswith("data: "):
            data = json.loads(chunk[6:])
            if "content" in data:
                content += data["content"]
    
    return ChatResponse(
        content=content,
        thinking=None,
        model=request.model or settings.OPENROUTER_MODEL
    )


@router.get("/models")
async def list_models(
    authorization: Optional[str] = Header(None)
):
    """
    List available models for the current configuration
    
    Returns:
        List of available models
    """
    models = [
        {
            "id": "anthropic/claude-3.5-sonnet",
            "name": "Claude 3.5 Sonnet",
            "provider": "openrouter",
            "thinking_supported": True
        },
        {
            "id": "openai/gpt-4-turbo",
            "name": "GPT-4 Turbo",
            "provider": "openrouter",
            "thinking_supported": True
        },
        {
            "id": "google/gemini-pro",
            "name": "Gemini Pro",
            "provider": "gemini",
            "thinking_supported": False
        },
        {
            "id": "mixtral-8x7b-32768",
            "name": "Mixtral 8x7B",
            "provider": "groq",
            "thinking_supported": False
        },
        {
            "id": "meta-llama/llama-3-70b-versatile",
            "name": "Llama 3 70B",
            "provider": "groq",
            "thinking_supported": False
        }
    ]
    
    # Filter based on available keys
    available = []
    if settings.OPENROUTER_API_KEY:
        available.extend([m for m in models if m["provider"] == "openrouter"])
    if settings.GROQ_API_KEY:
        available.extend([m for m in models if m["provider"] == "groq"])
    if settings.GEMINI_API_KEY:
        available.extend([m for m in models if m["provider"] == "gemini"])
    
    return {"models": available}