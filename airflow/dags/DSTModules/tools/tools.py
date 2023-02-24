

# Changer une liste de dictionnaires en liste de tuple contenant
# les valeurs des dictionnaires
def toListTuple(listDict) :
    listValues = [tuple((list(elt.values()))) for elt in listDict]
    return listValues

# 

