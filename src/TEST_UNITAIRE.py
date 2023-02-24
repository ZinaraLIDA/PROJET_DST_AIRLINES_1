config={ 
    "mongo": {
        "server": "127.0.0.1",
        "port": 27017,
        "username": "",
        "password": "",
        "db_name": "DSTAirline"
    },
    "mysql":{
        "host": "146.59.146.30",
        "port": 3306,
        "username": "root",
        "password": "baray",
        "db_name": "DSTAirline"
    },
    "path": {
        "path_json": "D:\david\Python_fichier\DST_Airlines_1\json",
        "path_log": "D:\david\Python_fichier\DST_Airlines_1\log",
        "path_sql": "D:\david\Python_fichier\DST_Airlines_1\sql",
        "create_sql": "D:\david\Python_fichier\DST_Airlines_1\sql\createDB.sql",
        "create_fk": "D:\david\Python_fichier\DST_Airlines_1\sql\createForeignKey.sql"
    },
    "api_airlabs":{
        "url": "https://airlabs.co/api/v9",
        "key": "058c5e67-9c3a-4afe-b8ca-697cf32daa79",
        "params_schedules": {"dep_iata":"CDG"},
        "params_flights": {"dep_iata":"CDG"}
    },
    "api_aviationstack":{
        "url": "http://api.aviationstack.com/v1",
        "key_pyms": "12c5471474648073017f782c673c370a",
        "key_zinnara": "76f9cb073c29761ba05c23802b189dd2",
        "key": "9a4f1b4cc9c6e37e6cc96aa94089561e",
        "params_sav": [
            {"name": "countries", "limit": 252, "primary_key": "country_iso2"},
            {"name": "cities", "limit": 9369, "primary_key": "iata_code"},
            {"name": "airlines", "limit": 13131, "primary_key": "iata_code"},
            {"name": "airplanes", "limit": 19084, "primary_key": "id"},
            {"name": "airports", "limit": 6705, "primary_key": "iata_code"},
            {"name": "aircraft_types", "limit": 310, "primary_key": "iata_code"}
        ],
        "params": [
            {"name": "airplanes", "limit": 19084, "primary_key": "id"}
        ]
    },
    "api_lufthansa":{
        "url": "https://api.lufthansa.com/v1",
        "url_token": "https://api.lufthansa.com/v1/oauth/token",
        "client_id": "wxrnjrr63u4pwy5xb6kp3be4",
        "client_pass": "8ykm4YUp4Da27TNnj8Uy"
    },
    "api_openweathermap":{
        "url":"https://api.openweathermap.org/data/2.5",
        "appid":'a1f14a3c066d12e5e51a3ae5c832c6c5',
        "weather":"weather",
        "forecast":"forecast"
    }
}

from DSTModules.tools.param import getParamAll
from DSTModules.tools.files import updateLog
from DSTModules.tools.files import writeFile
import DSTModules.data.dataProcess 
from DSTModules.api import apiOpenweathermap as apiwe
import os,json, requests, pymongo 
from pymongo import MongoClient
from requests.exceptions import HTTPError
from datetime import datetime
from DSTModules.data.connectMongo import MongoConnect
import DSTModules.data.loadMongo as lm
from DSTModules.data import dataProcess

import pandas
import numpy as np

if __name__=='__main__':

    print("---------TEST CHARGEMENT FICHIER INI-----------------") 
  # Récupération du dossier de l’exécutable
    pathRoot = os.path.dirname(__file__)
    print("pathRoot :",pathRoot)
    # Recuperation des paramètres de configuration
    # config = getParamAll(pathRoot)
    'D:\david\Python_fichier\DST_Airlines_1\src\config.ini'
    c_mongo = config["mongo"]
    c_mysql = config["mysql"]
    c_path = config["path"]
    c_api = config["api_aviationstack"]
    #c_path = "D:\david\Python_fichier\PROJET\PymCode\DSTAirlines\FilesExtract"
    c_apiM = config["api_openweathermap"]
    print ("------------------------")
    print ("config :",config)
    print ("------------------------")
    print("c_path : ",c_path)
    print ("------------------------")
    print("c_apiM :", c_apiM)

print("---------TEST CONNEXION-----------------") 
try:
    Client = MongoClient('mongodb+srv://Nuage:Mongo2022db@cluster0.2drh1dy.mongodb.net/?retryWrites=true&w=majority')
    print (Client.list_database_names())
    print (Client['OPENWEATHERMAP'].list_collection_names())
except Exception as e:
    print("ERREUR D'EXECUTION: " , e, c_path)

print("---------TEST CHARGEMENT JSON ET DICTIONNAIRE-----------------") 
chargement = lm.loadMongo(Client['OPENWEATHERMAP'],c_path, c_apiM)
# Liste_Lat_long:list[float]=[21.414698,6.90228]
# # JsonFile01 = chargement.getDataInJsonMeteo(uri="weather",paramApi=[Liste_Lat_long[0],Liste_Lat_long[1]])
# # print("\n")
# # print("jsonFile01 : ",JsonFile01)
# # print("\n")
# # datafromjson01=chargement.getResultJsonMeteo(JsonFile01)
# # print("\n")
# # print("type du datjson lat long :",type(datafromjson01))
# # print("\n")
# # print("contenu dico lat et long :",datafromjson01)

