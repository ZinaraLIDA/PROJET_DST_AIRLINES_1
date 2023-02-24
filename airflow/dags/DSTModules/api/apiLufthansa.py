#----------------------
# Client API LUFTHANSA
#----------------------
import requests
import json
from pprint import pprint
#
# Déclaration des constantes
urlToken = "https://api.lufthansa.com/v1/oauth/token"
clientId = "wxrnjrr63u4pwy5xb6kp3be4"
clientPass = "8ykm4YUp4Da27TNnj8Uy"
urlLuft = "https://api.lufthansa.com/v1"

#
# GET TOKEN
def getToken():
    headers={
        'Accept': 'application/json',
        'Content-Type':'application/x-www-form-urlencoded'
    }
    data = {'client_id':clientId,'client_secret': clientPass, 'grant_type': 'client_credentials'}
    response = requests.post(urlToken, headers=headers, data=data)

    if response.ok:
        result = response.json()
        return result["access_token"]
    else:
        raise Exception("Erreur dans la récupération du token:\n"+response.reason)

#
# GET DATA
def getData(token, uri, params={}):
    headers = {
            "Authorization" : "Bearer "+token,
            "Accept" : "application/json",
            "Content-type" : "application/json"
    }
    #url = urlLuft+"/"+uri+"/"+filtre
    url = urlLuft+"/"+uri
    #print(url)
    response = requests.get(url, headers=headers, params=params)

    if response.ok:
        result = json.dumps(response.json(), indent=4)
        return result
    else:
        raise Exception("Erreur get "+uri+":\n"+str(response.status_code)+" "+response.reason)
