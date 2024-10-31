import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

settings = {
    'host': os.getenv('ACCOUNT_HOST'),
    'master_key': os.getenv('ACCOUNT_KEY'),
    'database_id': os.getenv('COSMOS_DATABASE'),
    'container_id': os.getenv('COSMOS_CONTAINER'),
}