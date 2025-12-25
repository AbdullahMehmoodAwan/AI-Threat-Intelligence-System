import re

def extract_iocs(text):
    ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text)
    urls = re.findall(r"https?://[^\s]+", text)
    domains = re.findall(r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}\b", text)
    hashes = re.findall(r"\b[a-fA-F0-9]{32}\b|\b[a-fA-F0-9]{40}\b|\b[a-fA-F0-9]{64}\b", text)
    cves = re.findall(r"\bCVE-\d{4}-\d{4,7}\b", text)
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)

    return {
        "ips": list(set(ips)),
        "urls": list(set(urls)),
        "domains": list(set(domains)),
        "hashes": list(set(hashes)),
        "cves": list(set(cves)),
        "emails": list(set(emails))
    }
