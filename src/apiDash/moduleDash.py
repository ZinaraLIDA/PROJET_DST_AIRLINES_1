from requests.exceptions import HTTPError
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import BadRequest
import requests
import json
import pandas as pd
import plotly.express as px
from datetime import date, datetime
import os
import math
import numpy as np
import plotly.graph_objects as go

# Récupération des paramètres du fichier config.ini
def getParamAll(pathRoot):
    # fileObject = open(pathRoot + "/../config.ini", "r")
    fileObject = open("/src/config/config.ini", "r")
    objJson = fileObject.read()
    fileObject.close()
    obj = json.loads(objJson) 
    return obj

# Requête Get à l'API apiMongo
def getData(c_api, route, params={}):
    headers = {
            "Accept" : "application/json",
            "Content-type" : "application/json",
            "Authorization": c_api["key"]
    }
    url = c_api["url"]+"/"+route
    print(url)
    response = requests.get(url, headers=headers, params=params)
    if response.ok:
        result = json.dumps(response.json(), indent=4)
        json_result = json.loads(result)
        return json_result["data"]
    else:
        raise Exception("Erreur get "+route+":\n"+str(response.status_code)+" "+response.reason)

# Requête Post à l'API apiMongo
def postData(c_api, route, data={}):
    headers = {
            "Accept" : "application/json",
            "Content-type" : "application/json",
            "Authorization": c_api["key"]
    }
    url = c_api["url"]+"/"+route
    response = requests.post(url, headers=headers, json=data)
    if response.ok:
        result = json.dumps(response.json(), indent=4)
        json_result = json.loads(result)
        return json_result["data"]
    else:
        raise Exception("Erreur get "+route+":\n"+str(response.status_code)+" "+response.reason)


# requestAPI SQL

# Récupération des pays desservis par CDG
def getDictCountries(c_api: dict, dep_iata:str)->dict:
    url = c_api["url"] + "/getCountries"
    header = {"Content-Type":"application/json","Authorization":c_api["key"]}
    data = {"dep_iata":dep_iata}
    response = requests.post(url = url, json = data, headers = header)
    if response.ok:
        responseJson = response.json()
        return responseJson

    else:
        raise Exception("Erreur get countries:\n"+str(response.status_code)+" "+response.reason)

# Récupération des villes
def getDictCities(c_api: dict, dep_iata:str, arr_country_iso2:str)->dict:
    try :
        url = c_api["url"] + "/getCities"
        header = {"Content-Type":"application/json","Authorization":c_api["key"]}
        data = {"dep_iata":dep_iata, "arr_country_iso2":arr_country_iso2}
        print(data)
        response = requests.post(url = url, json = data, headers = header)
        print(response)
        responseJson = response.json()
        return responseJson
    except:
        raise Exception("Erreur get "+":\n"+str(response.status_code)+" "+response.reason)

# Récupération des aéroports
def getDictAirports(c_api: dict, dep_iata:str, arr_city_name:str)->dict:
    try:
        url = c_api["url"] + "/getAirports"
        header = {"Content-Type":"application/json","Authorization":c_api["key"]}
        data = {"dep_iata":dep_iata, "arr_city_name":arr_city_name}
        response = requests.post(url = url, json = data, headers = header)
        responseJson = response.json()
        return responseJson
    except:
        raise Exception("Erreur get "+":\n"+str(response.status_code)+" "+response.reason)

# Récupération des schedules
def getDictSchedules(c_api: dict, dep_iata:str, arr_airport_name:str, start_date:str, end_date:str)->dict:
    url = c_api["url"] + "/getSchedules"
    header = {"Content-Type":"application/json","Authorization":c_api["key"]}
    start_date_h = start_date + " 00:00"
    end_date_h = end_date + " 23:59"
    data = {"dep_iata":dep_iata, "arr_airport_name":arr_airport_name, "start_date":start_date_h, "end_date":end_date_h}
    print(data)
    response = requests.post(url = url, json = data, headers = header)
    if response.ok:
        responseJson = response.json()
        return responseJson
    else:
        raise Exception("Erreur get "+":\n"+str(response.status_code)+" "+response.reason)

# Récupération d'un vol précis
def getDictFlight(c_api: dict, id_schedule:str)->dict:
    url = c_api["url"] + "/getFlight"
    header = {"Content-Type":"application/json","Authorization":c_api["key"]}
    data = {"id_schedule":id_schedule}
    response = requests.post(url = url, json = data, headers = header)
    if response.ok:
        responseJson = response.json()
        return responseJson
    else:
        raise Exception("Erreur get "+":\n"+str(response.status_code)+" "+response.reason)

