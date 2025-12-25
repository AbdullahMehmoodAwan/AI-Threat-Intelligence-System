# src/ml/anomaly_detector.py

from sklearn.ensemble import IsolationForest
from sklearn.exceptions import NotFittedError
import numpy as np


class AnomalyDetector:
    """
    Wrapper around IsolationForest for future use.

    Currently not used by fusion_engine, but made robust so that if
    score() is called before training, it will safely return 0.0 instead
    of crashing the app.
    """

    def __init__(self, contamination: float = 0.05):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self._fitted = False

    def train(self, data):
        """
        data: numpy array of shape (n_samples, n_features)
        """
        self.model.fit(data)
        self._fitted = True

    def score(self, x):
        """
        x: 1D feature vector (length n_features).
        Returns a positive float: higher = more anomalous.
        """
        x = np.asarray(x).reshape(1, -1)
        if not self._fitted:
            # Not trained yet; don't crash, just return neutral anomaly.
            return 0.0

        try:
            return float(-self.model.decision_function(x)[0])
        except NotFittedError:
            return 0.0
