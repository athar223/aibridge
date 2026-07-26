"""AI services powering the Recommender and Prompt Generator features.

Wraps the Google Gemini API (via the google-genai SDK). All functions
return plain dicts and never raise to the caller — failures are surfaced
as an "error" key so views/templates can degrade gracefully.
"""
import json
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    """Raised when the Gemini client cannot be constructed or called."""


def _get_client():
    if not settings.GEMINI_API_KEY:
        raise AIServiceError(
            "GEMINI_API_KEY is not configured. Add it to your .env file to enable AI features."
        )
    from google import genai

    return genai.Client(api_key=settings.GEMINI_API_KEY)


def _extract_json(text):
    """Best-effort extraction of a JSON object from a Gemini text response."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:]
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1:
        cleaned = cleaned[start : end + 1]
    return json.loads(cleaned)


def get_ai_recommendations(name, user_type, goal):
    """Ask Gemini for AI tool recommendations tailored to a user's goal.

    Returns a dict with keys: tools (list of {name, why}), resources
    (list of str), next_steps (list of str), and optionally "error".
    """
    prompt = f"""You are AIBridge's AI adoption advisor. A {user_type} named {name} shared this goal:
"{goal}"

Recommend real, well-known AI tools that would help them achieve this goal.

Respond with ONLY valid JSON (no markdown code fences, no commentary) in exactly this shape:
{{
  "tools": [{{"name": "Tool name", "why": "One or two sentences on why it helps with this goal"}}],
  "resources": ["A specific learning resource, course, or site name"],
  "next_steps": ["A concrete, actionable next step"]
}}

Include 3 to 5 items in "tools", 3 to 5 items in "resources", and 3 to 5 items in "next_steps".
"""
    try:
        client = _get_client()
        response = client.models.generate_content(model=settings.GEMINI_MODEL, contents=prompt)
        data = _extract_json(response.text)
        data.setdefault("tools", [])
        data.setdefault("resources", [])
        data.setdefault("next_steps", [])
        return data
    except Exception as exc:  # noqa: BLE001 - surface any failure as a friendly error
        logger.exception("Gemini recommendation request failed")
        return {"tools": [], "resources": [], "next_steps": [], "error": str(exc)}


def generate_prompt(task):
    """Ask Gemini to produce beginner/professional/advanced prompts for a task.

    Returns a dict with keys: beginner, professional, advanced (all str),
    and optionally "error".
    """
    prompt = f"""You are AIBridge's prompt engineering assistant. A user wants to accomplish this task:
"{task}"

Write three versions of a prompt they could paste into an AI chatbot to accomplish this task.

Respond with ONLY valid JSON (no markdown code fences, no commentary) in exactly this shape:
{{
  "beginner": "A short, simple prompt anyone could write",
  "professional": "A well-structured prompt with clear context, format, and constraints",
  "advanced": "A highly-optimized prompt using techniques like role assignment, step-by-step reasoning cues, explicit output format, and constraints"
}}
"""
    try:
        client = _get_client()
        response = client.models.generate_content(model=settings.GEMINI_MODEL, contents=prompt)
        data = _extract_json(response.text)
        data.setdefault("beginner", "")
        data.setdefault("professional", "")
        data.setdefault("advanced", "")
        return data
    except Exception as exc:  # noqa: BLE001 - surface any failure as a friendly error
        logger.exception("Gemini prompt generation failed")
        return {"beginner": "", "professional": "", "advanced": "", "error": str(exc)}