# Récupération des données de météo d'un vol précis
def getDictWeather(c_api: dict, id_schedule:str)->dict:
    url = c_api["url"] + "/getWeather"
    header = {"Content-Type":"application/json","Authorization":c_api["key"]}
    data = {"id_schedule":id_schedule}
    response = requests.post(url = url, json = data, headers = header)
    if response.ok:
        responseJson = response.json()
        return responseJson
    else:
        raise Exception("Erreur get "+":\n"+str(response.status_code)+" "+response.reason)

def addDepArrToDict(data, id, df_airports, prefix):
    airport = df_airports.loc[df_airports["iata_code"]==data[prefix + "_iata"]]

    lat = airport["latitude"]
    lon = airport["longitude"]
    element = {
        "_id": id,
        "aircraft_icao": data["schedule_id"],
        "airline_iata": data["airline_iata"],
        "airline_icao": data["airline_icao"],
        "alt": 0,
        "arr_iata": data["arr_iata"],
        "arr_icao": data["arr_icao"],
        "dep_iata": data["dep_iata"],
        "dep_icao": data["dep_icao"],
        "dir": data["dir"],
        "flag": data["flag"],
        "flag_meteo": 0,
        "flight_iata": data["flight_iata"],
        "flight_icao": data["flight_icao"],
        "flight_number": data["flight_number"],
        "hex": data["hex"],
        "lat": float(lat),
        "lng": float(lon),
        "load_date": data["load_date"],
        "load_json": data["load_json"],
        "load_time": data["load_time"],
        "reg_number": data["reg_number"],
        "schedule_id": data["schedule_id"],
        "speed": 0,
        "squawk": data["squawk"],
        "status": data["status"],
        "updated": data["updated"],
        "v_speed": data["v_speed"]
    }
    return element


# Création d'un dataframe à partir d'un dictionnaire
def transformDictToDf(dict_:dict, df_airports=None) :        
    data_ = dict_["response"]
    if len(data_) != 0:
        columns_ = list(data_[0].keys())
        df = pd.DataFrame(columns=columns_)
        if df_airports is not None:
            print("data_num", len(data_))
            data_.insert(0, addDepArrToDict(data_[0], data_[0]["_id"], df_airports, "dep"))
            data_.append(addDepArrToDict(data_[0], data_[len(data_)-1]["_id"], df_airports, "arr"))
            print("data_num", len(data_))
        for i in range(len(data_)) :
            if columns_ == list(data_[i].keys()) :
                df.loc[i] = list(data_[i].values())
            # else:
            #     print("Col init:", columns_)
            #     print("Col data:", list(data_[i].keys()))
        return df
    else:
        raise Exception("Vol sans aucunes données mises à jours")

def map(dataframe):
    # print(dataframe.sort_values(by=['updated']))
    # dataframe = dataframe.sort_values(by=['load_time'])
    # fig = px.scatter_mapbox(dataframe, lat="lat_x", lon="lng", color="flight_iata", zoom=3, height=950, color_discrete_sequence=['red'])
    # fig.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=4, mapbox_center_lat = 41,
    #     margin={"r":0,"t":0,"l":0,"b":0})
    zoom, center = zoom_center(
        lons=dataframe["lng"],
        lats=dataframe["lat_x"]
    )
    print("zoom:", zoom)
    dataframe["temp"] = dataframe["temp"]-273
    dataframe["marker_size"] = 10
    fig = px.scatter_mapbox(dataframe, lat="lat_x", lon="lng", color="temp", size="marker_size", size_max=11, height=850, zoom=zoom, center=center, color_continuous_scale=px.colors.cyclical.IceFire,
    hover_data=["alt", "speed", "dep_iata", "arr_iata", "humidity", "pressure", "visibility", "weather_description", "wind_speed", "temp"])
    fig.update_layout(mapbox_style="stamen-terrain", 
        margin={"r":0,"t":0,"l":0,"b":0})
    fig.add_traces(px.line_mapbox(dataframe.loc[dataframe.index], lat="lat_x", lon="lng",
    hover_data=["alt", "speed", "dep_iata", "arr_iata", "humidity", "pressure", "visibility", "weather_description", "wind_speed", "temp"]).data)
    return fig

