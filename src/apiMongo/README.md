 # API MongoDB

Récupération des jeux de données au format JSON de la base MongoDB DSTAirline.

Périmètres des données: Vols au départ de Paris Charles de Gaulle.

Routes disponibles:
* **getListSchedules**: Liste des vols suivant plusieurs critères tel que la date et la destination
* **getFlight**: Informations complètes d'un vol avec données en cours de vol et météo
* **statFlightsCompany**: Statistiques de vols par compagnies aériennes
* **statDelayCompany**: Statistiques sur le retards de vols par compagnies aériennes
* **statAircrafts**: Statistiques sur les différents types d'avions
* **statFleets**: Statistiques sur les flottes des différentes compagnies aériennes

## Lancement de l'API

Lancement en tâche de fond:

~/DST_Airlines_1/src/apiMongo/apiMongo.py &

L'API s'exécute sur le port 5001.  
La clé d'authentification se trouve dans le fichier config.ini de l'application.

## Ressource getListSchedules 
Liste des vols suivant plusieurs critères tel que la date et la destination.
### Exemple d'un appel avec CURL:
```
curl -X POST "146.59.146.30:5001/getListSchedules" \
-H "Content-Type: application/json" \
-H "Authorization: qcze93jhj999993hjjhj" \
-d '{"dates": ["2022-11-29", "2022-11-30"],"destinations": ["BIQ", "BER"],"fields": ["arr_iata", "dep_time"]}'
```
### Paramètres dans l'entête de la requête:
| Paramètre  | Description |
| ------------- | ------------- |
| Authorization  | Doit contenir la clef d'accès à l'API  |
### Paramètres dans le corps de la requête:
| Paramètre  | Description |
| ------------- | ------------- |
| dates  | Liste d'une date ou de 2 dates (début et fin). Format yyyy-mm-dd |
| destinations| Liste d'une ou plusieurs destinations (code iata de l'aéroport). Si liste vide: toutes les destinations  |
| fields | Liste des champs en sortie. Si liste vide: tous les champs |

Exemple 1:  
```
{"dates": ["2022-11-29", "2022-11-30"],"destinations": ["BIQ", "BER"],"fields": ["arr_iata", "dep_time"]}
```
Exemple 2:  
```
{"dates": ["2022-11-29"],"destinations": [],"fields": []}
```
### Exemple de sortie:
```
{
    "search": {
        "begin_date": "2022-11-29 00:00",
        "end_date": "2022-11-30 23:59",
        "destinations": [
            "BIQ",
            "BER"
        ]
    },
    "result": {
        "count": 11
    },
    "data": [
        {
            "_id": "AF1434-1669702500",
            "aircraft_icao": null,
            "airline_iata": "AF",
            "airline_icao": "AFR",
            "arr_actual": "2022-11-29 08:55",
            "arr_actual_ts": 1669708500.0,
            "arr_actual_utc": "2022-11-29 07:55",
            "arr_baggage": "A3",
            "arr_delayed": NaN,
            "arr_estimated": "2022-11-29 08:55",
            "arr_estimated_ts": 1669708500.0,
            "arr_estimated_utc": "2022-11-29 07:55",
            "arr_gate": "A06",
            "arr_iata": "BER",
            "arr_icao": "EDDB",
            "arr_terminal": "1",
            "arr_time": "2022-11-29 09:00",
            "arr_time_ts": 1669708800,
            "arr_time_utc": "2022-11-29 08:00",
            "cs_airline_iata": "A5",
            "cs_flight_iata": "A51434",
            "cs_flight_number": "1434",
            "delayed": 2.0,
            "dep_actual": "2022-11-29 07:17",
            "dep_actual_ts": 1669702620.0,
            "dep_actual_utc": "2022-11-29 06:17",
            "dep_delayed": 2.0,
            "dep_estimated": "2022-11-29 07:17",
            "dep_estimated_ts": 1669702620.0,
            "dep_estimated_utc": "2022-11-29 06:17",
            "dep_gate": "G29",
            "dep_iata": "CDG",
            "dep_icao": "LFPG",
            "dep_terminal": "2G",
            "dep_time": "2022-11-29 07:15",
            "dep_time_ts": 1669702500,
            "dep_time_utc": "2022-11-29 06:15",
            "duration": 105,
            "flight_iata": "AF1434",
            "flight_icao": "AFR1434",
            "flight_number": "1434",
            "load_date": "29-11-2022",
            "load_json": "/home/ubuntu/DST_Airlines_1/json/Files_2022-11-29/schedules_1669709702_31135.json",
            "load_time": "08:15:02",
            "status": "landed",
            "nb_flights": 1
        }, {
          ...
        }]
    }
```
## Ressource getFlight 
Informations complètes d'un vol avec données en cours de vol et météo.
### Exemple d'un appel avec CURL:
```
curl -X POST "146.59.146.30:5001/getFlight" \
-H "Content-Type: application/json" \
-H "Authorization: qcze93jhj899993hjjhj" \
-d '{"schedule_id": "AF1234-1669808400"}'
```
### Paramètres dans l'entête de la requête:
| Paramètre  | Description |
| ------------- | ------------- |
| Authorization  | Doit contenir la clef d'accès à l'API  |
### Paramètres dans le corps de la requête:
| Paramètre  | Description |
| ------------- | ------------- |
| schedule_id  | ID du vol demandé (à récupérer dans le résultat de getListSchedules) |

