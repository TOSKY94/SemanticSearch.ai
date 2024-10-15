from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class Vectorizer:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def vectorize_text(self, text: str):
        return self.model.encode(text)
    
    def chunk_text(self, text: str, chunk_size : int):
        words = text.split()
        chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
        return chunks
    
    def vectorize_chunks(self, text: str, chunk_size : int):
        chunks = self.chunk_text(text, chunk_size)
        embeddings = [self.vectorize_text(chunk) for chunk in chunks]
        return chunks, embeddings