from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from business import *
from client import *
from get_data import *
from worker import *


if __name__ == '__main__':
    # Create DB object
    client = MongoClient("mongodb+srv://db:1112@cluster0.hscucjd.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
    db = client.vls
    
    #while True:
    ### Update db
    update(db)
    
    position=[3.068022,50.631750][::-1]
    location_program(db, position, dist=1000)