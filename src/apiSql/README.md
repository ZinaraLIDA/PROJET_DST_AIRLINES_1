# API SQL
---
Récupération des jeux de données au format *liste* ou *dictionnaire* de la base MongoDb DSTAirline et de la base MySQL DSTAirline.

Périmètres des données: Vols au départ de Paris Charles De Gaulle.

Routes disponibles:
* **status** : controle de l'api.
* **getArrivalAirports** : Code iata des aéroports desservis par les vols en partance de Paris Charles De Gaulle.
* **getCountries** : Les pays desservis par les vols en partance de Paris Charles De Gaulle.
* **getCities** : Les villes desservis par les vols en partance de Paris Charles De Gaulle pour un pays précis.
* **getAirports** : Informations complètes sur l'/les aéroport(s) desservi(s) par les vols en partance de Paris Charles De Gaulle pour une ville précise.
* **getSchedules** : Les vols disponibles pour un trajet précis entre deux dates.
* **getFlight** : Les données de vols disponibles pour un vol précis.
* **getWeather** : Les données météo disponibles pour un vol précis.
* **getDateRange** : Une fenêtre de date à définir.

# Lancement de l'API
---
Lancement en tâche de fond:

~/DST_Airlines_1/src/apiSQL/API_SQL.py &

L'API s'exécute sur le port 5002.

Les clés d'authentification se trouve dans le fichier config.ini de l'application.
