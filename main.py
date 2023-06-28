import geopandas as gpd
import pandas as pd
import numpy as np
from flask import Flask
from numpy import nan
import contextily as cx
import matplotlib.pyplot as plt
import matplotlib.markers as mrk
import glob
import mapclassify
import glob

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                           Importation                         #
#                               des                             #
#                             données                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

geoDonnées = gpd.read_file("rga2020_dataviz_challenge.geojson")
données = {
    'age' : gpd.read_file("fichier_traite_rga/age-Tableau 1.csv"),
    'cheptel' : gpd.read_file("fichier_traite_rga/cheptel-Tableau 1.csv"),
    'devenir' : gpd.read_file("fichier_traite_rga/devenir_exploitation-Tableau 1.csv"),
    'evolution' : gpd.read_file("fichier_traite_rga/evolution-Tableau 1.csv"),
    'donnéesGenerales' : gpd.read_file("fichier_traite_rga/Feuil1-Tableau 1.csv"),
    'mainOeuvre' : gpd.read_file("fichier_traite_rga/main_d_oeuvre-Tableau 1.csv"),
    'nombreExp' : gpd.read_file("fichier_traite_rga/nombre_exploitation-Tableau 1.csv"),
    'otexCommune' : gpd.read_file("fichier_traite_rga/otex_commune-Tableau 1.csv"),
    'otex' : gpd.read_file("fichier_traite_rga/otex-Tableau 1.csv"),
    'statutExp' : gpd.read_file("fichier_traite_rga/statut_exploitation-Tableau 1.csv"),
    'tailleExp' : gpd.read_file("fichier_traite_rga/taille_exploitation-Tableau 1.csv"),
    'valorisation' : gpd.read_file("fichier_traite_rga/valorisation-Tableau 1.csv")
}

