import requests

def enrich_domain_threatminer(domain):
    url = f"https://api.threatminer.org/v2/domain.php?q={domain}&rt=1"
    try:
        res = requests.get(url, timeout=6).json()
        return res
    except:
        return {"error": "lookup failed"}
