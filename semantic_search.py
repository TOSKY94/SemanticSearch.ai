from scipy.spatial.distance import cosine
from vectorizer import Vectorizer
from db_utils import DBUtils

class SemanticSearch:
    def __init__(self):
        pass

    def store_text(self, text: str, session_id: str):
        """Stores the text by chunking and embedding it."""
        print("Storing text")
        try:
            vectorizer = Vectorizer()
            chunks, embeddings = vectorizer.vectorize_chunks(text)

            db = DBUtils()
            db.store_chunk(session_id, chunks, embeddings)
            return True
        except Exception as e:
            print(e)
            return False

    def search_text(self, query: str, session_id: str, limit: int = 3):
        """Searches for the most similar text chunks to the query."""
        print("Searching text")
        try:
            db = DBUtils()
            chunks, embeddings = db.get_chunks(session_id)  # Retrieve stored chunks and embeddings
            
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
