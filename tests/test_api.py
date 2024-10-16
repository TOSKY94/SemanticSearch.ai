import pytest
import json
import azure.functions as func
from unittest.mock import patch, MagicMock
from semanticsearchazf import main

@pytest.fixture
def mock_req():
    return MagicMock(spec=func.HttpRequest)

def test_add_text_success(mock_req):
    # Arrange
    mock_req.get_json.return_value = {
        "text": "This is a sample text to be chunked.",
        "session_id": "1234",
        "chunk_size": 300
    }
    mock_req.route_params = {"route": "text"}

    # Act
    with patch("app.services.semantic_search.SemanticSearch.store_text", return_value=(True, 2)):
        response = main(mock_req)

    # Assert
    assert response.status_code == 200
    body = json.loads(response.get_body())
    assert body["message"] == "Text stored successfully"
    assert body["chunks"] == 2

def test_add_text_failure(mock_req):
    # Arrange
    mock_req.get_json.return_value = {
        "text": "This is a failing test.",
        "session_id": "1234",
        "chunk_size": 300
    }
    mock_req.route_params = {"route": "text"}

    # Act
    with patch("app.services.semantic_search.SemanticSearch.store_text", return_value=(False, None)):
        response = main(mock_req)

    # Assert
    assert response.status_code == 500
    assert response.get_body().decode() == 'Error storing text'

def test_search_text_success(mock_req):
    # Arrange
    mock_req.get_json.return_value = {
        "query": "Sample query",
        "session_id": "1234",
        "limit": 2
    }
    mock_req.route_params = {"route": "search"}

    # Act
    with patch("app.services.semantic_search.SemanticSearch.search_text", return_value=["chunk1", "chunk2"]):
        response = main(mock_req)

    # Assert
    assert response.status_code == 200
    body = json.loads(response.get_body())
    assert body["query"] == "Sample query"
    assert len(body["top_results"]) == 2

def test_search_text_no_results(mock_req):
    # Arrange
    mock_req.get_json.return_value = {
        "query": "no match",
        "session_id": "1234",
        "limit": 5
    }
    mock_req.route_params = {"route": "search"}

    # Act
    with patch("app.services.semantic_search.SemanticSearch.search_text", return_value=None):
        response = main(mock_req)

    # Assert
    assert response.status_code == 404
    assert response.get_body().decode() == 'No results found'

def test_healthcheck(mock_req):
    # Arrange
    mock_req.route_params = {"route": "healthcheck"}

    # Act
    response = main(mock_req)

    # Assert
    assert response.status_code == 200
    assert response.get_body().decode() == 'Semantic Search API is running!'

def test_invalid_route(mock_req):
    # Arrange
    mock_req.route_params = {"route": "invalid"}

    # Act
    response = main(mock_req)

    # Assert
    assert response.status_code == 404
    assert response.get_body().decode() == 'Route not found'