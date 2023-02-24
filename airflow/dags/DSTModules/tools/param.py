import json
import sys

# Test de l'os pour déterminer les chemins de fichiers
folder_separator = "/"
if(sys.platform=="win32"): folder_separator = "\\"

def getParamAll(pathRoot):
    fileObject = open(pathRoot + folder_separator + "config.ini", "r")
    objJson = fileObject.read()
    fileObject.close()
    obj = json.loads(objJson) 
    # insertion du sépérateur de dossier dans la config c_path
    obj["path"]["folder_separator"] = folder_separator
    return obj

def getParamMongo(pathRoot, folder_separator):
    fileObject = open(pathRoot + "/config.ini", "r")
    objJson = fileObject.read()
    fileObject.close()
    obj = json.loads(objJson)
    return obj["mongo"]

def getParamMySql(pathRoot, folder_separator):
    fileObject = open(pathRoot + "/config.ini", "r")
    objJson = fileObject.read()
    fileObject.close()
    obj = json.loads(objJson)
    return obj["mysql"]

def getParamPath(pathRoot, folder_separator):
    fileObject = open(pathRoot + "/config.ini", "r")
    objJson = fileObject.read()
    fileObject.close()
    obj = json.loads(objJson)
    obj["path"]["folder_separator"] = folder_separator
    return obj["path"]

def getParamApiAL(pathRoot, folder_separator):
    fileObject = open(pathRoot + "/config.ini", "r")
    objJson = fileObject.read()
    fileObject.close()
    obj = json.loads(objJson)
    return obj["api_airlabs"]

def getParamApiAS(pathRoot):
    fileObject = open(pathRoot + "/config.ini", "r")
    objJson = fileObject.read()
    fileObject.close()
    obj = json.loads(objJson)
    return obj["api_aviationstack"]

def getParamApiOWP(pathRoot):
    fileObject = open(pathRoot + "/config.ini", "r")
    objJson = fileObject.read()
    fileObject.close()
    obj = json.loads(objJson)
    return obj["api_openweathermap"]

def getParamApiLU(pathRoot):
    fileObject = open(pathRoot + "/config.ini", "r")
    objJson = fileObject.read()
    fileObject.close()
    obj = json.loads(objJson)
    return obj["api_lufthansa"]

def getParamApiMongo(pathRoot):
    fileObject = open(pathRoot + "/config.ini", "r")
    objJson = fileObject.read()
    fileObject.close()
    obj = json.loads(objJson)
    return obj["api_Mongo"]

def getParamApiSql(pathRoot):
    fileObject = open(pathRoot + "/config.ini", "r")
    objJson = fileObject.read()
    fileObject.close()
    obj = json.loads(objJson)
    return obj["api_Sql"]
