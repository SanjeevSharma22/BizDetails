from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DropName API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EnrichRequest(BaseModel):
    company_name: str
    country: str | None = None
    industry: str | None = None
    size: str | None = None
    keywords: str | None = None

class EnrichResponse(BaseModel):
    domain: str
    confidence: int
    method: str

@app.post("/enrich", response_model=EnrichResponse)
async def enrich(data: EnrichRequest):
    # TODO: replace with real logic
    return EnrichResponse(domain=f"{data.company_name.lower().replace(' ', '')}.com",
                          confidence=50,
                          method="manual")

