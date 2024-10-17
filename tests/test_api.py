import pytest
import json
import azure.functions as func
from unittest.mock import patch, MagicMock
from search_func import main as search_main
from text_func import main as text_main
from healthcheck_func import main as healthcheck_main
from pdf2text_func import main as pdf2text_main

@pytest.fixture
def mock_req():
    return MagicMock(spec=func.HttpRequest)

# Define a function to create a mock PDF file
def create_mock_pdf_file(filename="test.pdf", content=b"%PDF-1.4 fake pdf content"):
    mock_file = MagicMock()
    mock_file.filename = filename
    mock_file.read.return_value = content
    return mock_file

mock_pdf_content = b"%PDF-1.4 fake pdf content"
mock_extracted_text = "This is extracted text from PDF."

# Test for extracting text successfully
@patch('app.services.pdf_utils.PDFUtils.extract_text_from_pdf', return_value=mock_extracted_text)
@patch('os.remove')
def test_pdf2text_success(mock_remove, mock_extract_text, mock_req):
    # Arrange
    file_data = {'file': create_mock_pdf_file()}
    mock_req.files = file_data

    # Act
    response = pdf2text_main(mock_req)

    # Assert
    assert response.status_code == 200
    body = json.loads(response.get_body().decode())
    assert body["extracted_text"] == mock_extracted_text

# Test for extracting text with invalid file type
@patch('app.services.pdf_utils.PDFUtils.extract_text_from_pdf', return_value=mock_extracted_text)
@patch('os.remove')
def test_pdf2text_invalid_file_type(mock_remove, mock_extract_text, mock_req):
    # Arrange
    file_data = {'file': create_mock_pdf_file(filename="test.txt", content=b"This is a text file.")}
    mock_req.files = file_data

    # Act
    response = pdf2text_main(mock_req)

    # Assert
    assert response.status_code == 400
    body = json.loads(response.get_body().decode())
    assert body['error'] == 'Invalid file type. Only PDF is allowed.'

# Test for pdf extraction error
@patch('app.services.pdf_utils.PDFUtils.extract_text_from_pdf', side_effect=Exception("Failed to process PDF"))
@patch('os.remove')
def test_pdf2text_processing_error(mock_remove, mock_extract_text, mock_req):
    # Arrange
    file_data = {'file': create_mock_pdf_file()}
    mock_req.files = file_data

    # Act
    response = pdf2text_main(mock_req)

    # Assert
    assert response.status_code == 500
    body = json.loads(response.get_body().decode())
    assert 'error' in body
    assert body['error'] == 'Failed to process PDF'

# Test for file deletion error
@patch('os.remove', side_effect=Exception("Failed to delete file"))
@patch('app.services.pdf_utils.PDFUtils.extract_text_from_pdf', return_value=mock_extracted_text)
def test_pdf2text_file_deletion_error(mock_extract_text, mock_remove, mock_req):
    # Arrange
    file_data = {'file': create_mock_pdf_file()}
    mock_req.files = file_data

    # Act
    response = pdf2text_main(mock_req)

    # Assert
    assert response.status_code == 200
    body = json.loads(response.get_body().decode())
    assert body["extracted_text"] == mock_extracted_text
    mock_remove.assert_called_once()
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
    body = json.loads(response.get_body().decode())
    assert body['error'] == 'Error storing text'

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
    body = json.loads(response.get_body().decode())
    assert body['error'] == 'No results found'

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