def zoom_center(lons: tuple=None, lats: tuple=None, lonlats: tuple=None,
        format: str='lonlat', projection: str='mercator',
        width_to_height: float=2.0):
    if lons is None and lats is None:
        if isinstance(lonlats, tuple):
            lons, lats = zip(*lonlats)
        else:
            raise ValueError(
                'Must pass lons & lats or lonlats'
            )
    
    maxlon, minlon = max(lons), min(lons)
    maxlat, minlat = max(lats), min(lats)
    center = {
        'lon': round((maxlon + minlon) / 2, 6),
        'lat': round((maxlat + minlat) / 2, 6)
    }
    
    # longitudinal range by zoom level (20 to 1)
    # in degrees, if centered at equator
    lon_zoom_range = np.array([
        0.0007, 0.0014, 0.003, 0.006, 0.012, 0.024, 0.048, 0.096,
        0.192, 0.3712, 0.768, 1.536, 3.072, 6.144, 11.8784, 23.7568,
        47.5136, 98.304, 190.0544, 360.0
    ])
    
    if projection == 'mercator':
        margin = 1.2
        height = (maxlat - minlat) * margin * width_to_height
        width = (maxlon - minlon) * margin
        lon_zoom = np.interp(width , lon_zoom_range, range(20, 0, -1))
        lat_zoom = np.interp(height, lon_zoom_range, range(20, 0, -1))
        zoom = round(min(lon_zoom, lat_zoom), 2)
    else:
        raise NotImplementedError(
            f'{projection} projection is not implemented'
        )
    
    return zoom, center

def getDateRange(c_api_mongo):
    response = getData(c_api_mongo, "getDateRange")
    str_start_date = list(response)[0]["start_date"].split(" ")[0]
    str_end_date = list(response)[0]["end_date"].split(" ")[0]
    init_start_date = date(int(str_start_date.split("-")[0]), int(str_start_date.split("-")[1]), int(str_start_date.split("-")[2]))
    init_end_date = date(int(str_end_date.split("-")[0]), int(str_end_date.split("-")[1]), int(str_end_date.split("-")[2]))
    return init_start_date, init_end_date

def initApp():
    # # Récupération du dossier de l’exécutable
    # pathRoot = os.path.dirname(os.path.abspath(__file__))
    # # Recuperation des paramètres de configuration
    # config = getParamAll(pathRoot)
    config = {
        "api_airlabs":{
            "params_schedules": {"dep_iata": os.environ.get('DEP_IATA')},
            "params_flights": {"dep_iata": os.environ.get('DEP_IATA')}
        },
        "api_aviationstack":{
            "dep_iata": os.environ.get('DEP_IATA')
        },
        "api_Mongo":{
            "url": os.environ.get('API_MONGO_URL'),
            "key": os.environ.get('MONGO_KEY')
        },
        "api_Sql":{
            "url": os.environ.get('API_MYSQL_URL'),
            "key": os.environ.get('MYSQL_KEY')
        }
    }
    # c_path = config["path"]
    c_api_mongo = config["api_Mongo"]
    c_api_sql = config["api_Sql"]
    dep_iata = config["api_aviationstack"]["dep_iata"]
    # récupération des dates de début et de fin des données
    init_start_date, init_end_date = getDateRange(c_api_mongo)
    return c_api_mongo, c_api_sql, dep_iata, init_start_date, init_end_date

def createDataframe(c_api_mongo, c_api_sql, dep_iata):
    response = getData(c_api_mongo, "getAirlines")
    df_airlines = pd.DataFrame(list(response))
    response = getData(c_api_mongo, "getActiveAirlines")
    df_active_airlines = pd.DataFrame(list(response))
    # Récupération Aircrafts
    response = getData(c_api_mongo, "getAircrafts")
    df_aircrafts = pd.DataFrame(list(response))
    # Récupération Airplanes
    response = getData(c_api_mongo, "getAirplanesGroupBy")
    df_airplanes_groupby = pd.DataFrame(list(response))
    response = getData(c_api_mongo, "getAirplanes")
    df_airplanes = pd.DataFrame(list(response))
    # Récupération Airport
    response = getData(c_api_mongo, "getAirports")
    df_airports = pd.DataFrame(list(response))
    # Récupération statFlightsCompany
    response = postData(c_api_mongo, "statFlightsCompany", {'dates': [], 'sort': {'nb_departure':-1}, 'limit': 10})
    df = pd.DataFrame(list(response))
    df = df.merge(df_airlines, how='inner', left_on='_id', right_on='_id')
    # Récupération des pays
    dictCountries = getDictCountries(c_api_sql, dep_iata)
    return df_airlines, df_active_airlines, df_aircrafts, df_airplanes_groupby, df_airplanes, df_airports, dictCountries, df
