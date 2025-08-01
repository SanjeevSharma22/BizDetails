from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.models.uploaded_file import FileStatus


# Base UploadedFile schema
class UploadedFileBase(BaseModel):
    filename: str
    total_records: int = 0


# Schema for creating an uploaded file
class UploadedFileCreate(UploadedFileBase):
    user_id: UUID


# Schema for updating an uploaded file
class UploadedFileUpdate(BaseModel):
    filename: Optional[str] = None
    status: Optional[FileStatus] = None
    total_records: Optional[int] = None


# Schema for reading an uploaded file (response)
class UploadedFile(UploadedFileBase):
    id: UUID
    user_id: UUID
    status: FileStatus
    created_at: datetime

    class Config:
        from_attributes = True


# Schema with relationships included
class UploadedFileWithRelations(UploadedFile):
    from app.schemas.company_request import CompanyRequest
    company_requests: List[CompanyRequest] = []