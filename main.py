import geopandas as gpd
import pandas as pd
from flask import Flask
from numpy import nan
import contextily as ctx
import geodatasets as gds
import folium
from folium.plugins import StripePattern

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                           Importation                         #
#                               des                             #
#                             données                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

geoDonnees = gpd.read_file("rga2020_dataviz_challenge.geojson")
geoDonneesPole = gpd.read_file("contour_capb_poles_territoriaux.geojson")
"""
donnees = {
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

infosPole = {
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
"""
# Nettoyage des données par suppression de CA du Pays Basque
# geoDonnees = geoDonnees.loc[geoDonnees['echelle'] != 'ca_du_pays_basque', :]
# ax = geoDonnees.plot(column="echelle", cmap="summer", legend=True, legend_kwds={"loc": "center left", "bbox_to_anchor": (1, 0.5), "fmt": "{:.0f}"})
# ctx.add_basemap(ax, crs = geoDonnees.crs)



chiffresCles =  pd.read_table("Data/chiffres_cles_des_poles.csv", sep=';')

ageParPole = chiffresCles.loc[chiffresCles["type"] == "age_moy", :]

geoDonneesAge = geoDonnees.merge(ageParPole, on='echelle')

mainDf = pd.read_table("Data/devenir_exploitation.csv", sep=";",decimal=",")

geoDonneesDevenirExploitation = geoDonnees.merge(mainDf, on="echelle")

geoDonneesMainDf = geoDonneesPole.merge(mainDf, on="echelle")

"""
ax = geoDonneesDevenirExploitation.plot(column="pas de départ du chef ou coexploitant envisagé dans l'immédiat",
                                        cmap="summer", 
                                        legend=True,
                                        legend_kwds={'location':'right','label':'blabla','boundaries':[i for i in range(0,101,10)]})

ax.set_axis_off()
ctx.add_basemap(ax, crs = geoDonneesDevenirExploitation.crs)


ax = geoDonneesAge.plot(column="2010",cmap="summer", legend=True, legend_kwds={"loc": "center left", "bbox_to_anchor": (1, 0.5), "fmt": "{:.0f}"})
ax.set_axis_off()
ctx.add_basemap(ax, crs = geoDonneesAge.crs)

ax = geoDonneesAge.plot(column="2020",cmap="summer", legend=True, legend_kwds={"loc": "center left", "bbox_to_anchor": (1, 0.5), "fmt": "{:.0f}"})
ax.set_axis_off()
ctx.add_basemap(ax, crs = geoDonneesAge.crs)

"""

devenirExploitation = {1:"pas de départ du chef ou coexploitant envisagé dans l'immédiat",
                       2:"disparition des terres au profit d'un usage non agricole",
                       3:"nombre d'exploitations non concernées",
                       4:"reprise par un coexploitant, un membre de la famille ou un tiers",
                       5:"ne sait pas",
                       6:"total d'exploitations concernées",
                       7:"disparition au profit de l'agrandissement d'une ou plusieurs autres exploitations"}


for i in devenirExploitation:
    m = folium.Map(location=[43.3758766,-1.2983944], # center of the folium map
                    tiles="OpenStreetMap",
                    min_zoom=6, max_zoom=15, # zoom range
                    zoom_start=9) # initial zoom


    folium.Choropleth(geo_data=geoDonneesMainDf,
                    data=geoDonneesMainDf,
                    columns=["echelle",devenirExploitation[i]],
                    key_on="feature.properties.echelle",
                    fill_color="YlGn",
                    fill_opacity=0.85,
                    smooth_factor=0,
                    Highlight= True,
                    line_color = "#0000",
                    name = "Données",
                    show=True,
                    overlay=True,).add_to(m)

    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}

    IHM = folium.features.GeoJson(
        data = geoDonneesMainDf,
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=folium.features.GeoJsonTooltip(
            fields=['echelle',devenirExploitation[i]],
            aliases=['echelle',devenirExploitation[i] + ' (en %)'],
            style=("background-color: white; color: #222222; font-family: arial; font-size: 12px; padding: 10px;") 
        )
    )
    m.add_child(IHM)
    m.keep_in_front(IHM)

    # Ajout de de mode de carte 
    folium.TileLayer('cartodbdark_matter',name="dark mode",control=True).add_to(m)
    folium.TileLayer("Stamen Terrain",name="relief",control=True).add_to(m)

    # Ajout d'une interface de contrôle
    folium.LayerControl(collapsed=False).add_to(m)


    filename = 'carte' + str(i) + '.html'
    m.save(filename)
