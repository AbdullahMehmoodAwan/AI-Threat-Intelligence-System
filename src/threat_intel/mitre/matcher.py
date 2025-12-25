from src.threat_intel.mitre.techniques import MITRE_TECHNIQUES

def map_to_mitre(summary: str, iocs: dict):
    summary = summary.lower()
    mitre_hits = []

    def add_hit(t):
        mitre_hits.append({
            "id": t["id"],
            "technique": t["technique"],
            "tactic": t["tactic"]
        })

    # Match based on summary text
    for tech in MITRE_TECHNIQUES:
        for keyword in tech["keywords"]:
            if keyword in summary:
                add_hit(tech)
                break

    # Match based on IOC types
    if iocs.get("domains"):
        add_hit(next(t for t in MITRE_TECHNIQUES if t["id"] == "T1568"))

    if iocs.get("hashes"):
        add_hit(next(t for t in MITRE_TECHNIQUES if t["id"] == "T1204"))

    if iocs.get("emails"):
        add_hit(next(t for t in MITRE_TECHNIQUES if t["id"] == "T1566"))

    return mitre_hits
