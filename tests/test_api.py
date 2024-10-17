import pytest
import json
import azure.functions as func
from unittest.mock import patch, MagicMock
from search_func import main as search_main
from text_func import main as text_main
from healthcheck_func import main as healthcheck_main

@pytest.fixture
def mock_req():
    return MagicMock(spec=func.HttpRequest)

# Test for adding text successfully
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
        response = text_main(mock_req)

    # Assert
    assert response.status_code == 200
    body = json.loads(response.get_body().decode())
    assert body["message"] == "Text stored successfully"
    assert body["chunks"] == 2

# Test for failing to add text
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
        response = text_main(mock_req)

    # Assert
    assert response.status_code == 500
    assert response.get_body().decode() == 'Error storing text'

# Test for successful search
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
        response = search_main(mock_req)

    # Assert
    assert response.status_code == 200
    body = json.loads(response.get_body().decode())
    assert body["query"] == "Sample query"
    assert len(body["top_results"]) == 2

# Test for no search results
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
        response = search_main(mock_req)

    # Assert
    assert response.status_code == 404
    assert response.get_body().decode() == 'No results found'

# Test for healthcheck route
def test_healthcheck(mock_req):
    # Arrange
    mock_req.route_params = {"route": "healthcheck"}

    # Act
    with patch("app.services.db_utils.DBUtils.db_health_check", return_value=(False, "Error setting up Cosmos DB connection: Missing Cosmos DB environment variables: COSMOS_URI, COSMOS_KEY, COSMOS_DATABASE, COSMOS_CONTAINER")):
        response = healthcheck_main(mock_req)

    # Assert
    assert response.status_code == 200
    body = json.loads(response.get_body().decode())
    assert body["is_healthy"] == False
    assert body["message"] == "Error setting up Cosmos DB connection: Missing Cosmos DB environment variables: COSMOS_URI, COSMOS_KEY, COSMOS_DATABASE, COSMOS_CONTAINER"

