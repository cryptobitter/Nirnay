from pydantic import BaseModel, EmailStr
from typing import List, Optional, Any
from datetime import datetime
from uuid import UUID

# --- Auth Schemas ---
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: str = "staff"  # admin, reviewer, staff
    institution_name: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    role: str
    institution_id: str

class UserResponse(BaseModel):
    id: UUID
    email: str
    name: str
    role: str
    institution_id: UUID

    class Config:
        from_attributes = True

# --- Document Schemas ---
class DocumentResponse(BaseModel):
    id: UUID
    institution_id: UUID
    filename: str
    upload_date: datetime
    page_count: int
    status: str

    class Config:
        from_attributes = True

# --- Q&A / Assessment Schemas ---
class AskQuestionRequest(BaseModel):
    question: str

class SourceChunk(BaseModel):
    document_name: str
    text: str
    page_number: Optional[int] = None

class AssessmentResponse(BaseModel):
    id: UUID
    institution_id: UUID
    user_id: UUID
    question: str
    answer: str
    sources: List[SourceChunk]
    confidence_score: float
    decision: str
    record_hash: str
    chain_tx_hash: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True

# --- Verification Schemas ---
class VerificationResult(BaseModel):
    status: str  # verified, failed, not_found
    is_valid: bool
    record_id: Optional[str] = None
    calculated_hash: Optional[str] = None
    db_hash: Optional[str] = None
    on_chain_hash: Optional[str] = None
    # Unix timestamp from blockchain, seconds since epoch
    on_chain_timestamp: Optional[int] = None
    message: str