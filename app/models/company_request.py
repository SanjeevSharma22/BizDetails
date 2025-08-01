from sqlalchemy import Column, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
import enum


class RequestStatus(enum.Enum):
    queued = "queued"
    enriching = "enriching"
    done = "done"
    failed = "failed"


class CompanyRequest(Base):
    __tablename__ = "company_requests"
    
    file_id = Column(UUID(as_uuid=True), ForeignKey("uploaded_files.id"), nullable=False)
    company_name = Column(String, nullable=False)
    country = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    status = Column(SQLEnum(RequestStatus), default=RequestStatus.queued, nullable=False)
    
    # Relationships
    file = relationship("UploadedFile", back_populates="company_requests")
    enrichment = relationship("CompanyEnrichment", back_populates="request", uselist=False, cascade="all, delete-orphan")