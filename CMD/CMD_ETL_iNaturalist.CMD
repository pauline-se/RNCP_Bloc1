REM @echo off
setlocal

cd ..

REM Chemin vers repertoire de travail
set repTravail=%cd%

REM Definition du timestamp
set timestamp=%date:~-4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%

REM Chemin vers le dossier où extraire les donnees
set input_folder_api=%repTravail%\Data\A_TRAITER\API\

REM Chemin vers le dossier où extraire les donnees
set input_folder_webscp=%repTravail%\Data\A_TRAITER\WEBSCRAPING\

REM Definition du fichier de sauvegarde des fichiers json zippes
set output_folder=%repTravail%\Data\TRAITE\

REM Nom du fichier de logs
set logfile=logs-CMD-ETL-%timestamp%.txt

REM on se place dans le repertoire de travail pour lancer les extractions
cd %repTravail%


echo --------------------------------------DEBUT--SCRIPT---------------------------------------------- >> %repTravail%\LOGS\%logfile%
echo. >> %repTravail%\LOGS\%logfile%
echo Timestamp : %timestamp% >> %repTravail%\LOGS\%logfile%
echo Chemin vers repertoire de travail : %repTravail% >> %repTravail%\LOGS\%logfile%
echo Chemin vers le dossier où extraire les donnees : %input_folder_api% >> %repTravail%\LOGS\%logfile%
echo Nom du fichier de logs : %logfile% >> %repTravail%\LOGS\%logfile%
echo. >> %repTravail%\LOGS\%logfile%
echo. >> %repTravail%\LOGS\%logfile%


echo --------------------Phase 1 Extraction de donnees par webscraping--------------------------------- >> %repTravail%\LOGS\%logfile%
echo. >> %repTravail%\LOGS\%logfile%

echo %input_folder_webscp% >> %repTravail%\LOGS\%logfile%


REM Execution de la commande d'extraction
Python Scripts_python\1_extraction_inaturalist_webscraping_V4.py --id_taxon 42184 --page_debut 1 --nb_obs_total 15 --nom_dossier %input_folder_webscp% >> %repTravail%\LOGS\%logfile%

echo. >> %repTravail%\LOGS\%logfile%
echo Extraction de donnes webscraping terminee >> %repTravail%\LOGS\%logfile%

set timestamp=%date:~-4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%
echo Timestamp : %timestamp% >> %repTravail%\LOGS\%logfile%
echo. >> %repTravail%\LOGS\%logfile%

echo -----------------------Fin de phase 1 Webscraping------------------------------------------------- >> %repTravail%\LOGS\%logfile%
echo. >> %repTravail%\LOGS\%logfile%

echo ----------------------Phase 2 Extraction de donnees via API -------------------------------------- >> %repTravail%\LOGS\%logfile%
echo. >> %repTravail%\LOGS\%logfile%


REM Execution de la commande d'extraction
Python Scripts_python\2_extraction_inaturalist_V5.py --id_taxon 42184 --page_debut 1 --nb_obs_total 30 --nb_obs_par_fichier 10 --nom_dossier %input_folder_api% >> %repTravail%\LOGS\%logfile%

echo. >> %repTravail%\LOGS\%logfile%
echo Extraction de donnees terminee >> %repTravail%\LOGS\%logfile%

set timestamp=%date:~-4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%
echo Timestamp : %timestamp% >> %repTravail%\LOGS\%logfile%
echo. >> %repTravail%\LOGS\%logfile%

echo ----------------------Fin de phase 2 Extraction de donnees via API--------------------------------- >> %repTravail%\LOGS\%logfile%
echo. >> %repTravail%\LOGS\%logfile%



echo ----------------------Phase 3 Transformation des donnees dans KNIME-------------------------------- >> %repTravail%\LOGS\%logfile%
echo. >> %repTravail%\LOGS\%logfile%

REM Lancement de KNIME
"C:\Program Files\KNIME\knime.exe" -nosave -consoleLog -nosplash -reset -application  org.knime.product.KNIME_BATCH_APPLICATION -workflowDir="C:\Users\pauli\knime-workspace\Projet_fil_rouge" -workflow.variable=input_folder_api,%input_folder_api%,String -workflow.variable=output_folder,%output_folder%,String -workflow.variable=input_folder_webscp,%input_folder_webscp%,String >> %repTravail%\LOGS\%logfile%

echo. >> %repTravail%\LOGS\%logfile%
echo Transformation des donnees dans KNIME terminee >> %repTravail%\LOGS\%logfile%

set timestamp=%date:~-4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%
echo Timestamp : %timestamp% >> %repTravail%\LOGS\%logfile%
echo. >> %repTravail%\LOGS\%logfile%

echo ----------------------Fin de phase 3 Transformation des donnees dans KNIME--------------------------- >> %repTravail%\LOGS\%logfile%
echo. >> %repTravail%\LOGS\%logfile%

echo ----------------------Phase 4 Preparation des donnees par script python avec bibiothèque Pandas--- >> %repTravail%\LOGS\%logfile%
echo. >> %repTravail%\LOGS\%logfile%

Python Scripts_python\3_data_preparation.py

echo. >> %repTravail%\LOGS\%logfile%
echo ---------------Fin de phase 4 Prepartion des donnees par script python avec bibiothèque Pandas--- >> %repTravail%\LOGS\%logfile%
echo. >> %repTravail%\LOGS\%logfile%

echo ------------------------------------FIN--SCRIPT--------------------------------------------------- >> %repTravail%\LOGS\%logfile%


endlocal
pause
