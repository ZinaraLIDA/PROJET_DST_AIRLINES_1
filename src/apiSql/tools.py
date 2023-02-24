from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import Unauthorized

# Récupération de l'authentification dans le header
def getAuthentification(headers):
    key = ""
    if "Authorization" in headers:
        key = headers["Authorization"]
    else:
        raise BadRequest("Votre requête est incorrect. Veuillez renseigner la clé dans le header de la requête.")
    return key

# Vérification de la clé d'authentification utilisée
def checkKey(key, c_api):
    # print(key)
    # print(c_api["key"])
    if key != c_api["key"]:
        raise Unauthorized("La clé d'authentification est incorrect")

# Création liste des codes iata des aérport déservis depuis CDG
def listeCodeIataAirportsArrival(listMongo:list)->list:
    liste_arr_iata = list()
    for element in listMongo:
        liste_arr_iata.append(element["arr_iata"])
    return list(set(liste_arr_iata))

# Préparation de transformation liste en str
def transformListStr(liste_arr_iata:list)->str:
    chaine = ""
    for element in liste_arr_iata:
        chaine += "'"+str(element)+"'"+","
    chaine = chaine[:-1]
    return chaine

# Transformation d'une liste de dictionnaire en dictionnaire
def transformDictListToDict(listDict:list)->dict:
    dict_ = {}
    for elt in listDict:
        for k, v in elt.items() :
            dict_[k] = v
    return dict_

# Transformation d'une liste de tuple en dictionnaire
def transformTupleListToDict(listTuple:list)->dict:
    dict_ = {str(elt[0]):str(elt[1]) for elt in listTuple}
    return dict_


# Filtre et suppression doublon (tuple)
def supprimerDoublonTuple(liste:list)->list:
    """liste = list(set(liste))
    liste.sort()
    return liste.copy()"""

    Liste_sans_doublon_city=[]
    for element in liste:
        # print(element[0])
        count:int=0
        for unite in Liste_sans_doublon_city:
            # print(unite[0])
            if element[0] == unite[0]:
                count+=1
        if(count==0):
            Liste_sans_doublon_city.append(element)
            print(Liste_sans_doublon_city)
    Liste_sans_doublon_city.sort()
    return Liste_sans_doublon_city

