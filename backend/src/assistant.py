from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, MarkdownListOutputParser
from langchain_core.vectorstores import VectorStore
from langchain_core.documents import Document
from pydantic import BaseModel

def get_context_from_document(doc: Document):
    
    text = doc.page_content
    source = doc.metadata.get("source")

    context = f"""
    {
        'text': '{text}',
        'metadata': {
            'source': '{source}'
        }
    }
    """

    return context.format(text=doc.page_content, source=doc.metadata.get("source"))

class AzureChatOpenAIConfig(BaseModel):
    openai_api_version: str
    azure_deployment: str
    azure_endpoint: str
    openai_api_key: str

class RestaurantAssistant:
    def __init__(self, chat_model_config: AzureChatOpenAIConfig, vector_store: VectorStore):
        self.chat_model_config = chat_model_config
        self.vector_store = vector_store
        pass

    async def ask(self, question: str):
        
        try:
            llm = AzureChatOpenAI(
                openai_api_version=self.chat_model_config.openai_api_version,
                azure_deployment=self.chat_model_config.azure_deployment,
                azure_endpoint=self.chat_model_config.azure_endpoint,
                temperature=0,
                openai_api_key=self.chat_model_config.openai_api_key
            )

            # RETRIEVE THE MOST SIMILAR DOCUMENTS
            similar_docs = await self.vector_store.asimilarity_search(question, k=6)

            # AUGMENT THE QUESTION
            prompt = ChatPromptTemplate.from_template("""
            You are a helpful restaurant assistant. Use the following pieces of retrieved context to answer the question. Provide citations in the answer using the Document source.
            If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
            Respond in Markdown format.
            Question: {question} 
            Context: {context} """
            )
            context = ""
            for doc in similar_docs:
                context += "\n" + (
                    f"\nDocument source: {doc.metadata.get('source')}\n"
                    f"\nDocument content: {doc.page_content}\n"
                ) + "\n"

            output_parser = StrOutputParser()
            chain = prompt | llm | output_parser

            # GENERATE THE ANSWER
            result = chain.invoke({"question": question, "context": context})

            print("PROMPT: ", prompt)
            print("RESULT: ", result)

            return {"answer": result}
        except Exception as e:
            return {"Error": str(e)}
    