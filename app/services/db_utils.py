from azure.cosmos import CosmosClient, PartitionKey
import os
import logging
import uuid
import numpy as np 

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class DBUtils:
    def __init__(self):
        logger.debug("setting up comos db")
        self.client = CosmosClient(os.environ.get("COSMOS_URI"), os.environ.get("COSMOS_KEY"))
        self.database = self.client.get_database_client(os.environ.get("COSMOS_DATABASE"))
        self.container = self.database.get_container_client(os.environ.get("COSMOS_CONTAINER"))

    def store_chunk(self, session_id: str, chunks: list, embeddings: list):
        logger.debug("Storing chunks")
        try:
            for i, chunk in enumerate(chunks):
                embedding = embeddings[i].tolist() if isinstance(embeddings[i], np.ndarray) else embeddings[i]

                item = {
                    'id': str(uuid.uuid4()),
                    'session_id': session_id,
                    'chunk': chunk,
                    'embedding': embedding
                }

                self.container.upsert_item(item)
            logger.debug("Storing chunks completed!")

        except Exception as e:
            logger.error(f"error occured:: {e}")


    def get_chunks(self, session_id: str):
        logger.debug("Retrieving chunks")
        try:
            query = f'SELECT * FROM c WHERE c.session_id = "{session_id}"'
            results = self.container.query_items(query=query, enable_cross_partition_query=True)
            chunks = []
            embeddings = []
            for result in results:
                chunks.append(result['chunk'])
                embeddings.append(result['embedding'])
            return chunks, embeddings
        
        except Exception as e:
            logger.error(f"error occured:: {e}")
