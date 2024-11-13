# cosmos_client.py
from azure.cosmos import CosmosClient, exceptions

COSMOS_DB_ENDPOINT = "https://fin-data-db.documents.azure.com:443/"
COSMOS_DB_KEY = "arneIEEzvee0hQFxog0li1WSGXpbZRK9axK4c0V2Alkwjr93DC7ZWU1KGH0WpWfXa8Rko9rSwncvACDbNdxbyQ"
DATABASE_NAME = "ToDoList"
CONTAINER_NAME = "Items"

client = CosmosClient(COSMOS_DB_ENDPOINT, COSMOS_DB_KEY)
database = client.create_database_if_not_exists(DATABASE_NAME)
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME,
    partition_key="/id",  # Customize the partition key if needed
)

def create_user(data):
    container.create_item(body=data)
