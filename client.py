def find_all(db):
    # filtre nearby dans global
    found = db.stations.find({})
    found = list(found)
    if len(found)>0:
        # get datas row corresponding to id
        for f in found:
            found_data = list(db.datas.find({"station_id" : f["_id"]}).sort([("date", -1)]).limit(1))[0]
            print(f"Station {f['_id']}: {f['name']} : {found_data['bike_availbale']}/{f['size']} ({found_data['date']})")
            print(f"position : {f['geometry']['coordinates']}")
            print('\n')
    else:
        print("No station in area")

 


def find_in_area(db,pos,dist=100):
    # filtre nearby dans global
    db.stations.create_index([('geometry','2dsphere')])
    found = db.stations.find({'geometry': {'$near': {
                                                '$geometry': {
                                                    'type': "Point" ,
                                                    'coordinates': pos},
                                                 "$maxDistance": dist
                                                }}})

    found = list(found)
    if len(found)>0:
        # get datas row corresponding to id
        for f in found:
            found_data = list(db.datas.find({"station_id" : f["_id"]}).sort([("date", -1)]).limit(1))[0]
            print(f"Station {f['_id']}: {f['name']} : {found_data['bike_availbale']}/{f['size']} ({found_data['date']})")
            print(f"position : {f['geometry']['coordinates']}")
            print('\n')
    else:
        print("No station in area")




if __name__ == '__main__':
    from pymongo.mongo_client import MongoClient
    from pymongo.server_api import ServerApi
    from get_data import *
    
    # Create DB object
    client = MongoClient("mongodb+srv://db:1112@cluster0.hscucjd.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
    db = client.vls
    
    update(db)
        
    position=[3.048567, 50.634268]
    #find_all(db)
    find_in_area(db, position, dist=300)
