#!/bin/python3
#========================================
# Initialisation de la base de données SQL 
# - Creation des Tables
# - Alimentation des tables à partir de Mongo
#========================================

from DSTModules.tools.param import getParamAll
from DSTModules.tools.files import updateLog
from DSTModules.data.connectMongo import MongoConnect
from DSTModules.data.connectSql import SqlConnect
from DSTModules.data import dataProcess
from DSTModules.data.loadSql import loadSql
import os

# Récupération du dossier de l’exécutable
pathRoot = os.path.dirname(os.path.abspath(__file__))

# Recuperation des paramètres de configuration
config = getParamAll(pathRoot)
c_mongo = config["mongo"]
c_mysql = config["mysql"]
c_path = config["path"]

# Mise à jour fichier log
updateLog("DEMMARAGE DE L'INITIALISATION DE LA BASE DE DONNEES", c_path, logName="LogSql")

try:
    # Connection à la base de données Mongo
    conn_mongo = MongoConnect(c_mongo)
    db_mongo = conn_mongo.db_airline
    # Connection à la base de données MySQL
    db_sql = SqlConnect(c_mysql)
    
    # Instance classe loadSql
    ls = loadSql(db_mongo, db_sql, c_path)

    # Creation des tables
    updateLog("Création des tables", c_path, logName="LogSql")
    ls.createTables()
    # Reinit connexion Sql et de l'instance
    db_sql.close()
    db_sql = SqlConnect(c_mysql)
    ls = loadSql(db_mongo, db_sql, c_path)

    # Insertion table countries
    updateLog("Insert countries", c_path, logName="LogSql")
    retour = ls.insertCountries()
    updateLog(retour, c_path, False, logName="LogSql")

    # Insertion table cities
    updateLog("Insert cities", c_path, logName="LogSql")
    retour = ls.insertCities()
    updateLog(retour, c_path, False, logName="LogSql")

    # Insertion table airlines
    updateLog("Insert airlines", c_path, logName="LogSql")
    retour = ls.insertAirlines()
    updateLog(retour, c_path, False, logName="LogSql")

    # Insertion table aircraft
    updateLog("Insert aircraft", c_path, logName="LogSql")
    retour = ls.insertAircraft()
    updateLog(retour, c_path, False, logName="LogSql")

    # Insertion table airplanes
    updateLog("Insert airplanes", c_path, logName="LogSql")
    retour = ls.insertAirplanes()
    updateLog(retour, c_path, False, logName="LogSql")

    # Insertion table airports
    updateLog("Insert airports", c_path, logName="LogSql")
    retour = ls.insertAirports()
    updateLog(retour, c_path, False, logName="LogSql")

    updateLog("Création des clés étrangères", c_path, logName="LogSql")
    ls.createForeignKey()

except Exception as e:
    updateLog("ERREUR D'EXECUTION: " + str(e), c_path, logName="LogSql")
    updateLog("FIN ANORMALE DE L'INITIALISATION DE LA BASE DE DONNEES\n", c_path, logName="LogSql")
else:
    updateLog("FIN DE L'INITIALISATION DE LA BASE DE DONNEES\n", c_path, logName="LogSql")
finally:
    conn_mongo.close()
    db_sql.close()