infosPôle = {
    "Amikuze" : {
        "age" : pd.read_table("fichiersParPole/fts_ra2020_amikuze/age-Tableau 1.csv", sep=';'),
        "chiffres_cles" : pd.read_table("fichiersParPole/fts_ra2020_amikuze/chiffres_cles-Tableau 1.csv", sep=';'),
        "communes" : pd.read_table("fichiersParPole/fts_ra2020_amikuze/communes-Tableau 1.csv", sep=';'),
        "devenir" : pd.read_table("fichiersParPole/fts_ra2020_amikuze/devenir-Tableau 1.csv", sep=';'),
        "dim_eco" : pd.read_table("fichiersParPole/fts_ra2020_amikuze/dim_eco-Tableau 1.csv", sep=';'),
        "effectifs_cheptel" : pd.read_table("fichiersParPole/fts_ra2020_amikuze/effectifs_cheptel-Tableau 1.csv", sep=';'),
        "evolution_n_exploit_sau" : pd.read_table("fichiersParPole/fts_ra2020_amikuze/evolution_n_exploit_sau-Tableau 1.csv", sep=';'),
        "main_doeuvre" : pd.read_table("fichiersParPole/fts_ra2020_amikuze/main_doeuvre-Tableau 1.csv", sep=';'),
        "otex_com" : pd.read_table("fichiersParPole/fts_ra2020_amikuze/otex_com-Tableau 1.csv", sep=';'),
        "otex" : pd.read_table("fichiersParPole/fts_ra2020_amikuze/otex-Tableau 1.csv", sep=';'),
        "statut" : pd.read_table("fichiersParPole/fts_ra2020_amikuze/statut-Tableau 1.csv", sep=';'),
        "surfaces" : pd.read_table("fichiersParPole/fts_ra2020_amikuze/surfaces-Tableau 1.csv", sep=';'),
        "valorisation" : pd.read_table("fichiersParPole/fts_ra2020_amikuze/valorisation-Tableau 1.csv", sep=';')
        },
    "Cote Basque Adour" : {
        "age" : pd.read_table("fichiersParPole/fts_ra2020_cote_basque_adour/age-Tableau 1.csv", sep=';'),
        "chiffres_cles" : pd.read_table("fichiersParPole/fts_ra2020_cote_basque_adour/chiffres_cles-Tableau 1.csv", sep=';'),
        "communes" : pd.read_table("fichiersParPole/fts_ra2020_cote_basque_adour/communes-Tableau 1.csv", sep=';'),
        "devenir" : pd.read_table("fichiersParPole/fts_ra2020_cote_basque_adour/devenir-Tableau 1.csv", sep=';'),
        "dim_eco" : pd.read_table("fichiersParPole/fts_ra2020_cote_basque_adour/dim_eco-Tableau 1.csv", sep=';'),
        "effectifs_cheptel" : pd.read_table("fichiersParPole/fts_ra2020_cote_basque_adour/effectifs_cheptel-Tableau 1.csv", sep=';'),
        "evolution_n_exploit_sau" : pd.read_table("fichiersParPole/fts_ra2020_cote_basque_adour/evolution_n_exploit_sau-Tableau 1.csv", sep=';'),
        "main_doeuvre" : pd.read_table("fichiersParPole/fts_ra2020_cote_basque_adour/main_doeuvre-Tableau 1.csv", sep=';'),
        "otex_com" : pd.read_table("fichiersParPole/fts_ra2020_cote_basque_adour/otex_com-Tableau 1.csv", sep=';'),
        "otex" : pd.read_table("fichiersParPole/fts_ra2020_cote_basque_adour/otex-Tableau 1.csv", sep=';'),
        "statut" : pd.read_table("fichiersParPole/fts_ra2020_cote_basque_adour/statut-Tableau 1.csv", sep=';'),
        "surfaces" : pd.read_table("fichiersParPole/fts_ra2020_cote_basque_adour/surfaces-Tableau 1.csv", sep=';'),
        "valorisation" : pd.read_table("fichiersParPole/fts_ra2020_cote_basque_adour/valorisation-Tableau 1.csv", sep=';')
        },
    "Errobi" : {
        "age" : pd.read_table("fichiersParPole/fts_ra2020_errobi/age-Tableau 1.csv", sep=';'),
        "chiffres_cles" : pd.read_table("fichiersParPole/fts_ra2020_errobi/chiffres_cles-Tableau 1.csv", sep=';'),
        "communes" : pd.read_table("fichiersParPole/fts_ra2020_errobi/communes-Tableau 1.csv", sep=';'),
        "devenir" : pd.read_table("fichiersParPole/fts_ra2020_errobi/devenir-Tableau 1.csv", sep=';'),
        "dim_eco" : pd.read_table("fichiersParPole/fts_ra2020_errobi/dim_eco-Tableau 1.csv", sep=';'),
        "effectifs_cheptel" : pd.read_table("fichiersParPole/fts_ra2020_errobi/effectifs_cheptel-Tableau 1.csv", sep=';'),
        "evolution_n_exploit_sau" : pd.read_table("fichiersParPole/fts_ra2020_errobi/evolution_n_exploit_sau-Tableau 1.csv", sep=';'),
        "main_doeuvre" : pd.read_table("fichiersParPole/fts_ra2020_errobi/main_doeuvre-Tableau 1.csv", sep=';'),
        "otex_com" : pd.read_table("fichiersParPole/fts_ra2020_errobi/otex_com-Tableau 1.csv", sep=';'),
        "otex" : pd.read_table("fichiersParPole/fts_ra2020_errobi/otex-Tableau 1.csv", sep=';'),
        "statut" : pd.read_table("fichiersParPole/fts_ra2020_errobi/statut-Tableau 1.csv", sep=';'),
        "surfaces" : pd.read_table("fichiersParPole/fts_ra2020_errobi/surfaces-Tableau 1.csv", sep=';'),
        "valorisation" : pd.read_table("fichiersParPole/fts_ra2020_errobi/valorisation-Tableau 1.csv", sep=';')
        },
    "Garazi Baigorri" : {
        "age" : pd.read_table("fichiersParPole/fts_ra2020_garazi_baigorri/age-Tableau 1.csv", sep=';'),
        "chiffres_cles" : pd.read_table("fichiersParPole/fts_ra2020_garazi_baigorri/chiffres_cles-Tableau 1.csv", sep=';'),
        "communes" : pd.read_table("fichiersParPole/fts_ra2020_garazi_baigorri/communes-Tableau 1.csv", sep=';'),
        "devenir" : pd.read_table("fichiersParPole/fts_ra2020_garazi_baigorri/devenir-Tableau 1.csv", sep=';'),
        "dim_eco" : pd.read_table("fichiersParPole/fts_ra2020_garazi_baigorri/dim_eco-Tableau 1.csv", sep=';'),
        "effectifs_cheptel" : pd.read_table("fichiersParPole/fts_ra2020_garazi_baigorri/effectifs_cheptel-Tableau 1.csv", sep=';'),
        "evolution_n_exploit_sau" : pd.read_table("fichiersParPole/fts_ra2020_garazi_baigorri/evolution_n_exploit_sau-Tableau 1.csv", sep=';'),
        "main_doeuvre" : pd.read_table("fichiersParPole/fts_ra2020_garazi_baigorri/main_doeuvre-Tableau 1.csv", sep=';'),
        "otex_com" : pd.read_table("fichiersParPole/fts_ra2020_garazi_baigorri/otex_com-Tableau 1.csv", sep=';'),
        "otex" : pd.read_table("fichiersParPole/fts_ra2020_garazi_baigorri/otex-Tableau 1.csv", sep=';'),
        "statut" : pd.read_table("fichiersParPole/fts_ra2020_garazi_baigorri/statut-Tableau 1.csv", sep=';'),
        "surfaces" : pd.read_table("fichiersParPole/fts_ra2020_garazi_baigorri/surfaces-Tableau 1.csv", sep=';'),
        "valorisation" : pd.read_table("fichiersParPole/fts_ra2020_garazi_baigorri/valorisation-Tableau 1.csv", sep=';')
        },
    "Iholdi Oztibarre" : {
        "age" : pd.read_table("fichiersParPole/fts_ra2020_iholdi_oztibarre/age-Tableau 1.csv", sep=';'),
        "chiffres_cles" : pd.read_table("fichiersParPole/fts_ra2020_iholdi_oztibarre/chiffres_cles-Tableau 1.csv", sep=';'),
        "communes" : pd.read_table("fichiersParPole/fts_ra2020_iholdi_oztibarre/communes-Tableau 1.csv", sep=';'),
        "devenir" : pd.read_table("fichiersParPole/fts_ra2020_iholdi_oztibarre/devenir-Tableau 1.csv", sep=';'),
        "dim_eco" : pd.read_table("fichiersParPole/fts_ra2020_iholdi_oztibarre/dim_eco-Tableau 1.csv", sep=';'),
        "effectifs_cheptel" : pd.read_table("fichiersParPole/fts_ra2020_iholdi_oztibarre/effectifs_cheptel-Tableau 1.csv", sep=';'),
        "evolution_n_exploit_sau" : pd.read_table("fichiersParPole/fts_ra2020_iholdi_oztibarre/evolution_n_exploit_sau-Tableau 1.csv", sep=';'),
        "main_doeuvre" : pd.read_table("fichiersParPole/fts_ra2020_iholdi_oztibarre/main_doeuvre-Tableau 1.csv", sep=';'),
        "otex_com" : pd.read_table("fichiersParPole/fts_ra2020_iholdi_oztibarre/otex_com-Tableau 1.csv", sep=';'),
        "otex" : pd.read_table("fichiersParPole/fts_ra2020_iholdi_oztibarre/otex-Tableau 1.csv", sep=';'),
        "statut" : pd.read_table("fichiersParPole/fts_ra2020_iholdi_oztibarre/statut-Tableau 1.csv", sep=';'),
        "surfaces" : pd.read_table("fichiersParPole/fts_ra2020_iholdi_oztibarre/surfaces-Tableau 1.csv", sep=';'),
        "valorisation" : pd.read_table("fichiersParPole/fts_ra2020_iholdi_oztibarre/valorisation-Tableau 1.csv", sep=';')
        },
    "Nive Adour" : {
        "age" : pd.read_table("fichiersParPole/fts_ra2020_nive_adour/age-Tableau 1.csv", sep=';'),
        "chiffres_cles" : pd.read_table("fichiersParPole/fts_ra2020_nive_adour/chiffres_cles-Tableau 1.csv", sep=';'),
        "communes" : pd.read_table("fichiersParPole/fts_ra2020_nive_adour/communes-Tableau 1.csv", sep=';'),
        "devenir" : pd.read_table("fichiersParPole/fts_ra2020_nive_adour/devenir-Tableau 1.csv", sep=';'),
        "dim_eco" : pd.read_table("fichiersParPole/fts_ra2020_nive_adour/dim_eco-Tableau 1.csv", sep=';'),
        "effectifs_cheptel" : pd.read_table("fichiersParPole/fts_ra2020_nive_adour/effectifs_cheptel-Tableau 1.csv", sep=';'),
        "evolution_n_exploit_sau" : pd.read_table("fichiersParPole/fts_ra2020_nive_adour/evolution_n_exploit_sau-Tableau 1.csv", sep=';'),
        "main_doeuvre" : pd.read_table("fichiersParPole/fts_ra2020_nive_adour/main_doeuvre-Tableau 1.csv", sep=';'),
        "otex_com" : pd.read_table("fichiersParPole/fts_ra2020_nive_adour/otex_com-Tableau 1.csv", sep=';'),
        "otex" : pd.read_table("fichiersParPole/fts_ra2020_nive_adour/otex-Tableau 1.csv", sep=';'),
        "statut" : pd.read_table("fichiersParPole/fts_ra2020_nive_adour/statut-Tableau 1.csv", sep=';'),
        "surfaces" : pd.read_table("fichiersParPole/fts_ra2020_nive_adour/surfaces-Tableau 1.csv", sep=';'),
        "valorisation" : pd.read_table("fichiersParPole/fts_ra2020_nive_adour/valorisation-Tableau 1.csv", sep=';')
        },
    "Pays de Bidache" : {
        "age" : pd.read_table("fichiersParPole/fts_ra2020_pays_de_bidache/age-Tableau 1.csv", sep=';'),
        "chiffres_cles" : pd.read_table("fichiersParPole/fts_ra2020_pays_de_bidache/chiffres_cles-Tableau 1.csv", sep=';'),
        "communes" : pd.read_table("fichiersParPole/fts_ra2020_pays_de_bidache/communes-Tableau 1.csv", sep=';'),
        "devenir" : pd.read_table("fichiersParPole/fts_ra2020_pays_de_bidache/devenir-Tableau 1.csv", sep=';'),
        "dim_eco" : pd.read_table("fichiersParPole/fts_ra2020_pays_de_bidache/dim_eco-Tableau 1.csv", sep=';'),
        "effectifs_cheptel" : pd.read_table("fichiersParPole/fts_ra2020_pays_de_bidache/effectifs_cheptel-Tableau 1.csv", sep=';'),
        "evolution_n_exploit_sau" : pd.read_table("fichiersParPole/fts_ra2020_pays_de_bidache/evolution_n_exploit_sau-Tableau 1.csv", sep=';'),
        "main_doeuvre" : pd.read_table("fichiersParPole/fts_ra2020_pays_de_bidache/main_doeuvre-Tableau 1.csv", sep=';'),
        "otex_com" : pd.read_table("fichiersParPole/fts_ra2020_pays_de_bidache/otex_com-Tableau 1.csv", sep=';'),
        "otex" : pd.read_table("fichiersParPole/fts_ra2020_pays_de_bidache/otex-Tableau 1.csv", sep=';'),
        "statut" : pd.read_table("fichiersParPole/fts_ra2020_pays_de_bidache/statut-Tableau 1.csv", sep=';'),
        "surfaces" : pd.read_table("fichiersParPole/fts_ra2020_pays_de_bidache/surfaces-Tableau 1.csv", sep=';'),
        "valorisation" : pd.read_table("fichiersParPole/fts_ra2020_pays_de_bidache/valorisation-Tableau 1.csv", sep=';')
        },
    "Pays d'Hasparren" : {
        "age" : pd.read_table("fichiersParPole/fts_ra2020_pays_d_hasparren/age-Tableau 1.csv", sep=';'),
        "chiffres_cles" : pd.read_table("fichiersParPole/fts_ra2020_pays_d_hasparren/chiffres_cles-Tableau 1.csv", sep=';'),
        "communes" : pd.read_table("fichiersParPole/fts_ra2020_pays_d_hasparren/communes-Tableau 1.csv", sep=';'),
        "devenir" : pd.read_table("fichiersParPole/fts_ra2020_pays_d_hasparren/devenir-Tableau 1.csv", sep=';'),
        "dim_eco" : pd.read_table("fichiersParPole/fts_ra2020_pays_d_hasparren/dim_eco-Tableau 1.csv", sep=';'),
        "effectifs_cheptel" : pd.read_table("fichiersParPole/fts_ra2020_pays_d_hasparren/effectifs_cheptel-Tableau 1.csv", sep=';'),
        "evolution_n_exploit_sau" : pd.read_table("fichiersParPole/fts_ra2020_pays_d_hasparren/evolution_n_exploit_sau-Tableau 1.csv", sep=';'),
        "main_doeuvre" : pd.read_table("fichiersParPole/fts_ra2020_pays_d_hasparren/main_doeuvre-Tableau 1.csv", sep=';'),
        "otex_com" : pd.read_table("fichiersParPole/fts_ra2020_pays_d_hasparren/otex_com-Tableau 1.csv", sep=';'),
        "otex" : pd.read_table("fichiersParPole/fts_ra2020_pays_d_hasparren/otex-Tableau 1.csv", sep=';'),
        "statut" : pd.read_table("fichiersParPole/fts_ra2020_pays_d_hasparren/statut-Tableau 1.csv", sep=';'),
        "surfaces" : pd.read_table("fichiersParPole/fts_ra2020_pays_d_hasparren/surfaces-Tableau 1.csv", sep=';'),
        "valorisation" : pd.read_table("fichiersParPole/fts_ra2020_pays_d_hasparren/valorisation-Tableau 1.csv", sep=';')
        },
    "Soule Xiberoa" : {
        "age" : pd.read_table("fichiersParPole/fts_ra2020_soule_xiberoa/age-Tableau 1.csv", sep=';'),
        "chiffres_cles" : pd.read_table("fichiersParPole/fts_ra2020_soule_xiberoa/chiffres_cles-Tableau 1.csv", sep=';'),
        "communes" : pd.read_table("fichiersParPole/fts_ra2020_soule_xiberoa/communes-Tableau 1.csv", sep=';'),
        "devenir" : pd.read_table("fichiersParPole/fts_ra2020_soule_xiberoa/devenir-Tableau 1.csv", sep=';'),
        "dim_eco" : pd.read_table("fichiersParPole/fts_ra2020_soule_xiberoa/dim_eco-Tableau 1.csv", sep=';'),
        "effectifs_cheptel" : pd.read_table("fichiersParPole/fts_ra2020_soule_xiberoa/effectifs_cheptel-Tableau 1.csv", sep=';'),
        "evolution_n_exploit_sau" : pd.read_table("fichiersParPole/fts_ra2020_soule_xiberoa/evolution_n_exploit_sau-Tableau 1.csv", sep=';'),
        "main_doeuvre" : pd.read_table("fichiersParPole/fts_ra2020_soule_xiberoa/main_doeuvre-Tableau 1.csv", sep=';'),
        "otex_com" : pd.read_table("fichiersParPole/fts_ra2020_soule_xiberoa/otex_com-Tableau 1.csv", sep=';'),
        "otex" : pd.read_table("fichiersParPole/fts_ra2020_soule_xiberoa/otex-Tableau 1.csv", sep=';'),
        "statut" : pd.read_table("fichiersParPole/fts_ra2020_soule_xiberoa/statut-Tableau 1.csv", sep=';'),
        "surfaces" : pd.read_table("fichiersParPole/fts_ra2020_soule_xiberoa/surfaces-Tableau 1.csv", sep=';'),
        "valorisation" : pd.read_table("fichiersParPole/fts_ra2020_soule_xiberoa/valorisation-Tableau 1.csv", sep=';')
        },
    "Sud Pays Basque" : {
        "age" : pd.read_table("fichiersParPole/fts_ra2020_sud_pays_basque/age-Tableau 1.csv", sep=';'),
        "chiffres_cles" : pd.read_table("fichiersParPole/fts_ra2020_sud_pays_basque/chiffres_cles-Tableau 1.csv", sep=';'),
        "communes" : pd.read_table("fichiersParPole/fts_ra2020_sud_pays_basque/communes-Tableau 1.csv", sep=';'),
        "devenir" : pd.read_table("fichiersParPole/fts_ra2020_sud_pays_basque/devenir-Tableau 1.csv", sep=';'),
        "dim_eco" : pd.read_table("fichiersParPole/fts_ra2020_sud_pays_basque/dim_eco-Tableau 1.csv", sep=';'),
        "effectifs_cheptel" : pd.read_table("fichiersParPole/fts_ra2020_sud_pays_basque/effectifs_cheptel-Tableau 1.csv", sep=';'),
        "evolution_n_exploit_sau" : pd.read_table("fichiersParPole/fts_ra2020_sud_pays_basque/evolution_n_exploit_sau-Tableau 1.csv", sep=';'),
        "main_doeuvre" : pd.read_table("fichiersParPole/fts_ra2020_sud_pays_basque/main_doeuvre-Tableau 1.csv", sep=';'),
        "otex_com" : pd.read_table("fichiersParPole/fts_ra2020_sud_pays_basque/otex_com-Tableau 1.csv", sep=';'),
        "otex" : pd.read_table("fichiersParPole/fts_ra2020_sud_pays_basque/otex-Tableau 1.csv", sep=';'),
        "statut" : pd.read_table("fichiersParPole/fts_ra2020_sud_pays_basque/statut-Tableau 1.csv", sep=';'),
        "surfaces" : pd.read_table("fichiersParPole/fts_ra2020_sud_pays_basque/surfaces-Tableau 1.csv", sep=';'),
        "valorisation" : pd.read_table("fichiersParPole/fts_ra2020_sud_pays_basque/valorisation-Tableau 1.csv", sep=';')
        }
}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                           Diagrammes                          #
#                               en                              #
#                             barres                            #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#Créer les graphes étudiant les cheptels en 2010

