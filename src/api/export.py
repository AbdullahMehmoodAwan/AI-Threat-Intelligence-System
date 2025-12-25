from fastapi import APIRouter
from fastapi.responses import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import red, yellow, green, blue
import uuid
import os

router = APIRouter()
EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

def severity_color(level):
    if level >= 3: return red
    if level == 2: return yellow
    if level == 1: return green
    return blue

@router.post("/export/pdf")
def export_pdf(data: dict):
    file_path = f"{EXPORT_DIR}/{uuid.uuid4()}.pdf"

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "SentinelAI Threat Report")

    # Severity
    c.setFillColor(severity_color(data["threat_type"]))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 90, f"Threat Level: {data['threat_type']}")
    c.setFillColor(blue)

    # Summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 130, "Summary:")
    c.setFont("Helvetica", 12)

    t = c.beginText(50, height - 150)
    t.textLines(data["summary"])
    c.drawText(t)

    # IOCs
    y = height - 250
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Indicators of Compromise:")
    y -= 20
    c.setFont("Helvetica", 12)
    for k, arr in data["iocs"].items():
        for i in arr:
            c.drawString(50, y, f"- {k}: {i}")
            y -= 15

    # Anomaly score
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y - 30, f"Anomaly Score: {data['anomaly_score']}")

    c.save()
    return FileResponse(file_path, filename="SentinelAI_Report.pdf")
