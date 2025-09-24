
import re
from typing import Tuple

SENSITIVE_KEYWORDS = [
    "suicide", "suicídio", "suicidio", "bomb", "explosive", "assalto", "ataque", "terror",
    "sexo", "porn", "drugs", "drogas", "homicidio", "homicídio"
]

PII_PATTERNS = [
    re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"),  # CPF
    re.compile(r"\b\d{11}\b"),  # 11 digits
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")  # email
]

def check_guardrails(text: str) -> Tuple[bool, str]:
    t = text.lower()
    for kw in SENSITIVE_KEYWORDS:
        if kw in t:
            return True, f"sensitive_keyword:{kw}"
    for pat in PII_PATTERNS:
        if pat.search(text):
            return True, "pii_detected"
    return False, "ok"
