def enrich_hash_virustotal(h):
    return {
        "note": "Public VirusTotal page exists",
        "url": f"https://www.virustotal.com/gui/file/{h}"
    }
