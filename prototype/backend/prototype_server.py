import os
import json
import re
import unicodedata
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

app = FastAPI(title="LawSathi Prototype API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
CONTENT_DIR = os.path.join(PROJECT_ROOT, "content")
CORPUS_PATH = os.path.join(BASE_DIR, "corpus.json")

# Load Corpus
with open(CORPUS_PATH, "r", encoding="utf-8") as f:
    CORPUS_CHUNKS = json.load(f)

# Load Helplines
helplines_path = os.path.join(CONTENT_DIR, "helplines.json")
with open(helplines_path, "r", encoding="utf-8") as f:
    raw = json.load(f)
    HELPLINES_DATA = raw.get("items", raw) if isinstance(raw, dict) else raw

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# ───────────────────── 1. SAFETY ROUTER ─────────────────────
SAFETY_TRIGGERS = [
    r"\b(suicide|kill myself|end my life|hanging|harm myself|आत्महत्या|जीव देणे)\b",
    r"\b(someone is killing me|knife|gun|attacked right now|he is beating me|मारहाण|हल्ला)\b",
    r"\b(rape|assault|child abuse|kidnapped|अपहरण)\b"
]

# ───────────────────── MULTILINGUAL MESSAGES ─────────────────────
MESSAGES = {
    "en": {
        "emergency": "EMERGENCY DETECTED: If you are in immediate danger, call 112 right now. Your safety comes first.",
        "no_corpus": "I cannot confirm this from the official law text. Please refer to verified playbooks or call the helpline.",
        "no_corpus_summary": "No verified legal provisions found for this specific query.",
        "mock_summary": "Under {act} Section {section}, you are legally protected. Refer to the verbatim clause above.",
        "mock_note": "Prototype Mock Mode (Set GEMINI_API_KEY for live generation)",
        "cannot_answer": "I cannot confirm this from the official law text.",
        "cannot_answer_summary": "No verified provision directly addresses this query.",
        "guard_hallucination": "Guard rejection: Quoted law text could not be verified against the official gazette.",
        "guard_hallucination_summary": "Unverified legal claims were rejected by LawSathi's guard.",
        "guard_section": "Guard rejection: Section citation unverified.",
        "guard_section_summary": "Verification failed.",
        "provider_error": "Service temporarily unavailable.",
        "provider_error_summary": "Offline fallback active.",
    },
    "hi": {
        "emergency": "आपातकाल पहचाना गया: यदि आप तत्काल खतरे में हैं, तो अभी 112 पर कॉल करें। आपकी सुरक्षा सर्वोपरि है।",
        "no_corpus": "मैं इसे आधिकारिक कानून पाठ से पुष्टि नहीं कर सकता। कृपया सत्यापित प्लेबुक देखें या हेल्पलाइन पर कॉल करें।",
        "no_corpus_summary": "इस विशिष्ट प्रश्न के लिए कोई सत्यापित कानूनी प्रावधान नहीं मिला।",
        "mock_summary": "{act} की धारा {section} के अंतर्गत आप कानूनी रूप से सुरक्षित हैं। ऊपर दी गई मूल धारा देखें।",
        "mock_note": "प्रोटोटाइप मॉक मोड (लाइव जनरेशन के लिए GEMINI_API_KEY सेट करें)",
        "cannot_answer": "मैं इसे आधिकारिक कानून पाठ से पुष्टि नहीं कर सकता।",
        "cannot_answer_summary": "इस प्रश्न का कोई सत्यापित कानूनी प्रावधान उपलब्ध नहीं है।",
        "guard_hallucination": "गार्ड अस्वीकृति: उद्धृत कानून पाठ को आधिकारिक गजट से सत्यापित नहीं किया जा सका।",
        "guard_hallucination_summary": "असत्यापित कानूनी दावों को LawSathi के गार्ड ने अस्वीकार कर दिया।",
        "guard_section": "गार्ड अस्वीकृति: धारा उद्धरण असत्यापित।",
        "guard_section_summary": "सत्यापन विफल।",
        "provider_error": "सेवा अस्थायी रूप से अनुपलब्ध है।",
        "provider_error_summary": "ऑफलाइन फ़ॉलबैक सक्रिय।",
    },
    "mr": {
        "emergency": "आपत्कालीन परिस्थिती आढळली: जर तुम्ही तात्काळ धोक्यात असाल तर आत्ताच 112 वर कॉल करा. तुमची सुरक्षा सर्वोपरि आहे.",
        "no_corpus": "मी हे अधिकृत कायद्याच्या मजकुरातून पुष्टी करू शकत नाही. कृपया सत्यापित प्लेबुक पहा किंवा हेल्पलाइनवर कॉल करा.",
        "no_corpus_summary": "या विशिष्ट प्रश्नासाठी कोणतेही सत्यापित कायदेशीर तरतूद आढळली नाही.",
        "mock_summary": "{act} च्या कलम {section} अंतर्गत तुम्ही कायदेशीरदृष्ट्या संरक्षित आहात. वरील मूळ कलम पहा.",
        "mock_note": "प्रोटोटाइप मॉक मोड (लाइव्ह जनरेशनसाठी GEMINI_API_KEY सेट करा)",
        "cannot_answer": "मी हे अधिकृत कायद्याच्या मजकुरातून पुष्टी करू शकत नाही.",
        "cannot_answer_summary": "या प्रश्नासाठी थेट कोणतीही सत्यापित तरतूद नाही.",
        "guard_hallucination": "गार्ड नकार: उद्धृत कायद्याचा मजकूर अधिकृत गॅझेटशी सत्यापित केला जाऊ शकला नाही.",
        "guard_hallucination_summary": "असत्यापित कायदेशीर दावे LawSathi च्या गार्डने नाकारले.",
        "guard_section": "गार्ड नकार: कलम उद्धरण असत्यापित.",
        "guard_section_summary": "सत्यापन अयशस्वी.",
        "provider_error": "सेवा तात्पुरती अनुपलब्ध आहे.",
        "provider_error_summary": "ऑफलाइन फॉलबॅक सक्रिय.",
    },
}

def msg(lang: str, key: str, **kwargs) -> str:
    """Get a translated message string, falling back to English."""
    lang_msgs = MESSAGES.get(lang, MESSAGES["en"])
    text = lang_msgs.get(key, MESSAGES["en"].get(key, key))
    return text.format(**kwargs) if kwargs else text

def check_safety(text: str, lang: str = "en") -> Optional[Dict[str, Any]]:
    lowered = text.lower()
    for pattern in SAFETY_TRIGGERS:
        if re.search(pattern, lowered, re.IGNORECASE):
            return {
                "kind": "immediate_danger",
                "message": msg(lang, "emergency"),
                "helplines": ["112", "181"]
            }
    return None

# ───────────────────── 2. DETERMINISTIC GUARD ─────────────────────
def normalize_text(text: str) -> str:
    """Normalize text: remove punctuation, collapse whitespace, lowercase."""
    text = unicodedata.normalize("NFKC", text).lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def verify_quote(quote: str, original_chunk_text: str) -> bool:
    """Deterministic check: quoted text must exist verbatim in the official chunk."""
    norm_quote = normalize_text(quote)
    norm_source = normalize_text(original_chunk_text)
    words = norm_quote.split()
    if len(words) < 3:
        return False
    return norm_quote in norm_source

# ───────────────────── 3. IN-MEMORY RETRIEVAL ─────────────────────
def search_corpus(query: str, top_k: int = 2) -> List[Dict[str, Any]]:
    """Simple keyword & token overlap retrieval for prototype."""
    query_tokens = set(normalize_text(query).split())
    scored_chunks = []

    for chunk in CORPUS_CHUNKS:
        score = 0
        keywords = chunk.get("keywords", [])
        for kw in keywords:
            if kw in query.lower():
                score += 3
        chunk_tokens = set(normalize_text(chunk["text"] + " " + chunk["heading"]).split())
        score += len(query_tokens.intersection(chunk_tokens))
        if score > 0:
            scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return [chunk for score, chunk in scored_chunks[:top_k]]

# ───────────────────── 4. SCHEMAS ─────────────────────
class AskRequest(BaseModel):
    question: str
    lang: str = "en"

# ───────────────────── 5. ROUTES ─────────────────────
@app.get("/health")
def health():
    return {
        "status": "ok",
        "corpus_chunks": len(CORPUS_CHUNKS),
        "gemini_configured": bool(GEMINI_API_KEY)
    }

@app.get("/v1/helplines")
def get_helplines():
    return {"items": HELPLINES_DATA}

@app.get("/v1/playbooks/{playbook_id}")
def get_playbook(playbook_id: str, lang: str = "en"):
    filename = f"{playbook_id}.{lang}.json"
    filepath = os.path.join(CONTENT_DIR, "playbooks", filename)
    if not os.path.exists(filepath):
        filepath = os.path.join(CONTENT_DIR, "playbooks", f"{playbook_id}.en.json")
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Playbook not found")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

@app.post("/v1/ask")
async def ask_legal_question(req: AskRequest):
    lang = req.lang if req.lang in MESSAGES else "en"

    # Phase A: Safety Router
    safety_alert = check_safety(req.question, lang)
    if safety_alert:
        return {
            "tier": 3,
            "badge": "emergency_override",
            "safety": safety_alert,
            "answer": {
                "quotes": [],
                "summary": safety_alert["message"],
                "helplines": safety_alert["helplines"]
            }
        }

    # Phase B: Retrieval
    retrieved = search_corpus(req.question)
    if not retrieved:
        return {
            "tier": 3,
            "badge": "not_confirmed",
            "message": msg(lang, "no_corpus"),
            "answer": {
                "quotes": [],
                "summary": msg(lang, "no_corpus_summary"),
                "helplines": ["112", "15100"]
            }
        }

    # Mock Mode: No GEMINI_API_KEY configured — return grounded chunk with translated summary
    if not GEMINI_API_KEY:
        top_chunk = retrieved[0]
        # Use plain_line from the playbook JSON for the selected language if available
        plain_summary = _get_localised_plain_line(top_chunk["section_id"], lang)
        if not plain_summary:
            plain_summary = msg(lang, "mock_summary",
                                act=top_chunk["act"],
                                section=top_chunk["section"])
        return {
            "tier": 2,
            "badge": "from_the_law",
            "note": msg(lang, "mock_note"),
            "answer": {
                "quotes": [
                    {
                        "section_id": top_chunk["section_id"],
                        "act": top_chunk["act"],
                        "section": top_chunk["section"],
                        "quote": top_chunk["text"][:300] + "...",
                        "verified": True
                    }
                ],
                "summary": plain_summary,
                "helplines": ["112"]
            }
        }


def _get_localised_plain_line(section_id: str, lang: str) -> str:
    """Look up a human-readable plain_line for a section from the playbook files."""
    if lang == "en":
        return ""  # let caller use generic English template
    for playbook_file in ["fir_refusal"]:
        filepath = os.path.join(CONTENT_DIR, "playbooks", f"{playbook_file}.{lang}.json")
        if not os.path.exists(filepath):
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            pb = json.load(f)
        for law in pb.get("law", []):
            if law.get("section_id") == section_id:
                return law.get("plain_line", "")
    return ""

    # Phase C: LLM Generation with Grounding Prompt
    chunk_context = "\n\n".join(
        [f"[{c['section_id']}] ({c['act']} §{c['section']}): {c['text']}" for c in retrieved]
    )
    prompt = f"""You are LawSathi. Answer the citizen's question strictly and exclusively from the Legal Context provided below.
Rules:
1. Extract an EXACT, VERBATIM quote from the context that directly answers the question. Do not modify or translate the quote.
2. Write a 1-sentence plain-language explanation of what this means for the citizen.
3. If the context does not contain the answer, respond with "CANNOT_ANSWER".

Legal Context:
{chunk_context}

Citizen Question:
{req.question}

Respond ONLY in JSON format:
{{
  "section_id": "<section_id from context>",
  "quote": "<exact verbatim sentence from text>",
  "plain_summary": "<1-sentence plain explanation>"
}}
"""

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.0, "responseMimeType": "application/json"}
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.post(url, json=payload)
            res.raise_for_status()
            data = res.json()
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed = json.loads(raw_text)

        if "CANNOT_ANSWER" in raw_text or not parsed.get("quote"):
            return {
                "tier": 3,
                "badge": "not_confirmed",
                "message": msg(lang, "cannot_answer"),
                "answer": {
                    "quotes": [],
                    "summary": msg(lang, "cannot_answer_summary"),
                    "helplines": ["112"]
                }
            }

        # Phase D: Quote-Verification Guard
        matching_chunk = next(
            (c for c in retrieved if c["section_id"] == parsed["section_id"]), None
        )
        if not matching_chunk:
            return {
                "tier": 3,
                "badge": "not_confirmed",
                "message": msg(lang, "guard_section"),
                "answer": {"quotes": [], "summary": msg(lang, "guard_section_summary"), "helplines": ["112"]}
            }

        is_valid = verify_quote(parsed["quote"], matching_chunk["text"])
        if not is_valid:
            return {
                "tier": 3,
                "badge": "not_confirmed",
                "guard_status": "REJECTED_HALLUCINATION",
                "message": msg(lang, "guard_hallucination"),
                "answer": {
                    "quotes": [],
                    "summary": msg(lang, "guard_hallucination_summary"),
                    "helplines": ["112"]
                }
            }

        # Tier 2 Verified Response — use localised plain_line if available
        localised_summary = _get_localised_plain_line(matching_chunk["section_id"], lang)
        return {
            "tier": 2,
            "badge": "from_the_law",
            "guard_status": "VERIFIED",
            "answer": {
                "quotes": [
                    {
                        "section_id": matching_chunk["section_id"],
                        "act": matching_chunk["act"],
                        "section": matching_chunk["section"],
                        "quote": parsed["quote"],
                        "verified": True
                    }
                ],
                "summary": localised_summary or parsed["plain_summary"],
                "helplines": ["112", "15100"]
            }
        }

    except Exception as e:
        return {
            "tier": 3,
            "badge": "provider_error",
            "message": msg(lang, "provider_error"),
            "answer": {
                "quotes": [],
                "summary": msg(lang, "provider_error_summary"),
                "helplines": ["112"]
            }
        }
