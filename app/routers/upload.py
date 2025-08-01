import csv
import io
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.models.uploaded_file import UploadedFile, FileStatus
from app.models.company_request import CompanyRequest
from app.schemas.uploaded_file import UploadedFile as UploadedFileSchema, UploadedFileCreate
from app.schemas.company_request import CompanyRequest as CompanyRequestSchema
from app.routers.auth import get_current_active_user

router = APIRouter()


@router.post("/upload", response_model=UploadedFileSchema)
async def upload_csv_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload CSV file for company enrichment"""
    
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are allowed"
        )
    
    # Validate file size
    contents = await file.read()
    if len(contents) > settings.max_file_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size is {settings.max_file_size} bytes"
        )
    
    # Create uploaded file record
    db_file = UploadedFile(
        user_id=current_user.id,
        filename=file.filename,
        status=FileStatus.processing
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    try:
        # Process CSV content
        csv_content = contents.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        
        company_requests = []
        record_count = 0
        
        for row in csv_reader:
            # Extract company information from CSV row
            company_name = row.get('company_name') or row.get('Company Name') or row.get('name')
            country = row.get('country') or row.get('Country') or None
            industry = row.get('industry') or row.get('Industry') or None
            
            if not company_name:
                continue
                
            company_request = CompanyRequest(
                file_id=db_file.id,
                company_name=company_name.strip(),
                country=country.strip() if country else None,
                industry=industry.strip() if industry else None
            )
            company_requests.append(company_request)
            record_count += 1
        
        # Bulk insert company requests
        if company_requests:
            db.add_all(company_requests)
        
        # Update file status and record count
        db_file.status = FileStatus.done
        db_file.total_records = record_count
        db.commit()
        db.refresh(db_file)
        
        return db_file
        
    except Exception as e:
        # Update file status to error
        db_file.status = FileStatus.error
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing CSV file: {str(e)}"
        )


@router.get("/files", response_model=List[UploadedFileSchema])
def get_uploaded_files(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's uploaded files"""
    files = db.query(UploadedFile).filter(UploadedFile.user_id == current_user.id).all()
    return files


@router.get("/files/{file_id}", response_model=UploadedFileSchema)
def get_uploaded_file(
    file_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get specific uploaded file"""
    file = db.query(UploadedFile).filter(
        UploadedFile.id == file_id,
        UploadedFile.user_id == current_user.id
    ).first()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    return file


@router.get("/files/{file_id}/companies", response_model=List[CompanyRequestSchema])
def get_file_companies(
    file_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get companies from uploaded file"""
    # Verify file ownership
    file = db.query(UploadedFile).filter(
        UploadedFile.id == file_id,
        UploadedFile.user_id == current_user.id
    ).first()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    companies = db.query(CompanyRequest).filter(CompanyRequest.file_id == file_id).all()
    return companies