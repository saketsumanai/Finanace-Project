"""
Firebase Authentication API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
import os

from app.core.database import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.user import Token, UserResponse
from app.services.firebase_token_verifier import get_token_verifier


router = APIRouter()


class GoogleAuthRequest(BaseModel):
    """Google authentication request."""
    id_token: str
    email: EmailStr
    full_name: str
    profile_picture: Optional[str] = None


class FirebaseLoginRequest(BaseModel):
    """Firebase login request."""
    id_token: str
    email: EmailStr


class FirebaseRegisterRequest(BaseModel):
    """Firebase register request."""
    id_token: str
    email: EmailStr
    full_name: str


@router.post("/google", response_model=Token)
async def google_auth(
    data: GoogleAuthRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate with Google using Firebase ID token.
    """
    try:
        # Get project ID from environment
        project_id = os.getenv('FIREBASE_PROJECT_ID', 'oil-gas-f78c8')
        
        # Verify Firebase ID token using our custom verifier
        verifier = get_token_verifier(project_id)
        decoded_token = verifier.verify_id_token(data.id_token)
        
        firebase_uid = decoded_token['sub']
        email = decoded_token.get('email')
        
        if email != data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email mismatch"
            )
        
        # Check if user exists
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            # Create new user
            user = User(
                email=email,
                full_name=data.full_name,
                hashed_password="",
                google_id=firebase_uid,
                oauth_provider="google",
                profile_picture=data.profile_picture,
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # Update existing user
            if not user.google_id:
                user.google_id = firebase_uid
                user.oauth_provider = "google"
                if data.profile_picture:
                    user.profile_picture = data.profile_picture
                db.commit()
                db.refresh(user)
        
        # Create JWT access token
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
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication error: {str(e)}"
        )


@router.post("/firebase-login", response_model=Token)
async def firebase_login(
    data: FirebaseLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login with Firebase email/password authentication.
    """
    try:
        # Get project ID from environment
        project_id = os.getenv('FIREBASE_PROJECT_ID', 'oil-gas-f78c8')
        
        # Verify Firebase ID token
        verifier = get_token_verifier(project_id)
        decoded_token = verifier.verify_id_token(data.id_token)
        
        email = decoded_token.get('email')
        
        if email != data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email mismatch"
            )
        
        # Check if user exists
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found. Please register first."
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User account is inactive"
            )
        
        # Create JWT access token
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
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login error: {str(e)}"
        )


@router.post("/firebase-register", response_model=Token)
async def firebase_register(
    data: FirebaseRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register with Firebase email/password authentication.
    """
    try:
        # Get project ID from environment
        project_id = os.getenv('FIREBASE_PROJECT_ID', 'oil-gas-f78c8')
        
        # Verify Firebase ID token
        verifier = get_token_verifier(project_id)
        decoded_token = verifier.verify_id_token(data.id_token)
        
        firebase_uid = decoded_token['sub']
        email = decoded_token.get('email')
        
        if email != data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email mismatch"
            )
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Create new user
        user = User(
            email=email,
            full_name=data.full_name,
            hashed_password="",
            google_id=firebase_uid,
            oauth_provider="firebase",
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create JWT access token
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
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration error: {str(e)}"
        )