# # JsonFile02 = chargement.getDataInJsonMeteo(uri="weather",paramApi=['PARIS'])
# # datafromjson02=chargement.getResultJsonMeteo(JsonFile02)
# # print("\n")
# # print("jsonFile01 : ",JsonFile02)
# # print("\n")
# # print("type du datjson ville :",type(datafromjson02))
# # print("\n")
# # print("contenu datjson ville :",datafromjson02)
# # print("\n")


# # print("---------TEST REGLAGE PROFRONDEUR WEATHER------------------") 
# # datameteo=chargement.alignementDocumentMeteoCourante(datafromjson01)
# # print(datameteo)
# # print("\n")
# # datameteo2=chargement.alignementDocumentMeteoCourante(datafromjson02)
# # print(datameteo2)
# # print("\n")


# dataMeteoLongLat={'lat': 21.4147, 'lon': 6.9023, 'weather': 'Clouds', 'weather_description': 'broken clouds', 'temp': 295.85, 
# 'feels_like': 294.44, 'temp_min': 295.85, 'temp_max': 295.85, 'pressure': 1016, 'humidity': 10, 'visibility': 10000,
#  'wind_speed': 2.39, 'wind_direction': 79, 'cloudiness': 56, 'date_unix': 1668965510, 'date_sunrise': 
# 1668923193, 'date_sunset': 1668962983, 'timezone': 3600, 'name': ''}

# dataMeteoLoVille={'lat': 48.8534, 'lon': 2.3488, 'weather': 'Clear', 'weather_description': 'clear sky', 'temp': 281.58,
#  'feels_like': 279.16, 'temp_min': 279.74, 'temp_max': 282.58, 'pressure': 1011, 'humidity': 85, 'visibility': 10000,
#   'wind_speed': 4.12, 'wind_direction': 260, 'cloudiness': 0, 'date_unix': 1668965488, 'country': 'FR', 'date_sunrise': 1668928027,
#    'date_sunset': 1668960335, 'timezone': 3600, 'name': 'PARIS'}

# print("---------TEST TRANSFORMATION----------------")
# data=chargement.transformMeteoData(ressource="weather",data=dataMeteoLongLat,Id_Vol='AF958-1668591300')
# print(data)

# retour= {'lat': 21.4147, 'lon': 6.9023, 'weather': 'Clouds', 'weather_description': 'broken clouds', 'temp': 295.85,
#  'feels_like': 294.44, 'temp_min': 295.85, 'temp_max': 295.85, 'pressure': 1016, 'humidity': 10, 'visibility': 10000,
#   'wind_speed': 2.39, 'wind_direction': 79, 'cloudiness': 56, 'date_unix': 1668965510, 'date_sunrise': 1668923193,
#    'date_sunset': 1668962983, 'timezone': 3600, 'name': '',
#     'load_date': '20-11-2022', 'load_time': '18:36:52', 'load_json': 'D:\\david\\Python_fichier\\DST_Airlines_1\\json\\Files_2022-11-20/weather_1668965812_742326.json',
#      '_id': '21.4147_6.9023_1668965510', 'Id_Vol': 'AF958-1668591300'}

# # data2=chargement.transformMeteoData(ressource="weather",data=dataMeteoLoVille,Id_Vol='AF999-1668591400')
# # print(data2)

# retour2={'lat': 48.8534, 'lon': 2.3488, 'weather': 'Clear', 'weather_description': 'clear sky', 'temp': 281.58,
#  'feels_like': 279.16,'temp_min': 279.74, 'temp_max': 282.58, 'pressure': 1011, 'humidity': 85,
#   'visibility': 10000, 'wind_speed': 4.12, 'wind_direction': 260, 'cloudiness': 0, 'date_unix': 
# 1668965488, 'country': 'FR', 'date_sunrise': 1668928027, 'date_sunset': 1668960335, 'timezone': 3600,
#  'name': 'PARIS', 'load_date': '20-11-2022', 'load_time': '18:36:52',
#   'load_json': 'D:\\david\\Python_fichier\\DST_Airlines_1\\json\\Files_2022-11-20/weather_1668965812_742326.json',
#    '_id': '48.8534_2.3488_1668965488', 'Id_Vol': 'AF999-1668591400'}
# print("\n")
# print("---------INSERTION_MONGO----------------")
# print("nombre insertion :",chargement.putMongoMeteo(ressource="weather",data=retour))  
# print("nombre insertion :",chargement.putMongoMeteo(ressource="weather",data=retour2))  

print("---------TEST GETFLIGHTMETEO-----------------") 


# Mise à jour fichier log
updateLog("DEMMARAGE DE LA COLLECTE DES DONNEES", c_path)

try:
    #Données API Airlabs ressource flights
    param_Api=('AF958-1668591300',21.414698,6.90228)
    # param_Api=('AF958-1668591300',"PARIS")
    updateLog("OPENWEATHERMAP - weather", c_path)
    retour = dataProcess.getDataMeteoFlights(db=Client['OPENWEATHERMAP'],ressource="weather",c_path=c_path,c_apiM=c_apiM,paramApi=param_Api)
    print(retour)
    updateLog(retour, c_path, False)

except Exception as e:
    updateLog("ERREUR D'EXECUTION: " + str(e), c_path)
    updateLog("FIN ANORMALE DE LA COLLECTE DE DONNEES\n", c_path)
else:
    updateLog("FIN DE LA COLLECTE DES DONNEES\n", c_path)
# # finally:
# #     conn.close()
# #     Client.close()

