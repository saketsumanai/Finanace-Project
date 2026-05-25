"""
Project database model.
"""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Project(Base):
    """Project model for M&A valuation projects."""
    
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    project_type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="active", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    owner = relationship("User", backref="projects")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name}, status={self.status})>"
