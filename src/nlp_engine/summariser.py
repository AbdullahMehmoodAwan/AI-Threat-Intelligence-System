# src/nlp_engine/summariser.py

import re


def summarise_text(text: str, max_len: int = 240) -> str:
    """
    Simple, SOC-style rule-based summariser for logs.

    Instead of using a generic language model (like T5),
    this function looks for common security patterns and
    produces short, professional summaries that an analyst
    can actually understand and act on.
    """

    if not text or not text.strip():
        return "No log content provided."

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    lower = text.lower()

    # --- Helpers ---
    def first_ip() -> str | None:
        ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text)
        return ips[0] if ips else None

    def first_cve() -> str | None:
        cves = re.findall(r"\bCVE-\d{4}-\d{4,7}\b", text, flags=re.IGNORECASE)
        return cves[0].upper() if cves else None

    ip = first_ip()
    cve = first_cve()

    # --- SSH brute-force attempts ---
    if "sshd" in lower and "failed password" in lower:
        attempts = lower.count("failed password")
        src_ip = ip or "an external IP address"
        return (
            f"Detected {attempts} failed SSH login attempt(s) from {src_ip}; "
            f"this activity is consistent with a possible SSH brute-force attack."
        )

    # --- Exploit / CVE activity ---
    if cve:
        if ip:
            return (
                f"Detected possible exploitation activity related to {cve} "
                f"originating from {ip}."
            )
        return f"Detected log activity referencing vulnerability {cve}."
