import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://fin-data-db.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'arneIEEzvee0hQFxog0li1WSGXpbZRK9axK4c0V2Alkwjr93DC7ZWU1KGH0WpWfXa8Rko9rSwncvACDbNdxbyQ=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'ToDoList'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'Items'),
}
