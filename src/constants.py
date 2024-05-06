import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")
