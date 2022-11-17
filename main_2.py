from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pprint

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
    running=True
    while running:
        print("Choose an action : \n 1 - Give station next to user \n 2 - Search station by name \n 3 - Update a station \n 4"
              + " - Delete a station \n 5 - Desactivate all station in an area\n 6 -  Give all stations with a ratio bike/total_stand under 20%\n Other entry - Exit " +
              " \n -------------------------------------------------------------------------------------------------------------")
        try:
            choice = int(input())
        except:
            print("Thanks for using our application, see you soon :) ")
            running=False
            break
        if choice==1: #give station nearby
            pass
        
        elif choice==2: #search by name
            print("Enter the name of the station (or some letters)")
            name = input()
            search_station_by_name(db,name)
            
        elif choice==3: #update a station
            print("Enter the station ID to modify (use search by name option to get the ID)")
            try:
                id = int(input())
            except:
                print("Wrong entry please enter an integer")
                break
            updating=True
            fields = []
            values = []
            while updating:
                station = db.stations.find({"_id": id})
                print("Here is information of this station : \n")
                pprint.pprint(list(station))
                print("Enter the field to modify : ")
                field = input()
                print("Enter the new value of ",field)
                value = input()
                fields.append(field)
                values.append(value)
                print("Do you want to modify another field ? Enter y if yes or anything else if no : ")
                continue_choice = input()
                if continue_choice != "y":
                    updating=False
            
            modif_dict = {field:value for field,value in zip(fields,values)} 
            update_station(db,id,modif_dict)
            print(f"Station {id} has been successfully updated !")
            
        elif choice==4: #delete station
            print("Enter the station ID to delete (use search by name option to get the ID)")
            try:
                id = int(input())
            except:
                print("Wrong entry")
                break
            
            print("Here is information of this station : \n Press d to confirm the suppression : ")
            pprint.pprint(list(db.stations.find({"_id": id})))
            delete_choice = input()
            if delete_choice == "d":
                delete_station(db,id)
                print(f"Station {id} has been successfully deleted")
            else:
                print("Suppression canceled")
        elif choice==5: #desactivate in area
            pass
        elif choice==6: #give all stations with ratio bike/total_stand under 20%
            pass
        else:
            running=False
            print("Thanks for using our application, see you soon :) ")
           
            
            
    """    
    #for station in db.stations.find():
    #    pprint.pprint(list(station))
    desactivate_station(db,240)
    search_station_by_name(db,"Poste")
    #delete_station(db,240)
    #search_station_by_name(db,"Poste")
    update_station(db,53,{"name":"Poste","size":12})
    search_station_by_name(db,"Poste")
    
    #position=[3.068022,50.631750][::-1]
    #location_program(db, position, dist=1000)
    
    """