donneesCheptels = pd.read_table("fichier_traite_rga/cheptel-Tableau 1_2.csv", sep=';', index_col=0, na_values=-999)

#Enlever la ligne avec pour index ca_du_pays_basque car c'est le bilan des 10 pôles
donneesCheptels = donneesCheptels.loc[donneesCheptels.index != 'ca_du_pays_basque', :]

#Enlever les valeurs manquantes
donneesCheptels.replace(nan, 0, inplace=True)

#Transposition du dataframe pour les traitements suivants
donneesCheptels = donneesCheptels.T

#Conversion des cheptels en pourcentage sur chaque pole
for i in donneesCheptels:
    somme = donneesCheptels[i].sum()
    for j in range(len(donneesCheptels[i])):
        donneesCheptels[i][j] = donneesCheptels[i][j] / somme

#Réordonner les indexs
index=donneesCheptels.index
nouvelindex=[index[2], index[4], index[6], index[5], index[1], index[0], index[3]]
donneesCheptels = donneesCheptels.reindex(nouvelindex)

#Trier les données des colonnes dans l'ordre
donneesCheptels = donneesCheptels.T
donneesCheptels = donneesCheptels.sort_values(by = 'total bovins', ascending=False)

#Renommer les colonnes pour être plus clair
nouvellesColonnes=['Cheptels bovins', 'Cheptels Ovins', 'Cheptels de Volailles', 'Cheptels Porcins',
                   'Cheptel Equins', 'Apiculture', 'Cheptels Caprins']
