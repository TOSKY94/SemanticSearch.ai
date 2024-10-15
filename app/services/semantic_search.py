from scipy.spatial.distance import cosine
from app.services.vectorizer import Vectorizer
from app.services.db_utils import DBUtils

class SemanticSearch:
    def __init__(self):
        pass

    def store_text(self, text: str, session_id: str, chunk_size: int):
        """Stores the text by chunking and embedding it."""
        try:
            vectorizer = Vectorizer()
            chunks, embeddings = vectorizer.vectorize_chunks(text, chunk_size)

            db = DBUtils()
            db.store_chunk(session_id, chunks, embeddings)
            return (True, len(chunks))
        except Exception as e:
            print(e)
            return (False, 0)

    def search_text(self, query: str, session_id: str, limit: int = 3):
        """Searches for the most similar text chunks to the query."""
        try:
            db = DBUtils()
            chunks, embeddings = db.get_chunks(session_id)  # Retrieve stored chunks and embeddings

            if (len(chunks) == 0 or len(embedding) == 0):
                return None
            similarity_scores = []
            vectorizer = Vectorizer()
            query_embedding = vectorizer.vectorize_text(query)  # Vectorize the query

            # Calculate cosine similarity for each chunk embedding
            for i, embedding in enumerate(embeddings):
                similarity = cosine(query_embedding, embedding)  # Lower is better (more similar)
                similarity_scores.append((i, similarity))  # Store index and similarity score

            # Sort the results by similarity (ascending order)
            similarity_scores.sort(key=lambda x: x[1])  # Sort by similarity score (lower is better)

            # Retrieve the top N most similar chunks
            results = []
            for i in range(min(limit, len(similarity_scores))):
                chunk_index = similarity_scores[i][0]  # Get the chunk index
                results.append(chunks[chunk_index])    # Append the corresponding chunk

            return results

        except Exception as e:
            print(f"Error during search: {e}")
            return None