Exemple:  
```
{"schedule_id": "AF1234-1669808400"}
```
### Exemple de sortie:
```
{
    "search": {
        "schedule_id": "AF1234-1669808400"
    },
    "result": {
        "count_schedule": 1,
        "count_flights": 6,
        "count_weather": 6
    },
    "schedule": [
        {
            "_id": "AF1234-1669808400",
            "aircraft_icao": "E190",
            "airline_iata": "AF",
            "airline_icao": "AFR",
            "arr_actual": NaN,
            "arr_actual_ts": NaN,
            "arr_actual_utc": NaN,
            "arr_baggage": null,
            "arr_delayed": 10.0,
            "arr_estimated": "2022-11-30 14:35",
            "arr_estimated_ts": 1669815300.0,
            "arr_estimated_utc": "2022-11-30 13:35",
            "arr_gate": null,
            "arr_iata": "BER",
            "arr_icao": "EDDB",
            "arr_terminal": "1",
            "arr_time": "2022-11-30 14:25",
            "arr_time_ts": 1669814700,
            "arr_time_utc": "2022-11-30 13:25",
            "cs_airline_iata": "A5",
            "cs_flight_iata": "A51234",
            "cs_flight_number": "1234",
            "delayed": 7.0,
            "dep_actual": "2022-11-30 12:47",
            "dep_actual_ts": 1669808820.0,
            "dep_actual_utc": "2022-11-30 11:47",
            "dep_delayed": 7.0,
            "dep_estimated": "2022-11-30 12:47",
            "dep_estimated_ts": 1669808820.0,
            "dep_estimated_utc": "2022-11-30 11:47",
            "dep_gate": "G31",
            "dep_iata": "CDG",
            "dep_icao": "LFPG",
            "dep_terminal": "2G",
            "dep_time": "2022-11-30 12:40",
            "dep_time_ts": 1669808400,
            "dep_time_utc": "2022-11-30 11:40",
            "duration": 105,
            "flight_iata": "AF1234",
            "flight_icao": "AFR1234",
            "flight_number": "1234",
            "load_date": "30-11-2022",
            "load_json": "/home/ubuntu/DST_Airlines_1/json/Files_2022-11-30/schedules_1669815901_977408.json",
            "load_time": "13:45:01",
            "status": "active",
            "nb_flights": 6
        }
    ],
    "flights": [
        {
            "_id": "AF1234-1669813697",
            "aircraft_icao": "E190",
            "airline_iata": "AF",
            "airline_icao": "AFR",
            "alt": 7162,
            "arr_iata": "BER",
            "arr_icao": "EDDB",
            "dep_iata": "CDG",
            "dep_icao": "LFPG",
            "dir": 54,
            "flag": "FR",
            "flight_iata": "AF1234",
            "flight_icao": "AFR1234",
            "flight_number": "1234",
            "hex": "398568",
            "lat": 51.647827,
            "lng": 11.720927,
            "load_date": "30-11-2022",
            "load_json": "/home/ubuntu/DST_Airlines_1/json/Files_2022-11-30/flights_1669814103_059176.json",
            "load_time": "13:15:03",
            "reg_number": "F-HBLI",
            "schedule_id": "AF1234-1669808400",
            "speed": 683,
            "squawk": "1000",
            "status": "en-route",
            "updated": 1669813697,
            "v_speed": NaN,
            "flag_meteo": 1
        },
        {
          ...
        }
    ],
    "weather": [
        {
            "_id": "51.6478_11.7209_1669814231",
            "cloudiness": 92,
            "country": "DE",
            "date_sunrise": 1669791336,
            "date_sunset": 1669820893,
            "date_unix": 1669814231,
            "feels_like": 277.55,
            "flight_id": "AF1234-1669813697",
            "humidity": 76,
            "lat": 51.6478,
            "load_date": "30-11-2022",
            "load_json": "/home/ubuntu/DST_Airlines_1/json/Files_2022-11-30/weather_1669814231_020725.json",
            "load_time": "13:17:11",
            "lon": 11.7209,
            "name": "ZICKERITZ",
            "pressure": 1023,
            "schedule_id": "AF1234-1669808400",
            "temp": 279.27,
            "temp_max": 279.62,
            "temp_min": 278.09,
            "timezone": 3600,
            "visibility": 10000,
            "weather": "Clouds",
            "weather_description": "overcast clouds",
            "wind_direction": 94,
            "wind_speed": 2.29
        },
        {
          ...
        }]
    }
```
## Ressource statFlightsCompany
Statistiques de vols par compagnies aériennes.
### Exemple d'un appel avec CURL:
```
curl -X POST "146.59.146.30:5001/statFlightsCompany" \
-H "Content-Type: application/json" \
-H "Authorization: qcze93jhj899999hjjhj" \
-d '{"dates": [], "sort": {"nb_departure":-1}, "limit": 10}'
```
### Paramètres dans l'entête de la requête:
| Paramètre  | Description |
| ------------- | ------------- |
| Authorization  | Doit contenir la clef d'accès à l'API  |
### Paramètres dans le corps de la requête:
| Paramètre  | Description |
| ------------- | ------------- |
| dates  | Liste de 2 dates (début et fin). Format yyyy-mm-dd. Si liste vide: toutes les données de la base |
| sort | Dictionnaire contenant le tri à effectuer. A indiquer dans la clef le champ à trier, et en valeur 1 pour un tri croissant et -1 pour un tri décroissant |
| limit | Nombres de documents en sortie. 0 pour tous les documents |

