from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import cast, String

from database.db import get_db
from database.models import Assessment
from models.schemas import VerificationResult
from services.hasher import generate_record_hash, build_hash_payload_from_assessment
from services.blockchain_service import blockchain_service

router = APIRouter(prefix="/verify", tags=["Public Verification"])

@router.get("/{identifier}", response_model=VerificationResult)
def verify_record(identifier: str, db: Session = Depends(get_db)):
    """
    Public zero-trust verification endpoint. Re-hashes localized DB state 
    and checks against Polygon Amoy on-chain record bytes.
    """
    # Find assessment by UUID or Hash
    assessment = db.query(Assessment).filter(
        (Assessment.id.cast(String) == identifier) | (Assessment.record_hash == identifier)
    ).first()

    if not assessment:
        return VerificationResult(
            status="not_found",
            is_valid=False,
            message="Assessment record not found in system database."
        )

    # 1. Re-calculate deterministic local hash using the shared payload builder
    hash_payload = build_hash_payload_from_assessment(assessment)
    recalculated_hash = generate_record_hash(hash_payload)

    # 2. Compare local recalculated hash against recorded DB hash
    if recalculated_hash != assessment.record_hash:
        return VerificationResult(
            status="failed",
            is_valid=False,
            record_id=str(assessment.id),
            calculated_hash=recalculated_hash,
            db_hash=assessment.record_hash,
            message="TAMPERING DETECTED: Database record does not match its hash digest."
        )

    # 3. Query Polygon testnet via smart contract
    on_chain_res = blockchain_service.verify_record_on_chain(assessment.record_hash)

    if not on_chain_res.get("exists", False):
        return VerificationResult(
            status="failed",
            is_valid=False,
            record_id=str(assessment.id),
            calculated_hash=recalculated_hash,
            db_hash=assessment.record_hash,
            message="UNANCHORED RECORD: Record exists locally but missing on Polygon smart contract."
        )

    return VerificationResult(
        status="verified",
        is_valid=True,
        record_id=str(assessment.id),
        calculated_hash=recalculated_hash,
        db_hash=assessment.record_hash,
        on_chain_hash=assessment.record_hash,
        on_chain_timestamp=on_chain_res.get("timestamp"),
        message="AUTHENTIC: Record integrity verified matching on-chain Polygon ledger."
    )