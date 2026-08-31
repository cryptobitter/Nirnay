from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import Assessment, User
from models.schemas import AssessmentResponse
from routers.auth import get_current_user

router = APIRouter(prefix="/audit", tags=["Audit Log"])

@router.get("", response_model=List[AssessmentResponse])
def get_institution_audit_logs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Admin-only endpoint returning all assessment logs across the institution.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to institution administrators"
        )

    return db.query(Assessment).filter(
        Assessment.institution_id == current_user.institution_id
    ).order_by(Assessment.timestamp.desc()).all()