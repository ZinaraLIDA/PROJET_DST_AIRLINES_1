#!/bin/python3
#========================================
# Récupération des données Air Labs 
# - Schedules
#========================================

from DSTModules.tools.param import getParamAll
from DSTModules.tools.files import updateLog
from DSTModules.data.connectMongo import MongoConnect
from DSTModules.data import dataProcess
import os

# Récupération du dossier de l’exécutable
pathRoot = os.path.dirname(os.path.abspath(__file__))
# Recuperation des paramètres de configuration
config = getParamAll(pathRoot)
c_mongo = config["mongo"]
c_path = config["path"]
c_api = config["api_airlabs"]
c_apiM = config["api_openweathermap"]


# Mise à jour fichier log
updateLog("DEMMARAGE DE LA COLLECTE DES DONNEES", c_path)

try:
    # Connection à la base de données Mongo
    conn = MongoConnect(c_mongo)
    db = conn.db_airline

    # Données API Airlabs ressource schedules
    updateLog("Process AirLabs - Schedules", c_path)
    retour, dt_schedules = dataProcess.getSchedules(db, c_path, c_api)
    updateLog(retour, c_path, False)

    # Données API Airlabs ressource flights
    updateLog("Process AirLabs - Flights", c_path)
    retour, dt_flights = dataProcess.getFlights(db, c_path, c_api)
    updateLog(retour, c_path, False)

    # Modification du nbr de flights dans Schedule
    updateLog("Modification du nbr de flights dans Schedule", c_path)
    retour = dataProcess.updSchedules(db, c_path, c_api)
    updateLog(retour, c_path, False)

    # Données API OpenWeatherMap
    updateLog("Process OpenWeatherMap - weather", c_path)
    retour = dataProcess.getDataMeteo(db, "weather", c_path, c_apiM, dt_flights)
    updateLog(retour, c_path, False)

except Exception as e:
    print("ERREUR D'EXECUTION: ", str(e))
    updateLog("ERREUR D'EXECUTION: " + str(e), c_path)
    updateLog("FIN ANORMALE DE LA COLLECTE DE DONNEES\n", c_path)
    conn.close()
    raise Exception("ERREUR D'EXECUTION: ", str(e))
else:
    print("FIN NORMALE")
    updateLog("FIN DE LA COLLECTE DES DONNEES\n", c_path)
    conn.close()

