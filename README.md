# Semantic Search API

## Overview

This project demonstrates a scalable semantic search API using Python and Azure Functions. The API supports:

- Chunking and vectorizing large bodies of text.
- Storing the text chunks and their vector embeddings in Azure Cosmos DB.
- Performing semantic search queries to retrieve the most relevant text chunks.
- PDF-to-text extraction.

## Features

- Text Chunking: Breaks large input text into smaller, manageable chunks (e.g., 300-word chunks).
- Text Vectorization: Converts each chunk of text into vector embeddings using a pre-trained `SentenceTransformer`.
- Cosmos DB Storage: Stores the text chunks and their embeddings in Azure Cosmos DB for scalable and persistent storage.
- Semantic Search: Retrieves the most relevant text chunks using cosine similarity based on user queries.
- PDF-to-Text Extraction: Upload a PDF file, extract its text, and use it for further processing.

## Project Structure

```bash
semantic-search-api/
│
├── healthcheck_func/
│   ├── __init__.py              # Healthcheck function code
│   └── function.json            # Function configuration
|
├── search_func/
│   ├── __init__.py              # Search function code
│   └── function.json            # Function configuration
|
├── text_func/
│   ├── __init__.py              # Text function code
│   └── function.json            # Function configuration
|
├── pdf2text_func/
│   ├── __init__.py              # Pdf text extraction function code
│   └── function.json            # Function configuration
│
├── app/
│   ├── models/
│   │   └── models.py            # model classes
│   └── services/
│       ├── pdf_utils.py         # Pdf extraction logic
│       ├── semantic_search.py   # semantic search logic
│       ├── vectorizer.py        # Vectorization logic
│       └── db_utils.py          # Cosmos DB interactions
│
├── tests/                      # Unit and integration tests
│   ├── test_vectorizer.py
│   ├── test_pdf_utils.py
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

- Open `local.settings.json` and provide your Cosmos DB connection details:

```
{
  "COSMOS_URI": "your-cosmos-db-uri",
  "COSMOS_KEY": "your-cosmos-db-key",
  "COSMOS_DATABASE": "your-database-name",
  "COSMOS_CONTAINER": "your-container-name"
}
```

## Running the API Locally with Azure Functions Core Tools

1. Install Azure Functions Core Tools.
2. Start the function app:

```
func start
```

3. Access the API at `http://localhost:7071`:

```

## API Endpoints

1. Add Text

- Endpoint: `POST /texts`
- Description: Add a large body of text to be chunked, vectorized, and stored in Cosmos DB.
- Request Body:

```

{
"session_id": "string",
"text": "string",
"chunk_size": 300
}

```

- Response:

```

{
"status": "success",
"message": "Text stored successfully",
"data": {
"chunks_stored": 10
}
}

```

2. Search for Text

- Endpoint: `POST /search`
- Description: Search for the most semantically relevant text chunks based on a query.
- Request Body:

```

{
"query": "string",
"session_id": "string",
"limit": 2,
"base_similarity": 0.7
}

```

- Response:

```

{
"status": "success",
"message": "Search results returned successfully",
"data": {
"query": "string",
"top_results": [
{
"chunk": "string",
"similarity_score": 0.89
}
]
}
}

```

3. PDF-to-Text Extraction

- Endpoint: `POST /pdf2text`
- Description: Uploads a PDF file, extracts the text from the PDF, and returns the extracted text.
- Request: Upload a PDF file (multipart/form-data).
- Response:

```

{
"status": "success",
"message": "Text extracted successfully",
"data": {
"extracted_text": "The extracted text from the PDF..."
}
}

````

4. Healthcheck

- Endpoint: `GET /healthcheck`
- Description: Checks if the API and Cosmos DB connection are functioning correctly.
- Response:
```bash
{
  "status": "success",
  "message": "DB Health Check",
  "data": {
    "is_healthy": true
  }
}
````

## Project Configuration

- Cosmos DB Configuration:
  - You can modify Cosmos DB connection settings in the `local.settings.json` file:
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
pytest -v tests/test_api.py         # Run API tests
pytest -v tests/test_vectorizer.py  # Run vectorizer tests
pytest -v tests/test_db_utils.py    # Run db utility tests
pytest -v tests/test_pdf_utils.py   # Run pdf utility tests
```

## Key Libraries Used

Azure Functions: Serverless functions for handling HTTP requests.
Azure Cosmos DB SDK: For storing and retrieving text chunks and embeddings.
Sentence-Transformers: Pre-trained models for generating embeddings from text.
Scipy: For calculating cosine similarity between embeddings.
Pytest: For unit and integration testing.

## Future Enhancements

- Approximate Nearest Neighbor (ANN) Search: Implementing a more efficient search mechanism for larger datasets.
- Indexing: Introduce indexing for faster querying.
- Support for Multiple Languages: Add support for semantic search in different languages using multilingual models.
