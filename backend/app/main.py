"""
AMK AI Coder Platform - Backend Application
FastAPI application for AI chat with Firebase authentication
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, chat

# Create FastAPI application
app = FastAPI(
    title="AMK AI Coder Platform API",
    description="Backend API for AMK AI Coder Platform with Firebase authentication and OpenRouter integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://*.vercel.app",
        "https://*.amk-ai.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AMK AI Coder Platform API",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "api": "operational",
            "firebase": "configured" if os.getenv("FIREBASE_PROJECT_ID") else "not configured",
            "openrouter": "configured" if os.getenv("OPENROUTER_API_KEY") else "not configured"
        }
    }

# Import os for environment check
import os