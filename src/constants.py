import os
from dotenv import load_dotenv

# !!! IMPORTANT !!!
# Make sure to create a .env file in the root directory of the project

# Let's first load the environment variables from the .env file
load_dotenv()

# DATABASE RELATED CONSTANTS
SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")

# JWT RELATED CONSTANTS
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
