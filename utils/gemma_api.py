import os
import re
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", ""))

LANGUAGE_NAMES = {
    "en": "English",
    "fr": "French",
    "ar": "Arabic",
    "sw": "Swahili",
}

HEALTH_SYSTEM_PROMPT = """You are ZOE, an AI healthcare assistant for underserved communities.

CRITICAL: Output ONLY the final response. No thinking steps, no reasoning bullets, no draft markers, no self-evaluation.

Your response must follow this exact format:
URGENCY: [Low/Moderate/High/Emergency]
[Your response in {language} — max 150 words, simple language, empathetic tone]

Rules:
- Never diagnose. Use "may indicate" or "possible"
- For Emergency: say SEEK EMERGENCY CARE IMMEDIATELY
- Respond in {language}
- Emergency symptoms: chest pain, difficulty breathing, heavy bleeding, loss of consciousness, stroke signs"""

EDUCATION_SYSTEM_PROMPT = """You are ZOE, an AI health educator for underserved communities.

CRITICAL: Output ONLY the educational answer. No thinking, no reasoning, no draft markers, no checklists.

Respond in {language}. Max 150 words. Simple language. No diagnosis or prescriptions.
Start your response directly with the educational content."""

PREFERRED_MODELS = ["gemini-2.5-flash", "gemma-4-31b-it", "gemini-2.0-flash"]


def _get_model(model_name: str, system: str = ""):
    return genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system if system else None,
        generation_config={"temperature": 0.3, "max_output_tokens": 400},
    )


def _extract_final(text: str) -> str:
    """Extract only the actual response, stripping chain-of-thought reasoning."""
    # If model included a Draft: section, take only the last one
    draft_split = re.split(r'\*{0,2}Draft:\*{0,2}\s*', text, flags=re.IGNORECASE)
    if len(draft_split) > 1:
        return draft_split[-1].strip()

    # Strip lines that are reasoning bullets: lines starting with * "..." or * text in quotes
    lines = text.splitlines()
    clean = []
    for line in lines:
        s = line.strip()
        # Skip reasoning bullet lines (start with * followed by space or quote)
        if re.match(r'^\*\s+[\"\']?[A-Z]', s) and not re.match(r'^\*\*', s):
            continue
        # Skip checklist lines
        if re.search(r'\?\s*(Yes|No)\.?$', s, re.IGNORECASE):
            continue
        # Skip lines with self-evaluation markers
        if any(m in s.lower() for m in ['draft:', 'self-correction', 'alternative', 'wait,', 'actually,', 'hmm,', 'let me']):
            continue
        clean.append(line)

    result = '\n'.join(clean).strip()

    # If still too noisy, take the last coherent paragraph
    if result.count('*') > 10:
        paragraphs = re.split(r'\n{2,}', text)
        for para in reversed(paragraphs):
            if len(para.strip()) > 40 and para.count('*') < 3:
                return para.strip()

    return result


def _extract_urgency(text: str) -> str:
    match = re.search(r"URGENCY:\s*(Low|Moderate|High|Emergency)", text, re.IGNORECASE)
    if match:
        return match.group(1).capitalize()
    lower = text.lower()
    if "emergency" in lower:
        return "Emergency"
    if "high" in lower:
        return "High"
    if "moderate" in lower:
        return "Moderate"
    return "Low"


def _call_with_fallback(user_prompt: str, system: str = "") -> str:
    last_error = None
    for model_name in PREFERRED_MODELS:
        try:
            model = _get_model(model_name, system)
            response = model.generate_content(user_prompt)
            return response.text
        except Exception as e:
            last_error = e
            continue
    error_str = str(last_error)
    if "quota" in error_str.lower() or "429" in error_str:
        raise RuntimeError("quota_exceeded")
    raise RuntimeError(f"api_error: {error_str[:200]}")


def get_health_response(symptoms: str, language: str = "en") -> dict:
    lang_name = LANGUAGE_NAMES.get(language, "English")
    system = HEALTH_SYSTEM_PROMPT.format(language=lang_name)
    try:
        raw = _call_with_fallback(f"Patient symptoms: {symptoms}", system)
        urgency = _extract_urgency(raw)
        text = _extract_final(raw)
        clean = re.sub(r"URGENCY:\s*(Low|Moderate|High|Emergency)\n?", "", text, flags=re.IGNORECASE).strip()
        return {"response": clean, "urgency": urgency}
    except RuntimeError as e:
        if "quota_exceeded" in str(e):
            msg = ("⚠️ AI service unavailable — API quota exceeded. "
                   "If this is an emergency, please call emergency services immediately.")
        else:
            msg = "Unable to process your request. Please seek medical attention if this is an emergency."
        return {"response": msg, "urgency": "Low"}


def get_education_response(question: str, language: str = "en") -> str:
    lang_name = LANGUAGE_NAMES.get(language, "English")
    system = EDUCATION_SYSTEM_PROMPT.format(language=lang_name)
    try:
        raw = _call_with_fallback(f"Question: {question}", system)
        return _extract_final(raw)
    except RuntimeError as e:
        if "quota_exceeded" in str(e):
            return "⚠️ AI service unavailable — API quota exceeded."
        return "Unable to answer right now. Please consult a healthcare professional."
