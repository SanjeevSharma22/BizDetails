from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.company_enrichment import EnrichmentSource, EnrichmentStatus


# Base CompanyEnrichment schema
class CompanyEnrichmentBase(BaseModel):
    domain: Optional[str] = None
    legal_name: Optional[str] = None
    linkedin_url: Optional[str] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    enrichment_source: Optional[EnrichmentSource] = None


# Schema for creating a company enrichment
class CompanyEnrichmentCreate(CompanyEnrichmentBase):
    request_id: UUID
    status: EnrichmentStatus


# Schema for updating a company enrichment
class CompanyEnrichmentUpdate(BaseModel):
    domain: Optional[str] = None
    legal_name: Optional[str] = None
    linkedin_url: Optional[str] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    enrichment_source: Optional[EnrichmentSource] = None
    status: Optional[EnrichmentStatus] = None


# Schema for reading a company enrichment (response)
class CompanyEnrichment(CompanyEnrichmentBase):
    id: UUID
    request_id: UUID
    status: EnrichmentStatus
    enriched_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True