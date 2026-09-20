from typing import List

import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class AIDecision(BaseModel):
    action: str
    confidence: float
    reason: str
    sources: List[str]

def make_decision(ticket_message, retrieved_chunks):
    context = "\n\n".join(
        [
            f"Source: {chunk['source']}\n{chunk['text']}"
            for chunk in retrieved_chunks
        ]
    )

    prompt = f"""
You are a support ticket decision assistant.

Use only the policy information provided below.

Ticket:
{ticket_message}

Relevant policies:
{context}

Decide the correct action based on the policies.
The action must be exactly one of these:
REQUEST_PHOTOS
APPROVE_RETURN
OPEN_SHIPPING_INVESTIGATION
REPLACE_CORRECT_ITEM
NEEDS_MORE_INFORMATION
REQUEST_DEFECT_EVIDENCE
APPROVE_REFUND_OR_REPLACEMENT
REFUND
REPLACE

If the policy requires a specific piece of evidence or action before approval,
return the action that requests that evidence.

Use NEEDS_MORE_INFORMATION only when the ticket is missing information needed
to determine which policy applies or what action should be taken.

Return only valid JSON in this format:
{{
    "action": "ACTION_NAME",
    "confidence": 0.0,
    "reason": "Short explanation based on the policy",
    "sources": ["policy_file.md"]
}}

The confidence must be a number between 0 and 1.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return AIDecision.model_validate_json(response.text.strip().replace("```json", "").replace("```", ""))

if __name__ == "__main__":
    test_chunks = [
        {
            "source": "damaged_goods.md",
            "text": (
                "Damage reported within 7 days is eligible. "
                "For orders above ₹2,000, photographs are required "
                "before approval."
            ),
        }
    ]

    result = make_decision(
        "My ₹3,500 order arrived damaged yesterday.",
        test_chunks,
    )

    print(result.model_dump_json(indent=2))