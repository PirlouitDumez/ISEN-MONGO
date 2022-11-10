import db_controllers as dbc
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time



import matplotlib.pyplot as plt
import numpy as np
import folium

import osmnx as ox




def d(u,v):
    return ((u[0]-v[0])**2+(u[1]-v[1])**2)**0.5


if __name__ == '__main__':
    # Create DB object
    client = MongoClient("mongodb+srv://db:1112@cluster0.hscucjd.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
    db = client.vls
    
    #while True:
    # Update db
    #dbc.update(db)
    #print('updated')
    
    
    q = db.datas.find({"bike_availbale": {"$gt" : 0}})
    ids = [e["station_id"] for e in q]
    q = db.stations.find({"_id": {"$in" : ids}})
    
    position = [50.631750,3.068022][::-1]
    l = sorted(q, key=lambda a:d(a['geometry']['coordinates'], position))
    
    
    
    pos = [50.631750,3.068022]
    m = folium.Map(pos, zoom_start=15)
    
    folium.Marker(location=pos, color='red').add_to(m)
    m.save('cafes.html')
    
    for station in l[:5]:
        folium.CircleMarker(location=station['geometry']['coordinates'][::-1], color='red').add_to(m)
        m.save('cafes.html')
        
    for station in l[5:]:
        folium.CircleMarker(location=station['geometry']['coordinates'][::-1], color='blue').add_to(m)
        m.save('cafes.html')
        
    print('ok')


    
        
        
    #print(dbc.get_stations_with_available_bikes(db))
    
    
    