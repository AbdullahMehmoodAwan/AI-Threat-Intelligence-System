# src/anomaly_detection/ae_model.py

import os
import pandas as pd


class AutoencoderScorer:
    """
    Heuristic anomaly scorer used by the app.

    It estimates how unusual a log's length is compared to a baseline
    distribution stored in data/processed/autoencoder_scores.csv.

    This is a lightweight stand-in for a full autoencoder-based anomaly
    detector, but is now robust and will not crash if the CSV is missing.
    """

    def __init__(self, score_file: str):
        self.mean = 200.0
        self.std = 50.0

        if os.path.isfile(score_file):
            try:
                df = pd.read_csv(score_file)
                if "score" in df.columns and not df["score"].empty:
                    m = float(df["score"].mean())
                    s = float(df["score"].std())
                    if s == 0:
                        s = 1.0
                    self.mean = m
                    self.std = s
            except Exception:
                # Fallback to defaults if file is malformed
                self.mean = 200.0
                self.std = 50.0

        if self.std == 0:
            self.std = 1.0

    def score_text(self, text: str) -> float:
        """
        Returns a stable float anomaly score:
        - roughly a z-score of length relative to baseline.
        - higher = more unusual.
        """
        length = len(text or "")
        z = abs(length - self.mean) / (self.std + 1e-6)
        return float(round(z, 3))
