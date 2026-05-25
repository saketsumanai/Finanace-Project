"""
Authentication API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.api.deps import get_current_user


router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.
    
    Args:
        user_data: User registration data
        db: Database session
    
    Returns:
        Created user
    
    Raises:
        HTTPException: If email already exists
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role="analyst"  # Default role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    
    Args:
        credentials: User login credentials
        db: Database session
    
    Returns:
        JWT token and user information
    
    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account"
        )
    
    # Create access token
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information.
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        User information
    """
    return current_user


@router.get("/google/login")
async def google_login():
    """
    Initiate Google OAuth login flow.
    
    Returns:
        Redirect URL to Google OAuth consent screen
    """
    from urllib.parse import urlencode
    
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    
    return {"auth_url": auth_url}


@router.get("/google/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):
    """
    Handle Google OAuth callback.
    
    Args:
        code: Authorization code from Google
        db: Database session
    
    Returns:
        JWT token and user information
    
    Raises:
        HTTPException: If OAuth flow fails
    """
    import httpx
    from fastapi.responses import RedirectResponse
    
    # Exchange code for access token
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    
    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, data=token_data)
        
        if token_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to obtain access token from Google"
            )
        
        tokens = token_response.json()
        access_token = tokens.get("access_token")
        
        # Get user info from Google
        userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        userinfo_response = await client.get(userinfo_url, headers=headers)
        
        if userinfo_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user info from Google"
            )
        
        user_info = userinfo_response.json()
    
    # Check if user exists
    google_id = user_info.get("id")
    email = user_info.get("email")
    full_name = user_info.get("name", email.split("@")[0])
    profile_picture = user_info.get("picture")
    
    user = db.query(User).filter(
        (User.google_id == google_id) | (User.email == email)
    ).first()
    
    if user:
        # Update existing user
        if not user.google_id:
            user.google_id = google_id
            user.oauth_provider = "google"
        if profile_picture:
            user.profile_picture = profile_picture
        db.commit()
        db.refresh(user)
    else:
        # Create new user
        user = User(
            email=email,
            full_name=full_name,
            google_id=google_id,
            oauth_provider="google",
            profile_picture=profile_picture,
            role="analyst",
            hashed_password=None  # No password for OAuth users
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Create JWT token
    jwt_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }
    )
    
    # Redirect to frontend with token
    redirect_url = f"{settings.FRONTEND_URL}/auth/callback?token={jwt_token}"
    return RedirectResponse(url=redirect_url)
