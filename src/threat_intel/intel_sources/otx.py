# src/threat_intel/intel_sources/otx.py

import requests
from bs4 import BeautifulSoup

def enrich_ip_otx(ip):
    url = f"https://otx.alienvault.com/indicator/ip/{ip}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=6)
        soup = BeautifulSoup(res.text, "lxml")

        pulses = soup.find_all("div", {"class": "pulse-box"})
        pulse_titles = [p.find("h3").text.strip() for p in pulses[:5]]

        return {
            "pulse_count": len(pulses),
            "pulse_titles": pulse_titles,
            "source": url
        }
    except Exception as e:
        return {"error": str(e)}
