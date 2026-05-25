"""
Uploaded file database model.
"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, DECIMAL, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class UploadedFile(Base):
    """Model for tracking uploaded files."""
    
    __tablename__ = "uploaded_files"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)  # production, financial, other
    file_size = Column(Integer, nullable=False)
    file_path = Column(String(500), nullable=False)
    status = Column(String(50), nullable=False, default="pending")  # pending, processing, completed, failed
    error_message = Column(Text)
    quality_score = Column(DECIMAL(5, 2))
    uploaded_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    processed_at = Column(DateTime(timezone=True))
    
    # Relationships
    project = relationship("Project", backref="uploaded_files")
    uploader = relationship("User")
    
    def __repr__(self):
        return f"<UploadedFile(id={self.id}, filename={self.filename}, status={self.status})>"
