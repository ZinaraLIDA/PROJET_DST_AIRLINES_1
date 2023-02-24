#!/bin/python3
from flask import Flask, request, make_response, jsonify
from pydantic import BaseModel
from flask_pydantic import validate
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import Unauthorized
from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import HTTPException
from pymongo import MongoClient
import numpy as np
import json
import os

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
        "api_Mongo":{
            "key": os.environ.get('MONGO_KEY')
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

# Récupération de l'authentification dans le header
def getAuthentification(headers):
    key = ""
    if "Authorization" in headers:
        key = headers["Authorization"]
    if key=="":
        raise BadRequest("Votre requête est incorrect. Veuillez renseigner la clé dans le header de la requête.")
    return key

# Vérification de la clé d'authentification
def checkKey(key):
    if key != c_api_Mongo["key"]:
        raise Unauthorized("La clé d'authentification est incorrect")

# Récupération du dossier de l’exécutable
# pathRoot = os.path.dirname(os.path.abspath(__file__))
# Recuperation des paramètres de configuration
# config = getParamAll(pathRoot)
config = getParamAll()
c_mongo = config["mongo"]
# c_path = config["path"]
c_api_Mongo = config["api_Mongo"]

db = mongoConnect(c_mongo)

class bodySchedules(BaseModel):
    dates:list
    destinations:list
    fields:list

class bodyFlight(BaseModel):
    schedule_id:str

class bodyStatFlightsCompany(BaseModel):
    dates:list
    sort:dict
    limit:int

class bodyStatDelayCompany(BaseModel):
    dates:list
    sort:dict
    limit:int

class bodyStatAircrafts(BaseModel):
    sort:dict
    limit:int

class bodyStatFleets(BaseModel):
    sort:dict
    limit:int

app = Flask(__name__)

@app.route("/status", methods=["GET"])
def status():
    return "1"

@app.route("/getListSchedules", methods=["POST"])
@validate()
def getListSchedules(body:bodySchedules):
    body_dict = body.dict()
    # récupération des critères de la demande
    destinations = body_dict["destinations"]
    dates = body_dict["dates"]
    fields = body_dict["fields"]
    # Verification de l'authentification
    key = getAuthentification(request.headers)
    checkKey(key)

    # formatage des champs à renvoyer
    project = {}
    for field in fields:
        project[field] = 1
    # formatage des dates à sélectionner
    if len(dates) > 1:
        dates[1] = dates[1] + " 23:59"
    else:
        dates.append(dates[0] + " 23:59")
    dates[0] = dates[0] + " 00:00"
    # construction du filtre
    match = [{"nb_flights": {"$gt": 0}}]
    match.append({"dep_time": {"$gte": dates[0]}})
    match.append({"dep_time": {"$lte": dates[1]}})
    if len(destinations) > 0:
        match.append({"arr_iata": {"$in": destinations}})
    # recherche dans la collection schedule
    data = list(db.schedules.find({"$and": match}, project))
    # Contruction de la réponse
    response = {"search": {"begin_date": dates[0], "end_date": dates[1], "destinations": destinations}, 
            "result": {"count": len(data)},
            "data": data}

    return json.dumps(response, indent=4)

@app.route("/getFlight", methods=["POST"])
@validate()
def getListFlight(body:bodyFlight):
    body_dict = body.dict()
    # récupération des critères de la demande
    schedule_id = body_dict["schedule_id"]
    # Verification de l'authentification
    key = getAuthentification(request.headers)
    checkKey(key)

    # construction du filtre
    match1 = {"_id": schedule_id}
    match2 = {"schedule_id": schedule_id}
    # recherche dans les collections
    data_schedule = list(db.schedules.find(match1))
    data_flights = list(db.flights.find(match2))
    data_meteo = list(db.weather.find(match2))
    # Contruction de la réponse
    response = {"search": {"schedule_id": schedule_id}, 
            "result": {"count_schedule": len(data_schedule), "count_flights": len(data_flights), "count_weather": len(data_meteo)},
            "schedule": data_schedule,
            "flights": data_flights,
            "weather": data_meteo}

    return json.dumps(response, indent=4)


@app.route("/statFlightsCompany", methods=["POST"])
@validate()
def statFlightsCompany(body:bodyStatFlightsCompany):
    body_dict = body.dict()
    # récupération des critères de la demande
    dates = body_dict["dates"]
    sort = body_dict["sort"]
    limit = body_dict["limit"]
    if limit==0: limit=1000000
    # Verification de l'authentification
    key = getAuthentification(request.headers)
    checkKey(key)
    # formatage des dates à sélectionner
    if len(dates)!=0 and len(dates)!=2:
        raise BadRequest("Sélection de dates incorrect: liste vide pour la totalité de la base, ou date de début et date de fin de recherche")
    match = {}
    if len(dates)==2:
        dates[0] = dates[0] + " 00:00"
        dates[1] = dates[1] + " 23:59"
        # construction du filtre
        match = {"$and": [{"dep_time": {"$gte": dates[0]}}, {"dep_time": {"$lte": dates[1]}}]}
    # recherche dans la collection schedule
    data = list(db.schedules.aggregate([
    {"$match": match},
    {"$group": {
        "_id":"$airline_iata", 
        "nb_departure":{"$sum":1 }, 
        "first_departure":{"$first": "$dep_time" }, 
        "last_departure":{"$last": "$dep_time" }
        }
    },
    {"$project": {
        "_id": 1,
        "nb_departure": 1,
        "first_departure": 1,
        "last_departure": 1,
        "nb_days": {
            "$add": [
                {"$convert":{
                "input": {"$dateDiff": {
                    "startDate": {"$dateFromString": {"dateString": "$first_departure"}},
                    "endDate": {"$dateFromString": {"dateString": "$last_departure"}},
                    "unit": "day"
                    }
                }, "to": "int"}
                }, 1]
        },
        "departure_day_avg": {"$divide": ["$nb_departure", {"$add": [{"$convert":
        {
            "input": {"$dateDiff": {"startDate": {"$dateFromString": {"dateString": "$first_departure"}},
            "endDate": {"$dateFromString": {"dateString": "$last_departure"}},
            "unit": "day"}},
            "to": "int",
        }}, 1]}]}
    }},
        {"$sort": sort }, {"$limit": limit}
    ]))

    # Contruction de la réponse
    response = {"search": {"begin_date": "" if len(dates)==0 else dates[0], 
                "end_date": "" if len(dates)==0 else dates[1],
                "sort": sort,
                "limit": limit
                }, 
            "result": {"count": len(data)},
            "data": data}
    return json.dumps(response, indent=4)


@app.route("/statDelayCompany", methods=["POST"])
@validate()
def statDelayCompany(body:bodyStatDelayCompany):
    body_dict = body.dict()
    # récupération des critères de la demande
    dates = body_dict["dates"]
    sort = body_dict["sort"]
    limit = body_dict["limit"]
    if limit==0: limit=1000000
    # Verification de l'authentification
    key = getAuthentification(request.headers)
    checkKey(key)
    # formatage des dates à sélectionner
    if len(dates)!=0 and len(dates)!=2:
        raise BadRequest("Sélection de dates incorrect: liste vide pour la totalité de la base, ou date de début et date de fin de recherche")
    match = {}
    if len(dates)==2:
        dates[0] = dates[0] + " 00:00"
        dates[1] = dates[1] + " 23:59"
        # construction du filtre
        match = {"$and": [{"dep_time": {"$gte": dates[0]}}, {"dep_time": {"$lte": dates[1]}}]}
    # mise à jour du delayed à 0 s'il n'existe pas
    db.schedules.update_many({"delayed": np.nan}, {"$set": {"delayed": 0}})
    # recherche dans la collection schedule
    data = list(db.schedules.aggregate([
    {"$match": match},
    {"$group": {"_id":"$airline_iata", "delayed_avg":{"$avg":"$delayed" }, "delayed_max":{"$max":"$delayed" }, "nb_flights":{"$sum":1 }}},
    {"$project": {
        "_id": 1,
        "delayed_avg": 1,
        "delayed_max": 1,
        "nb_flights": 1
    }},
        {"$sort": sort }, {"$limit": limit}
    ]))
    # Contruction de la réponse
    response = {"search": {"begin_date": "" if len(dates)==0 else dates[0], 
                "end_date": "" if len(dates)==0 else dates[1],
                "sort": sort,
                "limit": limit
                }, 
            "result": {"count": len(data)},
            "data": data}
    return json.dumps(response, indent=4)


@app.route("/statAircrafts", methods=["POST"])
@validate()
def statAircrafts(body:bodyStatAircrafts):
    body_dict = body.dict()
    # récupération des critères de la demande
    sort = body_dict["sort"]
    limit = body_dict["limit"]
    if limit==0: limit=1000000
    # Verification de l'authentification
    key = getAuthentification(request.headers)
    checkKey(key)
    # recherche dans la collection schedule
    data = list(db.flights.aggregate([
        {"$match": {"aircraft_icao": {"$ne": np.nan}}},
        {"$group": {"_id":"$aircraft_icao", "alt_max":{"$max":"$alt" }, "speed_max":{"$max":"$speed" }, "speed_avg":{"$avg":"$speed" },
        "airlines": {"$addToSet": '$airline_iata'}, "schedules": {"$addToSet": '$schedule_id'}
    }},
    {"$project": {
        "_id": 1,
        "alt_max": 1,
        "speed_max": 1,
        "speed_avg": 1,
        "airlines": 1,
        "nb_airlines": {"$size": "$airlines"},
        "nb_schedules": {"$size": "$schedules"}
    }},
        {"$sort": sort }, {"$limit": limit}
    ]))
    # Contruction de la réponse
    response = {"search": {"sort": sort,"limit": limit}, 
            "result": {"count": len(data)},
            "data": data}
    return json.dumps(response, indent=4)


@app.route("/statFleets", methods=["POST"])
@validate()
def statFleets(body:bodyStatFleets):
    body_dict = body.dict()
    # récupération des critères de la demande
    sort = body_dict["sort"]
    limit = body_dict["limit"]
    if limit==0: limit=1000000
    # Verification de l'authentification
    key = getAuthentification(request.headers)
    checkKey(key)
    # recherche dans la collection schedule
    data = list(db.airplanes.aggregate([
        {"$match": {"$and": [{"airline_iata_code": {"$ne": np.nan}}, {"plane_status": "active"}, 
        {"$expr": { "$lt": [{"$convert":{"input": "$plane_age","to": "int"}}, 100] }}
        ]}}, 
        {"$group": {"_id":"$airline_iata_code", "nb_aircrafts":{"$count":{} }, 
            "aircrafts": {"$addToSet": '$iata_code_long'},
            "plane_age_avg":{"$avg": {"$convert":{"input": "$plane_age","to": "int",}} },
            "plane_age_min":{"$min": {"$convert":{"input": "$plane_age","to": "int",}} },
            "plane_age_max":{"$max": {"$convert":{"input": "$plane_age","to": "int",}} }
        }},
        {"$project": {
            "_id": 1,
            "nb_aircrafts": 1,
            "aircrafts": 1,
            "plane_age_avg": 1,
            "plane_age_min": 1,
            "plane_age_max": 1
        }},
            {"$sort": sort }, {"$limit": limit}
        ]))

    # Contruction de la réponse
    response = {"search": {"sort": sort,"limit": limit}, 
            "result": {"count": len(data)},
            "data": data}
    return json.dumps(response, indent=4)


@app.route("/getDateRange", methods=["GET"])
@validate()
def getDateRange():
    # Verification de l'authentification
    key = getAuthentification(request.headers)
    checkKey(key)
    # recherche dans la collection schedule

    data = list(db.schedules.aggregate([
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

@app.route("/getAirports", methods=["GET"])
@validate()
def getAirports():
    # Verification de l'authentification
    key = getAuthentification(request.headers)
    checkKey(key)
    # recherche dans la collection
    data = list(db.airports.find({}, {"iata_code": 1, "airport_name": 1, "longitude": 1, "latitude": 1}))
    # Contruction de la réponse
    response = {"search": {}, 
            "result": {"count": len(data)},
            "data": data}
    return json.dumps(response, indent=4)


@app.route("/getAirlines", methods=["GET"])
@validate()
def getAirlines():
    # Verification de l'authentification
    key = getAuthentification(request.headers)
    checkKey(key)
    # recherche dans la collection
    data = list(db.airlines.find({}, {"iata_code": 1, "airline_name": 1, "country_iso2": 1, "country_name": 1}))
    # Contruction de la réponse
    response = {"search": {}, 
            "result": {"count": len(data)},
            "data": data}
    return json.dumps(response, indent=4)

@app.route("/getAircrafts", methods=["GET"])
@validate()
def getAircrafts():
    # Verification de l'authentification
    key = getAuthentification(request.headers)
    checkKey(key)
    # recherche dans la collection
    data = list(db.aircraft_types.find({}, {"iata_code": 1, "aircraft_name": 1}))
    # Contruction de la réponse
    response = {"search": {}, 
            "result": {"count": len(data)},
            "data": data}
    return json.dumps(response, indent=4)

@app.route("/getAirplanesGroupBy", methods=["GET"])
@validate()
def getAirplanesGroupBy():
    # Verification de l'authentification
    key = getAuthentification(request.headers)
    checkKey(key)
    # recherche dans la collection 
    data = list(db.airplanes.aggregate([
        {"$group": {"_id":"$iata_code_long", "aircraft_iata":{"$first":"$iata_code_short" }}}
    ]))
    # Contruction de la réponse
    response = {"search": {}, 
            "result": {"count": len(data)},
            "data": data}
    return json.dumps(response, indent=4)


@app.route("/getAirplanes", methods=["GET"])
@validate()
def getAirplanes():
    # Verification de l'authentification
    key = getAuthentification(request.headers)
    checkKey(key)
    # recherche dans la collection 
    data = list(db.airplanes.find())
    # Contruction de la réponse
    response = {"search": {}, 
            "result": {"count": len(data)},
            "data": data}
    return json.dumps(response, indent=4)


@app.route("/getActiveAirlines", methods=["GET"])
@validate()
def getActiveAirlines():
    # Verification de l'authentification
    key = getAuthentification(request.headers)
    checkKey(key)
    # recherche dans la collection schedule

    data = list(db.schedules.aggregate([
        {"$group": {"_id": "$airline_iata", 
            "nb_schedules":{"$sum": 1 }
        }},
        {"$project": {
            "_id": 1,
            "nb_schedules": 1
        }}
        ]))
    # Contruction de la réponse
    response = {"search": {}, 
            "result": {"count": len(data)},
            "data": data}
    return json.dumps(response, indent=4)


@app.errorhandler(NotFound)
def handler_error(err):
  return "L'appel à l'API a échoué, veuillez vérifier votre requête", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5001,debug=True)


