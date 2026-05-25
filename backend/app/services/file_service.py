"""
File upload and storage service.
"""
import os
import uuid
from typing import Tuple
from fastapi import UploadFile
from werkzeug.utils import secure_filename

from app.core.config import settings


class FileService:
    """Service for handling file uploads and storage."""
    
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        self.max_file_size = settings.MAX_UPLOAD_SIZE
        self.allowed_extensions = settings.ALLOWED_EXTENSIONS
        
        # Create upload directory if it doesn't exist
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def validate_file(self, file: UploadFile) -> Tuple[bool, str]:
        """
        Validate uploaded file.
        
        Args:
            file: Uploaded file
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if file exists
        if not file or not file.filename:
            return False, "No file provided"
        
        # Check file extension
        file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        if file_extension not in self.allowed_extensions:
            return False, f"File type not allowed. Allowed types: {', '.join(self.allowed_extensions)}"
        
        # Check file size (if available)
        if hasattr(file, 'size') and file.size and file.size > self.max_file_size:
            return False, f"File too large. Maximum size: {self.max_file_size / 1024 / 1024:.0f}MB"
        
        return True, ""
    
    async def save_file(self, file: UploadFile, project_id: str) -> Tuple[str, str]:
        """
        Save uploaded file to disk.
        
        Args:
            file: Uploaded file
            project_id: Project UUID
        
        Returns:
            Tuple of (file_path, unique_filename)
        """
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
        unique_filename = f"{uuid.uuid4()}_{original_filename}"
        
        # Create project-specific directory
        project_dir = os.path.join(self.upload_dir, str(project_id))
        os.makedirs(project_dir, exist_ok=True)
        
        # Full file path
        file_path = os.path.join(project_dir, unique_filename)
        
        # Save file
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        return file_path, unique_filename
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete file from disk.
        
        Args:
            file_path: Path to file
        
        Returns:
            True if deleted successfully
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False
    
    def get_file_size(self, file_path: str) -> int:
        """
        Get file size in bytes.
        
        Args:
            file_path: Path to file
        
        Returns:
            File size in bytes
        """
        if os.path.exists(file_path):
            return os.path.getsize(file_path)
        return 0
