from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class RAGEngine:

    def __init__(self):

        self.vectorizer = TfidfVectorizer()

        self.text_chunks = []

        self.vectors = None

    def create_embeddings(self, df):

        self.text_chunks = []

        for _, row in df.iterrows():

            text = ' | '.join([
                f'{col}: {row[col]}'
                for col in df.columns
            ])

            self.text_chunks.append(text)

        self.vectors = self.vectorizer.fit_transform(
            self.text_chunks
        )

    def search(self, query, top_k=5):

        if self.vectors is None:
            return []

        query_vector = self.vectorizer.transform([query])

        similarities = cosine_similarity(
            query_vector,
            self.vectors
        )[0]

        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []

        for idx in top_indices:
            results.append(self.text_chunks[idx])

        return results