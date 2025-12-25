# src/threat_intel/intel_sources/abuseipdb.py

import requests
from bs4 import BeautifulSoup

def enrich_ip_abuseipdb(ip):
    url = f"https://www.abuseipdb.com/check/{ip}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        resp = requests.get(url, headers=headers, timeout=6)
        soup = BeautifulSoup(resp.text, "lxml")

        score_tag = soup.find("div", {"class": "well"})
        if not score_tag:
            return {"error": "No data"}

        score_text = score_tag.text.strip()

        return {
            "score_text": score_text[:200],
            "source": url
        }
    except Exception as e:
        return {"error": str(e)}
