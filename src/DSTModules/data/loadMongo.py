#========================================
# Récupération des données API et Chargement dans MongoDB
#========================================

from DSTModules.api.apiAirLabs import apiAirLabs
from DSTModules.api.apiAviationStack import apiAviationStack
from DSTModules.api.apiOpenweathermap import apiOpenweathermap
from DSTModules.tools.files import writeFile
from datetime import datetime, timedelta
import json
import os
import pandas
import numpy as np
#from pymongo import UpdateOne
import pymongo

class loadMongo:
    def __init__(self, db, c_path, c_api):
        self.dt = datetime.now()
        self.db = db
        self.c_api = c_api
        self.c_path = c_path

        fDate = self.dt.strftime('%Y-%m-%d')
        # self.pathOutDay = c_path["path_json"]+"/Files_"+fDate
        self.pathOutDay = c_path["path_json"]+self.c_path["folder_separator"]+"Files_"+fDate
        if (not os.path.exists(self.pathOutDay)): os.mkdir(self.pathOutDay)

    def getDataInJson(self, ressource, params={}, api="AirLabs"):
        if(api=="AirLabs"):
            api = apiAirLabs(self.c_api)
        elif(api=="AviationStack"):
            api = apiAviationStack(self.c_api)
        result = api.getData(ressource, params)
    
        ts = str(datetime.timestamp(self.dt)).replace(".","_")
        # fileOut = self.pathOutDay+"/"+ressource+"_"+ts+".json"
        fileOut = self.pathOutDay+self.c_path["folder_separator"]+ressource+"_"+ts+".json"
        writeFile(fileOut, result)
        return fileOut

    def getResultJson(self, fileJson, response="response"):
        fileObject = open(fileJson, "r")
        objJson = fileObject.read()
        fileObject.close()
        obj = json.loads(objJson)

        if(response in obj.keys()):
            result = obj[response]        
        else:
            result = ""
        return result

    def transformDataAL(self, ressource, data):
        df = pandas.DataFrame(list(data))

        fDate = self.dt.strftime('%d-%m-%Y')
        fTime = self.dt.strftime('%H:%M:%S')
        ts = str(datetime.timestamp(self.dt)).replace(".","_")
        fileJson = self.pathOutDay+"/"+ressource+"_"+ts+".json"
        df["load_date"] = fDate
        df["load_time"] = fTime
        df["load_json"] = fileJson

        df.insert(0,"_id", False)
        df = df.dropna(axis=0, how='any', subset=["flight_iata"])
        if (ressource=="schedules"):
            df = df.dropna(axis=0, how='any', subset=["dep_time_ts"])
            df["_id"] = df.apply(lambda n: n["flight_iata"]+"-"+str(n["dep_time_ts"]), axis=1)
            return df.to_dict("records")
        elif (ressource=="flights"):
            df = df.dropna(axis=0, how='any', subset=["updated"])
            df["_id"] = df.apply(lambda n: str(n["flight_iata"])+"-"+str(n["updated"]), axis=1)
            df.insert(1,"schedule_id", np.nan)
            #print("Nb Total:", len(df))
            for ind, row in df.iterrows():
                #print(ind, row["flight_iata"])
                listSchedule = list(self.db.schedules.find({"$and": [{"flight_iata": row["flight_iata"]}, {"status": "active"}]}, {"_id": 1})\
                    .sort("dep_time_ts",pymongo.DESCENDING).limit(1))
                if(len(listSchedule)>0):
                    schedule = listSchedule[0]
                    df.loc[df._id == row["_id"], "schedule_id"] = schedule["_id"]
                    #print(df.loc[df._id == ind, "schedule_id"])
            nbNan = df["schedule_id"].isna().sum()
            #print("Nb Nan:", nbNan)
            df = df.dropna(axis=0, how='any', subset=["schedule_id"])
            return df.to_dict("records"), nbNan


    def transformDataAS(self, ressource, data, primary_key):
        df = pandas.DataFrame(list(data))

        fDate = self.dt.strftime('%d-%m-%Y')
        fTime = self.dt.strftime('%H:%M:%S')
        ts = str(datetime.timestamp(self.dt)).replace(".","_")
        fileJson = self.pathOutDay+"/"+ressource+"_"+ts+".json"
        df["load_date"] = fDate
        df["load_time"] = fTime
        df["load_json"] = fileJson

        df = df.dropna(axis=0, how='any', subset=[primary_key])
        if(ressource=="countries"):
            df = df.dropna(axis=0, how='any', subset=["country_name"])
        elif(ressource=="cities"):
            df = df.dropna(axis=0, how='any', subset=["city_name"])
            df = df.dropna(axis=0, how='any', subset=["country_iso2"])
        elif(ressource=="airlines"):
            df = df.dropna(axis=0, how='any', subset=["airline_name"])
            df = df.dropna(axis=0, how='any', subset=["country_iso2"])
        elif(ressource=="airplanes"):
            df = df.dropna(axis=0, how='any', subset=["airline_iata_code"])
        elif(ressource=="airports"):
            df = df.dropna(axis=0, how='any', subset=["airport_name"])
            df = df.dropna(axis=0, how='any', subset=["city_iata_code"])
            df = df.dropna(axis=0, how='any', subset=["country_iso2"])
        elif(ressource=="aircraft_types"):
            df = df.dropna(axis=0, how='any', subset=["aircraft_name"])

        df.insert(0,"_id", False)
        df["_id"] = df.apply(lambda n: n[primary_key], axis=1)

        return df.to_dict("records")

    def putMongo(self, ressource, data):
        fDate = self.dt.strftime('%d-%m-%Y')
        fTime = self.dt.strftime('%H:%M:%S')
        ts = str(datetime.timestamp(self.dt)).replace(".","_")
        nbInsert = 0
        if(len(data)>0):
            #     self.db[colTmp].insert_many(data)    
            #     self.db[colTmp].update_many({ },{ "$set": { "load_info": {"date":fDate, "time":fTime, "json":fileJson}} })
            upserts=[pymongo.UpdateOne({'_id':x['_id']}, {'$set':x}, upsert=True) for x in data]
            self.db[ressource].bulk_write(upserts)
        nbInsert = self.db[ressource].count_documents({ "$and": [{"load_date": fDate}, {"load_time": fTime}]})

        return nbInsert


    def getDataInJsonMeteo(self,ressource, paramApi:list,params={})->json:
        api = apiOpenweathermap(self.c_api,paramApi)
        result = api.getData(ressource, params)
        ts = str(datetime.timestamp(self.dt)).replace(".","_")
        fileOut = self.pathOutDay+"/"+ressource+"_"+ts+".json"
        writeFile(fileOut, result)
        return fileOut

    def getResultJsonMeteo(self, fileJson)->dict:
        with open(fileJson) as json_file:
            data = json.load(json_file)
        #print("type :",type(data))
        return data

    def alignementDocumentMeteoCourante(self,data:dict)->dict:
        dataMeteo={}
        for element in data:
            if (element =='coord'):
                dataMeteo['lat']=data[element]['lat']
                dataMeteo['lon']=data[element]['lon']
            if(element =='weather'):
                dataMeteo['weather']=data[element][0]['main']
                dataMeteo['weather_description']=data[element][0]['description']
            if(element=='main'):
                dataMeteo['temp']=data[element]['temp']
                dataMeteo['feels_like']=data[element]['feels_like']
                dataMeteo['temp_min']=data[element]['temp_min']
                dataMeteo['temp_max']=data[element]['temp_max']
                dataMeteo['pressure']=data[element]['pressure']
                dataMeteo['humidity']=data[element]['humidity']
            if(element=='visibility'):
                dataMeteo['visibility']=data[element]
            if(element=='wind'):
                dataMeteo['wind_speed']=data[element]['speed']
                dataMeteo['wind_direction']=data[element]['deg']
            if(element=='clouds'):
                dataMeteo['cloudiness']=data[element]['all']
            if(element =='dt'):
                dataMeteo['date_unix']=data[element]
            if(element =='sys'):
                dico_sys=data[element]
                for key in dico_sys:
                    if (key =='country'):
                        dataMeteo['country']=data[element]['country']
                dataMeteo['date_sunrise']=data[element]['sunrise']
                dataMeteo['date_sunset']=data[element]['sunset']
            if(element=='timezone'):
                dataMeteo['timezone']=data[element]
            if(element=='name'):
                dataMeteo['name']=data[element].upper()
        return dataMeteo

    def alignementDocumentMeteo5jours(self,forecast:dict)->list:
        Liste_prevision5jours=[]
        for element in forecast:
            if (element =='list'):
                for liste in forecast['list']:
                    dataMeteo={}
                    for cle in liste: 
                        if(cle =='dt'):
                            dataMeteo['date_unix']=liste[cle]
                        if(cle =='dt_txt'):
                            dataMeteo['date']=liste[cle]
                        if(cle=='main'):
                            dataMeteo['temp']=liste[cle]['temp']
                            dataMeteo['feels_like']=liste[cle]['feels_like']
                            dataMeteo['temp_min']=liste[cle]['temp_min']
                            dataMeteo['temp_max']=liste[cle]['temp_max']
                            dataMeteo['pressure']=liste[cle]['pressure']
                            dataMeteo['humidity']=liste[cle]['humidity']
                        if(cle == 'weather'):
                            dataMeteo['weather']=liste[cle][0]['main']
                            dataMeteo['weather_description']=liste[cle][0]['description']
                        if(cle =='visibility'):
                            dataMeteo['visibility']=liste[cle]
                        if(cle=='wind'):
                            dataMeteo['wind_speed']=liste[cle]['speed']
                            dataMeteo['wind_direction']=liste[cle]['deg']
                        if(cle == 'clouds'):
                            dataMeteo['cloudiness']=liste[cle]['all']
                        if (cle =='pop'):
                            dataMeteo['proba_precipitation']=liste[cle]
                        if(cle == 'sys'):
                            dataMeteo['partie_jour']=liste[cle]['pod']
                        if(cle =='rain'):
                            dataMeteo['rain_3hours']=liste[cle]['3h']
                    # print(dataMeteo)
                    Liste_prevision5jours.append(dataMeteo)
            if (element == 'city'):
                for dico in Liste_prevision5jours:
                    for infoville in forecast[element]:
                        if(infoville == 'name'):
                            dico['name']=forecast[element][infoville]
                        if(infoville == 'coord'):
                            dico['lat']=forecast[element][infoville]['lat']
                            dico['lon']=forecast[element][infoville]['lon']
                        if(infoville == 'country'):
                            dico['country']=forecast[element][infoville]
                        if(infoville == 'timezone'):
                            dico['timezone']=forecast[element][infoville] 
                        if(infoville == 'sunrise'):
                            dico['sunrise']=forecast[element][infoville]
                        if (infoville == 'sunset'):
                            dico['sunset']=forecast[element][infoville]
        return Liste_prevision5jours


    def transformMeteoData(self, ressource, data, schedule_id, flight_id)->json:
        # df = pandas.DataFrame(list(data))
        #print(data)
        fDate = self.dt.strftime('%d-%m-%Y')
        fTime = self.dt.strftime('%H:%M:%S')
        ts = str(datetime.timestamp(self.dt)).replace(".","_")
        fileJson = self.pathOutDay+"/"+ressource+"_"+ts+".json"
        data["load_date"] = fDate
        data["load_time"] = fTime
        data["load_json"] = fileJson
        data["_id"]= str(data["lat"])+"_"+str(data["lon"])+"_"+str(data['date_unix'])
        data["schedule_id"] = schedule_id
        data["flight_id"] = flight_id
        # print(data)
        # jsonFile =json.dumps(data, indent = 4)
        # print(jsonFile)
        return data
    
    def putMongoMeteo(self, ressource, data)->int:
        self.db[ressource].update_one({"_id": data["_id"]}, {'$set':data}, upsert=True)
        # mise à jour flag Meteo à 1 dans la collection flights
        self.db["flights"].update_one({'_id':data["flight_id"]},{"$set":{'flag_meteo':1}})

    def updateNbFlights(self):
        today = datetime.now()
        today3 = today + timedelta(days=-3)
        ts_today3 = int(today3.timestamp())

        list_nb_flights = list(self.db.flights.aggregate([
            {"$match" : {"updated": {"$gte":ts_today3}}},
            {"$group": {"_id":"$schedule_id", "nb_flights":{"$sum":1 }}},
            {"$project": {"nb_flights": 1}}
        ]))

        maj=[pymongo.UpdateOne({'_id':x['_id']}, {'$set':x}) for x in list_nb_flights]
        self.db.schedules.bulk_write(maj)

        return len(list_nb_flights)

