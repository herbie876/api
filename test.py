from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from Keys import Passwords
from urllib.parse import quote_plus

uri = f"mongodb+srv://{quote_plus('capstoneprojectjm')}:{quote_plus(Passwords['MongoDB'])}@capstone.s9r9myf.mongodb.net/LOM?retryWrites=true&w=majority"
# Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    # client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)