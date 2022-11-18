from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pprint

from business import *
from client import *
from get_data import *
from get_under_20 import *

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
              + " - Delete a station \n 5 - Activate/Desactivate all station in an area\n 6 -  Give all stations with a ratio bike/total_stand under 20%\n Other entry - Exit " +
              " \n -------------------------------------------------------------------------------------------------------------")
        try:
            choice = int(input())
        except:
            print("Thanks for using our application, see you soon :) ")
            running=False
            break
        if choice==1: #give station nearby
            print("Enter your geo position : \n  ")
            try:
                longitude = float(input("Longitude : "))
            except:
                print('Wrong entry')
                break
            try:
                latitude = float(input("Latitude : ")) 
            except:
                print("Wrong entry")
                break    
            print("Enter the maximum distance between you and the station : ")
            try:
                distance = float(input()) 
            except:
                print("Wrong entry")
                break    

            find_in_area(db,[longitude,latitude],distance)
            
        
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
        elif choice==5: #activate/desactivate in area
            print("Enter a to activate a station, d to desactivate a station and any other character to go back to main menu")
            alpha = 0.005
            default_coords =  [[[3.048567+alpha, 50.634268], [3.048567, 50.634268+alpha], [3.048567-alpha, 50.634268], [3.048567, 50.634268-alpha], [3.048567+alpha, 50.634268]]]
            choice_activation = input()
            if choice_activation == "a":
                print(f"Activating stations in this polygon : {[default_coords]} (modify the main source code to change coords because it's too long to enter it manually)")
                activate_in_polygon(db,default_coords)
            elif choice_activation == "d":
                print(f"Desactivating stations in this polygon : {[default_coords]} (modify the main source code to change coords because it's too long to enter it manually)")
                desactivate_in_polygon(db,default_coords)
            else:
                pass
            pass
        elif choice==6: #give all stations with ratio bike/total_stand under 20%
            print("Enter the time slot you want")
            print("Hour of start : ")
            try:
                hourstart = int(input())
            except:
                print("Wrong entry, please enter a valid hour between 0 and 23, in the right order")
                break
            print("Hour of end : ")
            try:
                hourend = int(input())
            except:
                print("Wrong entry, please enter a valid hour between 0 and 23, in the right order")
                break
            print("Here are the stations by ids with a ratio bike/total_stand_number under 20% during week days : " )
            get_stations_under20(db,hourstart,hourend)
        else:
            running=False
            print("Thanks for using our application, see you soon :) ")
           
            
            
    