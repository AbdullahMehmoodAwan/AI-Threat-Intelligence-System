import joblib
import pandas as pd

class TraditionalAnomalyDetector:
    def __init__(self):
        self.if_model = joblib.load("models/isolation_forest.pkl")
        self.svm_model = joblib.load("models/oneclass_svm.pkl")

    def predict_isolation_forest(self, X):
        preds = self.if_model.predict(X)
        return [1 if p == -1 else 0 for p in preds]

    def predict_svm(self, X):
        preds = self.svm_model.predict(X)
        return [1 if p == -1 else 0 for p in preds]
