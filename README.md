# Company Enrichment API

A comprehensive FastAPI backend for company data enrichment using SQLAlchemy and PostgreSQL.

## Features

- 🔐 **User Authentication** - JWT-based authentication with user registration and login
- 📁 **File Upload** - CSV file upload with automatic processing
- 🏢 **Company Management** - Track and manage company requests for enrichment
- 🔍 **Data Enrichment** - Enrich company data with domain, legal name, LinkedIn URL, etc.
- 📊 **Task Tracking** - Monitor background enrichment tasks with Celery
- 🔗 **Relationship Mapping** - Graph-based entity relationships
- 🚀 **Production Ready** - Railway.com compatible, with Alembic migrations

## Technology Stack

- **FastAPI** - Modern web framework for APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Robust relational database
- **Alembic** - Database migration tool
- **Pydantic** - Data validation using Python type annotations
- **JWT** - JSON Web Tokens for authentication
- **Celery** - Distributed task queue (optional)
- **Redis** - In-memory data store for Celery backend

## Project Structure

```
app/
├── main.py                 # FastAPI application entry point
├── models/                 # SQLAlchemy database models
│   ├── user.py
│   ├── uploaded_file.py
│   ├── company_request.py
│   ├── company_enrichment.py
│   ├── celery_task_log.py
│   └── graph_edge.py
├── schemas/                # Pydantic schemas
│   ├── user.py
│   ├── uploaded_file.py
│   ├── company_request.py
│   ├── company_enrichment.py
│   ├── celery_task_log.py
│   └── graph_edge.py
├── routers/                # API route handlers
│   ├── auth.py            # Authentication endpoints
│   ├── upload.py          # File upload endpoints
│   └── enrichment.py      # Company enrichment endpoints
├── db/                     # Database configuration
│   ├── session.py         # Database session management
│   └── base_class.py      # SQLAlchemy base class
└── core/
    └── config.py          # Application configuration
alembic/                   # Database migrations
├── versions/              # Migration scripts
├── env.py                # Alembic environment
└── script.py.mako        # Migration template
requirements.txt           # Python dependencies
alembic.ini               # Alembic configuration
.env.example              # Environment variables template
```

## Database Models

### User
- Authentication and user management
- Fields: id, email, hashed_password, is_active, is_superuser, created_at

### UploadedFile
- Track CSV file uploads
- Fields: id, user_id, filename, status, total_records, created_at

### CompanyRequest
- Individual company enrichment requests
- Fields: id, file_id, company_name, country, industry, status, created_at

### CompanyEnrichment
- Enriched company data
- Fields: id, request_id, domain, legal_name, linkedin_url, confidence_score, enrichment_source, status, enriched_at, created_at

### CeleryTaskLog
- Background task tracking
- Fields: id, task_name, args_json, result_json, status, started_at, finished_at, created_at

### GraphEdge
- Entity relationships
- Fields: id, source_entity, target_entity, relationship, weight, created_at

## Quick Start

### 1. Environment Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd company-enrichment-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
DATABASE_URL=postgresql://username:password@localhost:5432/your_db
SECRET_KEY=your-secret-key-here
```

### 3. Database Setup

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 4. Run the Application

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/token` - Login and get access token
- `GET /auth/me` - Get current user info

### File Upload
- `POST /upload/upload` - Upload CSV file
- `GET /upload/files` - Get user's uploaded files
- `GET /upload/files/{file_id}` - Get specific file
- `GET /upload/files/{file_id}/companies` - Get companies from file

### Company Enrichment
- `POST /enrichment/enrich/{request_id}` - Create enrichment data
- `GET /enrichment/enrichments` - Get user's enrichments
- `GET /enrichment/enrichments/{enrichment_id}` - Get specific enrichment
- `PUT /enrichment/enrichments/{enrichment_id}` - Update enrichment
- `DELETE /enrichment/enrichments/{enrichment_id}` - Delete enrichment
- `POST /enrichment/requests/{request_id}/start-enrichment` - Start enrichment process

## CSV Upload Format

The API expects CSV files with the following columns (flexible naming):

```csv
company_name,country,industry
"Acme Corp","United States","Technology"
"Global Ltd","Canada","Manufacturing"
```

Supported column names:
- **Company Name**: `company_name`, `Company Name`, `name`
- **Country**: `country`, `Country`
- **Industry**: `industry`, `Industry`

## Railway.com Deployment

### 1. Prepare for Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login
```

### 2. Setup PostgreSQL

1. Create new Railway project
2. Add PostgreSQL service
3. Copy the DATABASE_URL from Railway dashboard

### 3. Deploy Application

```bash
# Initialize Railway project
railway init

# Set environment variables
railway variables set SECRET_KEY=your-production-secret-key
railway variables set DATABASE_URL=your-railway-postgres-url

# Deploy
railway up
```

### 4. Run Migrations

```bash
# Connect to Railway and run migrations
railway run alembic upgrade head
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `SECRET_KEY` | JWT secret key | Required |
| `ALGORITHM` | JWT algorithm | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration | 30 |
| `APP_NAME` | Application name | Company Enrichment API |
| `DEBUG` | Debug mode | False |
| `CELERY_BROKER_URL` | Celery broker URL | redis://localhost:6379/0 |
| `CELERY_RESULT_BACKEND` | Celery result backend | redis://localhost:6379/0 |
| `MAX_FILE_SIZE` | Maximum upload size (bytes) | 10485760 (10MB) |
| `UPLOAD_DIR` | Upload directory | uploads |

## Development

### Code Structure Guidelines

- **Models**: Define database tables using SQLAlchemy
- **Schemas**: Define API request/response models using Pydantic
- **Routers**: Group related endpoints together
- **Dependencies**: Use FastAPI's dependency injection for database sessions and authentication

### Adding New Endpoints

1. Create/update model in `app/models/`
2. Create/update schema in `app/schemas/`
3. Add endpoints to appropriate router in `app/routers/`
4. Create migration with `alembic revision --autogenerate -m "Description"`
5. Apply migration with `alembic upgrade head`

### Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## Security Considerations

- Change default `SECRET_KEY` in production
- Use environment variables for sensitive data
- Configure CORS appropriately for your frontend
- Implement rate limiting for production
- Use HTTPS in production
- Regularly update dependencies

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
