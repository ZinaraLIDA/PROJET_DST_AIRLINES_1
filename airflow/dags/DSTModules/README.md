# DST_Airlines_1/src/DST_Modules

Modules de l'application

  
## DST_Modules/api
   
### apiAirLabs.py
Classe apiAirLabs
Envoi des requêtes vers l'API AirLabs pour récupération des données de référence.
```
from DSTModules.api.apiAirLabs import apiAirLabs
api = apiAirLabs(c_api: dict)
```

#### Attributs

| Attribut  | Description | Type |
| ------------- | ------------- | ------------- |
| url  | URL de l'API  | str |
| key  | Clé d'authentification à l'API  | str |

#### Méthodes
  
| Méthode  | Description | Sortie |
| ------------- | ------------- | ------------- |
| getData(route: str, params: dict)  | Requête vers l'api  | json |


### apiAviationStack.py
Classe apiAviationStack
Envoi des requêtes vers l'API AviationsStack pour récupération des données de vol en temps réels.
```
from DSTModules.api.apiAviationStack import apiAviationStack
api = apiAviationStack(c_api dict)
```

#### Attributs
| Attribut  | Description | Type |
| ------------- | ------------- | ------------- |
| url  | URL de l'API  | str |
| key  | Clé d'authentification à l'API  | str |

#### Méthodes
  
| Méthode  | Description | Sortie |
| ------------- | ------------- | ------------- |
| getData(route: str, params: dict)  | Requête vers l'api  | json |


### apiOpenweathermap.py
Classe apiOpenweathermap
Envoi des requêtes vers l'API OpenWeatherMap pour récupération des données de météo.
```
from DSTModules.api.apiOpenweathermap import apiOpenweathermap
apiOpenweathermap(c_api: str, paramApi: list)
```

#### Attributs
| Attribut  | Description | Type |
| ------------- | ------------- | ------------- |
| url  | URL de l'API  | str |
| key  | Clé d'authentification à l'API  | str |
| paramApiVol  | Paramètres du vol associé  | list |

#### Méthodes
  
| Méthode  | Description | Sortie |
| ------------- | ------------- | ------------- |
| getData(route: str, params: dict)  | Requête vers l'api  | json |


## DST_Modules/data

### connectMongo.py
Classe MongoConnect  
Connexion à MongoDB
```
from DSTModules.data.connectMongo import MongoConnect
client = MongoConnect(c_mongo: dict)
```

#### Attributs
| Attribut  | Description | Type |
| ------------- | ------------- | ------------- |
| client  | Client MongoDB  | MongoClient |
| db_airline  | Base de données MongoDB  | MongoClient.db |

#### Méthodes
  
| Méthode  | Description | Sortie |
| ------------- | ------------- | ------------- |
| close()  | Déconnexion de MongoDB  |  |
  

### connectSql.py
Classe SqlConnect
Connexion à MySql
```
from DSTModules.data.connectSql import SqlConnect
conn = SqlConnect(c_mysql: str)
```
#### Attributs
| Attribut  | Description | Type |
| ------------- | ------------- | ------------- |
| conn  | Objet Connexion  | mysql.connector.connect |

#### Méthodes
  
| Méthode  | Description | Sortie |
| ------------- | ------------- | ------------- |
| close()  | Déconnexion de MySql  |  |

### dataProcess.py
Module dataProcess  
Différents process de traitement batch
```
from DSTModules.data import dataProcess
```
#### Fonctions
  
| Fonction  | Description | Sortie |
| ------------- | ------------- | ------------- |
| getSchedules(db: ClientMongo.db, c_path: dict, c_api: dict)  | Récupération des données schedules et chargement dans MongoDB  | resultat: str, dt: timestamp |
| getFlights(db: ClientMongo.db, c_path: dict, c_api: dict)  | Récupération des données flights et chargement dans MongoDB  | resultat: str, dt: timestamp |
| getDataRef(db: ClientMongo.db, route: str, c_path: dict, c_api: dict, c_params: dict)  | Récupération des données de référence et chargement dans MongoDB  | resultat: str |
| getDataMeteo(db: ClientMongo.db, route: str, c_path: dict, c_api: dict, dt_flights: datetime)  | Récupération des données météo et chargement dans MongoDB  | resultat: str |
| getDataMeteo(db: ClientMongo.db, route: str, c_path: dict, c_api: dict, dt_flights: datetime)  | Traitement des données météo par lot  | resultat: str |
| getDataMeteoFlights(db: ClientMongo.db, route: str, c_path: dict, c_api: dict, paramApi: list)  | Données météo par position et chargement dans MongoDB | resultat: int |
| updSchedules(db: ClientMongo.db, route: str, c_path: dict, c_api: dict)  | Mise à jour collection schedules avec les données de flights | resultat: str |

