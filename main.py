import geopandas as gpd
from flask import Flask
from numpy import nan

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                           Importation                         #
#                               des                             #
#                             données                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

geoDonnées = gpd.read_file("rga2020_dataviz_challenge.geojson")
données = {
    'age' : gpd.read_file("fichier_traite_rga/age-Tableau 1.csv"), 
    'ageMoyen' : gpd.read_file("fichier_traite_rga/age_moyen_par_pole.csv"),
    'cheptel' : gpd.read_file("fichier_traite_rga/cheptel-Tableau 1.csv"),
    'devenir' : gpd.read_file("fichier_traite_rga/devenir_exploitation-Tableau 1.csv"),
    'evolution' : gpd.read_file("fichier_traite_rga/evolution-Tableau 1.csv"),
    'donnéesGenerales' : gpd.read_file("fichier_traite_rga/Feuil1-Tableau 1.csv"),
    'mainOeuvre' : gpd.read_file("fichier_traite_rga/main_d_oeuvre-Tableau 1.csv"),
    'nombreExp' : gpd.read_file("fichier_traite_rga/nombre_exploitation-Tableau 1.csv"),
    'otexCommune' : gpd.read_file("fichier_traite_rga/otex_commune-Tableau 1.csv"),
    'otex' : gpd.read_file("/Users/feror/DataViz/fichier_traite_rga/otex-Tableau 1.csv"),
    'statutExp' : gpd.read_file("fichier_traite_rga/statut_exploitation-Tableau 1.csv"),
    'tailleExp' : gpd.read_file("fichier_traite_rga/taille_exploitation-Tableau 1.csv"),
    'valorisation' : gpd.read_file("fichier_traite_rga/valorisation-Tableau 1.csv")
}

infosPôle = {
    "Amikuze" : {
        "age" : gpd.read_file("fichiersParPole/fts_ra2020_amikuze/age-Tableau 1.csv"),
        "chiffres_cles" : gpd.read_file("fichiersParPole/fts_ra2020_amikuze/chiffres_cles-Tableau 1.csv"),
        "communes" : gpd.read_file("fichiersParPole/fts_ra2020_amikuze/communes-Tableau 1.csv"),
        "devenir" : gpd.read_file("fichiersParPole/fts_ra2020_amikuze/devenir-Tableau 1.csv"),
        "dim_eco" : gpd.read_file("fichiersParPole/fts_ra2020_amikuze/dim_eco-Tableau 1.csv"),
        "effectifs_cheptel" : gpd.read_file("fichiersParPole/fts_ra2020_amikuze/effectifs_cheptel-Tableau 1.csv"),
        "evolution_n_exploit_sau" : gpd.read_file("fichiersParPole/fts_ra2020_amikuze/evolution_n_exploit_sau-Tableau 1.csv"),
        "main_doeuvre" : gpd.read_file("fichiersParPole/fts_ra2020_amikuze/main_doeuvre-Tableau 1.csv"),
        "otex_com" : gpd.read_file("fichiersParPole/fts_ra2020_amikuze/otex_com-Tableau 1.csv"),
        "otex" : gpd.read_file("fichiersParPole/fts_ra2020_amikuze/otex-Tableau 1.csv"),
        "statut" : gpd.read_file("fichiersParPole/fts_ra2020_amikuze/statut-Tableau 1.csv"),
        "surfaces" : gpd.read_file("fichiersParPole/fts_ra2020_amikuze/surfaces-Tableau 1.csv"),
        "valorisation" : gpd.read_file("fichiersParPole/fts_ra2020_amikuze/valorisation-Tableau 1.csv")
        },
    "Cote Basque Adour" : {
        "age" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/age-Tableau 1.csv"),
        "chiffres_cles" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/chiffres_cles-Tableau 1.csv"),
        "communes" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/communes-Tableau 1.csv"),
        "devenir" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/devenir-Tableau 1.csv"),
        "dim_eco" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/dim_eco-Tableau 1.csv"),
        "effectifs_cheptel" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/effectifs_cheptel-Tableau 1.csv"),
        "evolution_n_exploit_sau" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/evolution_n_exploit_sau-Tableau 1.csv"),
        "main_doeuvre" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/main_doeuvre-Tableau 1.csv"),
        "otex_com" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/otex_com-Tableau 1.csv"),
        "otex" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/otex-Tableau 1.csv"),
        "statut" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/statut-Tableau 1.csv"),
        "surfaces" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/surfaces-Tableau 1.csv"),
        "valorisation" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/valorisation-Tableau 1.csv")
        },
    "Erobi" : {
        "age" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/age-Tableau 1.csv"),
        "chiffres_cles" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/chiffres_cles-Tableau 1.csv"),
        "communes" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/communes-Tableau 1.csv"),
        "devenir" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/devenir-Tableau 1.csv"),
        "dim_eco" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/dim_eco-Tableau 1.csv"),
        "effectifs_cheptel" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/effectifs_cheptel-Tableau 1.csv"),
        "evolution_n_exploit_sau" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/evolution_n_exploit_sau-Tableau 1.csv"),
        "main_doeuvre" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/main_doeuvre-Tableau 1.csv"),
        "otex_com" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/otex_com-Tableau 1.csv"),
        "otex" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/otex-Tableau 1.csv"),
        "statut" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/statut-Tableau 1.csv"),
        "surfaces" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/surfaces-Tableau 1.csv"),
        "valorisation" : gpd.read_file("fichiersParPole/fts_ra2020_ca_du_pays_basque/valorisation-Tableau 1.csv")
        },
    "Garazi Baigorri" : {},
    "Iholdi Oztibarre" : {},
    "Nive Adour" : {},
    "Pays de Bidache" : {},
    "Pays d'Hasparren" : {},
    "Soule Xiberoa" : {},
    "Sud Pays Basque" : {}
}

