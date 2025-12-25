# src/threat_intel/intel_sources/greynoise.py

import requests
from bs4 import BeautifulSoup

def enrich_ip_greynoise(ip):
    url = f"https://viz.greynoise.io/ip/{ip}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        resp = requests.get(url, headers=headers, timeout=6)
        soup = BeautifulSoup(resp.text, "lxml")

        tag = soup.find("span", text=lambda t: t and "Classification" in t)
        classification = tag.find_next("span").text.strip() if tag else "unknown"

        return {
            "classification": classification,
            "source": url
        }
    except Exception as e:
        return {"error": str(e)}
