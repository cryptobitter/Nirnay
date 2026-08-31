from typing import List

FLAGGED_KEYWORDS: List[str] = [
    "data sharing",
    "third-party",
    "third party",
    "termination",
    "penalty",
    "liability",
    "indemnity",
    "breach"
]

def evaluate_policy_rules(confidence_score: float, answer_text: str) -> str:
    """
    Rule-based policy audit decision logic:
    - Escalate: Low confidence score (< 70) requiring human inspection.
    - Flag: High confidence but contains sensitive operational/legal terms.
    - Approve: High confidence and free from compliance flags.
    """
    lower_answer = answer_text.lower()

    if confidence_score < 70.0:
        return "escalated"

    for keyword in FLAGGED_KEYWORDS:
        if keyword in lower_answer:
            return "flagged"

    return "approved"