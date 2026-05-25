"""
Financial data database model.
"""
from sqlalchemy import Column, Date, DateTime, ForeignKey, Float, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class FinancialData(Base):
    """Model for financial data."""
    
    __tablename__ = "financial_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    file_id = Column(Integer, ForeignKey("uploaded_files.id", ondelete="SET NULL"))
    date = Column(Date, nullable=False, index=True)
    revenue = Column(Float)
    operating_cost = Column(Float)
    capex = Column(Float)
    opex = Column(Float)
    taxes = Column(Float)
    royalties = Column(Float)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    project = relationship("Project", backref="financial_data")
    file = relationship("UploadedFile")
    
    def __repr__(self):
        return f"<FinancialData(project_id={self.project_id}, date={self.date})>"
