import geopandas as gpd

geoDonnées = gpd.read_file("rga2020_dataviz_challenge.geojson")
données = {'age' : gpd.read_file("fichier_traite_rga/age-Tableau 1.csv"), 
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