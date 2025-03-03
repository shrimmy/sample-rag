#from langchain_qdrant import QdrantVectorStore
from langchain.vectorstores import Qdrant
from langchain_core.vectorstores import InMemoryVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_openai import AzureOpenAIEmbeddings
from pydantic import BaseModel
from enum import Enum

class VectorStoreType(Enum):
    IN_MEMORY = "IN_MEMORY"
    QDRANT = "QDRANT"

class EmbeddingsModelConfig(BaseModel):
    openai_api_version: str
    azure_deployment: str
    azure_endpoint: str
    openai_api_key: str

# factory method for creating vector stores
def init_vector_store(vector_store_type: VectorStoreType, embeddings_model_config: EmbeddingsModelConfig):
    
    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=embeddings_model_config.azure_endpoint,
        azure_deployment=embeddings_model_config.azure_deployment,
        openai_api_version=embeddings_model_config.openai_api_version,
        openai_api_key=embeddings_model_config.openai_api_key
    )

    # return the appropriate vector store
    # see this for other vector stores: https://python.langchain.com/docs/modules/data_connection/vectorstores
    if vector_store_type == VectorStoreType.QDRANT.value:
        
        #### QDRANT VECTOR STORE ####
        menus_collection = "menus_collection"
        client = QdrantClient(url="http://qdrant:6333")
        
        if not client.collection_exists(menus_collection):
            client.create_collection(
                collection_name=menus_collection,
                vectors_config=VectorParams(
                    size=1536,
                    distance=Distance.COSINE
                )
            )

        vector_store = Qdrant(client=client, collection_name=menus_collection, embeddings=embeddings)
        print("QDRANT VECTOR STORE INITIALIZED")
        return vector_store
    
    else:
        
        #### IN MEMORY VECTOR STORE ####
        vector_store = InMemoryVectorStore(embedding=embeddings)
        print("IN MEMORY VECTOR STORE INITIALIZED")
        return vector_store