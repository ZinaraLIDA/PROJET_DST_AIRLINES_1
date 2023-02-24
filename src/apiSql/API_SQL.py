#!/bin/python3
from tools import *
import os
import sys
# sys.path.insert(1, pathRoot+"/../")
# from DSTModules.tools.param import *
# from DSTModules.data.connectMongo import MongoConnect
# from DSTModules.data.connectSql import SqlConnect
from flask import Flask, request, make_response, jsonify
from pydantic import BaseModel
from flask_pydantic import validate
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import Unauthorized
from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import HTTPException
from mysql.connector import connect
from pymongo import MongoClient
import json

# Pour afficher les "print" dans le log du pod kubernetes
os.environ["PYTHONUNBUFFERED"] = "1"
os.environ["PYTHONIOENCODING"] = "UTF-8"

# Récupération des paramètres du fichier config.ini
def getParamAll():
    config = {
        "mongo": {
            "server": os.environ.get('MONGO_SERVER'),
            "port": int(os.environ.get('MONGO_PORT')),
            "username": os.environ.get('MONGO_USER'),
            "password": os.environ.get('MONGO_PASSWORD'),
            "db_name": os.environ.get('MONGO_DBNAME')
        },
        "mysql":{
            "host": os.environ.get('MYSQL_SERVER'),
            "port": int(os.environ.get('MYSQL_PORT')),
            "username": os.environ.get('MYSQL_USER'),
            "password": os.environ.get('MYSQL_PASSWORD'),
            "db_name": os.environ.get('MYSQL_DBNAME')
        },
        "api_Mongo":{
            "key": os.environ.get('MONGO_KEY')
        },
        "api_Sql":{
            "key": os.environ.get('MYSQL_KEY')
        }
    }
    return config
    # # fileObject = open(pathRoot + "/../config.ini", "r")
    # fileObject = open("/src/config/config.ini", "r")
    # objJson = fileObject.read()
    # fileObject.close()
    # obj = json.loads(objJson) 
    # return obj

# Connection à la base MongoDB
def mongoConnect(c_mongo):
    if (c_mongo["username"]!=""):
        client = MongoClient(host=c_mongo["server"],port = c_mongo["port"],username=c_mongo["username"],password=c_mongo["password"])
    else:
        client = MongoClient(host=c_mongo["server"],port = c_mongo["port"])
    return client[c_mongo["db_name"]]

# Connection à la base MySql
class mysqlConnect():
    def __init__(self, c_mysql):
        self.c_mysql = c_mysql
        self.conn = connect(host=self.c_mysql["host"], port=self.c_mysql["port"], username=self.c_mysql["username"], password=self.c_mysql["password"], database=self.c_mysql["db_name"])
    def reinit(self):        
        self.conn = connect(host=self.c_mysql["host"], port=self.c_mysql["port"], username=self.c_mysql["username"], password=self.c_mysql["password"], database=self.c_mysql["db_name"])

def querySql(query):
    if not db_sql.conn.is_connected(): 
        db_sql.reinit()
        print("Reinit connexion MySql")
    curseur = db_sql.conn.cursor()
    curseur.execute(query)
    listeOut=curseur.fetchall()
    curseur.close()
    return listeOut

# Recuperation des paramètres de configuration
# pathRoot = os.path.dirname(os.path.abspath(__file__))
# config = getParamAll(pathRoot+"/../")
config = getParamAll()
c_mongo = config["mongo"]
c_mysql = config["mysql"]
# c_path = config["path"]
c_api_Mongo = config["api_Mongo"]
c_api_Sql = config["api_Sql"]

db_mongo = mongoConnect(c_mongo)
# db_sql = mysqlConnect(c_mysql)
db_sql = mysqlConnect(c_mysql)
print("Connextion MySQL:", db_sql.conn.is_connected())

# Classes body
class bodyAirport(BaseModel):
    dep_iata:str

class bodyCountries(BaseModel):
    dep_iata:str

class bodyCities(BaseModel):
    dep_iata:str
    arr_country_iso2:str

class bodyAirportslist(BaseModel):
    dep_iata:str
    arr_city_name:str

class bodySchedules(BaseModel):
    dep_iata:str
    arr_airport_name:str
    start_date:str
    end_date:str

class bodyFlight(BaseModel):
    id_schedule:str

class bodyWeather(BaseModel):
    id_schedule:str

# Route de vérification  connection à API_SQL
app = Flask(__name__)
@app.route("/status", methods=["GET"])
def status()->str:
    retour:int = 1
    try:
        key = getAuthentification(request.headers)
        print(key)
        checkKey(key, c_api_Sql)
        return str(retour)+"\n"
    except NotFound as nf:
        print(nf)
        return ("requete non trouvee",400)
    except BadRequest as bq:
        print(bq)
        return ("erreur sur requete",400)

