# Semantic Search API

## Overview

This project demonstrates how to build a scalable semantic search API using Python, FastAPI, Sentence Transformers for vectorization, and Azure Cosmos DB for storage. The API allows users to submit large bodies of text, break them into chunks, store the chunks with vector embeddings, and perform semantic search queries to retrieve the most relevant text chunks.

## Features

- Text Chunking: Breaks large input text into smaller, manageable chunks (e.g., 300-word chunks).
- Text Vectorization: Converts each chunk of text into vector embeddings using a pre-trained `SentenceTransformer`.
- Cosmos DB Storage: Stores the text chunks and their embeddings in Azure Cosmos DB for scalable and persistent storage.
- Semantic Search: Retrieves the most relevant text chunks using cosine similarity based on user queries.

## Project Structure

```bash
semantic-search-api/
│
├── SemanticSearchFunction/
│   ├── __init__.py              # Main function code
│   └── function.json            # Function configuration
│
├── app/
│   ├── api/
│   │   └── endpoints.py         # API routes and endpoints
│   └── services/
│       ├── vectorizer.py        # Vectorization logic
│       └── db_utils.py          # Cosmos DB interactions
│
├── tests/                      # Unit and integration tests
│   ├── test_vectorizer.py
│   ├── test_db_utils.py
│   └── test_api.py
│
├── local.settings.json          # Local settings (including Cosmos DB credentials)
├── host.json                    # Host configuration
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

## Requirements

Make sure you have the following installed:

- Python 3.7+
- Azure Cosmos DB Account (for storing and retrieving text chunks)
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the Repository:

```
git clone https://github.com/yourusername/semantic-search-api.git
cd semantic-search-api
```

2. Set Up Environment:

- Create a virtual environment (optional but recommended):

```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

- Install dependencies:

```
pip install -r requirements.txt
```

3. Set Up Cosmos DB Credentials:

- Open `config/app_settings.json` and provide your Cosmos DB connection details:

```
{
  "COSMOS_URI": "your-cosmos-db-uri",
  "COSMOS_KEY": "your-cosmos-db-key",
  "COSMOS_DATABASE": "your-database-name",
  "COSMOS_CONTAINER": "your-container-name"
}
```

## Running the API

1. Start the FastAPI server using Uvicorn:

```
uvicorn main:app --reload
```

2. Access the API:

- Visit the interactive API documentation (provided by FastAPI and Swagger) at:

```
http://localhost:8000/docs
```

## API Endpoints

1. Add Text

- Endpoint: `POST /texts`
- Description: Add a large body of text to be chunked, vectorized, and stored in Cosmos DB.
- Request Body:

```
{
  "session_id": "string",
  "text": "string"
}
```

- Response:

```
{
  "message": "Text added successfully",
  "session_id": "string",
  "chunks_stored": 10
}
```

2. Search for Text

- Endpoint: `POST /search`
- Description: Search for the most semantically relevant text chunks based on a query.
- Request Body:

```
{
  "query": "string"
}
```

- Response:

```
{
  "query": "string",
  "top_chunks": [
    {
      "text_id": "string",
      "chunk": "string",
      "similarity_score": 0.89
    }
  ]
}
```

## Project Configuration

- Cosmos DB Configuration:
  - You can modify Cosmos DB connection settings in the `config/app_settings.json` file:
  ```
  {
      "COSMOS_URI": "your-cosmos-db-uri",
      "COSMOS_KEY": "your-cosmos-db-key",
      "COSMOS_DATABASE": "your-database-name",
      "COSMOS_CONTAINER": "your-container-name"
  }
  ```
- Chunk Size:
  - By default, the chunking size is set to 300 words. You can modify this in app/services/chunking.py.

## Testing the Project

This project includes unit and integration tests for the API and services. The tests are located in the `tests/` folder.

1. Install Test Dependencies:
   If you haven't already, install `pytest` and other test dependencies:

```
pip install pytest pytest-asyncio httpx
```

2. Run All Tests:
   You can run all tests with the following command:

```
pytest tests/
```

3. Run Specific Test Files:

```
pytest tests/test_api.py     # Run API tests
pytest tests/test_vectorizer.py  # Run vectorizer tests
```

## Key Libraries Used

- FastAPI: Fast web framework for building APIs.
- Azure Cosmos DB SDK: For storing and retrieving text chunks and embeddings.
- Sentence-Transformers: For generating embeddings from text using pre-trained models.
- Scipy: For calculating cosine similarity between embeddings.
- Pytest: For unit and integration testing.

## Future Enhancements

- Approximate Nearest Neighbor (ANN) Search: Implementing a more efficient search mechanism for larger datasets.
- Indexing: Introduce indexing for faster querying.
- Support for Multiple Languages: Add support for semantic search in different languages using multilingual models.
