import requests
from pymongo import MongoClient


# Définir l'URL de l'API
url = "https://api.inaturalist.org/v1/observations"

# Paramètres de la requête
params = {
    "taxon_id": "42184",
    "per_page": "200",
    "page": "1"
}

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://cptetechpauline:FkuXsgtmVMU4mjK2@inaturalist.pv8sin5.mongodb.net/?retryWrites=true&w=majority')
print(type(client))


db = client['iNaturalist']
print(type(db))

coll = db['collection_42184']

print(coll)
print(type(coll))


# client = MongoClient("mongodb+srv://protonalpha:v3BgrOQELNJ5mlwz@cluster0.febntob.mongodb.net/?retryWrites=true&w=majority")
# print(type(client))


# db_name = "iNaturalist"
# db = client[db_name]
# print(type(db))

# coll_name = "collection_42184"
# coll = db[coll_name]
# print(type(coll))


# Boucle pour récupérer les 20000 premières observations (200 par 200)
for i in range(100):
    # Mettre à jour le numéro de page dans les paramètres de la requête
    params["page"] = str(i + 1)
    
    # Faire la requête à l'API
    response = requests.get(url, params=params)
    
    # Vérifier que la réponse est OK
    if response.status_code == 200:
        # Insérer les observations dans la collection MongoDB
        coll.insert_many(response.json()["results"])
    else:
        # Afficher un message d'erreur si la réponse est invalide
        print(f"Erreur {response.status_code} lors de la récupération des observations à la page {i + 1}")
        break

# Afficher le nombre total d'observations récupérées
print(f"Nombre total d'observations : {coll.count_documents({})}")
