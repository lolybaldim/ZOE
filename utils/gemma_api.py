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

HEALTH_SYSTEM_PROMPT = """You are ZOE, an AI healthcare assistant for underserved communities in Rwanda, Sudan, and across sub-Saharan Africa and the Middle East.

Your role:
1. Analyze symptoms provided by the user
2. Respond with possible health concerns (NOT a diagnosis)
3. Assign one urgency level: Low / Moderate / High / Emergency
4. Recommend appropriate action (rest at home / visit a clinic / seek emergency care)
5. Always advise consulting a real doctor for medical decisions
6. Respond in {language}
7. Use simple, clear language suitable for low-literacy users
8. Be empathetic, calm, and supportive

IMPORTANT RULES:
- Never diagnose. Say "possible" or "may indicate"
- For Emergency urgency: always say SEEK EMERGENCY CARE IMMEDIATELY
- Keep responses concise (max 250 words)
- Format: start with urgency level on its own line as: URGENCY: [level]

Emergency symptoms that ALWAYS require Emergency urgency:
- Chest pain or tightness
- Difficulty breathing / shortness of breath
- Heavy or uncontrolled bleeding
- Loss of consciousness or fainting
- Sudden severe headache with vision changes
- Signs of stroke (face drooping, arm weakness, speech difficulty)
- Severe allergic reaction
"""

EDUCATION_SYSTEM_PROMPT = """You are ZOE, an AI health educator for underserved communities.

Provide clear, factual, and supportive health education. Respond in {language}.
Keep answers simple, under 200 words, suitable for low-literacy users.
Do NOT diagnose or prescribe. Always recommend professional medical consultation.
Topics: maternal health, hygiene, nutrition, disease prevention, mental health, child health.
"""


PREFERRED_MODELS = ["gemma-4-31b-it", "gemini-2.5-flash", "gemini-2.0-flash"]


def _get_model(model_name: str = PREFERRED_MODELS[0], system: str = ""):
    return genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system if system else None,
        generation_config={"temperature": 0.4, "max_output_tokens": 500},
    )


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
    if "quota" in error_str.lower() or "exhausted" in error_str.lower() or "429" in error_str:
        raise RuntimeError("quota_exceeded")
    raise RuntimeError(f"api_error: {error_str[:200]}")


def get_health_response(symptoms: str, language: str = "en") -> dict:
    lang_name = LANGUAGE_NAMES.get(language, "English")
    system = HEALTH_SYSTEM_PROMPT.format(language=lang_name)
    try:
        text = _call_with_fallback(f"Patient symptoms: {symptoms}", system)
        urgency = _extract_urgency(text)
        clean_response = re.sub(r"URGENCY:\s*(Low|Moderate|High|Emergency)\n?", "", text, flags=re.IGNORECASE).strip()
        return {"response": clean_response, "urgency": urgency}
    except RuntimeError as e:
        if "quota_exceeded" in str(e):
            msg = ("⚠️ The AI service is temporarily unavailable due to API quota limits. "
                   "Please ask the administrator to enable billing on the Google Cloud project. "
                   "If this is an emergency, please call emergency services immediately.")
        else:
            msg = ("I'm unable to process your request right now. "
                   "Please seek immediate medical attention if this is an emergency.")
        return {"response": msg, "urgency": "Low"}


def get_education_response(question: str, language: str = "en") -> str:
    lang_name = LANGUAGE_NAMES.get(language, "English")
    system = EDUCATION_SYSTEM_PROMPT.format(language=lang_name)
    try:
        return _call_with_fallback(f"Question: {question}", system)
    except RuntimeError as e:
        if "quota_exceeded" in str(e):
            return ("⚠️ The AI service is temporarily unavailable due to API quota limits. "
                    "Please ask the administrator to enable billing on the Google Cloud project.")
        return "I'm unable to answer that question right now. Please consult a healthcare professional."
