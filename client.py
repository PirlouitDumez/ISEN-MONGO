import pprint

def location_program(db,pos,dist=100):
    """
    find all the stations in a certain radius from the user
    """
    # filtre nearby dans global
    found= db.stations.find({"Geo": 
                                   {"$near": 
                                    {"$geometry":
                                     {"type": "Point",
                                      "coordinates": pos},
                                                     "$maxDistance": dist}}, "Available":"True"})

    if len(list(found))>0:
        # for each station found, we look for stations in lille by id
        print("Stations found:")
        for f in found:        

            foundLille = db.datas.find({"idstation" : f["_id"]}).sort([("datemaj", -1)]).limit(1)


            for fl in foundLille:
                pprint.pprint(fl)
    else:
        print("No station found")
