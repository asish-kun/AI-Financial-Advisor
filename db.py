# db.py

import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
from chromadb.config import Settings
import chromadb
from config import settings

# Azure Cosmos DB settings
HOST = settings['host']
MASTER_KEY = settings['master_key']
DATABASE_ID = settings['database_id']
CONTAINER_ID = settings['container_id']

# Initialize the Cosmos client
cosmos_client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY})

# Get or create the database
try:
    db = cosmos_client.create_database(id=DATABASE_ID)
    print('Database with id \'{0}\' created'.format(DATABASE_ID))
except exceptions.CosmosResourceExistsError:
    db = cosmos_client.get_database_client(DATABASE_ID)
    print('Database with id \'{0}\' was found'.format(DATABASE_ID))

# Get or create the container
try:
    container = db.create_container(id=CONTAINER_ID, partition_key=PartitionKey(path='/partitionKey'))
    print('Container with id \'{0}\' created'.format(CONTAINER_ID))
except exceptions.CosmosResourceExistsError:
    container = db.get_container_client(CONTAINER_ID)
    print('Container with id \'{0}\' was found'.format(CONTAINER_ID))

# Initialize the ChromaDB client
chroma_settings = Settings(persist_directory="chroma_data")
chroma_client = chromadb.Client(chroma_settings)
collection = chroma_client.get_or_create_collection("stock_data")
