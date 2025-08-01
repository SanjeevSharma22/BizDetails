from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.company_request import CompanyRequest, RequestStatus
from app.models.company_enrichment import CompanyEnrichment, EnrichmentStatus
from app.schemas.company_request import CompanyRequest as CompanyRequestSchema
from app.schemas.company_enrichment import (
    CompanyEnrichment as CompanyEnrichmentSchema,
    CompanyEnrichmentCreate,
    CompanyEnrichmentUpdate
)
from app.routers.auth import get_current_active_user

router = APIRouter()


@router.post("/enrich/{request_id}", response_model=CompanyEnrichmentSchema)
def create_enrichment(
    request_id: str,
    enrichment: CompanyEnrichmentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create enrichment data for a company request"""
    
    # Verify the company request exists and belongs to user
    company_request = db.query(CompanyRequest).join(
        CompanyRequest.file
    ).filter(
        CompanyRequest.id == request_id,
        CompanyRequest.file.has(user_id=current_user.id)
    ).first()
    
    if not company_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company request not found"
        )
    
    # Check if enrichment already exists
    existing_enrichment = db.query(CompanyEnrichment).filter(
        CompanyEnrichment.request_id == request_id
    ).first()
    
    if existing_enrichment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Enrichment already exists for this request"
        )
    
    # Create enrichment
    db_enrichment = CompanyEnrichment(**enrichment.dict())
    db.add(db_enrichment)
    
    # Update company request status
    company_request.status = RequestStatus.done
    
    db.commit()
    db.refresh(db_enrichment)
    
    return db_enrichment


@router.get("/enrichments", response_model=List[CompanyEnrichmentSchema])
def get_enrichments(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get user's company enrichments"""
    enrichments = db.query(CompanyEnrichment).join(
        CompanyEnrichment.request
    ).join(
        CompanyRequest.file
    ).filter(
        CompanyRequest.file.has(user_id=current_user.id)
    ).offset(skip).limit(limit).all()
    
    return enrichments


@router.get("/enrichments/{enrichment_id}", response_model=CompanyEnrichmentSchema)
def get_enrichment(
    enrichment_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get specific enrichment"""
    enrichment = db.query(CompanyEnrichment).join(
        CompanyEnrichment.request
    ).join(
        CompanyRequest.file
    ).filter(
        CompanyEnrichment.id == enrichment_id,
        CompanyRequest.file.has(user_id=current_user.id)
    ).first()
    
    if not enrichment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrichment not found"
        )
    
    return enrichment


@router.put("/enrichments/{enrichment_id}", response_model=CompanyEnrichmentSchema)
def update_enrichment(
    enrichment_id: str,
    enrichment_update: CompanyEnrichmentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update enrichment data"""
    enrichment = db.query(CompanyEnrichment).join(
        CompanyEnrichment.request
    ).join(
        CompanyRequest.file
    ).filter(
        CompanyEnrichment.id == enrichment_id,
        CompanyRequest.file.has(user_id=current_user.id)
    ).first()
    
    if not enrichment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrichment not found"
        )
    
    # Update fields
    update_data = enrichment_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(enrichment, field, value)
    
    db.commit()
    db.refresh(enrichment)
    
    return enrichment


@router.delete("/enrichments/{enrichment_id}")
def delete_enrichment(
    enrichment_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete enrichment"""
    enrichment = db.query(CompanyEnrichment).join(
        CompanyEnrichment.request
    ).join(
        CompanyRequest.file
    ).filter(
        CompanyEnrichment.id == enrichment_id,
        CompanyRequest.file.has(user_id=current_user.id)
    ).first()
    
    if not enrichment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrichment not found"
        )
    
    db.delete(enrichment)
    db.commit()
    
    return {"message": "Enrichment deleted successfully"}


@router.post("/requests/{request_id}/start-enrichment")
def start_enrichment_process(
    request_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Start enrichment process for a company request (placeholder for Celery task)"""
    
    # Verify the company request exists and belongs to user
    company_request = db.query(CompanyRequest).join(
        CompanyRequest.file
    ).filter(
        CompanyRequest.id == request_id,
        CompanyRequest.file.has(user_id=current_user.id)
    ).first()
    
    if not company_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company request not found"
        )
    
    # Update status to enriching
    company_request.status = RequestStatus.enriching
    db.commit()
    
    # TODO: Here you would trigger a Celery task for actual enrichment
    # Example: enrich_company_task.delay(request_id)
    
    return {"message": "Enrichment process started", "request_id": request_id}