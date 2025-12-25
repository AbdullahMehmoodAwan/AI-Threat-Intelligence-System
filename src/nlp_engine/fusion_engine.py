# src/nlp_engine/fusion_engine.py

import os
import torch

from transformers import AutoTokenizer, AutoModelForSequenceClassification

from src.nlp_engine.ioc_extractor import extract_iocs
from src.nlp_engine.summariser import summarise_text
from src.anomaly_detection.ae_model import AutoencoderScorer
from src.threat_intel.enrich import enrich_iocs
from src.threat_intel.mitre.matcher import map_to_mitre


# ------------------------------
# PATHS & MODEL LOADING
# ------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "bert_threat_classifier")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
classifier = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH, local_files_only=True
)

AE_PATH = os.path.join(BASE_DIR, "data", "processed", "autoencoder_scores.csv")
ae = AutoencoderScorer(AE_PATH)


# ------------------------------
# THREAT CLASSIFICATION
# ------------------------------

def classify_threat(text: str) -> int:
    """
    Run the BERT threat classifier and clamp output to 0–3
    so it matches the UI's Low/Med/High/Critical levels.
    """
    tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        logits = classifier(**tokens).logits

    raw_label = int(logits.argmax(dim=1).item())
    # Clamp to 0–3 for frontend + analytics:
    # 0 = Low, 1 = Medium, 2 = High, 3 = Critical
    return max(0, min(raw_label, 3))


# ------------------------------
# IOC FLATTENING FOR UI
# ------------------------------

def flatten_iocs(enriched_iocs: dict) -> dict:
    """
    Take enriched IOC structures like:
        {"value": "1.2.3.4", "abuseipdb": {...}, ...}
    and return a simple dict of lists of strings for the frontend:
        {"ips": ["1.2.3.4", ...], ...}
    """
    clean = {}
    for key, arr in enriched_iocs.items():
        clean[key] = []
        for item in arr:
            if isinstance(item, dict):
                # Prefer the 'value' field if present
                clean[key].append(item.get("value", str(item)))
            else:
                clean[key].append(str(item))
    return clean


# ------------------------------
# MAIN FUSION ENGINE
# ------------------------------

def fusion_engine(text: str) -> dict:
    """
    Main analysis pipeline used by /fusion endpoint.
    Returns only the fields that the FastAPI FusionOutput model expects:
        - threat_type: int
        - iocs: dict
        - summary: str
        - anomaly_score: float
    """

    # 1. Threat level (0–3)
    threat_type = classify_threat(text)

    # 2. Raw IOC extraction
    raw_iocs = extract_iocs(text)

    # 3. IOC enrichment (AbuseIPDB, OTX, GreyNoise, VT, ThreatMiner, etc.)
    enriched_iocs = enrich_iocs(raw_iocs)

    # 4. Flatten IOCs for clean dashboard display
    ui_iocs = flatten_iocs(enriched_iocs)

    # 5. Summary (T5-based)
    summary = summarise_text(text)

    # 6. Stable heuristic anomaly score
    anomaly_score = float(ae.score_text(text))

    # 7. MITRE mapping (available if you want to log/use it)
    _mitre_hits = map_to_mitre(summary, raw_iocs)
    # You can log _mitre_hits to history or a separate field later if needed.

    # FINAL RESPONSE: match FusionOutput schema exactly
    return {
        "threat_type": threat_type,
        "iocs": ui_iocs,
        "summary": summary,
        "anomaly_score": anomaly_score,
    }
