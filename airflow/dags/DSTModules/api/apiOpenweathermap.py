import requests
import json
from pprint import pprint
import os
#
class apiOpenweathermap:
    '''
    cette classe permet de créér un objet de type apiOpenweathermap qui vise 
    l'envoi des requête et la récupération du json pour les méthodes de l'API
    weather et forcast

    point d'interrogation : indiquer l'id du vol à ce moment là pour établri le lien avec les collections 
    flights et schedules
    '''

    def __init__(self,config,paramApiVol:list):
        self.url = config["url"]
        self.key = config["appid"]
        self.paramApiVol=paramApiVol

    def getData(self, uri, params={}):
        headers = {
                "Accept" : "application/json",
                "Content-type" : "application/json"
        }
        if(len(self.paramApiVol)==1):
            params={
            'q':self.paramApiVol[0],
            'appid':self.key
            }
        elif(len(self.paramApiVol)==2):
            params={
            'lat':self.paramApiVol[0],
            'lon':self.paramApiVol[1],
            'appid':self.key
             }
        # params["appid"] = self.key
        url = self.url+"/"+uri
        # print("url :",url)
        # print("params :",params)
        response = requests.get(url, params=params)
        # print("retour requete :",response.json())
        # print(" controle URL post requete:",response.url)
        # print(" retour de la requete exception :",response.status_code)

        if response.ok:
            # creation fichier de type json_string
            result = json.dumps(response.json(), indent=4)
            #print("json_string : ",result)
            return result
        else:
            raise Exception("Erreur get "+uri+":\n"+str(response.status_code)+" "+response.reason)
