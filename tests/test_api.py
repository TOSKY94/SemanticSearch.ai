import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)

@pytest.mark.asyncio
@patch("app.services.semantic_search.SemanticSearch.store_text", return_value=(True, 2))
async def test_add_text_success(mock_store_text):

    # Act
    response = client.post("/text", json={
        "text": "This is a sample text to be chunked.",
        "session_id": "1234",
        "chunk_size": 300
    })

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Text stored successfully"
    assert response.json()["chunks"] == 2

@pytest.mark.asyncio
@patch("app.services.semantic_search.SemanticSearch.store_text", return_value=(False, None))
async def test_add_text_failure(mock_store_text):

    # Act
    response = client.post("/text", json={
        "text": "This is a failing test.",
        "session_id": "1234",
        "chunk_size": 300
    })

    # Assert
    assert response.status_code == 500
    assert response.json()["detail"] == "Error storing text"

@pytest.mark.asyncio
@patch("app.services.semantic_search.SemanticSearch.search_text", return_value = ["chunk1", "chunk2"])
async def test_search_text_success(mock_search_text):

    # Act
    response = client.post("/search", json={
        "query": "Sample query",
        "session_id": "1234",
        "limit": 2
    })

    # Assert
    assert response.status_code == 200
    assert response.json()["query"] == "Sample query"
    assert len(response.json()["top_results"]) == 2

@pytest.mark.asyncio
@patch("app.services.semantic_search.SemanticSearch.search_text", return_value = None)
async def test_search_text_no_results(mock_search_text):

    # Act
    response = client.post("/search", json={
        "query": "no match",
        "session_id": "1234",
        "limit": 5
    })

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "No results found"
