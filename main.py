import geopandas as gpd
import pandas as pd, requests, json
import numpy as np
from flask import Flask
from numpy import nan
import contextily as cx
import matplotlib.pyplot as plt
import mapclassify

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
#                             Création                          #
#                               de                              #
#                     Dataframe Pour Cheptels                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#Créer les graphes étudiant les cheptels en 2010

testCheptels = pd.read_table("fichier_traite_rga/cheptel-Tableau 1_2.csv", sep=';', index_col=0, na_values=-999)

testCheptels = testCheptels.loc[testCheptels.index != 'ca_du_pays_basque', :]

testCheptels.replace(nan, 0, inplace=True)

#Transposition du dataframe pour les traitements suivants
testCheptels = testCheptels.T

#Conversion des cheptels en pourcentage sur chaque pole
for i in testCheptels:
    somme = testCheptels[i].sum()
    for j in range(len(testCheptels[i])):
        testCheptels[i][j] = testCheptels[i][j] / somme

#Réordonner les indexs
index=testCheptels.index
nouvelindex=[index[2], index[4], index[6], index[5], index[1], index[0], index[3]]
testCheptels = testCheptels.reindex(nouvelindex)

#Trier les données des colonnes dans l'ordre
testCheptels = testCheptels.T
testCheptels = testCheptels.sort_values(by = 'total bovins', ascending=False)

#Renommer les colonnes pour être plus clair
nouvellesColonnes=['Cheptels bovins', 'Cheptels Ovins', 'Cheptels de Volailles', 'Cheptels Porcins',
                   'Cheptel Equins', 'Apiculture', 'Cheptels Caprins']
testCheptels.columns = nouvellesColonnes

testCheptels.plot(kind="bar",stacked=True)
plt.legend(title="Nombre de Cheptels", bbox_to_anchor = (1.05, 1.0), loc = 'upper left')
plt.xlabel("Pôle étudié")
plt.ylabel("Pourcentage sur le pôle")
plt.title("Répartition des cheptels selon le pôle étudié en 2010")

index=testCheptels.index
colonnes = testCheptels.columns 

####################################
# Etiquettes du « Cheptels bovins »
####################################

