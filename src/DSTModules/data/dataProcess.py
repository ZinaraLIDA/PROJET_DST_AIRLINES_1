from DSTModules.data.loadMongo import loadMongo
from time import sleep
import pandas

def getSchedules(db, c_path, c_api):
    retour = ""
    # Instance de la classe loadMongo
    lm = loadMongo(db, c_path, c_api)
    # Requête API et création d'un fichier Json
    fileJson = lm.getDataInJson("schedules", c_api["params_schedules"])
    # Récupération du résultat 
    data = lm.getResultJson(fileJson)
    if (data!=""):
        # Transformation des datas
        data = lm.transformDataAL("schedules", data)
        # Update MongoDB
        result = lm.putMongo("schedules", data)
        retour = "Nombre de documents insérés: " + str(result)
    else:
        retour = "Aucun résultat"
    return retour, lm.dt

def getFlights(db, c_path, c_api):
    retour = ""
    # Instance de la classe loadMongo
    lm = loadMongo(db, c_path, c_api)
    # Requête API et création d'un fichier Json
    fileJson = lm.getDataInJson("flights", c_api["params_flights"])
    # Récupération du résultat 
    data = lm.getResultJson(fileJson)
    if (data!=""):
        # Transformation des datas
        data, nbNan = lm.transformDataAL("flights", data)
        # Update MongoDB
        result = lm.putMongo("flights", data)
        retour = "Nombre de documents insérés: " + str(result) + "\n"
        retour += "Nombre de documents ignorés: " + str(nbNan)
    else:
        retour = "Aucun résultat"
    return retour, lm.dt

def getDataRef(db, ressource, c_path, c_api, c_params):
    retour = ""
    # Instance de la classe loadMongo
    lm = loadMongo(db, c_path, c_api)
    # Requête API et création d'un fichier Json
    params = {"offset": 0, "limit": c_params["limit"]}
    fileJson = lm.getDataInJson(ressource,  params,"AviationStack")
    # Récupération du résultat 
    data = lm.getResultJson(fileJson,"data")
    if (data!=""):
        # Transformation des datas
        data = lm.transformDataAS(ressource, data, c_params["primary_key"])
        # Update MongoDB
        result = lm.putMongo(ressource, data)
        retour = "Nombre de documents insérés: " + str(result)
    else:
        retour = "Aucun résultat"
    return retour

def getDataMeteo(db, ressourse, c_path, c_apiM, dt_flights):
    fDate = dt_flights.strftime('%d-%m-%Y')
    fTime = dt_flights.strftime('%H:%M:%S')
    
    # boucle sur les documents flights pour le dt et pour le flag_meteo inexistant
    listFlight = list(db.flights.find({"$and": [{"load_date": fDate}, {"load_time": fTime}, {"flag_meteo": {"$exists": False}}]}, \
        {"_id": 1, "schedule_id": 1, "lat": 1, "lng": 1}))

    nbInsert = 0
    for doc in listFlight:
        param_Api=(doc["schedule_id"], doc["_id"], doc["lat"], doc["lng"])
        retour = getDataMeteoFlights(db, "weather", c_path, c_apiM, param_Api)
        nbInsert += retour
        sleep(1)
    retour = "Nombre de documents insérés: " + str(nbInsert)
    return retour

def getDataMeteoFlights(db, ressource, c_path, c_apiM, paramApi):
    retour = ""
     # récupération Id_Vol
    schedule_id=paramApi[0]
    flight_id=paramApi[1]
    # préparation des paramètres cité ou latitude longitude
    listeParamApi=[paramApi[2], paramApi[3]]

    # Instance de la classe loadMongo
    lm = loadMongo(db, c_path, c_apiM)
    # Requête API et création d'un fichier Json
    fileJson = lm.getDataInJsonMeteo("weather",paramApi=listeParamApi,params={})
    # Récupération du résultat 
    data = lm.getResultJsonMeteo(fileJson)
    # aplatissement des niveaux du dictionnaire récupéré
    data_niveau=lm.alignementDocumentMeteoCourante(data)
    if (data!=""):
        # Transformation des datas
        data_transform= lm.transformMeteoData(ressource="weather",data= data_niveau,schedule_id=schedule_id,flight_id=flight_id)
        # Update MongoDB
        result = lm.putMongoMeteo("weather", data_transform)
        retour = 1
    else:
        retour = 0
    return retour

def updSchedules(db, c_path, c_api):
    retour = ""
    # Instance de la classe loadMongo
    lm = loadMongo(db, c_path, c_api)
    # Mise à jour du nombre de flights dans schedule
    result = lm.updateNbFlights()
    retour = "Nombre de documents modifiés: " + str(result)
    return retour
