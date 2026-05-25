"""
User database model.
"""
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    """User model for authentication and authorization."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=True)  # Nullable for Google OAuth users
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="analyst", index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # OAuth fields
    google_id = Column(String(255), unique=True, nullable=True, index=True)
    oauth_provider = Column(String(50), nullable=True)  # 'google', 'github', etc.
    profile_picture = Column(String(500), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
