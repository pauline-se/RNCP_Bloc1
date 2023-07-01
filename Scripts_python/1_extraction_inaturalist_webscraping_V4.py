from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import pandas as pd
from selenium_stealth import stealth
from datetime import datetime
import os
import argparse



# Install driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument("--host-resolver-rules=MAP *.googleapis.com 127.0.0.1, MAP maps.googleapis.com 127.0.0.1")

driver = webdriver.Chrome(options=chrome_options)


stealth(driver,
              languages=["fr-FR", "fr"],
              vendor="Google Inc.",
              platform="Win32",
              webgl_vendor="Intel Inc.",
              renderer="Intel Iris OpenGL Engine",
              fix_hairline=True,
          )





def scroll_to_end(driver):
    #ici, on doit le répéter 3 fois pour arriver à la fin de la page. 2 secondes de pauses me paraissent suffisants et sont ok dans les tests
    for i in range(0,3):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(2)

  
  

def  getSightings(id_taxon, page_debut, nb_obs_total, nom_dossier):


    if not os.path.exists(nom_dossier):  # vérifier si le dossier existe déjà
        os.makedirs(nom_dossier)  # créer le dossier s'il n'existe pas

    #nombre d'URL d'observations trouvées
    url_count = 0

    # Je choisi d'initialiser la variable page_en_cours à 0 et de faire l'incrémentation en début de boucle pour qu'on puisse avoir directement 
    # le nombre de pages dans lesquelles il a fallu chercher à la sortie du while (c'est restitué à l'utilisateur dans un print)

    page_en_cours = page_debut-1

    results_start = 0

    #un set d'URLS, pour qu'il ne puisse pas y avoir de doublons
    urls = set()

    # boucle while car on continue à aller chercher de nouvelles observations tant qu'on n'a pas atteind le nombre d'observations demandées 
    # (ou si on arrive à la page 10 pour ne pas faire de boucles infinies si il y a un pb - à enlever plus tard quand on voudra de grandes quantités de données)
    while((url_count < nb_obs_total) and (page_en_cours<10)):
        page_en_cours+=1

        #l'URL du site, avec id à remplacer par le taxon cherché, et la page en cours (ça commence par page 1)
        #exemple : 42184 : chevreuil européen
        url = f"https://www.inaturalist.org/observations?page={page_en_cours}&place_id=any&taxon_id={id_taxon}"
        driver.get(url)

        #le temps que la page finisse bien de se charger
        time.sleep(10)

        #on va jusqu'au bas de la page pour que toutes les obs de la page soient chargées
        scroll_to_end(driver)

        #on repère les éléments par XPATH (parce que c'est la seule méthode qui semble bien fonctionner :(   je fais un try au cas ou il y ait des problèmes)
        try:
            elements_URLS=driver.find_elements(By.XPATH,'//*[@id="result-grid"]/div//div/div/inat-taxon/span/a[3]')
        except:
            #si pb on passe directement à la page suivante
            continue

        #on fait un try pour catcher le href au cas ou et on vérifie que notre href soit bien une url avec https://www.inaturalist.org/observations/
        for element in elements_URLS[:nb_obs_total] :
            try:
                url = element.get_attribute('href')
                # print(url)
                if ('https://www.inaturalist.org/observations' in url) and (url_count < nb_obs_total) :
                    url_count+=1
                    print(url)
                    urls.add(url)

            except:
                pass

        
    totalResults=len(urls)

    print(f"Found: {totalResults} search results in {page_en_cours} pages. Extracting links from {results_start}:{totalResults}")
    

    observations = []

    for url in urls:
        driver.get(url)

        time.sleep(5)

        id_observation = url.split("/")[-1]
        
        try:
            img = driver.find_element(By.XPATH,'//*[@id="ObservationShow"]/div[1]/div/div[2]/div/div/div/div[1]/div/div/div//div/div/div/img')
            src_img = img.get_attribute('src')
        except:
            src_img = None

        print("image :", src_img)


        try:
            quality_grade = driver.find_element(By.XPATH,'//*[@id="ObservationShow"]/div[1]/div/div[1]/div[1]/div/span[2]')
            quality_grade = quality_grade.get_attribute('class').split(" ")
            quality_grade = quality_grade[1]

        except:
            quality_grade = None

        print("quality_grade :", quality_grade)


        try:
            rank = driver.find_element(By.XPATH,'//*[@id="activity_identification_503f15d9-ff92-4ed7-8703-5a3ec01fa079"]/div[2]/div[2]/div/div/div[2]/span/a[2]')
            rank = rank.text

        except:
            rank = None

        print("rank :", rank)

        try:
            taxon_name = driver.find_element(By.XPATH,'//*[@id="ObservationShow"]/div[1]/div/div[3]/div[2]/div[1]/div/div/div[2]/span[1]/a[2]/text()')
            # taxon_name = rank.text

        except:
            taxon_name = None

        print("taxon_name :", taxon_name)


        try:
            user_login = driver.find_element(By.XPATH,'//*[@id="ObservationShow"]/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[2]/div[1]/a')
            user_login = user_login.text

        except:
            user_login = None

        print("user_login :", user_login)


        

        try:
            date_obs=driver.find_element(By.XPATH,'//*[@id="ObservationShow"]/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div[1]/span[2]')
            date_obs = date_obs.get_attribute("title")
            date_object = datetime.strptime(date_obs, "%Y-%m-%dT%H:%M:%S%z")
            annee = date_object.year
            mois = date_object.month
            jour = date_object.day

        except:
            date_obs = None
            annee = None
            mois = None
            jour = None


        print("date :",date_obs)

    

        try:
            btn_details= driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div[2]/div[2]/div/button')
            btn_details.click()
            try:
                latitude =driver.find_element(By.XPATH,'/html//div[2]/div[3]/div[2]/div[2]/div/ul/li/div/div[1]/div[1]/span[2]')
                latitude = float(latitude.text)
            except:
                latitude = None

            try:
                longitude=driver.find_element(By.XPATH,'/html//div[2]/div[3]/div[2]/div[2]/div/ul/li/div/div[1]/div[2]/span[2]')
                longitude = float(longitude.text)
            except:
                longitude = None

        except:
            latitude = None
            longitude = None
        
        print("latitude, longitude :", latitude, longitude)
        

        tab={'id':id_observation, 'uri':url, 'observed_on_details':{'date':date_obs, 'day':jour ,'month':mois, 'year':annee},'quality_grade': quality_grade, 'taxon' : {'id':id_taxon, 'name':taxon_name}, 'default_photo':{'url':src_img}, 'user':{'login':user_login},'latitude':latitude, 'longitude':longitude}
        print(tab)

        observations.append(tab)
        print(observations)
    

        #description : xpath :  //*[@id="ObservationShow"]/div[1]/div/div[3]/div[1]/div[1]/div/div/span/p
        # observation avec un exemple : https://www.inaturalist.org/observations/162695787

    print("FIN DE LA BOUCLE")
    print(observations)

    driver.quit()


    if not os.path.exists(nom_dossier):  # vérifier si le dossier existe déjà
        os.makedirs(nom_dossier)  # créer le dossier s'il n'existe pas

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]
    filename = 'Extraction_inaturalist_webscrapping_{}.json'.format(timestamp)
    filepath = os.path.join(nom_dossier, filename)
    print(filename)
    print(filepath)
    print(nom_dossier)

    # # Enregistrer les données dans un fichier JSON
    with open(filepath, "w") as f:
        json.dump(observations, f)

    
    

