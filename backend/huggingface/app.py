"""
AMK AI Coder Platform - Backend API
Gradio app for HuggingFace Spaces deployment
"""
import os
import json
import asyncio
from typing import Optional, List, Dict, Any
from functools import lru_cache

import httpx
import gradio as gr
from gradio import Blocks, Textbox, Dropdown, Button, Chatbot

# Configuration from environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "deepseek/deepseek-v4-flash"

# Deep thinking system prompt
DEEP_THINKING_PROMPT = """You are an advanced AI coding assistant with enhanced deep thinking capabilities.
When analyzing problems, take time to:
1. Understand the core requirements
2. Consider edge cases and potential issues
3. Plan a structured approach
4. Write clean, efficient, and well-documented code
5. Explain your reasoning step by step

Provide comprehensive, thoughtful responses that demonstrate deep analysis."""

STANDARD_PROMPT = """You are an AI coding assistant. Provide helpful, accurate, and efficient responses.
Write clean, well-documented code with appropriate comments."""


class ChatSession:
    """Manages chat sessions with AI providers"""
    
    def __init__(self, api_key: str = ""):
        self.api_key = api_key or OPENROUTER_API_KEY
        self.messages: List[Dict[str, str]] = []
        self.use_deep_thinking = False
    
    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
    
    def get_context(self, system_prompt: str = STANDARD_PROMPT) -> List[Dict[str, str]]:
        context = [{"role": "system", "content": system_prompt}]
        context.extend(self.messages[-20:])  # Keep last 20 messages
        return context
    
    async def send_to_openrouter(
        self, 
        message: str, 
        model: str = DEFAULT_MODEL,
        stream: bool = True
    ) -> str:
        """Send message to OpenRouter API"""
        if not self.api_key:
            return "Error: OpenRouter API key not configured. Please set OPENROUTER_API_KEY."
        
        self.add_message("user", message)
        
        system_prompt = DEEP_THINKING_PROMPT if self.use_deep_thinking else STANDARD_PROMPT
        payload = {
            "model": model,
            "messages": self.get_context(system_prompt),
            "stream": stream,
            "temperature": 0.7,
            "max_tokens": 4096
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
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
                
                if response.status_code == 200:
                    data = response.json()
                    assistant_message = data["choices"][0]["message"]["content"]
                    self.add_message("assistant", assistant_message)
                    return assistant_message
                else:
                    error_msg = f"API Error: {response.status_code} - {response.text}"
                    return error_msg
                    
        except Exception as e:
            return f"Error: {str(e)}"
    
    def clear(self):
        self.messages = []


# Global chat session
chat_session = ChatSession()


def toggle_deep_thinking(enabled: bool):
    """Toggle deep thinking mode"""
    chat_session.use_deep_thinking = enabled


async def chat_response(
    message: str, 
    history: List[List[str]],
    model: str,
    deep_thinking: bool
) -> tuple:
    """Generate chat response"""
    chat_session.use_deep_thinking = deep_thinking
    
    response = await chat_session.send_to_openrouter(
        message=message,
        model=model,
        stream=False
    )
    
    history.append([message, response])
    return "", history


def clear_chat():
    """Clear chat history"""
    chat_session.clear()
    return []


# Gradio UI
with gr.Blocks(
    title="AMK AI Coder Backend",
    theme=gr.themes.Soft(
        primary_hue="indigo",
        secondary_hue="purple",
    )
) as demo:
    gr.Markdown("""
    # 🤖 AMK AI Coder Backend API
    
    Powered by **OpenRouter** with support for multiple AI models.
    
    ### Features:
    - 💬 Chat with AI models
    - 🧠 Deep Thinking Mode for complex problems
    - 📝 Code-focused responses
    """)
    
    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="Chat", height=400)
            
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="Ask me anything about coding...",
                    scale=4,
                    lines=3
                )
                submit_btn = gr.Button("Send", variant="primary", scale=1)
        
        with gr.Column(scale=1):
            model_dropdown = gr.Dropdown(
                choices=[
                    "anthropic/claude-3.5-sonnet",
                    "anthropic/claude-3-haiku",
                    "openai/gpt-4-turbo",
                    "google/gemini-pro",
                    "mistralai/mixtral-8x7b-instruct"
                ],
                value="anthropic/claude-3.5-sonnet",
                label="AI Model"
            )
            
            deep_thinking = gr.Checkbox(
                label="🧠 Deep Thinking Mode",
                info="Enable for complex problem solving"
            )
            
            clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary")
            
            gr.Markdown("""
            ### API Endpoints
            
            This backend provides:
            - `/chat` - Chat completions
            - `/models` - Available models
            
            ### Setup
            
            Set `OPENROUTER_API_KEY` in environment variables.
            """)
    
    # Event handlers
    submit_btn.click(
        fn=chat_response,
        inputs=[msg, chatbot, model_dropdown, deep_thinking],
        outputs=[msg, chatbot]
    )
    
    msg.submit(
        fn=chat_response,
        inputs=[msg, chatbot, model_dropdown, deep_thinking],
        outputs=[msg, chatbot]
    )
    
    clear_btn.click(
        fn=clear_chat,
        outputs=[chatbot]
    )

# Launch
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
