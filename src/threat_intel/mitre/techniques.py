MITRE_TECHNIQUES = [
    # ----- CREDENTIAL ACCESS -----
    {
        "id": "T1110",
        "tactic": "Credential Access",
        "technique": "Brute Force",
        "keywords": ["failed login", "authentication failure", "bruteforce", "ssh", "multiple failed"]
    },

    # ----- EXECUTION -----
    {
        "id": "T1059",
        "tactic": "Execution",
        "technique": "Command-Line Execution",
        "keywords": ["cmd.exe", "powershell", "bash", "shell command"]
    },
    {
        "id": "T1204",
        "tactic": "Execution",
        "technique": "User Execution",
        "keywords": [".exe downloaded", "file downloaded", "dropper", ".exe"]
    },

    # ----- DEFENSE EVASION -----
    {
        "id": "T1027",
        "tactic": "Defense Evasion",
        "technique": "Obfuscated/Encrypted File",
        "keywords": ["encoded", "encrypted", "packed", "obfuscated"]
    },

    # ----- PERSISTENCE -----
    {
        "id": "T1053",
        "tactic": "Persistence",
        "technique": "Scheduled Task",
        "keywords": ["cron", "scheduled task", "schtasks"]
    },

    # ----- C2 COMMUNICATION -----
    {
        "id": "T1568",
        "tactic": "Command and Control",
        "technique": "Dynamic Resolution",
        "keywords": ["dns", "domain", "c2", "command and control"]
    },
    {
        "id": "T1571",
        "tactic": "Command and Control",
        "technique": "Non-Standard Port",
        "keywords": ["port 8080", "port 4444", "weird port"]
    },

    # ----- EXFILTRATION -----
    {
        "id": "T1048",
        "tactic": "Exfiltration",
        "technique": "Exfiltration Over Alternative Protocol",
        "keywords": ["ftp", "http upload", "exfil"]
    },

    # ----- INITIAL ACCESS -----
    {
        "id": "T1189",
        "tactic": "Initial Access",
        "technique": "Drive-by Compromise",
        "keywords": ["url", "malicious site", "redirect"]
    },
    {
        "id": "T1566",
        "tactic": "Initial Access",
        "technique": "Phishing",
        "keywords": ["email", "phishing", "attachment"]
    }
]
