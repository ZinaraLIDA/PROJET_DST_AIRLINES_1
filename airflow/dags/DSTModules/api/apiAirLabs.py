#----------------------
# Client API AIR LABS
#----------------------
import requests
import json
from datetime import datetime
from pprint import pprint
#
class apiAirLabs:

    def __init__(self, config):
        self.url = config["url"]
        day = datetime.now().strftime('%d')
        key_name = config["key_days"][day]
        self.key = config["keys"][key_name]


    def getData(self, uri, params={}):
        headers = {
                "Accept" : "application/json",
                "Content-type" : "application/json"
        }
        params["api_key"] = self.key
        print(self.key)
        url = self.url+"/"+uri
        #print(url)
        response = requests.get(url, headers=headers, params=params)

        if response.ok:
            result = json.dumps(response.json(), indent=4)
            json_result = json.loads(result)
            if("error" in json_result):
                raise Exception(json_result["error"]["message"])

            return result
        else:
            raise Exception("Erreur get "+uri+":\n"+str(response.status_code)+" "+response.reason)
