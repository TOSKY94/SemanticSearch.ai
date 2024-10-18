from unittest import mock
from unittest.mock import MagicMock, patch
from app.services.db_utils import DBUtils
import numpy as np

sample_session_id = "test_session"
sample_chunks = ["This is chunk 1", "This is chunk 2"]
sample_embeddings = [np.array([0.1, 0.2, 0.3]), np.array([0.4, 0.5, 0.6])]

@patch.dict('os.environ', {
    'COSMOS_URI': 'mock_uri',
    'COSMOS_KEY': 'mock_key',
    'COSMOS_DATABASE': 'mock_db',
    'COSMOS_CONTAINER': 'mock_container'
})
@patch('app.services.db_utils.CosmosClient')
def test_store_chunk(mock_cosmos_client):
    
    # Arrange
    mock_db = MagicMock()
    mock_container = MagicMock()
    mock_cosmos_client.return_value.get_database_client.return_value = mock_db
    mock_db.get_container_client.return_value = mock_container

    # Act
    db_utils = DBUtils()
    db_utils.store_chunk(sample_session_id, sample_chunks, sample_embeddings)
    
    # Assert
    assert mock_container.upsert_item.call_count == 1


@patch.dict('os.environ', {
    'COSMOS_URI': 'mock_uri',
    'COSMOS_KEY': 'mock_key',
    'COSMOS_DATABASE': 'mock_db',
    'COSMOS_CONTAINER': 'mock_container'
})
@patch('app.services.db_utils.CosmosClient')
def test_get_chunks(mock_cosmos_client):
    
    # Arrange
    mock_db = MagicMock()
    mock_container = MagicMock()
    mock_query_results = [
        {'chunk': "This is chunk 1", 'embedding': [0.1, 0.2, 0.3]},
        {'chunk': "This is chunk 2", 'embedding': [0.4, 0.5, 0.6]}
    ]
    mock_container.query_items.return_value = mock_query_results
    
    mock_cosmos_client.return_value.get_database_client.return_value = mock_db
    mock_db.get_container_client.return_value = mock_container
    
    # Act
    db_utils = DBUtils()
    chunks, embeddings = db_utils.get_chunks(sample_session_id)

    # Assert
    expected_query = f'SELECT * FROM c WHERE c.session_id = "{sample_session_id}"'
    mock_container.query_items.assert_called_once_with(query=expected_query, enable_cross_partition_query=True)
    assert chunks == ["This is chunk 1", "This is chunk 2"]
    assert embeddings == [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
