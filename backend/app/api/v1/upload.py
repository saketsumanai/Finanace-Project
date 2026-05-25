"""
File upload API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.uploaded_file import UploadedFile
from app.services.file_service import FileService
from app.tasks.etl_tasks import process_uploaded_file
from app.api.deps import get_current_user
from app.services.data_generator import data_generator


router = APIRouter()
file_service = FileService()


@router.post("/generate-smart-data", status_code=status.HTTP_201_CREATED)
async def generate_smart_data(
    project_id: int = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate realistic production and financial data using AI.
    
    This endpoint uses smart algorithms to create realistic data based on
    project characteristics (deal size, project type).
    
    Args:
        project_id: Project ID
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Generated data summary
    """
    # Verify project exists and belongs to user
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Generate smart data based on project characteristics
    generated_data = data_generator.generate_smart_data(
        project_id=project_id,
        project_type=project.project_type or 'Acquisition',
        deal_size=float(project.deal_size or 50000000)
    )
    
    # Import models
    from app.models.production_data import ProductionData
    from app.models.financial_data import FinancialData
    
    # Insert production data
    for prod_data in generated_data['production']:
        prod_record = ProductionData(**prod_data)
        db.add(prod_record)
    
    # Insert financial data
    for fin_data in generated_data['financial']:
        fin_record = FinancialData(**fin_data)
        db.add(fin_record)
    
    db.commit()
    
    return {
        'success': True,
        'message': 'Smart data generated successfully using AI',
        'production_records': len(generated_data['production']),
        'financial_records': len(generated_data['financial']),
        'metadata': generated_data['metadata']
    }


@router.post("/production", status_code=status.HTTP_202_ACCEPTED)
async def upload_production_data(
    file: UploadFile = File(...),
    project_id: int = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload production data file (CSV or XLSX).
    
    Args:
        file: Uploaded file
        project_id: Project ID
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        File upload status and task ID
    """
    # Verify project exists and belongs to user
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Validate file
    is_valid, error_message = file_service.validate_file(file)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )
    
    # Save file
    file_path, unique_filename = await file_service.save_file(file, str(project_id))
    file_size = file_service.get_file_size(file_path)
    
    # Create file record
    file_record = UploadedFile(
        project_id=project_id,
        filename=file.filename,
        file_type='production',
        file_size=file_size,
        file_path=file_path,
        status='pending',
        uploaded_by=current_user.id
    )
    
    db.add(file_record)
    db.commit()
    db.refresh(file_record)
    
    # Queue background processing task (if celery is configured)
    # task = process_uploaded_file.delay(file_record.id)
    
    return {
        'file_id': file_record.id,
        'filename': file.filename,
        'file_size': file_size,
        'status': 'pending',
        'message': 'File uploaded successfully.'
    }


@router.post("/financials", status_code=status.HTTP_202_ACCEPTED)
async def upload_financial_data(
    file: UploadFile = File(...),
    project_id: int = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload financial data file (CSV or XLSX).
    
    Args:
        file: Uploaded file
        project_id: Project ID
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        File upload status and task ID
    """
    # Verify project exists and belongs to user
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Validate file
    is_valid, error_message = file_service.validate_file(file)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )
    
    # Save file
    file_path, unique_filename = await file_service.save_file(file, str(project_id))
    file_size = file_service.get_file_size(file_path)
    
    # Create file record
    file_record = UploadedFile(
        project_id=project_id,
        filename=file.filename,
        file_type='financial',
        file_size=file_size,
        file_path=file_path,
        status='pending',
        uploaded_by=current_user.id
    )
    
    db.add(file_record)
    db.commit()
    db.refresh(file_record)
    
    # Queue background processing task (if celery is configured)
    # task = process_uploaded_file.delay(file_record.id)
    
    return {
        'file_id': file_record.id,
        'filename': file.filename,
        'file_size': file_size,
        'status': 'pending',
        'message': 'File uploaded successfully.'
    }


@router.get("/{file_id}/status")
async def get_file_status(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get file processing status.
    
    Args:
        file_id: File ID
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        File processing status
    """
    # Get file record
    file_record = db.query(UploadedFile).filter(UploadedFile.id == file_id).first()
    
    if not file_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Verify user has access to this file's project
    project = db.query(Project).filter(
        Project.id == file_record.project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return {
        'file_id': file_record.id,
        'filename': file_record.filename,
        'status': file_record.status,
        'quality_score': float(file_record.quality_score) if file_record.quality_score else None,
        'error_message': file_record.error_message,
        'created_at': file_record.created_at.isoformat(),
        'processed_at': file_record.processed_at.isoformat() if file_record.processed_at else None
    }


@router.get("/project/{project_id}")
async def list_project_files(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all files for a project.
    
    Args:
        project_id: Project ID
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        List of files
    """
    # Verify project exists and belongs to user
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Get all files for project
    files = db.query(UploadedFile).filter(
        UploadedFile.project_id == project_id
    ).order_by(UploadedFile.created_at.desc()).all()
    
    return {
        'project_id': project_id,
        'files': [
            {
                'file_id': f.id,
                'filename': f.filename,
                'file_type': f.file_type,
                'file_size': f.file_size,
                'status': f.status,
                'quality_score': float(f.quality_score) if f.quality_score else None,
                'created_at': f.created_at.isoformat()
            }
            for f in files
        ]
    }