plt.text(0, testCheptels.loc[index[0],colonnes[0]]/2,
 str(round(testCheptels.loc[index[0],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(1, testCheptels.loc[index[1],colonnes[0]]/2,
 str(round(testCheptels.loc[index[1],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(2, testCheptels.loc[index[2],colonnes[0]]/2,
 str(round(testCheptels.loc[index[2],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(3, testCheptels.loc[index[3],colonnes[0]]/2,
 str(round(testCheptels.loc[index[3],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(4, testCheptels.loc[index[4],colonnes[0]]/2,
 str(round(testCheptels.loc[index[4],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(5, testCheptels.loc[index[5],colonnes[0]]/2,
 str(round(testCheptels.loc[index[5],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(6, testCheptels.loc[index[6],colonnes[0]]/2,
 str(round(testCheptels.loc[index[6],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(7, testCheptels.loc[index[7],colonnes[0]]/2,
 str(round(testCheptels.loc[index[7],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(8, testCheptels.loc[index[8],colonnes[0]]/2,
 str(round(testCheptels.loc[index[8],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(9, testCheptels.loc[index[9],colonnes[0]]/2,
 str(round(testCheptels.loc[index[9],colonnes[0]]*100,1))+ '%',
 ha = 'center')

####################################
# Etiquettes du « Cheptels Ovins »
####################################

plt.text(0, testCheptels.loc[index[0],colonnes[0]] + testCheptels.loc[index[0],colonnes[1]]/2,
 str(round(testCheptels.loc[index[0],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(1, testCheptels.loc[index[1],colonnes[0]] + testCheptels.loc[index[1],colonnes[1]]/2,
 str(round(testCheptels.loc[index[1],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(2, testCheptels.loc[index[2],colonnes[0]] + testCheptels.loc[index[2],colonnes[1]]/2,
 str(round(testCheptels.loc[index[2],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(3, testCheptels.loc[index[3],colonnes[0]] + testCheptels.loc[index[3],colonnes[1]]/2,
 str(round(testCheptels.loc[index[3],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(4, testCheptels.loc[index[4],colonnes[0]] + testCheptels.loc[index[4],colonnes[1]]/2,
 str(round(testCheptels.loc[index[4],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(5, testCheptels.loc[index[5],colonnes[0]] + testCheptels.loc[index[5],colonnes[1]]/2,
 str(round(testCheptels.loc[index[5],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(6, testCheptels.loc[index[6],colonnes[0]] + testCheptels.loc[index[6],colonnes[1]]/2,
 str(round(testCheptels.loc[index[6],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(7, testCheptels.loc[index[7],colonnes[0]] + testCheptels.loc[index[7],colonnes[1]]/2,
 str(round(testCheptels.loc[index[7],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(8, testCheptels.loc[index[8],colonnes[0]] + testCheptels.loc[index[8],colonnes[1]]/2,
 str(round(testCheptels.loc[index[8],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(9, testCheptels.loc[index[9],colonnes[0]] + testCheptels.loc[index[9],colonnes[1]]/2,
 str(round(testCheptels.loc[index[9],colonnes[1]]*100,1))+ '%',
 ha = 'center')

plt.show()

################################################
#Créer les graphes étudiant les cheptels en 2020
################################################

testCheptels = pd.read_table("fichier_traite_rga/cheptel-Tableau 1_3.csv", sep=';', index_col=0, na_values=-999)

testCheptels = testCheptels.loc[testCheptels.index != 'ca_du_pays_basque', :]

testCheptels.replace(nan, 0, inplace=True)

#Transposition du dataframe pour les traitements suivants
testCheptels = testCheptels.T

#Conversion des cheptels en pourcentage sur chaque pole
for i in testCheptels:
    somme = testCheptels[i].sum()
    for j in range(len(testCheptels[i])):
        testCheptels[i][j] = testCheptels[i][j] / somme

#Réordonner les indexs
index=testCheptels.index
nouvelindex=[index[2], index[4], index[6], index[5], index[1], index[0], index[3]]
testCheptels = testCheptels.reindex(nouvelindex)

#Trier les données des colonnes dans l'ordre
testCheptels = testCheptels.T
testCheptels = testCheptels.sort_values(by = 'total bovins', ascending=False)

#Renommer les colonnes pour être plus clair
nouvellesColonnes=['Cheptels bovins', 'Cheptels Ovins', 'Cheptels de Volailles', 'Cheptels Porcins',
                   'Cheptel Equins', 'Apiculture', 'Cheptels Caprins']
testCheptels.columns = nouvellesColonnes

testCheptels.plot(kind="bar",stacked=True)
plt.legend(title="Nombre de Cheptels", bbox_to_anchor = (1.05, 1.0), loc = 'upper left')
plt.xlabel("Pôle étudié")
plt.ylabel("Pourcentage sur le pôle")
plt.title("Répartition des cheptels selon le pôle étudié en 2020")

index=testCheptels.index
colonnes = testCheptels.columns 

####################################
# Etiquettes du « total bovins »
####################################

plt.text(0, testCheptels.loc[index[0],colonnes[0]]/2,
 str(round(testCheptels.loc[index[0],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(1, testCheptels.loc[index[1],colonnes[0]]/2,
 str(round(testCheptels.loc[index[1],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(2, testCheptels.loc[index[2],colonnes[0]]/2,
 str(round(testCheptels.loc[index[2],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(3, testCheptels.loc[index[3],colonnes[0]]/2,
 str(round(testCheptels.loc[index[3],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(4, testCheptels.loc[index[4],colonnes[0]]/2,
 str(round(testCheptels.loc[index[4],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(5, testCheptels.loc[index[5],colonnes[0]]/2,
 str(round(testCheptels.loc[index[5],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(6, testCheptels.loc[index[6],colonnes[0]]/2,
 str(round(testCheptels.loc[index[6],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(7, testCheptels.loc[index[7],colonnes[0]]/2,
 str(round(testCheptels.loc[index[7],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(8, testCheptels.loc[index[8],colonnes[0]]/2,
 str(round(testCheptels.loc[index[8],colonnes[0]]*100,1))+ '%',
 ha = 'center')
plt.text(9, testCheptels.loc[index[9],colonnes[0]]/2,
 str(round(testCheptels.loc[index[9],colonnes[0]]*100,1))+ '%',
 ha = 'center')

####################################
# Etiquettes du « Cheptels Ovins »
####################################

plt.text(0, testCheptels.loc[index[0],colonnes[0]] + testCheptels.loc[index[0],colonnes[1]]/2,
 str(round(testCheptels.loc[index[0],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(1, testCheptels.loc[index[1],colonnes[0]] + testCheptels.loc[index[1],colonnes[1]]/2,
 str(round(testCheptels.loc[index[1],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(2, testCheptels.loc[index[2],colonnes[0]] + testCheptels.loc[index[2],colonnes[1]]/2,
 str(round(testCheptels.loc[index[2],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(3, testCheptels.loc[index[3],colonnes[0]] + testCheptels.loc[index[3],colonnes[1]]/2,
 str(round(testCheptels.loc[index[3],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(4, testCheptels.loc[index[4],colonnes[0]] + testCheptels.loc[index[4],colonnes[1]]/2,
 str(round(testCheptels.loc[index[4],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(5, testCheptels.loc[index[5],colonnes[0]] + testCheptels.loc[index[5],colonnes[1]]/2,
 str(round(testCheptels.loc[index[5],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(6, testCheptels.loc[index[6],colonnes[0]] + testCheptels.loc[index[6],colonnes[1]]/2,
 str(round(testCheptels.loc[index[6],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(7, testCheptels.loc[index[7],colonnes[0]] + testCheptels.loc[index[7],colonnes[1]]/2,
 str(round(testCheptels.loc[index[7],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(8, testCheptels.loc[index[8],colonnes[0]] + testCheptels.loc[index[8],colonnes[1]]/2,
 str(round(testCheptels.loc[index[8],colonnes[1]]*100,1))+ '%',
 ha = 'center')
plt.text(9, testCheptels.loc[index[9],colonnes[0]] + testCheptels.loc[index[9],colonnes[1]]/2,
 str(round(testCheptels.loc[index[9],colonnes[1]]*100,1))+ '%',
 ha = 'center')

plt.show()