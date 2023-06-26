import geopandas as gpd
import pandas as pd, requests, json
import numpy as np
from flask import Flask
from numpy import nan
import contextily as cx
import matplotlib.pyplot as plt
import matplotlib.markers as mrk
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

donneesCheptels = pd.read_table("fichier_traite_rga/cheptel-Tableau 1_2.csv", sep=';', index_col=0, na_values=-999)

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
nouvelindex=[index[2], index[4], index[6], index[5], index[1], index[0], index[3]]
donneesCheptels = donneesCheptels.reindex(nouvelindex)

#Trier les données des colonnes dans l'ordre
donneesCheptels = donneesCheptels.T
donneesCheptels = donneesCheptels.sort_values(by = 'total bovins', ascending=False)

#Renommer les colonnes pour être plus clair
nouvellesColonnes=['Cheptels bovins', 'Cheptels Ovins', 'Cheptels de Volailles', 'Cheptels Porcins',
                   'Cheptel Equins', 'Apiculture', 'Cheptels Caprins']
donneesCheptels.columns = nouvellesColonnes

donneesCheptels.plot(kind="bar",stacked=True)
plt.legend(title="Nombre de Cheptels", bbox_to_anchor = (1.05, 1.0), loc = 'upper left')
plt.xlabel("Pôle étudié")
plt.ylabel("Pourcentage sur le pôle")
plt.title("Répartition des cheptels selon le pôle étudié en 2010")

index=donneesCheptels.index
colonnes = donneesCheptels.columns 

####################################
# Etiquettes du « Cheptels bovins »
####################################

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

####################################
# Etiquettes du « Cheptels Ovins »
####################################

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

nomFormat = 'svg'
nom = 'barreEmpileesCheptels2010.svg'
plt.savefig(nom, format=nomFormat, bbox_inches="tight")

plt.show()

################################################
#Créer les graphes étudiant les cheptels en 2020
################################################

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

####################################
# Etiquettes du « total bovins »
####################################

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

####################################
# Etiquettes du « Cheptels Ovins »
####################################

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

nomFormat = 'svg'
nom = 'barreEmpileesCheptels2020.svg'
plt.savefig(nom, format=nomFormat, bbox_inches="tight")

#Affichage graphique
plt.show()

################################################
#Créer graphe radar pour tester
################################################

for i in range(len(donneesCheptels)):
    #Pour 2010
    donneesCheptels = pd.read_table("fichier_traite_rga/cheptel-Tableau 1_2.csv", sep=';', index_col=0, na_values=-999)

    donneesCheptels = donneesCheptels.loc[donneesCheptels.index != 'ca_du_pays_basque', :]

    donneesCheptels.replace(nan, 0, inplace=True)

    #Conversion des cheptels en pourcentage sur chaque pole
    for x in donneesCheptels:
        somme = donneesCheptels[x].sum()
        for y in range(len(donneesCheptels[x])):
            donneesCheptels[x][y] = donneesCheptels[x][y] / somme

    categories=list(donneesCheptels.columns)
    pole1 = list(donneesCheptels.iloc[i, :])
    pole1.append(pole1[0])
    label_loc=np.linspace(start=0,stop=2*np.pi,num=len(pole1))

    rad=np.arange(12.)*np.pi/6
    r=np.degrees(rad)
    plt.figure(figsize=(8,8))
    plt.subplot(polar=True)
    plt.plot(label_loc, pole1, label=donneesCheptels.index[i], color='blue')
    lines, labels = plt.thetagrids(range(0,360,52),labels=categories)

    #Pour 2020
    donneesCheptels = pd.read_table("fichier_traite_rga/cheptel-Tableau 1_3.csv", sep=';', index_col=0, na_values=-999)

    donneesCheptels = donneesCheptels.loc[donneesCheptels.index != 'ca_du_pays_basque', :]

    donneesCheptels.replace(nan, 0, inplace=True)

    #Conversion des cheptels en pourcentage sur chaque pole
    for x in donneesCheptels:
        somme = donneesCheptels[x].sum()
        for y in range(len(donneesCheptels[x])):
            donneesCheptels[x][y] = donneesCheptels[x][y] / somme

    categories=list(donneesCheptels.columns)
    pole1 = list(donneesCheptels.iloc[i, :])
    pole1.append(pole1[0])
    label_loc=np.linspace(start=0,stop=2*np.pi,num=len(pole1))

    titre = 'Répartition des cheptels sur le pole de ' + str(donneesCheptels.index[i]) + ' en 2010 et 2020'
    plt.plot(label_loc, pole1, label=donneesCheptels.index[i], color='red')
    plt.title(titre)
    plt.legend(('2020', '2010'))
    plt.show()

    titre = titre + ".svg"
    nomFormat = 'svg'
    nom = 'barreEmpileesCheptels2010.svg'
    plt.savefig(titre, format=nomFormat, bbox_inches="tight")

#################################
"""
Bubble plot ca_du_pays_basque -------------------------------------
"""
#################################
'''

ls=[200,200,200,200,200,200,200,200]
pole=[1500,2108,771,76,1263,1628,1796,90]
ann=[14782.49,66239.88,38904.91,4470.63,14951.55,55015.5,44160.89,5424.04]
color=["#A93F3F","#3F4AA9","#3FA945","#813FA9",
    "#A93F3F","#3F4AA9","#3FA945","#813FA9"]
colTest=np.arange(10)

#2010
for n in range(len(pole)//2) :
    a = plt.scatter(pole[n],ann[n],s=ls[n],c=color[n], alpha=0.5)

#2020
for n in range(len(pole)//2, len(pole)) :
    b = plt.scatter(pole[n],ann[n],s=ls[n],c=color[n], alpha=0.6)


plt.xlabel("Nombre exploitation")
plt.ylabel("Surface exploitation")
plt.legend((a, b), ('2010', '2020'), title="Année concernée", bbox_to_anchor = (1.05, 1.0), loc = 'upper left')
plt.grid(which='both')
plt.show()

'''
#################################
#               Test            #
#           Diagramme type      #
#               radar           #
#################################

'''

# Libraries
from math import pi

# number of variable
categories=list(donneesCheptels.T)[1:]
N = len(categories)

# We are going to plot the first line of the data frame.
# But we need to repeat the first value to close the circular graph:
values=donneesCheptels.T.loc[0].drop('Étiquettes de lignes').values.flatten().tolist()
values += values[:1]
values

# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Initialise the spider plot
ax = plt.subplot(111, polar=True)

# Draw one axe per variable + add labels
plt.xticks(angles[:-1], categories, color='grey', size=8)

# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([10,20,30], ["10","20","30"], color="grey", size=7)
plt.ylim(0,40)

# Plot data
ax.plot(angles, values, linewidth=1, linestyle='solid')

# Fill area
ax.fill(angles, values, 'b', alpha=0.1)

# Show the graph
plt.show() 

'''