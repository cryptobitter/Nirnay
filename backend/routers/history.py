from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import Assessment, User
from models.schemas import AssessmentResponse
from routers.auth import get_current_user

router = APIRouter(prefix="/history", tags=["History"])

@router.get("", response_model=List[AssessmentResponse])
def get_user_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns history of assessments executed by the authenticated user.
    """
    return db.query(Assessment).filter(Assessment.user_id == current_user.id).order_by(Assessment.timestamp.desc()).all()