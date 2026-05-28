"""
Authentication routes for AMK AI Coder Platform
Firebase JWT verification middleware
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional
import firebase_admin
from firebase_admin import credentials, auth
from app.config import settings, get_firebase_credentials

router = APIRouter()
security = HTTPBearer(auto_error=False)


class TokenVerificationRequest(BaseModel):
    """Request model for token verification"""
    id_token: str


class TokenVerificationResponse(BaseModel):
    """Response model for token verification"""
    valid: bool
    user_id: Optional[str] = None
    email: Optional[str] = None
    email_verified: bool = False


class AuthStatusResponse(BaseModel):
    """Response model for auth status check"""
    authenticated: bool
    user_id: Optional[str] = None
    email: Optional[str] = None
    provider: Optional[str] = None


# Initialize Firebase Admin SDK
firebase_initialized = False

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    global firebase_initialized
    if firebase_initialized:
        return True
    
    creds_dict = get_firebase_credentials()
    if creds_dict:
        try:
            cred = credentials.Certificate(creds_dict)
            firebase_admin.initialize_app(cred)
            firebase_initialized = True
            return True
        except Exception as e:
            print(f"Firebase initialization failed: {e}")
            return False
    return False


async def verify_firebase_token(id_token: str) -> dict:
    """
    Verify Firebase ID token and return user info
    
    Args:
        id_token: Firebase ID token string
        
    Returns:
        User information dictionary
        
    Raises:
        HTTPException: If token verification fails
    """
    if not initialize_firebase():
        raise HTTPException(
            status_code=503,
            detail="Firebase authentication not configured"
        )
    
    try:
        decoded_token = auth.verify_id_token(id_token)
        return {
            "uid": decoded_token.get("uid"),
            "email": decoded_token.get("email"),
            "email_verified": decoded_token.get("email_verified", False),
            "name": decoded_token.get("name"),
            "picture": decoded_token.get("picture"),
            "provider": decoded_token.get("firebase", {}).get("sign_in_provider", "unknown")
        }
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except auth.InvalidIdTokenError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Token verification failed: {str(e)}"
        )


async def get_current_user(
    authorization: Optional[str] = Header(None)
) -> dict:
    """
    Dependency to get current authenticated user
    
    Args:
        authorization: Authorization header with Bearer token
        
    Returns:
        User information dictionary
        
    Raises:
        HTTPException: If not authenticated
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header required"
        )
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization format. Use: Bearer <token>"
        )
    
    token = authorization.replace("Bearer ", "")
    return await verify_firebase_token(token)


async def get_optional_user(
    authorization: Optional[str] = Header(None)
) -> Optional[dict]:
    """
    Optional user dependency - returns None if not authenticated
    
    Args:
        authorization: Authorization header with Bearer token
        
    Returns:
        User information or None
    """
    if not authorization:
        return None
    
    try:
        if not authorization.startswith("Bearer "):
            return None
        token = authorization.replace("Bearer ", "")
        return await verify_firebase_token(token)
    except HTTPException:
        return None


@router.post("/verify", response_model=TokenVerificationResponse)
async def verify_token(request: TokenVerificationRequest):
    """
    Verify a Firebase ID token
    
    Args:
        request: Token verification request with ID token
        
    Returns:
        Token verification result with user info
    """
    try:
        user_info = await verify_firebase_token(request.id_token)
        return TokenVerificationResponse(
            valid=True,
            user_id=user_info.get("uid"),
            email=user_info.get("email"),
            email_verified=user_info.get("email_verified", False)
        )
    except HTTPException:
        return TokenVerificationResponse(valid=False)


@router.get("/status", response_model=AuthStatusResponse)
async def auth_status(user: dict = Depends(get_current_user)):
    """
    Get current authentication status
    
    Args:
        user: Current authenticated user
        
    Returns:
        Authentication status with user info
    """
    return AuthStatusResponse(
        authenticated=True,
        user_id=user.get("uid"),
        email=user.get("email"),
        provider=user.get("provider")
    )


@router.post("/refresh")
async def refresh_token(user: dict = Depends(get_current_user)):
    """
    Refresh the session by validating the current token
    
    Args:
        user: Current authenticated user
        
    Returns:
        Success message
    """
    return {
        "status": "ok",
        "message": "Session refreshed",
        "user_id": user.get("uid")
    }


@router.get("/me")
async def get_user_info(user: dict = Depends(get_current_user)):
    """
    Get detailed user information
    
    Args:
        user: Current authenticated user
        
    Returns:
        Full user information
    """
    return {
        "uid": user.get("uid"),
        "email": user.get("email"),
        "email_verified": user.get("email_verified"),
        "name": user.get("name"),
        "picture": user.get("picture"),
        "provider": user.get("provider")
    }


@router.get("/health")
async def auth_health():
    """
    Check authentication service health
    
    Returns:
        Health status
    """
    firebase_status = "configured" if initialize_firebase() else "not configured"
    
    return {
        "status": "healthy",
        "firebase": firebase_status,
        "requires_auth": bool(settings.FIREBASE_PROJECT_ID)
    }