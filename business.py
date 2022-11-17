from pprint import pprint




def search_station_by_name(db,name):
    """find all stations containing the characters entered by the user"""
    found = db.stations.find({"name": {"$regex": name, "$options": "i" },"Available":True})
    
    pprint(list(found))
    return
    
    
def update_station(db,id,modif_dict):
    """update information on a station given its id
    modif_dict : {"field1":value1, "field2":value2,...}"""
    filter = { "_id" : id}
    
    db.stations.update_one(filter, {"$set" : modif_dict})
    print("fields updated")


def delete_station(db,id):
    """delete all information on a station given its id"""
    db.stations.delete_one( {"_id":id} )

    db.data.delete_many( {"idstation":id} )
    print("station information deleted")
    return

def desactivate_station(db,id):
    filter = { "_id" : id}
    db.stations.update_one(filter, {"$set":{"Available":False}})
    
def activate_station(db,id):
    filter = { "_id" : id}
    db.stations.update_one(filter, {"$set":{"Available":True}})