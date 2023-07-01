import requests
import json
import datetime
import os
import time
import numpy as np
import sys
import argparse


def getObservations(id_taxon, page_debut, nb_obs_total, nb_obs_par_fichier, nom_dossier):

    page = page_debut

    nb_obs_recuperees = 0




    while (nb_obs_recuperees < nb_obs_total):
        
        if nb_obs_total - nb_obs_recuperees < nb_obs_par_fichier:
            nb_obs_par_fichier = nb_obs_total - nb_obs_recuperees

        params_request = {
            "taxon_id": str(id_taxon),
            "per_page": str(nb_obs_par_fichier),
            "page": str(page)
        }

        url = "https://api.inaturalist.org/v1/observations"

        #On interroge l'API avec requests
        response = requests.get(url, params=params_request)
        print("page", page, ",",nb_obs_par_fichier, "observations")

        # On met à jour page pour passer à la page suivante
        
        page = page + 1
        params_request["page"] = str(page)
       

        # On vide la liste d'observations pour le fichier
        observations = []

        if response.status_code == 200:
            observations.extend(response.json()["results"])
            nb_obs_recuperees += nb_obs_par_fichier
        else:
            # Afficher un message d'erreur si la réponse est invalide
            print(f"Erreur {response.status_code} lors de la récupération des observations à la page {page}")
            pass

        if not os.path.exists(nom_dossier):  # vérifier si le dossier existe déjà
            os.makedirs(nom_dossier)  # créer le dossier s'il n'existe pas

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]
        filename = 'Extraction_inaturalist_page_'+str(page-1)+'_{}.json'.format(timestamp)
        filepath = os.path.join(nom_dossier, filename)

        # Enregistrer les données dans un fichier JSON
        with open(filepath, "w") as f:
            json.dump(observations, f)




if __name__ == "__main__":

    # Créer un objet ArgumentParser
    parser = argparse.ArgumentParser()

    # Ajouter un argument '--input'
    parser.add_argument('--id_taxon', help='Code du taxon a extraire')
    parser.add_argument('--page_debut', help='Page de debut de l\'extraction')
    parser.add_argument('--nb_obs_total', help='Nb observations total a extraire')
    parser.add_argument('--nb_obs_par_fichier', help='Nb observations par fichier')
    parser.add_argument('--nom_dossier', help='Dossier output')

    # Analyser les arguments de la ligne de commande
    args = parser.parse_args()
    

    # Récupérer la valeur de l'argument '--input'

    id_taxon = args.id_taxon
    page_debut = int(args.page_debut)
    nb_obs_total = int(args.nb_obs_total)
    nb_obs_par_fichier = int(args.nb_obs_par_fichier)
    nom_dossier = args.nom_dossier



    getObservations(id_taxon, page_debut, nb_obs_total, nb_obs_par_fichier, nom_dossier)
    
    #chevreuil : 42184
    #éléphant de Savane d'Afrique : 43694

