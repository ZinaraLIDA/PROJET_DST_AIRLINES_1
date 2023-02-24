# DST_Airlines_1/src

Exécutables et code source de l'application

## Dossiers

```
  DST_Airlines_1/src/apiDash                 API Dash                           DST_Airlines_1/src/apiDash/README.md
  DST_Airlines_1/src/apiMongo                API Flask pour requêter MongoDB    DST_Airlines_1/src/apiMongo/README.md
  DST_Airlines_1/src/apiSql                API Flask pour requêter MySql      DST_Airlines_1/src/apiSql/README.md
  DST_Airlines_1/src/DSTModules              Modules de l'application           DST_Airlines_1/src/DSTModules/README.md
```

## Fichier config.ini

Contient toutes les constantes nécessaires au fonctionnement de l'application:
```
- Chaîne de connexion aux bases de données
- Chemins des fichiers
- URL et clefs d'authentification aux API
```

## Batchs

### getReferenceData.py

#### Données concernées

Données de références:
```
- Pays
- Villes
- Compagnies aériennes
- Aéroports
- Types d'avion
- Flottes
```

#### Séquence du batch

```
- Appel à l'API AviationStack pour récupération des données de références
- Création de fichiers json contenant le résultat de chaque requête
- Chargement des données dans des collections MongoDB
```

#### Fréquence d'exécution

```
- A l'itinialisation de l'application
- A la demande pour réinitialisation des données de référence
```

### initDBSql.py

#### Données concernées

Données de références:
```
- Pays
- Villes
- Compagnies aériennes
- Aéroports
- Types d'avion
- Flotte
```

#### Séquence du batch

```
- Création de la Database et des table de la base MySql
- Chargement des données dans les tables MySql à partir de MongoDB
- Création des clés étrangères de la base MySql
```

#### Fréquence d'exécution

```
- A l'itinialisation de l'application
- A la demande pour réinitialisation des données de référence après un drop database
```

### getFlightsData.py

#### Données concernées

Récupération des données en temps réels:
```
- Liste des vols planifiés
- Données en temps réel envoyés par les avions en cours de vol
- Données Météo associé à chaque vol
```

#### Séquence du batch

```
- Appel à l'API AirLabs pour récupération des vols planifiés
  Chargement des vols planifiés dans MongoDB
- Appel à l'API AirLabs pour récupération des informations en temps réels
  Chargement des informations en temps réel dans les tables MongoDB
- Appel à l'API OpenWeatherMap pour récupération des données de météo
  Chargement des données méteo dans les tables MongoDB
```

Les données se cumulent dans 3 collections:
```
- schedules
- flights
- weather
```

Les données sont chargées en insertion si l'information n'existe pas, ou en modification si l'information existe déjà.

#### Fréquence d'exécution

```
- Tous les jours, toutes 15 minutes
- Planifié sur le serveur avec crontab
```

