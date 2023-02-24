from datetime import datetime
from pymongo import MongoClient
from DSTModules.data.connectMongo import MongoConnect

# Récupérer les vols disponibles du jour pour un aéroport de départ et de destination fixé
def getAvailableFlight(iataDepartureAirport, iataArrivalAirport):
    fDate = datetime.now()
    fDate = fDate.strftime('%Y-%m-%d')

    # Recuperation des paramètres de configuration
    config = getParamAll(pathRoot)
    c_mongo = config["mongo"]

    flightsInJson = db.flights.find({"load_date":"29-11-2022"})


    return fDate

print(getAvailableFlight("CDG", "JFK"))


# Transformer un dictionnaire en dataframe
