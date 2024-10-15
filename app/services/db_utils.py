from azure.cosmos import CosmosClient, PartitionKey
from config.settings import get_settings
import json
import uuid
import numpy as np 

class DBUtils:
    def __init__(self):
        settings = get_settings()
        self.client = CosmosClient(settings["COSMOS_URI"], settings["COSMOS_KEY"])
        self.database = self.client.get_database_client(settings["COSMOS_DATABASE"])
        self.container = self.database.get_container_client(settings["COSMOS_CONTAINER"])

    def store_chunk(self, session_id: str, chunks: list, embeddings: list):
        print("Storing chunks")
        for i, chunk in enumerate(chunks):
            # Check if the embedding is a NumPy array and convert it to a list
            embedding = embeddings[i].tolist() if isinstance(embeddings[i], np.ndarray) else embeddings[i]

            item = {
                'id': str(uuid.uuid4()),
                'session_id': session_id,
                'chunk': chunk,
                'embedding': embedding  # Now it's a JSON-serializable list
            }

            self.container.upsert_item(item)
        print("completed!")

    def get_chunks(self, session_id: str):
        print("Retrieving chunks")
        query = f'SELECT * FROM c WHERE c.session_id = "{session_id}"'
        results = self.container.query_items(query=query, enable_cross_partition_query=True)
        chunks = []
        embeddings = []
        for result in results:
            chunks.append(result['chunk'])
            embeddings.append(result['embedding'])
        return chunks, embeddings
