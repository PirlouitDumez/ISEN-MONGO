from business import *


def find_all(db, affichage=True, only_available=True):
    # filtre all stations
    if only_available:
        found = db.stations.find({"Available":True})
    else:
        found = db.stations.find({})
    found = list(found)
    
    if not affichage:
        return found
    
    if len(found)>0:
        # get datas row corresponding to id
        for f in found:
            found_data = list(db.datas.find({"station_id" : f["_id"]}).sort([("date", -1)]).limit(1))[0]
            print(f"Station {f['_id']}: {f['name']} : {found_data['bike_availbale']}/{f['size']} ({found_data['date']})")
            print(f"position : {f['geometry']['coordinates']}")
            print('\n')
    else:
        print("No station in area")
        
    return found

 


def find_in_area(db,pos,dist=100,affichage=True, only_available=True):
    # find stations in circle around position
    db.stations.create_index([('geometry','2dsphere')])
    if only_available:
        found = db.stations.find({'geometry': {'$near': {
                                                '$geometry': {'type': "Point" ,'coordinates': pos},
                                                 "$maxDistance": dist}},"Available":True})
    else:
       found = db.stations.find({'geometry': {'$near': {
                                                '$geometry': {'type': "Point" ,'coordinates': pos},
                                                 "$maxDistance": dist}}})
       
    found = list(found)
    
    if not affichage:
        return found
    
    if len(found)>0:
        # get datas row corresponding to id
        for f in found:
            found_data = list(db.datas.find({"station_id" : f["_id"]}).sort([("date", -1)]).limit(1))[0]
            print(f"Station {f['_id']}: {f['name']} : {found_data['bike_availbale']}/{f['size']} ({found_data['date']})")
            print(f"position : {f['geometry']['coordinates']}")
            print('\n')
    else:
        print("No station in area")
        
    return found




def find_in_polygon(db, coordinates, affichage=True, only_available=True):
    # find stations in polygon 
    db.stations.create_index([('geometry','2dsphere')])
    if only_available:
        found = db.stations.find({'geometry': {'$geoWithin': {
                                                '$geometry': {'type': "Polygon" ,'coordinates': coordinates}}},
                                  "Available":True})
    else:
        found = db.stations.find({'geometry': {'$geoWithin': {
                                                '$geometry': {'type': "Polygon" ,'coordinates': coordinates}}}})

    found = list(found)
    
    if not affichage:
        return found
    
    if len(found)>0:
        # get datas row corresponding to id
        for f in found:
            found_data = list(db.datas.find({"station_id" : f["_id"]}).sort([("date", -1)]).limit(1))[0]
            print(f"Station {f['_id']}: {f['name']} : {found_data['bike_availbale']}/{f['size']} ({found_data['date']})")
            print(f"position : {f['geometry']['coordinates']}")
            print('\n')
    else:
        print("No station in area")
        
    return found



def desactivate_in_area(db,pos,dist=100):
    # desactivate stations in circle around pos
    stations = find_in_area(db,pos,dist=dist,affichage=False)
    for s in stations:
        desactivate_station(db, s['_id'])
    return

def desactivate_in_polygon(db,coordinates):
    # desactivate stations in circle around pos
    stations = find_in_polygon(db,coordinates,affichage=False)
    for s in stations:
        desactivate_station(db, s['_id'])
    return

def activate_in_area(db,pos,dist=100):
    # desactivate stations in circle around pos
    stations = find_in_area(db,pos,dist=dist,affichage=False, only_available=False)
    for s in stations:
        activate_station(db, s['_id'])
    return

def activate_in_polygon(db,coordinates):
    # desactivate stations in circle around pos
    stations = find_in_polygon(db,coordinates,affichage=False, only_available=False)
    for s in stations:
        activate_station(db, s['_id'])
    return




if __name__ == '__main__':
    from pymongo.mongo_client import MongoClient
    from pymongo.server_api import ServerApi
    from get_data import *
    
    # Create DB object
    client = MongoClient("mongodb+srv://db:1112@cluster0.hscucjd.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
    db = client.vls
    
    update(db)
        
    position=[3.048567, 50.634268]
    stations = find_all(db, affichage=False)
    print(len(stations))
    
    stations = find_in_area(db, position, dist=300, affichage=False)
    print(len(stations))
    
    alpha = 0.005
    coords = [[[3.048567+alpha, 50.634268], [3.048567, 50.634268+alpha], [3.048567-alpha, 50.634268], [3.048567, 50.634268-alpha], [3.048567+alpha, 50.634268]]]
    stations = find_in_polygon(db, coords, affichage=True)
    print(len(stations))