### loadMongo.py
Classe loadMongo
Différentes étapes des process MongoDB
```
from DSTModules.data.loadMongo import loadMongo
lm = loadMongo(db: ClientMongo.db, c_path: dict, c_api: dict)
```
#### Attributs
| Attribut  | Description | Type |
| ------------- | ------------- | ------------- |
| dt  | Identification du process  | datetime |
| db  | Database MongoDB  | ClientMongo.db |
| c_api  | Paramètres API  | dict |
| c_path  | Chemins des fichiers  | dict |
| c_pathOutDay  | Chemin fichier jsons  | str |

#### Méthodes
  
| Méthode  | Description | Sortie |
| ------------- | ------------- | ------------- |
| getDataInJson(ressource: str, params: dict, api: str)  | Appel des classes apiAirLabs/apiAviationStack et création fichier json  | fileOut: str  |
| getResultJson(fileJson: str, response: str)  | Lecture fichier json  | result: json  |
| transformDataAL(ressource: str, data: json)  | Ajout de nouvelles colonnes aux collections venant de AirLabs | data: list, nbNan: int  |
| transformDataAS(ressource: str, data: json, primary_key:str)  | Nettoyage des collections venant AviationStack  | data: list  |
| putMongo(ressource: str, data: list)  | Chargement des données de vols dans MongoDB  | nbInsert: int  |
| getDataInJsonMeteo(ressource: str, paramApi: list, params: dict)  | Appel de la classe apiOpenWeatherMap et création fichier json  | fileOut: str  |
| getResultJsonMeteo(fileJson: str)  | Lecture fichier json météo | data: json  |
| transformMeteoData(ressource: str, data: schedule_id: str, flight_id: str)  | Ajout de nouvelles colonnes à la collection météo | data: list, nbNan: int  |
| putMongoMeteo(ressource: str, data: list)  | Chargement des données météo dans MongoDB  |  |
| updateNbFlights()  | Mise à jour collection schedules avec les données de flights  | nbModif: int  |

### loadSql.py
Classe loadSql
Différentes étapes des process Sql
```
from DSTModules.data.loadSql import loadSql
ls = loadSql(db_mongo: ClientMongo.db, db_sql: sql.connector.connect, c_path: dict)
```
#### Attributs
| Attribut  | Description | Type |
| ------------- | ------------- | ------------- |
| db_mongo  | Database client MongoDB  | ClientMongo.db |
| db_Sql  | Objet connection MySql  | sql.connector.connect |
| c_path  | Chemins des fichiers  | dict |

#### Méthodes
  
| Méthode  | Description | Sortie |
| ------------- | ------------- | ------------- |
| createTables()  | Lancement du script de création de la database et des tables  |  |
| insertTable(query: str, list_values: list)  | Insertion d'une liste de données dans une table Sql  | nb: int  |
| createForeignKey()  | Création des clefs étrangères |  |
| insertCountries()  | Insertion dans la table countries  | result: str  |
| insertCities()  | Insertion dans la table cities  | result: str  |
| insertAirlines()  | Insertion dans la table airlines  | result: str  |
| insertAircraft()  | Insertion dans la table aircrafts  | result: str  |
| insertAirplanes()  | Insertion dans la table airplanes  | result: str  |
| insertAirports()  | Insertion dans la table airports  | result: str  |


## DST_Modules/tools

### files.py
Module files
Opération sur les fichiers
```
from DSTModules.tools import files
```
#### Fonctions
  
| Fonction  | Description | Sortie |
| ------------- | ------------- | ------------- |
| writeFile(filename: str, text: str, openmode: str)  | Ecriture d'un nouveau fichier  |  |
| appendFile(filename: str, text: str, openmode: str)  | Ajout dans un fichier existant |  |
| updateLog(message: str, c_path: dict, withTime: bool, logName: str)  | Mise à jour des traces d'exécution des traitements |  |


### param.py
Module param
Récupération des paramètres du fichier config.ini
```
from DSTModules.tools import param
```
#### Fonctions
  
| Fonction  | Description | Sortie |
| ------------- | ------------- | ------------- |
| getParamAll(pathRoot: str)  | Récupération de tous les paramètres | param: dict |
| getParamMongo(pathRoot: str)  | Récupération des paramètres de MongoDB | param: dict |
| getParamMySql(pathRoot: str)  | Récupération des paramètres de MySql | param: dict |
| getParamPath(pathRoot: str)  | Récupération des chemins de fichiers | param: dict |
| getParamApiAL(pathRoot: str)  | Récupération des paramètres de l'API AirLabs | param: dict |
| getParamApiAS(pathRoot: str)  | Récupération des paramètres de l'API AviationStack | param: dict |
| getParamApiOWM(pathRoot: str)  | Récupération des paramètres de l'API OpenWeatherMap | param: dict |
| getParamApiMongo(pathRoot: str)  | Récupération des paramètres de l'API apiMongo | param: dict |
| getParamApiSql(pathRoot: str)  | Récupération des paramètres de l'API apiSql | param: dict |


### tools.py
Module tools
Outils divers
```
from DSTModules.tools import tools
```
#### Fonctions
  
| Fonction  | Description | Sortie |
| ------------- | ------------- | ------------- |
| toListTuple(listDict: list)  | Transforme une liste de dictionnaire en une liste de tuples | param: list |
