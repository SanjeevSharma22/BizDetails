from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base_class import Base
from datetime import datetime
import enum


class TaskStatus(enum.Enum):
    pending = "pending"
    started = "started"
    success = "success"
    failed = "failed"


class CeleryTaskLog(Base):
    __tablename__ = "celery_task_logs"
    
    task_name = Column(String, nullable=False)
    args_json = Column(JSONB, nullable=False)
    result_json = Column(JSONB, nullable=True)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.pending, nullable=False)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)