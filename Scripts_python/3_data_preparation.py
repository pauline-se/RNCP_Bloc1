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
        'LONGITUDE': document.get('LONGITUDE'),
        'SPECIES_GUESS': document.get('SPECIES_GUESS'),
        'SPECIES_NAME': document.get('SPECIES_NAME')
    }
    data_list.append(data)

data = pd.DataFrame(data_list)

# Fonction pour convertir les différentes formats de dates en un format cohérent
def convert_date(date_string):
    try:
        date = datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')
    return date.strftime('%Y-%m-%d')

#Modifications de certains champ selon besoin

# On repere les lignes avec des NULLS dans les colonnes ou les données ne doivent jamais être nulles
rows_nb_to_delete = data[['DATE', 'LATITUDE', 'LONGITUDE']].isna().any(axis=1)

#Nouveau dataframe : data_to_delete avec les lignes a supprimer
data_to_delete = data[rows_nb_to_delete]

# Suppression des documents correspondants dans la base MongoDB en utilisant les IDs
for row in data_to_delete.itertuples():
    collection.delete_one({'_id': row._1})

# On met à jour notre dataframe Pandas après ces suppressions
data = data[rows_nb_to_delete == False]

# Si pas jour du mois => remplacement par le 1er du mois
data['DAY'].fillna(1, inplace=True)

# Si rien de renseigné dans SEPCIES_GUESS => remplacement par le SPECIES_NAME, qui est toujours renseigné
data['SPECIES_GUESS'].fillna(data['SPECIES_NAME'], inplace=True)

# On applique les modifications de la fonction ci-dessus
data['DATE'] = data['DATE'].apply(convert_date)

#Mettre à jour les champs modifiés dans la BDD MongoDB
for row in data.itertuples():
    collection.update_one({'_id': row._1}, {'$set': {
        'DAY': row.DAY,
        'DATE': row.DATE,
        'SPECIES_GUESS': row.SPECIES_GUESS
    }})

print(data)