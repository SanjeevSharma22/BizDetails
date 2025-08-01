from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from app.models.celery_task_log import TaskStatus


# Base CeleryTaskLog schema
class CeleryTaskLogBase(BaseModel):
    task_name: str
    args_json: Dict[str, Any]


# Schema for creating a celery task log
class CeleryTaskLogCreate(CeleryTaskLogBase):
    status: TaskStatus = TaskStatus.pending


# Schema for updating a celery task log
class CeleryTaskLogUpdate(BaseModel):
    result_json: Optional[Dict[str, Any]] = None
    status: Optional[TaskStatus] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None


# Schema for reading a celery task log (response)
class CeleryTaskLog(CeleryTaskLogBase):
    id: UUID
    result_json: Optional[Dict[str, Any]] = None
    status: TaskStatus
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True