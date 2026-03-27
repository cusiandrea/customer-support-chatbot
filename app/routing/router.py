import re
from typing import Dict, List


CATEGORY_KEYWORDS = {
    "shipping": [
        "shipping", "shipment", "delivery", "deliver", "tracking",
        "where is my order", "late delivery", "package"
    ],
    "returns": [
        "return", "send back", "return policy", "return label"
    ],
    "refund": [
        "refund", "money back", "reimbursement"
    ],
    "payment": [
        "payment", "paid", "charged", "double charge", "card", "paypal",
        "billing", "invoice"
    ],
    "order_change": [
        "change order", "cancel order", "modify order", "change address"
    ]
}

COMPLEX_PATTERNS = [
    "double charge",
    "charged twice",
    "fraud",
    "scam",
    "account locked",
    "cannot access my account",
    "delivered but not received",
    "wrong item and refund",
    "urgent",
    "lawsuit",
    "chargeback"
]


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def detect_categories(text: str) -> List[str]:
    text = normalize_text(text)
    detected = []

    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                detected.append(category)
                break

    return detected


def is_complex(text: str, categories: List[str]) -> bool:
    text = normalize_text(text)

    if len(categories) > 1:
        return True

    for pattern in COMPLEX_PATTERNS:
        if pattern in text:
            return True

    if len(text.split()) > 35:
        return True

    return False


def route_query(text: str) -> Dict:
    categories = detect_categories(text)

    if not categories:
        return {
            "route": "complex",
            "category": "other",
            "reason": "No clear policy-related category detected."
        }

    complex_flag = is_complex(text, categories)

    return {
        "route": "complex" if complex_flag else "simple",
        "category": categories[0],
        #"category": categories,
        "reason": "Complex case detected by routing rules." if complex_flag
                 else "Single clear policy question detected."
    }