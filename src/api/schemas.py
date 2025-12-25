from pydantic import BaseModel

class LogInput(BaseModel):
    text: str

class FusionOutput(BaseModel):
    threat_type: int
    iocs: dict
    summary: str
    anomaly_score: float
