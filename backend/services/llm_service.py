import json
import anthropic
from typing import List, Dict, Any
from config import settings

def generate_policy_answer(question: str, context_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calls Anthropic Claude API using retrieved RAG chunks to synthesize an answer
    and estimate a confidence score based on chunk alignment.
    """
    if not settings.ANTHROPIC_API_KEY:
        # Development fallback response when no Anthropic key is present
        # Setting a low score (40.0) ensures the escalation logic can be tested
        return {
            "answer": "Demo Mode: Anthropic API key not configured. This is a stub response to test escalation logic.",
            "confidence_score": 40.0,
            "sources": context_chunks
        }

    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    # Format context for prompt
    context_str = "\n\n".join(
        [f"--- Source: {c['filename']} (Page {c['page_number']}) ---\n{c['text']}" for c in context_chunks]
    )

    prompt = f"""You are Nirnay, an official AI Policy Auditor.
Your job is to answer compliance queries accurately using ONLY the supplied policy document snippets.

DOCUMENT CONTEXT:
{context_str}

USER QUESTION:
{question}

INSTRUCTIONS:
Provide a response in JSON format containing exact fields:
1. "answer": Clear, structured, cited text referencing document names/pages.
2. "confidence_score": A floating point number from 0 to 100 assessing how complete and reliable the available policy context is for this question.

Ensure output is STRICT JSON.
"""

    try:
        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1000,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}]
        )
    except Exception as e:
        # Log the exception server-side and return a safe, actionable error response
        print(f"Anthropic API Error: {str(e)}")
        return {
            "answer": "Error generating answer: unable to reach the AI service. Please try again.",
            "confidence_score": 0.0,
            "sources": context_chunks
        }

    response_text = response.content[0].text.strip()

    # Strip leading/trailing markdown code fences if Claude includes them
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.lower().startswith("json"):
            response_text = response_text[4:]
        response_text = response_text.strip()

    try:
        parsed = json.loads(response_text)
        return {
            "answer": parsed.get("answer", response_text),
            "confidence_score": float(parsed.get("confidence_score", 75.0)),
            "sources": context_chunks
        }
    except Exception:
        return {
            "answer": response_text,
            "confidence_score": 70.0,
            "sources": context_chunks
        }