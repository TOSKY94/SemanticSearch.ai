from azure.cosmos import CosmosClient, PartitionKey
import os
import logging
import uuid
import numpy as np 

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

class DBUtils:
    def __init__(self):
        logger.debug("Setting up Cosmos DB")
        self.client = None
        self.database = None
        self.container = None
        self.connection_error = None
        self._setup_connection()

    def _setup_connection(self):
        try:
            cosmos_uri = os.environ.get("COSMOS_URI")
            cosmos_key = os.environ.get("COSMOS_KEY")
            cosmos_database = os.environ.get("COSMOS_DATABASE")
            cosmos_container = os.environ.get("COSMOS_CONTAINER")

            if not all([cosmos_uri, cosmos_key, cosmos_database, cosmos_container]):
                missing_vars = [var for var in ["COSMOS_URI", "COSMOS_KEY", "COSMOS_DATABASE", "COSMOS_CONTAINER"] if not os.environ.get(var)]
                raise ValueError(f"Missing Cosmos DB environment variables: {', '.join(missing_vars)}")

            self.client = CosmosClient(cosmos_uri, cosmos_key)
            self.database = self.client.get_database_client(cosmos_database)
            self.container = self.database.get_container_client(cosmos_container)
        except Exception as e:
            self.connection_error = str(e)
            logger.error(f"Error setting up Cosmos DB connection: {e}")

    def db_health_check(self):
        if self.connection_error:
            return False, self.connection_error
        
        try:
            list(self.container.read_all_items(max_item_count=1))
            return True, "Connected successfully"
        except Exception as e:
            return False, str(e)
    

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
                logger.debug(f"Storing chunk {i+1}/{len(chunks)}")  
            return True

        except Exception as e:
            logger.error(f"error occured:: {e}")
            raise e


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
            raise e
