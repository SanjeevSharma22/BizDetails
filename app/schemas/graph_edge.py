from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


# Base GraphEdge schema
class GraphEdgeBase(BaseModel):
    source_entity: UUID
    target_entity: UUID
    relationship: str
    weight: Optional[float] = None


# Schema for creating a graph edge
class GraphEdgeCreate(GraphEdgeBase):
    pass


# Schema for updating a graph edge
class GraphEdgeUpdate(BaseModel):
    relationship: Optional[str] = None
    weight: Optional[float] = None


# Schema for reading a graph edge (response)
class GraphEdge(GraphEdgeBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True