if __name__ == "__main__":
    
    # Créer un objet ArgumentParser
    parser = argparse.ArgumentParser()

    # Ajouter un argument '--input'
    parser.add_argument('--id_taxon', help='Code du taxon a extraire')
    parser.add_argument('--page_debut', help='Page de debut de l\'extraction')
    parser.add_argument('--nb_obs_total', help='Nb observations total a extraire')
    parser.add_argument('--nom_dossier', help='Dossier output')

    # Analyser les arguments de la ligne de commande
    args = parser.parse_args()

    # Récupérer la valeur de l'argument '--input'

    id_taxon = args.id_taxon
    page_debut = int(args.page_debut)
    nb_obs_total = int(args.nb_obs_total)
    nom_dossier = args.nom_dossier


    getSightings(id_taxon, page_debut, nb_obs_total, nom_dossier)
    # getSightings(42184,1,5,'.\Extract_files_webscraping')
    
    #chevreuil : 42184
    #éléphant de Savane d'Afrique : 43694

# 16/06: python extraction_inaturalist_webscraping_V4.py --id_taxon 42184 --page_debut 1 --nb_obs_total 15 --nom_dossier C:\Users\Pauline\Documents\Formation\RNCP\Bloc1\Data\A_TRAITER\WEBSCRAPING

# C:\Users\Pauline\Documents\Formation\RNCP\Bloc1\Scripts_python python extraction_inaturalist_webscraping_V4.py --id_taxon 42184 --page_debut 1 --nb_obs_total 15 --nom_dossier C:\Users\Pauline\Documents\Formation\RNCP\Bloc1\Data\A_TRAITER\WEBSCRAPING