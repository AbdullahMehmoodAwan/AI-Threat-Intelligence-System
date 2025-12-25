import torch
import pandas as pd
from src.anomaly_detection.autoencoder import Autoencoder

class AutoencoderEngine:
    def __init__(self, input_dim):
        self.model = Autoencoder(input_dim)
        self.model.load_state_dict(torch.load("models/autoencoder.pt"))
        self.model.eval()

    def compute_score(self, X):
        X = torch.tensor(X, dtype=torch.float32)
        with torch.no_grad():
            reconstructed = self.model(X)
            mse = torch.mean((X - reconstructed)**2, dim=1)
        return mse.numpy()
