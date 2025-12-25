"""



<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>SentinelAI Threat Dashboard v3</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">

<style>
    body {
        background-color: #0d1117;
        color: #c9d1d9;
        padding: 20px;
        font-family: "Inter", sans-serif;
    }

    .glass-card {
        background: rgba(22, 27, 34, 0.6);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        border: 1px solid rgba(48, 54, 61, 0.5);
        padding: 24px;
        box-shadow: 0 0 20px rgba(0,0,0,0.3);
    }

    .btn-analyze {
        background-color: #238636;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
    }

    .btn-analyze:hover {
        background-color: #2ea043;
    }

    .severity-high { color: #f85149; font-weight: bold; }
    .severity-medium { color: #ffa657; font-weight: bold; }
    .severity-low { color: #2ea043; font-weight: bold; }

    pre {
        background: rgba(13, 17, 23, 0.6);
        padding: 12px;
        border-radius: 8px;
        font-size: 14px;
        border: 1px solid #30363d;
    }

    /* Loading Overlay */
    #spinnerOverlay {
        display: none;
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.6);
        z-index: 9999;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

</style>

</head>

<body>

<!-- LOADING OVERLAY -->
<div id="spinnerOverlay">
    <div class="spinner-border text-success" style="width: 60px; height: 60px;"></div>
    <p class="mt-3 text-white">Analyzing logs...</p>
</div>

<div class="container">

    <h2 class="mb-4">🛡️ SentinelAI Threat Dashboard <span class="text-success">v3</span></h2>

    <!-- INPUT CARD -->
    <div class="glass-card mb-4">
        <h5>Enter Logs</h5>
        <textarea id="logInput" class="form-control mb-3" rows="6"
                  placeholder="Paste logs here..."></textarea>

        <button class="btn btn-analyze text-white" onclick="analyzeLog()">Analyze</button>
        <button class="btn btn-secondary ms-2" onclick="downloadPDF()">⬇ Download Report</button>
    </div>

    <!-- OUTPUT CARD -->
    <div class="glass-card">
        <h5>Output</h5>
        <div id="output" class="mt-3">Awaiting input...</div>
    </div>

</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>

<script>
    async function analyzeLog() {
        const logText = document.getElementById("logInput").value;
        const output = document.getElementById("output");
        const spinner = document.getElementById("spinnerOverlay");

        if (!logText.trim()) {
            output.innerHTML = `<p class="text-danger">Please enter logs first.</p>`;
            return;
        }

        // show loading
        spinner.style.display = "flex";

        try {
            const res = await fetch("/fusion", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ text: logText })  // Backend expects "text"
            });

            const data = await res.json();
            spinner.style.display = "none";

            if (!res.ok) {
                output.innerHTML = `<p class="text-danger">Error: ${data.detail || "Could not analyze logs."}</p>`;
                return;
            }

            output.innerHTML = `
                <h6>Threat Classification:</h6>
                <p class="${getSeverityClass(data.threat_type)}">Level: ${data.threat_type}</p>

                <h6>IOC Extraction:</h6>
                <pre>${JSON.stringify(data.iocs, null, 2)}</pre>

                <h6>Summary:</h6>
                <pre>${data.summary}</pre>

                <h6>Anomaly Score:</h6>
                <p>${data.anomaly_score}</p>
            `;

        } catch (err) {
            spinner.style.display = "none";
            output.innerHTML = `<p class="text-danger">Error: Could not analyze logs.</p>`;
        }
    }

    function getSeverityClass(value) {
        if (value >= 3) return "severity-high";
        if (value === 2) return "severity-medium";
        return "severity-low";
    }

    // Save screenshot
    function downloadPDF() {
        const element = document.querySelector(".glass-card:last-of-type");

        html2canvas(element).then(canvas => {
            const link = document.createElement("a");
            link.download = "SentinelAI_Report.png";
            link.href = canvas.toDataURL("image/png");
            link.click();
        });
    }
</script>

</body>
</html>





"""