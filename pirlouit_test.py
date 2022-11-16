import json
import requests
import pandas as pd
import re
from datetime import datetime

class api_connector:
    def get_api(self,url):
            response = requests.request("GET",url)
            response_json = json.loads(response.text.encode('utf-8'))
            return response_json.get("records",[])
        
    def get_lille(self):
            url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=-1&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
            return self.get_api(url)
        
        
        
class data_cleaner_for_collection():
    """
    Clean the differents datasets
    """
    
    def clean_lille(self,dflille):
        dflilleclean = dflille[['fields.nom','fields.geo','fields.type','fields.etat']].drop_duplicates(subset=['fields.nom'])
        dflilleclean = dflilleclean.rename(columns={'fields.nom':'Name','fields.geo':'Geo','fields.type':'TPE','fields.etat':'Available'})
        
        # get the size of Lille Stations by adding the number of availables places and bicycles
        size = []
        for i, row in dflille.iterrows():
            size.append(row['fields.nbvelosdispo']+row['fields.nbplacesdispo'])
    
        dflilleclean = pd.concat([dflilleclean,pd.DataFrame(size, columns = ['Size'])], axis=1, join='inner')
    
        # set the 'tpe' column with boolean
        dflilleclean['TPE'] = dflilleclean['TPE'].replace("AVEC TPE","True")
        for i, row in dflilleclean.iterrows():
            if not row['TPE'] == 'True':
                dflilleclean['TPE'].loc[i] = 'False'
    
        # set the 'Available' column with boolean
        dflilleclean['Available'] = dflilleclean['Available'].replace("EN SERVICE","True")
    
        for i, row in dflilleclean.iterrows():
            if not row['Available'] == 'True':
                dflilleclean['Available'].loc[i] = 'False'
                
        return(dflilleclean)
    
    
def send_collection():
    """
    Connect to the APIs and fill in 'global_velo' with a dict
    """
    # collect data
    ac = api_connector()
    
    dflille = pd.json_normalize(ac.get_lille())
    
   
    
    #clean data
    dc = data_cleaner_for_collection()
    response = dc.clean_lille(dflille)
    
    #add the _id
    idlist = []
    for i, row in response.iterrows():
        idlist.append(re.sub('[\W\_]', "", str(row['Geo'])))
    
    response = pd.concat([response,pd.DataFrame(idlist, columns = ['_id'])], axis=1, join='inner')
    
    return(response.to_dict('records'))

def send_live():
    """
    return what is needed to fill in the collection "lille_velo"
    """
    # collect data
    ac = api_connector()    
    dflille = pd.json_normalize(ac.get_lille())[["fields.nbvelosdispo","fields.nbplacesdispo","fields.datemiseajour",'fields.geo']]
    dflille = dflille.rename(columns={'fields.nbvelosdispo':'availbalebike','fields.nbplacesdispo':'availableplaces',"fields.datemiseajour":'datemaj','fields.geo':'idstation'})
    
    # change geo to id station
    idlist = []
    for i, row in dflille.iterrows():
        idlist.append(re.sub('[\W\_]', "", str(row['idstation'])))
    dflille['idstation'] = idlist
    
    #change date to the correct format
    datelist = []
    for i, row in dflille.iterrows():
        date = datetime.fromisoformat(row['datemaj'])
        datelist.append(date)
    dflille['datemaj'] = datelist
    
    return(dflille.to_dict('records'))
    
if __name__ == '__main__':
    print(send_collection())
    print(send_live())