# Route de récupération des aéroports arrivées
@app.route("/getArrivalAirports", methods=["POST"])
@validate()
def getArrivalAirports(body:bodyAirport):
    try:
        body_dict = body.dict()
        # récupération des critères de la demande
        dep_iata_airport=body_dict["dep_iata"]
         # Verification de l'authentification
        key = getAuthentification(request.headers)
        checkKey(key, c_api_Mongo)
        # Recherche dans la collection schedule des valeurs arr_iata d'airport

        match = {"$and": [{"nb_flights": {"$gte": 3}}, {"dep_iata":dep_iata_airport}]}

        listJson=list(db_mongo.schedules.find(match,{"_id":0,"arr_iata":1}))
        list_arr_iata_airport = listeCodeIataAirportsArrival(listJson)
        # Vérification insertion code arr_iata aéroport dans la liste list_arr_iata_airport
        print(" list : ",list_arr_iata_airport)
        return jsonify({"arr_iata": list_arr_iata_airport})
    except NotFound as nf:
        print(nf)
        return ("requete non trouvee",400)
    except BadRequest as bq:
        print(bq)
        return ("erreur sur requete",400)

# Route de la liste des pays déservis depuis CDG
@app.route("/getCountries", methods=["POST"])
@validate()
def getCountries(body:bodyCountries)->dict:
    try :
        body_dict = body.dict()
        # Récupération des critères de la demande
        dep_iata_airport=body_dict["dep_iata"]
         # Verification de l'authentification
        key = getAuthentification(request.headers)
        checkKey(key, c_api_Sql)
        # Recherche dans la collection schedule des valeurs arr_iata aéroport
        match = {"$and": [{"nb_flights": {"$gte": 3}}, {"dep_iata":dep_iata_airport}]}
        listJson=list(db_mongo.schedules.find(match,{"_id":0,"arr_iata":1}))
        list_arr_iata_airport = listeCodeIataAirportsArrival(listJson)
        # Croisement de la liste iata aéroport avec les tables SQL
        query = "SELECT distinct co.country_name, co.country_iso2 FROM countries as co \
            JOIN airports as a ON co.country_iso2=a.country_iso2 WHERE \
                a.iata_code in ("+transformListStr(list_arr_iata_airport)+")"
        listeCountry = querySql(query)
        listeCountry = transformTupleListToDict(listeCountry)
        return listeCountry
    except NotFound as nf:
        print(nf)
        return ("requete non trouvee",400)
    except BadRequest as bq:
        print(bq)
        return ("erreur sur requete",400)

# Route de la liste des villes déservis  depuis CDG d'un pays
@app.route("/getCities", methods=["POST"])
@validate()
def getCities(body:bodyCities)->dict:
    try:
        body_dict = body.dict()
        # Récupération des critères de la demande
        dep_iata_airport=body_dict["dep_iata"]
        arr_country_iso2=body_dict["arr_country_iso2"]
         # Verification de l'authentification
        key = getAuthentification(request.headers)
        checkKey(key, c_api_Sql)
        # Recherche dans la collection schedule des valeurs arr_iata aéroport
        match = {"$and": [{"nb_flights": {"$gte": 3}}, {"dep_iata":dep_iata_airport}]}
        listJson=list(db_mongo.schedules.find(match,{"_id":0,"arr_iata":1}))
        list_arr_iata_airport = listeCodeIataAirportsArrival(listJson)
        # Croisement de la liste iata aéroport avec le arr_country_iso2 et les tables SQL
        query = "SELECT distinct c.city_name ,c.iata_code FROM cities as c \
        JOIN airports as a ON c.iata_code=a.city_iata_code \
            WHERE a.iata_code in ("+transformListStr(list_arr_iata_airport)+") AND c.country_iso2='" + arr_country_iso2.replace("'","''") + "'"
        listeCities = querySql(query)
        listeCities = transformTupleListToDict(listeCities)
        return listeCities
    except NotFound as nf:
        print(nf)
        return ("requete non trouvee",400)
    except BadRequest as bq:
        print(bq)
        return ("erreur sur requete",400)

# Route de la liste des aérports déservis  depuis CDG
@app.route("/getAirports", methods=["POST"])
@validate()
def getAirports(body:bodyAirportslist)->dict:
    try:
        body_dict = body.dict()
        # Récupération des critères de la demande
        dep_iata_airport=body_dict["dep_iata"]
        arr_city_name=body_dict["arr_city_name"]
         # Verification de l'authentification
        key = getAuthentification(request.headers)
        checkKey(key, c_api_Sql)
        # Recherche dans la collection schedule des valeurs arr_iata aéroport
        match = {"$and": [{"nb_flights": {"$gte": 3}}, {"dep_iata":dep_iata_airport}]}
        listJson=list(db_mongo.schedules.find(match,{"_id":0,"arr_iata":1}))
        list_arr_iata_airport = listeCodeIataAirportsArrival(listJson)
        # Croisement de la liste iata aéroport avec les tables SQL
        query = "SELECT distinct a.airport_name ,a.iata_code FROM airports as a \
            JOIN cities as c ON c.iata_code=a.city_iata_code\
                WHERE a.iata_code in ("+transformListStr(list_arr_iata_airport)+") AND c.city_name='" + arr_city_name.replace("'","''") + "'"
        listeAirports = querySql(query)
        listeAirports = transformTupleListToDict(listeAirports)
        return listeAirports
    except NotFound as nf:
        print(nf)
        return ("requete non trouvee",400)
    except BadRequest as bq:
        print(bq)
        return ("erreur sur requete",400)

