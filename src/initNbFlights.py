#!/bin/python3

from DSTModules.data.connectMongo import MongoConnect
from DSTModules.tools.param import getParamAll
import pymongo
import os

# Récupération du dossier de l’exécutable
pathRoot = os.path.dirname(os.path.abspath(__file__))
# Recuperation des paramètres de configuration
config = getParamAll(pathRoot)
c_mongo = config["mongo"]
c_path = config["path"]

conn = MongoConnect(c_mongo)
db = conn.db_airline

# db.sav_schedules.insert_many(list(db.schedules.find()))

list_nb_flights = list(db.flights.aggregate([
    {"$group": {"_id":"$schedule_id", "nb_flights":{"$sum":1 }}},
    {"$project": {"nb_flights": 1}}
]))

maj=[pymongo.UpdateOne({'_id':x['_id']}, {'$set':x}) for x in list_nb_flights]
db.schedules.bulk_write(maj)

print("nb de schedules modifiés:", len(list_nb_flights))

