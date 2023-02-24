#!/bin/python3
#========================================
# Récupération des données Aviation Stack 
# - Données de référence
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
c_mysql = config["mysql"]
c_path = config["path"]
c_api = config["api_aviationstack"]

# Mise à jour fichier log
updateLog("DEMMARAGE DE LA RECUPERATION DES DONNEES DE REFERENCE", c_path, logName="LogRef")

try:
    # Connection à la base de données Mongo
    conn = MongoConnect(c_mongo)
    db = conn.db_airline

    #listReference = ["countries","cities","airlines","airplanes","airports","aircraft_types"]

    for c_params in c_api["params"]:
        # Données API AviationStack c_params["name"]
        print("collection", c_params["name"])
        updateLog("Process AviationStack - "+c_params["name"], c_path, logName="LogRef")
        retour = dataProcess.getDataRef(db, c_params["name"], c_path, c_api, c_params)
        updateLog(retour, c_path, False, logName="LogRef")

except Exception as e:
    updateLog("ERREUR D'EXECUTION: " + str(e), c_path, logName="LogRef")
    updateLog("FIN ANORMALE DE LA RECUPERATION DES DONNEES DE REFERENCE\n", c_path, logName="LogRef")
else:
    updateLog("FIN DE LA RECUPERATION DES DONNEES DE REFERENCE\n", c_path, logName="LogRef")
finally:
    conn.close()