# Route de la liste des vols disponibles
@app.route("/getSchedules", methods=["POST"])
@validate()
def getSchedules(body:bodySchedules)->dict:
    try:
        body_dict = body.dict()
        # Récupération des critères de la demande
        dep_iata_airport=body_dict["dep_iata"]
        arr_airport_name=body_dict["arr_airport_name"]
        start_date = body_dict["start_date"] 
        end_date = body_dict["end_date"]
         # Verification de l'authentification
        key = getAuthentification(request.headers)
        checkKey(key, c_api_Sql)
        # Récupération du code iata de l'aéroport d'arrivé
        query = "SELECT a.iata_code FROM airports AS a WHERE a.airport_name='" + arr_airport_name.replace("'","''") + "'"
        print(query)
        arr_iata_airport = querySql(query)
        arr_iata_airport = arr_iata_airport[0][0]
        # Recherche dans la collection schedule des valeurs arr_iata aéroport
        match = {"$and": [{"nb_flights": {"$gte": 3}}, {"dep_iata":dep_iata_airport},
        {"arr_iata":arr_iata_airport}, {"dep_time": {"$gte": start_date}},
        {"dep_time": {"$lte": end_date}}]}
        listJson=list(db_mongo.schedules.aggregate([
            {"$match": match},
            
            {"$project" : {"_id":1, "dep_estimated":1, "arr_estimated":1, "duration":1,
            "dep_terminal":1, "arr_terminal":1, "dep_gate":1, "arr_gate":1,
            "airline_iata":1, "flight_iata":1, "status":1}
            }
        ]))
        return {"response" : listJson}
    except NotFound as nf:
        print(nf)
        return ("requete non trouvee",400)
    except BadRequest as bq:
        print(bq)
        return ("erreur sur requete",400)

# Route des données d'un vol précis
@app.route("/getFlight", methods=["POST"])
@validate()
def getFlight(body:bodyFlight)->dict:
    try:
        body_dict = body.dict()
        # Récupération des critères de la demande
        id_schedule=body_dict["id_schedule"]
         # Verification de l'authentification
        key = getAuthentification(request.headers)
        checkKey(key, c_api_Sql)
        # Recherche dans la collection flights des vols associés au id_schedule
        listJson=list(db_mongo.flights.find({"schedule_id":id_schedule}))
        # flight_iata = id_schedule.split("-")[0]
        # listJson=list(db_mongo.flights.find({"flight_iata":flight_iata}))
        return {"response" : listJson}
    except NotFound as nf:
        print(nf)
        return ("requete non trouvee",400)
    except BadRequest as bq:
        print(bq)
        return ("erreur sur requete",400)

# Route des données météo d'un vol précis
@app.route("/getWeather", methods=["POST"])
@validate()
def getWeather(body:bodyWeather)->dict:
    try:
        body_dict = body.dict()
        # Récupération des critères de la demande
        id_schedule=body_dict["id_schedule"]
         # Verification de l'authentification
        key = getAuthentification(request.headers)
        checkKey(key, c_api_Sql)
        # Recherche dans la collection weather des données météo associés au id_schedule
        listJson=list(db_mongo.weather.find({"schedule_id":id_schedule}))
        return {"response" : listJson}
    except NotFound as nf:
        print(nf)
        return ("requete non trouvee",400)
    except BadRequest as bq:
        print(bq)
        return ("erreur sur requete",400)

# Route pour les fenêtres de dates
@app.route("/getDateRange", methods=["GET"])
def getDateRange():
    # Verification de l'authentification
    key = getAuthentification(request.headers)
    checkKey(key, c_api_Mongo)
    # recherche dans la collection schedule
    data = list(db_mongo.schedules.aggregate([
        {"$group": {"_id":1, 
            "start_date":{"$min": "$dep_time" },
            "end_date":{"$max": "$dep_time" }
        }},
        {"$project": {
            "_id": -1,
            "start_date": 1,
            "end_date": 1
        }}
        ]))
    # Contruction de la réponse
    response = {"search": {}, 
            "result": {"count": len(data)},
            "data": data}
    return json.dumps(response, indent=4)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5002,debug=True)
