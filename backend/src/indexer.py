from abc import ABC, abstractmethod
from typing import Any, List
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from enum import Enum

class IndexerType(Enum):
    DEFAULT = "DEFAULT"

class Indexer(ABC):
    @abstractmethod
    def add(self, documents: List[Any]) -> None:
        """Add documents to the index"""
        pass

class DefaultIndexer(Indexer):
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    # add documents to the index
    def add(self, file_Path: str):
        # load documents from file
        # see this for other loaders: https://python.langchain.com/v0.1/docs/modules/data_connection/document_loaders/
        loader = UnstructuredMarkdownLoader(file_path=file_Path)
        documents = loader.load()

        # split all documents into chunks
        # see this for other splitters: https://python.langchain.com/v0.1/docs/modules/data_connection/document_transformers/
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        all_chunks = text_splitter.split_documents(documents)

        # add all chunks to the vector store
        results = self.vector_store.add_documents(all_chunks)
        return results

    
# factory method for creating indexers
def create_indexer(indexer_type: IndexerType, vector_store: VectorStore) -> Indexer:
    if indexer_type == IndexerType.DEFAULT:
      return DefaultIndexer(vector_store=vector_store)
    else:
      return DefaultIndexer(vector_store=vector_store)