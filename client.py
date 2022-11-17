import pprint
from business import activate_station,desactivate_station

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

    if len(list(found))>0: #jai eu un bug en utilisant la longueur des listes comme ca pcq comme faut les pprint je crois elles sont bizarres
        # for each station found, we look for stations in lille by id
        print("Stations found:")
        for f in found:        

            foundLille = db.datas.find({"idstation" : f["_id"]}).sort([("datemaj", -1)]).limit(1)


            for fl in foundLille:
                pprint.pprint(fl)
    else:
        print("No station found")
