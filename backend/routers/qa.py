import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database.db import get_db
from database.models import Assessment, User
from models.schemas import AskQuestionRequest, AssessmentResponse
from routers.auth import get_current_user
from services.rag_retrieval import retrieve_relevant_chunks
from services.llm_service import generate_policy_answer
from services.policy_engine import evaluate_policy_rules
from services.hasher import generate_record_hash, build_hash_payload_from_assessment
from services.blockchain_service import blockchain_service

router = APIRouter(prefix="/qa", tags=["Q&A Assessment"])

@router.post("/ask", response_model=AssessmentResponse)
def ask_question(
    req: AskQuestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Defense-in-depth: Ensure the user's institution is verified before allowing queries
    if current_user.institution.status != "verified":
        raise HTTPException(status_code=403, detail="Your institution must be verified before asking questions")

    # 1. RAG Retrieval
    chunks = retrieve_relevant_chunks(
        question=req.question,
        institution_id=str(current_user.institution_id)
    )

    # 2. LLM Synthesis
    llm_output = generate_policy_answer(question=req.question, context_chunks=chunks)

    # 3. Policy Engine Evaluation
    decision = evaluate_policy_rules(
        confidence_score=llm_output["confidence_score"],
        answer_text=llm_output["answer"]
    )

    # 4. Create Draft Database Assessment Record
    assessment = Assessment(
        institution_id=current_user.institution_id,
        user_id=current_user.id,
        question=req.question,
        answer=llm_output["answer"],
        sources=llm_output["sources"],
        confidence_score=llm_output["confidence_score"],
        decision=decision,
        # Temporary unique placeholder to satisfy NOT NULL UNIQUE constraint during flush
        record_hash=f"pending_{uuid.uuid4()}", 
        chain_tx_hash=None,
        timestamp=datetime.utcnow()
    )
    db.add(assessment)
    db.flush()  # Assigns the auto-generated id without committing the transaction

    # 5. Calculate Canonical SHA-256 Hash using the shared payload builder now that it has an id
    hash_payload = build_hash_payload_from_assessment(assessment)
    record_hash = generate_record_hash(hash_payload)

    # 6. Set the real record hash on the object
    assessment.record_hash = record_hash

    # 7. Blockchain Anchor
    try:
        tx_hash = blockchain_service.submit_record_hash(record_hash)
    except RuntimeError as e:
        print(f"Blockchain submission failed, saving assessment without chain anchor: {e}")
        tx_hash = None

    # 8. Update Record with Transaction ID and Commit
    assessment.chain_tx_hash = tx_hash
    db.commit()
    db.refresh(assessment)

    return assessment