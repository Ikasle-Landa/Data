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

# Nettoyage des données par suppression de CA du Pays Basque
geoDonnées = geoDonnées.loc[geoDonnées['echelle'] != 'CA du Pays Basque', :]

# Suppression dans ageMoyen des valeurs à 0
données['ageMoyen'] = données['ageMoyen'].loc[données['ageMoyen']['moyenne_age'] != '0', :]

#Séparation des données de ageMoyen en deux dataframes, selon l'année
données['ageMoyen2010'] = données['ageMoyen'].loc[données['ageMoyen']['annee'] == '2010', :]
données['ageMoyen2020'] = données['ageMoyen'].loc[données['ageMoyen']['annee'] == '2020', :]
données['ageMoyen2010'] = données['ageMoyen2010'].set_index('echelle')
données['ageMoyen2020'] = données['ageMoyen2020'].set_index('echelle')

geoDonnées['ageMoyen2020'] = [int(0) for i in range(len(geoDonnées))]
for index, row in geoDonnées.iterrows():
    print(row['echelle'])
    if row['echelle'] in données['ageMoyen2020'].index:
        geoDonnées.at[index, 'ageMoyen2020'] = int(données['ageMoyen2020'].loc[row['echelle'], 'moyenne_age'])
    else:
        geoDonnées.at[index, 'ageMoyen2020'] = nan
        
geoDonnées.plot(column='ageMoyen2020', legend=True)

'Iholdi Otztibarre'
'Iholdi Oztibarre'