donneesCheptels.columns = nouvellesColonnes

#Affichage du graphique et esthétisme des barres/légendes
donneesCheptels.plot(kind="bar",stacked=True)
plt.legend(title="Nombre de Cheptels", bbox_to_anchor = (1.05, 1.0), loc = 'upper left')
plt.xlabel("Pôle étudié")
plt.ylabel("Pourcentage sur le pôle")
plt.title("Répartition des cheptels selon le pôle étudié en 2010")

#Récupérer les indexs et les colonnes pour ajouter les étiquettes des pourcentages sur les barres
index=donneesCheptels.index
colonnes = donneesCheptels.columns 

# # # # # # # # # # # # # # # # # # # # # # # # #
# Etiquettes du « Cheptels bovins »
# # # # # # # # # # # # # # # # # # # # # # # # #

plt.text(0, donneesCheptels.loc[index[0],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[0],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(1, donneesCheptels.loc[index[1],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[1],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(2, donneesCheptels.loc[index[2],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[2],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(3, donneesCheptels.loc[index[3],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[3],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(4, donneesCheptels.loc[index[4],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[4],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(5, donneesCheptels.loc[index[5],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[5],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(6, donneesCheptels.loc[index[6],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[6],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(7, donneesCheptels.loc[index[7],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[7],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(8, donneesCheptels.loc[index[8],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[8],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(9, donneesCheptels.loc[index[9],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[9],colonnes[0]]*100,1))+ '%',
 ha = 'center')

# # # # # # # # # # # # # # # # # # # # # # # # #
# Etiquettes du « Cheptels Ovins »
# # # # # # # # # # # # # # # # # # # # # # # # #

plt.text(0, donneesCheptels.loc[index[0],colonnes[0]] + donneesCheptels.loc[index[0],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[0],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(1, donneesCheptels.loc[index[1],colonnes[0]] + donneesCheptels.loc[index[1],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[1],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(2, donneesCheptels.loc[index[2],colonnes[0]] + donneesCheptels.loc[index[2],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[2],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(3, donneesCheptels.loc[index[3],colonnes[0]] + donneesCheptels.loc[index[3],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[3],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(4, donneesCheptels.loc[index[4],colonnes[0]] + donneesCheptels.loc[index[4],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[4],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(5, donneesCheptels.loc[index[5],colonnes[0]] + donneesCheptels.loc[index[5],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[5],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(6, donneesCheptels.loc[index[6],colonnes[0]] + donneesCheptels.loc[index[6],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[6],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(7, donneesCheptels.loc[index[7],colonnes[0]] + donneesCheptels.loc[index[7],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[7],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(8, donneesCheptels.loc[index[8],colonnes[0]] + donneesCheptels.loc[index[8],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[8],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(9, donneesCheptels.loc[index[9],colonnes[0]] + donneesCheptels.loc[index[9],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[9],colonnes[1]]*100,1))+ '%',
 ha = 'center')

'''
nomFormat = 'svg'
nom = 'barreEmpileesCheptels2010.svg'
plt.savefig(nom, format=nomFormat, bbox_inches="tight")
'''

plt.show()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                           Créer les graphes                   #
#                               étudiant                        #
#                        les cheptels en 2020                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

donneesCheptels = pd.read_table("fichier_traite_rga/cheptel-Tableau 1_3.csv", sep=';', index_col=0, na_values=-999)

donneesCheptels = donneesCheptels.loc[donneesCheptels.index != 'ca_du_pays_basque', :]

donneesCheptels.replace(nan, 0, inplace=True)

#Transposition du dataframe pour les traitements suivants
donneesCheptels = donneesCheptels.T

#Conversion des cheptels en pourcentage sur chaque pole
for i in donneesCheptels:
    somme = donneesCheptels[i].sum()
    for j in range(len(donneesCheptels[i])):
        donneesCheptels[i][j] = donneesCheptels[i][j] / somme

#Réordonner les indexs
index=donneesCheptels.index
nouvelindex=[index[2], index[4], index[6], index[1], index[5], index[0], index[3]]
donneesCheptels = donneesCheptels.reindex(nouvelindex)

#Trier les données des colonnes dans l'ordre
donneesCheptels = donneesCheptels.T
donneesCheptels = donneesCheptels.sort_values(by = 'total bovins', ascending=False)

#Renommer les colonnes pour être plus clair
nouvellesColonnes=['Cheptels bovins', 'Cheptels Ovins', 'Cheptels de Volailles', 'Cheptels Porcins',
                   'Cheptels Equins', 'Apiculture', 'Cheptels Caprins']
donneesCheptels.columns = nouvellesColonnes

donneesCheptels.plot(kind="bar",stacked=True)
plt.legend(title="Nombre de Cheptels", bbox_to_anchor = (1.05, 1.0), loc = 'upper left')
plt.xlabel("Pôle étudié")
plt.ylabel("Pourcentage sur le pôle")
plt.title("Répartition des cheptels selon le pôle étudié en 2020")

index=donneesCheptels.index
colonnes = donneesCheptels.columns 

# # # # # # # # # # # # # # # # # # # # # # # # #
# Etiquettes du « total bovins »
# # # # # # # # # # # # # # # # # # # # # # # # #

plt.text(0, donneesCheptels.loc[index[0],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[0],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(1, donneesCheptels.loc[index[1],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[1],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(2, donneesCheptels.loc[index[2],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[2],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(3, donneesCheptels.loc[index[3],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[3],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(4, donneesCheptels.loc[index[4],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[4],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(5, donneesCheptels.loc[index[5],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[5],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(6, donneesCheptels.loc[index[6],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[6],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(7, donneesCheptels.loc[index[7],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[7],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(8, donneesCheptels.loc[index[8],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[8],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(9, donneesCheptels.loc[index[9],colonnes[0]]/2,
 str(round(donneesCheptels.loc[index[9],colonnes[0]]*100,1))+ '%',
 ha = 'center')

# # # # # # # # # # # # # # # # # # # # # # # # #
# Etiquettes du « Cheptels Ovins »              #
# # # # # # # # # # # # # # # # # # # # # # # # #

plt.text(0, donneesCheptels.loc[index[0],colonnes[0]] + donneesCheptels.loc[index[0],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[0],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(1, donneesCheptels.loc[index[1],colonnes[0]] + donneesCheptels.loc[index[1],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[1],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(2, donneesCheptels.loc[index[2],colonnes[0]] + donneesCheptels.loc[index[2],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[2],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(3, donneesCheptels.loc[index[3],colonnes[0]] + donneesCheptels.loc[index[3],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[3],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(4, donneesCheptels.loc[index[4],colonnes[0]] + donneesCheptels.loc[index[4],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[4],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(5, donneesCheptels.loc[index[5],colonnes[0]] + donneesCheptels.loc[index[5],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[5],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(6, donneesCheptels.loc[index[6],colonnes[0]] + donneesCheptels.loc[index[6],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[6],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(7, donneesCheptels.loc[index[7],colonnes[0]] + donneesCheptels.loc[index[7],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[7],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(8, donneesCheptels.loc[index[8],colonnes[0]] + donneesCheptels.loc[index[8],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[8],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(9, donneesCheptels.loc[index[9],colonnes[0]] + donneesCheptels.loc[index[9],colonnes[1]]/2,
 str(round(donneesCheptels.loc[index[9],colonnes[1]]*100,1))+ '%',
 ha = 'center')

'''
nomFormat = 'svg'
nom = 'barreEmpileesCheptels2020.svg'
plt.savefig(nom, format=nomFormat, bbox_inches="tight")
'''

#Affichage graphique
plt.show()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               Graphes                         #
#                               radar                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

'''

#Boucle pour créer les 10 graphiques à chaque fois
for i in range(len(donneesCheptels)):
    
    #Pour 2010

    #Récupération des données de 2010
    donneesCheptels = pd.read_table("fichier_traite_rga/cheptel-Tableau 1_2.csv", sep=';', index_col=0, na_values=-999)

    #Enlever ca_du_pays_basque
    donneesCheptels = donneesCheptels.loc[donneesCheptels.index != 'ca_du_pays_basque', :]

    #Enlever les valeurs nulles
    donneesCheptels.replace(nan, 0, inplace=True)

    #Conversion des cheptels en pourcentage sur chaque pole
    for x in donneesCheptels:
        somme = donneesCheptels[x].sum()
        for y in range(len(donneesCheptels[x])):
            donneesCheptels[x][y] = donneesCheptels[x][y] / somme

    #Categories représente les totaux pour les cheptels en pourcentage
    categories=list(donneesCheptels.columns)

    #Prend la valeur des cheptels pour le pole visité
    pole1 = list(donneesCheptels.iloc[i, :])

    #Remettre la première valeur à la fin pour fermer le graphique en radar
    pole1.append(pole1[0])

    #Forme du  en radar
    label_loc=np.linspace(start=0,stop=2*np.pi,num=len(pole1))

    #formation de l'échelle
    rad=np.arange(12.)*np.pi/6
    r=np.degrees(rad)

    #Paramètres du graphique radar
    plt.figure(figsize=(8,8))
    plt.subplot(polar=True)

    #Création du graphique avec les paramètres créés précédemment
    plt.plot(label_loc, pole1, label=donneesCheptels.index[i], color='blue')

    #Grilles et axes
    lines, labels = plt.thetagrids(range(0,360,52),labels=categories)

    
    #Pour 2020
    #Récupération des données de 2020
    donneesCheptels = pd.read_table("fichier_traite_rga/cheptel-Tableau 1_3.csv", sep=';', index_col=0, na_values=-999)

    donneesCheptels = donneesCheptels.loc[donneesCheptels.index != 'ca_du_pays_basque', :]

    donneesCheptels.replace(nan, 0, inplace=True)

    #Conversion des cheptels en pourcentage sur chaque pole
    for x in donneesCheptels:
        somme = donneesCheptels[x].sum()
        for y in range(len(donneesCheptels[x])):
            donneesCheptels[x][y] = donneesCheptels[x][y] / somme

    #Categories représente les totaux pour les cheptels en pourcentage
    categories=list(donneesCheptels.columns)

    #Prend la valeur des cheptels pour le pole visité
    pole1 = list(donneesCheptels.iloc[i, :])

    #Remettre la première valeur à la fin pour fermer le graphique en radar
    pole1.append(pole1[0])

    #Forme du  en radar
    label_loc=np.linspace(start=0,stop=2*np.pi,num=len(pole1))

    #Mise en forme du graphique en radar et création
    titre = 'Répartition des cheptels sur le pole de ' + str(donneesCheptels.index[i]) + ' en 2010 et 2020'
    plt.plot(label_loc, pole1, label=donneesCheptels.index[i], color='red')
    plt.title(titre)
    plt.legend(('2020'))

    #exporter le graphique en svg
    titre = titre + ".svg"
    nomFormat = 'svg'
    plt.savefig(titre, format=nomFormat, bbox_inches="tight")

plt.show()
'''

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                 Etudes                        #
#                                au début                       #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #



# I m p o r t a t i o n
chiffresCles = pd.read_table("fichier_traite_rga/nombre_exploitation-Tableau 1.csv", sep=';', index_col=0, na_values=-999, decimal=',')

poles = 'Amikuze'

for poles in chiffresCles.index.unique():
    # Prendre seulement le pole qu'on veut
    chiffresClesPole = chiffresCles.loc[chiffresCles.index == poles, :]

    # Dataframe des années étudiées
    evol_sau_tot = pd.DataFrame(index = [1970, 1979, 1988, 2000, 2010, 2020])
    evol_sau_moy = pd.DataFrame(index = [1970, 1979, 1988, 2000, 2010, 2020])

    # Prendre les années et la sau Totale
    chiffresClesTot = chiffresClesPole.loc[:, ['annee','sau_tot_ha']]

    # Prendre les années et la sau moyenne
    chiffresClesMoy = chiffresClesPole.loc[:, ['annee','sau_moy_ha']]

    # fusionner les deux infos importantes pour le total
    evol_sau_tot=pd.merge(evol_sau_tot, chiffresClesTot, left_index=True, right_on='annee')
    evol_sau_tot.reset_index(drop=True, inplace=True)
    evol_sau_tot.set_index('annee', inplace=True)

    # fusionner les deux infos importantes pour le moy
    evol_sau_moy=pd.merge(evol_sau_moy, chiffresClesMoy, left_index=True, right_on='annee')
    evol_sau_moy.reset_index(drop=True, inplace=True)
    evol_sau_moy.set_index('annee', inplace=True)

    ##############################
    # Représentations graphiques #
    ##############################

    # Sau Totale
    #evol_sau_tot.plot(kind='bar', ylim=(100000, 140000))
    #plt.title('Evolution de la superficie agricole totale sur le pole de ' + poles)

    # Sau moyenne
    '''
    evol_sau_moy.plot(color='r', linewidth=5, use_index=True)
    plt.show()
    '''

    #Calcul du taux de variation SAU moyenne
    listeMoy=[]

    for annee in range(len(evol_sau_moy.index)-1):
        tauxDeVariationMoy = list(evol_sau_moy.loc[evol_sau_moy.index==evol_sau_moy.index[annee+1], 'sau_moy_ha'])[0]-list(evol_sau_moy.loc[evol_sau_moy.index==evol_sau_moy.index[annee], 'sau_moy_ha'])[0]
        tauxDeVariationMoy = tauxDeVariationMoy / list(evol_sau_moy.loc[evol_sau_moy.index==evol_sau_moy.index[annee], 'sau_moy_ha'])[0]
        listeMoy.append(tauxDeVariationMoy)


    #Calcul du taux de variation SAU totale
    listeTot=[]
    for annee in range(len(evol_sau_tot.index)-1):
        tauxDeVariationTot = list(evol_sau_tot.loc[evol_sau_tot.index==evol_sau_tot.index[annee+1], 'sau_tot_ha'])[0]-list(evol_sau_tot.loc[evol_sau_tot.index==evol_sau_tot.index[annee], 'sau_tot_ha'])[0]
        tauxDeVariationTot = tauxDeVariationTot / list(evol_sau_tot.loc[evol_sau_tot.index==evol_sau_tot.index[annee], 'sau_tot_ha'])[0]
        listeTot.append(tauxDeVariationTot)

    plt.plot([1979, 1988, 2000, 2010, 2020], listeMoy, color="r")
    plt.plot([1979, 1988, 2000, 2010, 2020], listeTot, color="b")
    titre = 'Taux de variation de la Sau Totale et de la Sau moyenne sur le pole de ' + str(poles)
    plt.title(titre)
    titre = titre + '.svg'
    nomFormat = 'svg'
    plt.legend(['sau moyenne', 'sau totale'], loc = 1)
    plt.savefig(titre, format=nomFormat, bbox_inches="tight")
    plt.show()