Exemple 1:  
```
{"dates": [], "sort": {"nb_departure":-1}, "limit": 10}
```
Exemple 2:
```
{"dates": ["2022-11-01", "2022-11-30"], "sort": {"nb_departure":-1}, "limit": 0}
```
### Exemple de sortie:
```
{
    "search": {
        "begin_date": "",
        "end_date": "",
        "sort": {
            "nb_departure": -1
        },
        "limit": 10
    },
    "result": {
        "count": 10
    },
    "data": [
        {
            "_id": "AF",
            "nb_departure": 3278,
            "first_departure": "2022-11-22 10:50",
            "last_departure": "2022-12-02 19:40",
            "nb_days": 11,
            "departure_day_avg": 298.0
        },
        {
            "_id": "DL",
            "nb_departure": 2094,
            "first_departure": "2022-11-22 10:30",
            "last_departure": "2022-12-02 19:35",
            "nb_days": 11,
            "departure_day_avg": 190.36363636363637
        },
        {
            ...
        }]
    }
```
## Ressource statDelayCompany
Statistiques sur le retards de vols par compagnies aériennes.
### Exemple d'un appel avec CURL:
```
curl -X POST "146.59.146.30:5001/statDelayCompany" \
-H "Content-Type: application/json" \
-H "Authorization: qcze93jhj899999hjjhj" \
-d '{"dates": [], "sort": {"delayed_avg":-1}, "limit": 10}'
```
### Paramètres dans l'entête de la requête:
| Paramètre  | Description |
| ------------- | ------------- |
| Authorization  | Doit contenir la clef d'accès à l'API  |
### Paramètres dans le corps de la requête:
| Paramètre  | Description |
| ------------- | ------------- |
| dates  | Liste de 2 dates (début et fin). Format yyyy-mm-dd. Si liste vide: toutes les données de la base |
| sort | Dictionnaire contenant le tri à effectuer. A indiquer dans la clef le champ à trier, et en valeur 1 pour un tri croissant et -1 pour un tri décroissant |
| limit | Nombres de documents en sortie. 0 pour tous les documents |

