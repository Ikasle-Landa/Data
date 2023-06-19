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
#                            Traitements                        #
#                               des                             #
#                             données                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #



# Nettoyage des données par suppression de CA du Pays Basque
geoDonnées = geoDonnées.loc[geoDonnées['echelle'] != 'ca_du_pays_basque', :]

'''
#Affichage de la carte
ax=geoDonnées.plot(column="echelle",
        legend = True,
        legend_kwds={"loc": "center left", "bbox_to_anchor": (1, 0.5), "fmt": "{:.0f}"})
ax.set_axis_off()

#Affichage avec fond de carte
ax = geoDonnées.plot(column="echelle",
        legend = True,
        legend_kwds={"loc": "center left", "bbox_to_anchor": (1, 0.5), "fmt": "{:.0f}"})
ax.set_axis_off()
cx.add_basemap(ax, crs=geoDonnées.crs)
'''

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                             Création                          #
#                               de                              #
#                            Dataframe                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#Création dataframe vide
donneesCheptels=pd.DataFrame(index=["Amikuze", "Cote Basque Adour", "Errobi",
                                        "Garazi Baigorri", "Iholdi Oztibarre", "Nive Adour",
                                        "Pays de Bidache", "Pays d'Hasparren", "Soule Xiberoa",
                                        "Sud Pays Basque"
                                        ])

'''AAAAAAAAAH

#Importer csv des cheptels
dataCheptels = pd.read_table("fichier_traite_rga/cheptel-Tableau 1.csv", sep=';')

#Remplir le dataframe des cheptels - leur nombre et nettoyage au passage
donneesCheptels = dataCheptels.loc[:, ['echelle', 'type', 'valeur', 'annee']]
donneesCheptels = donneesCheptels.loc[donneesCheptels['echelle']!= 'ca_du_pays_basque', :]
donneesCheptels = donneesCheptels.loc[donneesCheptels['annee'] == 2010, :]

#Dataframe pour les cheptels en 2010
donnees2010 = dataCheptels.loc[:, ['echelle', 'annee']]
donnees2010 = donnees2010.loc[donnees2010['echelle']!= 'ca_du_pays_basque', :]
donnees2010 = donnees2010.loc[donnees2010['annee'] == 2010, :]
donnees2010 = donnees2010.drop(columns=['annee'])

#Dataframe de l'Evolution des cheptels

donneesEvolutionCheptels = dataCheptels.loc[: , ['echelle', 'type', 'évolution']]

#Tentative de créer un graphique cool

typeCheptels = np.array(['apiculture (nombre de ruches)', 'total Ã©quins', 'total bovins',
       'total caprins', 'total ensemble du cheptel', 'total ovins',
       'total porcins', 'total volailles'])

for i in typeCheptels :
    donnees2010[i] = nan

for i in range(len(donnees2010)):
    for j in range(1, len(donnees2010.columns)):
        donnees2010.iloc[i, j] = donneesCheptels.loc[donneesCheptels.columns[j], 'valeur']
'''

testCheptels = pd.read_table("fichier_traite_rga/cheptel-Tableau 1_2.csv", sep=';', index_col=0, na_values=-999)

testCheptels = testCheptels.loc[testCheptels.index != 'ca_du_pays_basque', :]

testCheptels.replace(nan, 0, inplace=True)

testCheptels = testCheptels.T

for i in testCheptels:
    somme = testCheptels[i].sum()
    for j in range(len(testCheptels[i])):
        testCheptels[i][j] = testCheptels[i][j] / somme

testCheptels.T.plot(kind="bar",stacked=True)
plt.show()




'''##########################
#   Etude du nombre d'exploitations
##########################

#Sortir le ca du pays Basque de l'équation
geoDonnées = geoDonnées.loc[geoDonnées['echelle'] != 'ca_du_pays_basque', :]

#Importer les chiffres-clés
chiffresCles =  pd.read_table("./fichier_traite_rga/chiffres_cles_des_poles.csv", sep=';')

exploitationsParPoles = chiffresCles.loc[chiffresCles["nom"] == "nombre total d'exploitations", :]

geoDonneesExplois = geoDonnées.merge(exploitationsParPoles, on='echelle')

#Carte pour 2010
ax = geoDonneesExplois.plot(column="Part 2010", cmap="summer", legend=True, legend_kwds={"loc": "center left", "bbox_to_anchor": (1, 0.5), "fmt": "{:.0f}"})
ax.set_axis_off()
cx.add_basemap(ax, crs = geoDonneesExplois.crs)

#Carte pour 2020
ax = geoDonneesExplois.plot(column="Part 2020", cmap="summer", legend=True, legend_kwds={"loc": "center left", "bbox_to_anchor": (1, 0.5), "fmt": "{:.0f}"})
ax.set_axis_off()
cx.add_basemap(ax, crs = geoDonneesExplois.crs)'''


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                             Tests                             #
#                               de                              #
#                           Conversions                         #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

##############
#   Tests de Conversions Dataframe to geojson
##############

'''
#Importer le dataframe
response = requests.get("https://zabal-agriculture.opendata-paysbasque.fr/api/explore/v2.1/catalog/datasets/rga2020_dataviz_challenge/exports/json?lang=fr&timezone=Europe%2FBerlin")
testJSON = response.json()

#Conversion en Dataframe
df = pd.DataFrame(testJSON)'''

####         ####         #### 

'''
#Conversion GeoDataframe to GeoJson
geoDonneesJSON = geoDonnées.to_json()
with open('dataframeJSON.geojson' , 'w') as file:
    file.write(geoDonnées.to_json())
'''