from scipy.spatial.distance import cosine
from app.services.vectorizer import Vectorizer
from app.services.db_utils import DBUtils
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SemanticSearch:
    def __init__(self):
        pass

    def store_text(self, text: str, session_id: str, chunk_size: int):
        """Stores the text by chunking and embedding it."""
        try:
            vectorizer = Vectorizer()
            chunks, embeddings = vectorizer.vectorize_chunks(text, chunk_size)

            db = DBUtils()
            success = db.store_chunk(session_id, chunks, embeddings)

            if not success:
                return (False, 0)
            return (True, len(chunks))
        
        except Exception as e:
            logger.error(f"error occured:: {e}")
            raise e

    def search_text(self, query: str, session_id: str, limit: int = 3, base_similarity: float = 0.0):
        """Searches for the most similar text chunks to the query."""
        try:
            db = DBUtils()
            chunks, embeddings = db.get_chunks(session_id)  
            
            if len(chunks) == 0 or len(embeddings) == 0:
                return None

            similarity_scores = []
            vectorizer = Vectorizer()
            query_embedding = vectorizer.vectorize_text(query)  
            
            for i, embedding in enumerate(embeddings):
                similarity = 1 - cosine(query_embedding, embedding)
                if similarity >= base_similarity:
                    similarity_scores.append((i, similarity))

            similarity_scores.sort(key=lambda x: x[1], reverse = True)

            results = []
            for i in range(min(limit, len(similarity_scores))):
                chunk_index, score = similarity_scores[i]
                results.append((chunks[chunk_index], score))

            return results

        except Exception as e:
            logger.error(f"error occured:: {e}")
            raise e
