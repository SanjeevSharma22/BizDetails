from sqlalchemy import Column, String, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
import enum


class FileStatus(enum.Enum):
    pending = "pending"
    processing = "processing"
    done = "done"
    error = "error"


class UploadedFile(Base):
    __tablename__ = "uploaded_files"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    status = Column(SQLEnum(FileStatus), default=FileStatus.pending, nullable=False)
    total_records = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="uploaded_files")
    company_requests = relationship("CompanyRequest", back_populates="file", cascade="all, delete-orphan")