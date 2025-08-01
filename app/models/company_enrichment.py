from sqlalchemy import Column, String, Float, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
from datetime import datetime
import enum


class EnrichmentSource(enum.Enum):
    whois = "whois"
    langchain = "langchain"
    scraping = "scraping"
    manual = "manual"


class EnrichmentStatus(enum.Enum):
    success = "success"
    partial = "partial"
    failed = "failed"


class CompanyEnrichment(Base):
    __tablename__ = "company_enrichments"
    
    request_id = Column(UUID(as_uuid=True), ForeignKey("company_requests.id"), nullable=False, unique=True)
    domain = Column(String, nullable=True)
    legal_name = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    confidence_score = Column(Float, nullable=True)  # 0.0 to 1.0
    enrichment_source = Column(SQLEnum(EnrichmentSource), nullable=True)
    status = Column(SQLEnum(EnrichmentStatus), nullable=False)
    enriched_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    request = relationship("CompanyRequest", back_populates="enrichment")
    source_edges = relationship("GraphEdge", foreign_keys="GraphEdge.source_entity", back_populates="source")
    target_edges = relationship("GraphEdge", foreign_keys="GraphEdge.target_entity", back_populates="target")