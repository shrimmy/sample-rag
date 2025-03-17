# Overview
This project is a pipeline for creating a knowledge index from a set of documents and then querying the knowledge index for similar documents.

# Prerequisites
- Docker
- Chat completion model in Azure AI Foundry (Use personal MSDN Sub as this uses API Keys, or update this app to EntraID)
- Embeddings model in Azure AI Foundry
- Copy the .env.example file to .env and update the values with your model settings

## Installation
- Clone the repository
- Run `docker compose up -d`
- Navigate to [Chat](http://localhost:3000) to access the web interface
- Navigate to [Assistant SWAGGER UI](http://localhost:8000/docs) to access the API documentation
- Navigate to [Qdrant Vector Store Dashboard](http://localhost:6333/dashboard) to access the vector store dashboard

## Knowledge Files
For this sample, we will be indexing markdown files that contain menu information for a resturant. These files are loacted in the `/data/menus` folder. To load the initial data, POST to the /data/all endpoint. You can do this using the SWAGGER UI tools [add restaurant menus](http://localhost:8000/docs#/default/add_all_data_data_all_post), select "Try it out" and then "Execute". This will load the initial data into the knowledge index.

**Note:** 
*Delete has not yet been added and if you are using persistent storage, you will need to manually delete to avoid duplicates.*

### Indexing Knowledge Files


### Create your own knowledge files
- Prompt: `Create a markdown file with the following content: Name of the Restaurant, a menu with descriptions and prices in USD. Also add a story about the restaurant, no more than 2 paragraphs.`

## Customize and make it your own
- Change the Vector Store - https://python.langchain.com/docs/integrations/vectorstores/ 
- Change the Document Loader -  https://python.langchain.com/docs/how_to/#document-loaders
- Change the Text Splitter - https://python.langchain.com/docs/how_to/#text-splitters
- Add Memory - https://python.langchain.com/docs/how_to/chatbots_memory/
- Add Tools (Utilities) - https://python.langchain.com/docs/how_to/custom_tools/


## TODO:
- Upsert documents in knowledge index
- Add delete functionality
- Add EntraID

