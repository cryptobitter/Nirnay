import hashlib
import json
from typing import Any, Dict

def build_hash_payload_from_assessment(assessment) -> dict:
    """
    Builds the raw data dict from a SQLAlchemy Assessment object,
    to be passed into generate_record_hash(). This ensures the hash
    is computed identically whether called at creation time (qa.py)
    or verification time (verify.py) — using the same field extraction
    logic in exactly one place.
    """
    return {
        "id": assessment.id,
        "institution_id": assessment.institution_id,
        "user_id": assessment.user_id,
        "question": assessment.question,
        "answer": assessment.answer,
        "sources": assessment.sources,
        "confidence_score": assessment.confidence_score,
        "decision": assessment.decision,
        "timestamp": assessment.timestamp,
    }

def serialize_assessment_deterministically(data: Dict[str, Any]) -> str:
    """
    Serializes assessment attributes into a canonical JSON string
    with keys sorted to guarantee deterministic SHA-256 output.
    """
    ts = data["timestamp"]
    if hasattr(ts, "timestamp"):
        ts_value = int(ts.timestamp())
    else:
        ts_value = str(ts)

    canonical_dict = {
        "assessment_id": str(data["id"]),
        "institution_id": str(data["institution_id"]),
        "user_id": str(data["user_id"]),
        "question": str(data["question"]).strip(),
        "answer": str(data["answer"]).strip(),
        "sources": data["sources"],
        "confidence_score": round(float(data["confidence_score"]), 2),
        "decision": str(data["decision"]).strip(),
        "timestamp": ts_value
    }
    
    return json.dumps(canonical_dict, sort_keys=True, separators=(',', ':'))

def generate_record_hash(assessment_data: Dict[str, Any]) -> str:
    """
    Calculates SHA-256 digest of deterministic assessment string.
    """
    serialized_str = serialize_assessment_deterministically(assessment_data)
    return hashlib.sha256(serialized_str.encode('utf-8')).hexdigest()