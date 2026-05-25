"""
Celery tasks for ETL processing.
"""
from app.tasks import celery_app
from app.core.database import SessionLocal
from app.models.uploaded_file import UploadedFile
from app.models.production_data import ProductionData
from app.models.financial_data import FinancialData
from app.services.etl_service import ETLService
import logging

logger = logging.getLogger(__name__)


@celery_app.task(bind=True)
def process_uploaded_file(self, file_id: str):
    """
    Process uploaded file in background.
    
    Args:
        file_id: UUID of uploaded file
    
    Returns:
        Dict with processing results
    """
    db = SessionLocal()
    etl_service = ETLService()
    
    try:
        # Update task state
        self.update_state(state='PROCESSING', meta={'progress': 0})
        
        # Get file record
        file_record = db.query(UploadedFile).filter(UploadedFile.id == file_id).first()
        if not file_record:
            return {'status': 'error', 'message': 'File not found'}
        
        # Extract data
        self.update_state(state='PROCESSING', meta={'progress': 25})
        df = etl_service.extract_data(file_record.file_path, file_record.file_type)
        
        # Validate and transform based on file type
        self.update_state(state='PROCESSING', meta={'progress': 50})
        
        if file_record.file_type == 'production':
            is_valid, errors, quality_score = etl_service.validate_production_data(df)
            
            if is_valid:
                df = etl_service.transform_production_data(df)
                
                # Load data into database
                self.update_state(state='PROCESSING', meta={'progress': 75})
                
                for _, row in df.iterrows():
                    production_record = ProductionData(
                        project_id=file_record.project_id,
                        date=row['date'],
                        oil_production=row.get('oil_production'),
                        gas_production=row.get('gas_production'),
                        oil_price=row.get('oil_price'),
                        gas_price=row.get('gas_price')
                    )
                    db.merge(production_record)  # Use merge to handle duplicates
                
                db.commit()
                
                # Update file record
                file_record.validation_status = 'valid'
                file_record.quality_score = quality_score
                file_record.validation_errors = None
                db.commit()
                
                return {
                    'status': 'success',
                    'rows_processed': len(df),
                    'quality_score': quality_score
                }
            else:
                file_record.validation_status = 'invalid'
                file_record.quality_score = quality_score
                file_record.validation_errors = {'errors': errors}
                db.commit()
                
                return {
                    'status': 'invalid',
                    'errors': errors,
                    'quality_score': quality_score
                }
        
        elif file_record.file_type == 'financial':
            is_valid, errors, quality_score = etl_service.validate_financial_data(df)
            
            if is_valid:
                df = etl_service.transform_financial_data(df)
                
                # Load data into database
                self.update_state(state='PROCESSING', meta={'progress': 75})
                
                for _, row in df.iterrows():
                    financial_record = FinancialData(
                        project_id=file_record.project_id,
                        date=row['date'],
                        revenue=row.get('revenue'),
                        opex=row.get('opex'),
                        capex=row.get('capex'),
                        loe=row.get('loe'),
                        transportation_cost=row.get('transportation_cost'),
                        ga_expense=row.get('ga_expense'),
                        ebitda=row.get('ebitda')
                    )
                    db.merge(financial_record)  # Use merge to handle duplicates
                
                db.commit()
                
                # Update file record
                file_record.validation_status = 'valid'
                file_record.quality_score = quality_score
                file_record.validation_errors = None
                db.commit()
                
                return {
                    'status': 'success',
                    'rows_processed': len(df),
                    'quality_score': quality_score
                }
            else:
                file_record.validation_status = 'invalid'
                file_record.quality_score = quality_score
                file_record.validation_errors = {'errors': errors}
                db.commit()
                
                return {
                    'status': 'invalid',
                    'errors': errors,
                    'quality_score': quality_score
                }
        
        else:
            return {'status': 'error', 'message': f'Unknown file type: {file_record.file_type}'}
    
    except Exception as e:
        logger.error(f"Error processing file {file_id}: {str(e)}")
        
        # Update file record with error
        if file_record:
            file_record.validation_status = 'invalid'
            file_record.validation_errors = {'errors': [str(e)]}
            db.commit()
        
        return {'status': 'error', 'message': str(e)}
    
    finally:
        db.close()
