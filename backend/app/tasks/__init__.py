"""
Celery tasks package.
"""
from celery import Celery
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    'valuation_platform',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
)

# Import tasks
from app.tasks.etl_tasks import process_uploaded_file

__all__ = ['celery_app', 'process_uploaded_file']
