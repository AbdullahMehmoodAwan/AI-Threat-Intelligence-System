from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.cluster import KMeans

class LogEmbedder:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.kmeans = None

    def embed(self, text):
        return self.model.encode([text])[0]

    def train_clusters(self, embeddings):
        self.kmeans = KMeans(n_clusters=4)
        self.kmeans.fit(embeddings)

    def predict_cluster(self, embedding):
        return int(self.kmeans.predict([embedding])[0])
