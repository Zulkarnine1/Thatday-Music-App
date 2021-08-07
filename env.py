from dotenv import load_dotenv
import os
load_dotenv()

DB_CONNECTION = os.getenv("APP_DB_CONNECTION")
SALT_ROUNDS = os.getenv("SALT_ROUNDS")
HASH_METHOD = os.getenv("HASH_METHOD")
SECRET_KEY = os.getenv("SECRET_KEY")
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
SPOTIFY_ID = os.getenv("SPOTIFY_ID")
SPOTIFY_SECRET = os.getenv("SPOTIFY_SECRET")
ROOT_ROUTE = os.getenv("ROOT_ROUTE")

if(os.getenv("IS_PROD")=="TRUE"):
    IS_PROD = True
else:
    IS_PROD = False
