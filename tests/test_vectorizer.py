from app.services.vectorizer import Vectorizer
from numpy import ndarray


def test_chunk_text():

    # Arrange
    text = "This is a test. " * 50  

    # Act
    chunks = Vectorizer().chunk_text(text, chunk_size=5)  

    # Assert
    assert len(chunks) > 0  
    assert all(len(chunk.split()) <= 5 for chunk in chunks)

def test_vectorize_text():

    # Arrange
    text = "This is a test sentence."

    # Act
    embedding = Vectorizer().vectorize_text(text)

    # Assert
    assert isinstance(embedding, (list, ndarray))
    assert len(embedding) > 0 

def test_vectorize_chunks():

    # Arrange
    text = "This is a test sentence." * 50  

    # Act
    chunks, embeddings = Vectorizer().vectorize_chunks(text, chunk_size = 5)

    # Assert
    assert isinstance(embeddings, list)
    assert isinstance(chunks, list)
    assert len(embeddings) > 0 
    assert len(chunks) > 0