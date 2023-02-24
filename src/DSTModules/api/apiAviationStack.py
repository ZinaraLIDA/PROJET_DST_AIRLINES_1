#----------------------
# Client API AVIATION STACK
#----------------------
import requests
import json
from pprint import pprint
#
class apiAviationStack:

    def __init__(self, config):
        self.url = config["url"]
        self.key = config["key"]

    def getData(self, uri, params={}):
        headers = {
                "Accept" : "application/json",
                "Content-type" : "application/json"
        }
        params["access_key"] = self.key
        url = self.url+"/"+uri
        response = requests.get(url, headers=headers, params=params)

        if response.ok:
            result = json.dumps(response.json(), indent=4)
            return result
        else:
            raise Exception("Erreur get "+uri+":\n"+str(response.status_code)+" "+response.reason)


