from azure.cosmos import CosmosClient, PartitionKey
import json
import uuid
import numpy as np 

class DBUtils:
    def __init__(self):
        with open("appsettings.json") as config:
            config = json.load(config)
            print("setting up db")
            self.cosmos_uri = config["COSMOS_URI"]
            self.cosmos_key = config["COSMOS_key"]
            self.cosmos_database = config["COSMOS_DATABASE"]
            self.cosmos_container = config["COSMOS_CONTAINER"]
            self.client = CosmosClient(self.cosmos_uri, self.cosmos_key)
            self.database = self.client.get_database_client(self.cosmos_database)
            self.container = self.database.get_container_client(self.cosmos_container)

    def store_chunk(self, session_id: str, chunks: list, embeddings: list):
        print("Storing chunks")
        for i, chunk in enumerate(chunks):
            # Check if the embedding is a NumPy array and convert it to a list
            embedding = embeddings[i]
            if isinstance(embedding, np.ndarray):
                embedding = embedding.tolist()

            item = {
                'id': str(uuid.uuid4()),
                'session_id': session_id,
                'chunk': chunk,
                'embedding': embedding  # Now it's a JSON-serializable list
            }

            # Insert directly without using json.dumps (Cosmos SDK handles JSON encoding)
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
