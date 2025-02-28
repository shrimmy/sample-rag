import logging.config
import os
import debugpy
import logging
import sys

from typing import List
from fastapi import FastAPI
from fastapi_cors import CORS
from fastapi.responses import RedirectResponse
from pydantic import BaseModel  
from langchain_core.documents import Document
from dotenv import load_dotenv

from .assistant import RestaurantAssistant, AzureChatOpenAIConfig
from .vector_store import init_vector_store, EmbeddingsModelConfig, VectorStoreType
from .indexer import create_indexer

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

remote_debug = os.getenv("REMOTE_DEBUG")
if remote_debug:
    debugpy.listen(5678)

load_dotenv()

data_folder= os.getenv("DATA_FOLDER")
if not data_folder:
    data_folder = "./data"

app = FastAPI()
CORS(app)

class Question(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str

class Document(BaseModel):
    title: str
    path: str

class KnowledgeFile(BaseModel):
    fileName: str

# Load the configuration
chat_model_config = AzureChatOpenAIConfig(
    openai_api_version=os.getenv("AZURE_API_VERSION"), 
    azure_deployment=os.getenv("AZURE_DEPLOYMENT"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    openai_api_key=os.getenv("AZURE_API_KEY")   
)

embeddings_model_config = EmbeddingsModelConfig(
    openai_api_version=os.getenv("AZURE_API_VERSION_EMBEDDINGS"), 
    azure_deployment=os.getenv("AZURE_DEPLOYMENT_EMBEDDINGS"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT_EMBEDDINGS"),
    openai_api_key=os.getenv("AZURE_API_KEY_EMBEDDINGS")   
)

# Initialize the vector store and the assistant
vector_store_type = os.getenv("VECTORSTORE_TYPE") 
if not vector_store_type:
    vector_store_type = VectorStoreType.IN_MEMORY # (VectorStoreType.IN_MEMORY, VectorStoreType.QDRANT)
indexer_type = "DEFAULT" # only default available for now

logger.info("VECTORSTORE_TYPE: %s", vector_store_type)

vector_store = init_vector_store(vector_store_type=vector_store_type, embeddings_model_config=embeddings_model_config)
restaurant_assistant = RestaurantAssistant(chat_model_config=chat_model_config, vector_store=vector_store)
indexer = create_indexer(indexer_type=indexer_type, vector_store=vector_store)

@app.post("/question/")
async def answer(question: Question):
    result = await restaurant_assistant.ask(question.question)
    return result

@app.post("/data/all")
async def add_all_data():
    #TODO: delete all docs first, need to work out how to delete all data

    folder_path = data_folder
    chunks_added = 0
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            print("Adding file: ", file_path)
            result = indexer.add(file_path)
            chunks_added += len(result)


    return { "chunks_added": chunks_added }