Exemple 1:  
```
{"dates": [], "sort": {"delayed_avg":-1}, "limit": 10}
```
Exemple 2:
```
{"dates": ["2022-11-01", "2022-11-30"], "sort": {"delayed_avg":-1}, "limit": 0}
```
### Exemple de sortie:
```
{
    "search": {
        "begin_date": "",
        "end_date": "",
        "sort": {
            "delayed_avg": -1
        },
        "limit": 10
    },
    "result": {
        "count": 10
    },
    "data": [
        {
            "_id": "SM",
            "delayed_avg": 55.0,
            "delayed_max": 55.0,
            "nb_flights": 1
        },
        {
            "_id": "WX",
            "delayed_avg": 47.0,
            "delayed_max": 96.0,
            "nb_flights": 3
        },
        {
            ...
        }]
    }
```
## Ressource statAircrafts
Statistiques sur les différents types d'avions.
### Exemple d'un appel avec CURL:
```
curl -X POST "146.59.146.30:5001/statAircrafts" \
-H "Content-Type: application/json" \
-H "Authorization: qcze93jhj899999hjjhj" \
-d '{"sort": {"speed_max":-1}, "limit": 0}'
```
### Paramètres dans l'entête de la requête:
| Paramètre  | Description |
| ------------- | ------------- |
| Authorization  | Doit contenir la clef d'accès à l'API  |
### Paramètres dans le corps de la requête:
| Paramètre  | Description |
| ------------- | ------------- |
| sort | Dictionnaire contenant le tri à effectuer. A indiquer dans la clef le champ à trier, et en valeur 1 pour un tri croissant et -1 pour un tri décroissant |
| limit | Nombres de documents en sortie. 0 pour tous les documents |

Exemple:  
```
{"sort": {"speed_max":-1}, "limit": 0}
```
### Exemple de sortie:
```
{
    "search": {
        "sort": {
            "speed_max": -1
        },
        "limit": 10
    },
    "result": {
        "count": 10
    },
    "data": [
        {
            "_id": "B789",
            "alt_max": 12496,
            "speed_max": 1194,
            "speed_avg": 848.4215256971653,
            "airlines": ["TK","WY","TN","UA","UK","SV","AC","NH","MS","AM","LY","EY","AF"],
            "nb_airlines": 13,
            "nb_schedules": 127
        },
        {
            "_id": "B77W",
            "alt_max": 13228,
            "speed_max": 1174,
            "speed_avg": 855.7940160201036,
            "airlines": ["QR","AC","SQ","SV","BR","TG","UU","MU","KE","CX","JL","AF"],
            "nb_airlines": 12,
            "nb_schedules": 335
        },
        {
            ...
        }]
    }
```
## Ressource statFleets
Statistiques sur les flottes des différentes compagnies aériennes.
### Exemple d'un appel avec CURL:
```
curl -X POST "146.59.146.30:5001/statFleets" \
-H "Content-Type: application/json" \
-H "Authorization: qcze93jhj899999hjjhj" \
-d '{"sort": {"nb_aircrafts":-1}, "limit": 0}'
```
### Paramètres dans l'entête de la requête:
| Paramètre  | Description |
| ------------- | ------------- |
| Authorization  | Doit contenir la clef d'accès à l'API  |
### Paramètres dans le corps de la requête:
| Paramètre  | Description |
| ------------- | ------------- |
| sort | Dictionnaire contenant le tri à effectuer. A indiquer dans la clef le champ à trier, et en valeur 1 pour un tri croissant et -1 pour un tri décroissant |
| limit | Nombres de documents en sortie. 0 pour tous les documents |

Exemple:  
```
{"sort": {"nb_aircrafts":-1}, "limit": 0}
```
### Exemple de sortie:
```
{
    "search": {
        "sort": {
            "nb_aircrafts": -1
        },
        "limit": 10
    },
    "result": {
        "count": 10
    },
    "data": [
        {
            "_id": "AA",
            "nb_aircrafts": 881,
            "aircrafts": ["E190","A333","A320","MD83","B77W","A321","A319","MD82","A332","B763","B752","B772","B738"],
            "plane_age_avg": 13.569476082004556,
            "plane_age_min": 2,
            "plane_age_max": 31
        },
        {
            "_id": "DL",
            "nb_aircrafts": 729,
            "aircrafts": ["B738","A319","MD88","B77L","B739","B753","A333","B764","B744","B737","B772","A320","B712","B752","A332"],
            "plane_age_avg": 19.39614243323442,
            "plane_age_min": 3,
            "plane_age_max": 33
        },
        {
            ...
        }]
    }
```
