# src/threat_intel/enrich.py

import requests
from bs4 import BeautifulSoup
from src.threat_intel.intel_sources.abuseipdb import enrich_ip_abuseipdb
from src.threat_intel.intel_sources.otx import enrich_ip_otx
from src.threat_intel.intel_sources.greynoise import enrich_ip_greynoise
from src.threat_intel.intel_sources.virustotal import enrich_hash_virustotal
from src.threat_intel.intel_sources.threatminer import enrich_domain_threatminer

def enrich_iocs(iocs: dict):
    enriched = {
        "ips": [],
        "urls": [],
        "domains": [],
        "hashes": [],
        "emails": []
    }

    # ---- IP ENRICHMENT ----
    for ip in iocs.get("ips", []):
        info = {
            "value": ip,
            "abuseipdb": enrich_ip_abuseipdb(ip),
            "otx": enrich_ip_otx(ip),
            "greynoise": enrich_ip_greynoise(ip),
        }
        enriched["ips"].append(info)

    # ---- DOMAIN ENRICHMENT ----
    for domain in iocs.get("domains", []):
        enriched["domains"].append({
            "value": domain,
            "threatminer": enrich_domain_threatminer(domain)
        })

    # ---- HASH ENRICHMENT ----
    for h in iocs.get("hashes", []):
        enriched["hashes"].append({
            "value": h,
            "virustotal": enrich_hash_virustotal(h)
        })

    # Emails currently no enrichment
    for email in iocs.get("emails", []):
        enriched["emails"].append({"value": email, "note": "email enrichment coming soon"})

    return enriched