# Nettoyage des données par suppression de CA du Pays Basque
geoDonnées = geoDonnées.loc[geoDonnées['echelle'] != 'CA du Pays Basque', :]

# Suppression dans ageMoyen des valeurs à 0
données['ageMoyen'] = données['ageMoyen'].loc[données['ageMoyen']['moyenne_age'] != '0', :]

#Séparation des données de ageMoyen en deux dataframes, selon l'année
données['ageMoyen2010'] = données['ageMoyen'].loc[données['ageMoyen']['annee'] == '2010', :]
données['ageMoyen2020'] = données['ageMoyen'].loc[données['ageMoyen']['annee'] == '2020', :]
données['ageMoyen2010'] = données['ageMoyen2010'].set_index('echelle')
données['ageMoyen2020'] = données['ageMoyen2020'].set_index('echelle')

geoDonnées['ageMoyen2010'] = [int(0) for i in range(len(geoDonnées))]
for index, row in geoDonnées.iterrows():
    if row['echelle'] in données['ageMoyen2010'].index:
        geoDonnées.at[index, 'ageMoyen2010'] = int(données['ageMoyen2010'].loc[row['echelle'], 'moyenne_age'])
    else:
        geoDonnées.at[index, 'ageMoyen2010'] = nan
        
geoDonnées['ageMoyen2020'] = [int(0) for i in range(len(geoDonnées))]
for index, row in geoDonnées.iterrows():
    if row['echelle'] in données['ageMoyen2020'].index:
        geoDonnées.at[index, 'ageMoyen2020'] = int(données['ageMoyen2020'].loc[row['echelle'], 'moyenne_age'])
    else:
        geoDonnées.at[index, 'ageMoyen2020'] = nan
        
geoDonnées['ageMoyen2010'] = geoDonnées['ageMoyen2010'].astype(str)
geoDonnées['ageMoyen2020'] = geoDonnées['ageMoyen2020'].astype(str)

geoDonnées.plot(column='ageMoyen2010', legend=True, cmap='Wistia')
geoDonnées.plot(column='ageMoyen2020', legend=True, cmap='Wistia')