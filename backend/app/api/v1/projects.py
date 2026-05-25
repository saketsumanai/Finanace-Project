"""
Project management API endpoints.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
import math

from app.core.database import get_db
from app.models.user import User
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectList, ProjectDetail
from app.api.deps import get_current_user


router = APIRouter()


@router.get("", response_model=ProjectList)
async def list_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None, pattern="^(draft|active|archived)$"),
    sort_by: str = Query("created_at", pattern="^(created_at|updated_at|name)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all projects for the authenticated user.
    
    Args:
        page: Page number (1-indexed)
        page_size: Number of items per page
        status: Filter by project status
        sort_by: Field to sort by
        sort_order: Sort order (asc or desc)
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Paginated list of projects
    """
    # Build query
    query = db.query(Project).filter(Project.owner_id == current_user.id)
    
    # Apply status filter
    if status:
        query = query.filter(Project.status == status)
    
    # Apply sorting
    sort_column = getattr(Project, sort_by)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    projects = query.offset(offset).limit(page_size).all()
    
    # Calculate total pages
    pages = math.ceil(total / page_size) if total > 0 else 1
    
    return ProjectList(
        items=[ProjectResponse.model_validate(p) for p in projects],
        total=total,
        page=page,
        page_size=page_size,
        pages=pages
    )


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new project.
    
    Args:
        project_data: Project creation data
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Created project
    """
    new_project = Project(
        owner_id=current_user.id,
        name=project_data.name,
        description=project_data.description,
        project_type=project_data.project_type,
        status="active"
    )
    
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return ProjectResponse.model_validate(new_project)


@router.get("/{project_id}", response_model=ProjectDetail)
async def get_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get project details by ID.
    
    Args:
        project_id: Project UUID
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Project details
    
    Raises:
        HTTPException: If project not found or access denied
    """
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # TODO: Get actual counts from related tables
    project_detail = ProjectDetail(
        **ProjectResponse.model_validate(project).model_dump(),
        files_count=0,
        scenarios_count=0
    )
    
    return project_detail


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update project details.
    
    Args:
        project_id: Project UUID
        project_data: Project update data
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Updated project
    
    Raises:
        HTTPException: If project not found or access denied
    """
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Update fields
    update_data = project_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    
    return ProjectResponse.model_validate(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a project and all associated data.
    
    Args:
        project_id: Project UUID
        current_user: Current authenticated user
        db: Database session
    
    Raises:
        HTTPException: If project not found or access denied
    """
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db.delete(project)
    db.commit()
    
    return None
