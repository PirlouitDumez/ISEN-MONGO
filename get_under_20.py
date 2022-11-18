from datetime import datetime
from datetime import timedelta
import pprint

def get_stations_under20(db,hourstart,hourend):

    jours = 30
    start = datetime.now()
    end = (start - timedelta(days=jours))
    
    found = db.datas.aggregate([
        {"$project":
         
         {"hour":
          {"$hour":"$date"
          },
          
          "date":"$date",
          
          "idstation":"$station_id",
          
          "weekDay":{"$dayOfWeek":"$date"
          },
          
          "ratio": 
          {"$cond":
        [
            {'$gt':
             [
                 {"$add":
                  ["$stand_availbale","$bike_availbale"]
                 },
                 0
              ]
             },
             {"$divide" : 
              ["$bike_availbale", 
               {"$add":["$stand_availbale","$bike_availbale"]}
              ]
             },
             0
            ]}
         }
    
         
        },
        {"$match":
         {"hour":
          {"$in":[hourstart,hourend]},
          "date":
          {'$gte': end, '$lt': start},
          "weekDay":{'$gte': 2, '$lte': 6}
         }
        },
        
        {
            "$group" :
            {
              "_id" : "$idstation",
              "station_ratio": { "$avg": "$ratio"}
            }
        },
        {"$match":
         {"station_ratio":{'$lt': 0.2}
         }
        }
           
    ])



    for f in found:
        pprint.pprint(f)

