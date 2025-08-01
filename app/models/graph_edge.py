from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base


class GraphEdge(Base):
    __tablename__ = "graph_edges"
    
    source_entity = Column(UUID(as_uuid=True), ForeignKey("company_enrichments.id"), nullable=False)
    target_entity = Column(UUID(as_uuid=True), ForeignKey("company_enrichments.id"), nullable=False)
    relationship = Column(String, nullable=False)  # e.g., 'SUBSIDIARY_OF', 'PARENT_OF', 'PARTNER_OF'
    weight = Column(Float, nullable=True)
    
    # Relationships
    source = relationship("CompanyEnrichment", foreign_keys=[source_entity], back_populates="source_edges")
    target = relationship("CompanyEnrichment", foreign_keys=[target_entity], back_populates="target_edges")