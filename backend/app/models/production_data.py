"""
Production data database model.
"""
from sqlalchemy import Column, Date, DateTime, ForeignKey, Float, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class ProductionData(Base):
    """Model for oil and gas production data."""
    
    __tablename__ = "production_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    file_id = Column(Integer, ForeignKey("uploaded_files.id", ondelete="SET NULL"))
    date = Column(Date, nullable=False, index=True)
    well_name = Column(String)
    oil_volume = Column(Float)  # barrels
    gas_volume = Column(Float)  # MCF
    water_volume = Column(Float)  # barrels
    oil_price = Column(Float)  # USD per barrel
    gas_price = Column(Float)  # USD per MCF
    ngl_price = Column(Float)  # USD per gallon
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    project = relationship("Project", backref="production_data")
    file = relationship("UploadedFile")
    
    def __repr__(self):
        return f"<ProductionData(project_id={self.project_id}, date={self.date}, well={self.well_name})>"
