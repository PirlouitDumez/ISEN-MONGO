import db_controllers as dbc
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time

import matplotlib.pyplot as plt
import numpy as np
import folium

import osmnx as ox

# Connect with cmd : mongosh "mongodb+srv://cluster0.hscucjd.mongodb.net/myFirstDatabase" --apiVersion 1 --username db
# pwd : 1112

def d(u,v):
    return ((u[0]-v[0])**2+(u[1]-v[1])**2)**0.5



def order_stations_by_distance(db, position=[3.068022,50.631750], filter0=True):
    """ return stations ordered py distance to "position" """
    if filter0:
        q = db.datas.find({"bike_availbale": {"$gt" : 0}})
    else:
        q = db.datas.find({})
    ids = [e["station_id"] for e in q]
    q = db.stations.find({"_id": {"$in" : ids}})
    l = sorted(q, key=lambda a:d(a['geometry']['coordinates'], position))
    return l



def get_stations_history(db):
    """return dic with stations and history
    /!\ history contient les dates dans l'ordre décroissant : le premier élement de la liste est le plue récent"""
    # Get stations + data
    stations_ = list(db.stations.find({}))
    datas_ = list(db.datas.find({}))

    # Sort datas by date
    d = sorted(datas_, key=lambda x:x['date'], reverse=True)

    # Create dic
    dic = {s['_id'] : {"name":    s['name'], 
                       "geometry":s['geometry'], 
                       "size":    s['size'], 
                       "tpe":     s['tpe'],
                       "history": []} 
           for s in stations_}
    
    # Fill history
    for d in datas_:
        dic[d['station_id']]['history'].append([d['date'],d["bike_availbale"],d["stand_availbale"]])
    
    return dic



def show_stations(history):
    print('# Stations :')
    if len(history.keys() == 0):
        print("No stations")
        return 
    
    print("- {: <27}".format("NAME"),
          "{: <8}".format(f"BIKES"),
          "{: <25}".format("LOCATION"),
          "   TPE")
    for id in history:
        station = history[id]
        print("- {: <27}".format(station['name']),
              "{: <8}".format(f"{station['history'][-1][1]}/{station['size']}"),
              "{: <25}".format(str(station['geometry']['coordinates'])),
              " - tpe available" if station['tpe'] else "")
        


if __name__ == '__main__':
    # Create DB object
    client = MongoClient("mongodb+srv://db:1112@cluster0.hscucjd.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
    db = client.vls
    
    #while True:
    ### Update db
    #dbc.update(db)
    print('updated')

    ### Define user position
    position=[3.068022,50.631750]

    history = get_stations_history(db)
    
    show_stations(history)
    input()

    ### Print 10 closest stations with available stand numbers
    dic = history
    print(dic[66])
    l = [[i, dic[i]['name'], dic[i]['size'], dic[i]['history'][0], dic[i]['geometry']] for i in dic.keys()]
    l = sorted(l, key=lambda a:d(a[-1]['coordinates'], position))
    print(l[0])
    
    
    ### Order stations by distance to position
    position = [3.068022,50.631750]
    l = order_stations_by_distance(db, position=position, filter0=True)
    
    # Create Map in HTML format
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
    
    
    