"""
Project Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    """Base project schema with common attributes."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    project_type: str = Field(..., min_length=1, max_length=50)


class ProjectCreate(ProjectBase):
    """Schema for project creation."""
    pass


class ProjectUpdate(BaseModel):
    """Schema for project update."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(draft|active|archived)$")


class ProjectResponse(ProjectBase):
    """Schema for project response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    owner_id: int
    status: str
    created_at: datetime
    updated_at: datetime


class ProjectDetail(ProjectResponse):
    """Schema for detailed project response with counts."""
    files_count: int = 0
    scenarios_count: int = 0


class ProjectList(BaseModel):
    """Schema for paginated project list."""
    items: list[ProjectResponse]
    total: int
    page: int
    page_size: int
    pages: int
