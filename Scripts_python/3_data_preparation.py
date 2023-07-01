import pandas as pd
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb+srv://cptetechpauline:FkuXsgtmVMU4mjK2@inaturalist.pv8sin5.mongodb.net/')


db = client['iNaturalist']
collection = db['collection_42184']


documents = list(collection.find())

data_list = []

# # Extraire les données de premier niveau de chaque document
for document in documents:
    data = {
        '_id': document.get('_id'),
        'ID': document.get('ID'),
        'DATE': document.get('DATE'),
        'WEEK': document.get('WEEK'),
        'MONTH': document.get('MONTH'),
        'HOUR': document.get('HOUR'),
        'YEAR': document.get('YEAR'),
        'DAY': document.get('DAY'),
        'LATITUDE': document.get('LATITUDE'),
        'LONGITUDE': document.get('LONGITUDE')
    }
    data_list.append(data)

data = pd.DataFrame(data_list)

print(data)


# Fonction pour convertir les différentes formats de dates en un format cohérent
def convert_date(date_string):
    try:
        date = datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')
    return date.strftime('%Y-%m-%d')

data['DAY'].fillna(15, inplace=True)
mean_latitude = data['LATITUDE'].mean()
mean_longitude = data['LONGITUDE'].mean()
data['LATITUDE'].fillna(mean_latitude, inplace=True)
data['LONGITUDE'].fillna(mean_longitude, inplace=True)
data['DATE'].drpona(inplace=True)
data['DATE'] = data['DATE'].apply(convert_date)

# # Mettre à jour les champs modifiés dans la BDD MongoDB
for row in data.itertuples():
    collection.update_one({'_id': row._1}, {'$set': {
        'DAY': row.DAY,
        'LATITUDE': row.LATITUDE,
        'DATE': row.DATE
        # Ajoutez d'autres champs à mettre à jour ici
    }})

# # Afficher les données après la préparation
print(data)