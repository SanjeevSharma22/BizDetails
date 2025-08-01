from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.company_request import RequestStatus


# Base CompanyRequest schema
class CompanyRequestBase(BaseModel):
    company_name: str
    country: Optional[str] = None
    industry: Optional[str] = None


# Schema for creating a company request
class CompanyRequestCreate(CompanyRequestBase):
    file_id: UUID


# Schema for updating a company request
class CompanyRequestUpdate(BaseModel):
    company_name: Optional[str] = None
    country: Optional[str] = None
    industry: Optional[str] = None
    status: Optional[RequestStatus] = None


# Schema for reading a company request (response)
class CompanyRequest(CompanyRequestBase):
    id: UUID
    file_id: UUID
    status: RequestStatus
    created_at: datetime

    class Config:
        from_attributes = True


# Schema with relationships included
class CompanyRequestWithEnrichment(CompanyRequest):
    from app.schemas.company_enrichment import CompanyEnrichment
    enrichment: Optional[CompanyEnrichment] = None