from pymongo import MongoClient

class MongoConnect:

    def __init__(self, c_mongo):
        if (c_mongo["username"]!=""):
            self.client = MongoClient(host=c_mongo["server"],port = c_mongo["port"],username=c_mongo["username"],password=c_mongo["password"])
        else:
            self.client = MongoClient(host=c_mongo["server"],port = c_mongo["port"])

        self.db_airline = self.client[c_mongo["db_name"]]

    def close(self):
        self.client.close()
