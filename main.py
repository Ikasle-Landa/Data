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
        "age" : gpd.read_file("fichiersParPole/fts_ra2020_cote_basque_adour/age-Tableau 1.csv"),
        "chiffres_cles" : gpd.read_file("fichiersParPole/fts_ra2020_cote_basque_adour/chiffres_cles-Tableau 1.csv"),
        "communes" : gpd.read_file("fichiersParPole/fts_ra2020_cote_basque_adour/communes-Tableau 1.csv"),
        "devenir" : gpd.read_file("fichiersParPole/fts_ra2020_cote_basque_adour/devenir-Tableau 1.csv"),
        "dim_eco" : gpd.read_file("fichiersParPole/fts_ra2020_cote_basque_adour/dim_eco-Tableau 1.csv"),
        "effectifs_cheptel" : gpd.read_file("fichiersParPole/fts_ra2020_cote_basque_adour/effectifs_cheptel-Tableau 1.csv"),
        "evolution_n_exploit_sau" : gpd.read_file("fichiersParPole/fts_ra2020_cote_basque_adour/evolution_n_exploit_sau-Tableau 1.csv"),
        "main_doeuvre" : gpd.read_file("fichiersParPole/fts_ra2020_cote_basque_adour/main_doeuvre-Tableau 1.csv"),
        "otex_com" : gpd.read_file("fichiersParPole/fts_ra2020_cote_basque_adour/otex_com-Tableau 1.csv"),
        "otex" : gpd.read_file("fichiersParPole/fts_ra2020_cote_basque_adour/otex-Tableau 1.csv"),
        "statut" : gpd.read_file("fichiersParPole/fts_ra2020_cote_basque_adour/statut-Tableau 1.csv"),
        "surfaces" : gpd.read_file("fichiersParPole/fts_ra2020_cote_basque_adour/surfaces-Tableau 1.csv"),
        "valorisation" : gpd.read_file("fichiersParPole/fts_ra2020_cote_basque_adour/valorisation-Tableau 1.csv")
        },
    "Erobi" : {
        "age" : gpd.read_file("fichiersParPole/fts_ra2020_errobi/age-Tableau 1.csv"),
        "chiffres_cles" : gpd.read_file("fichiersParPole/fts_ra2020_errobi/chiffres_cles-Tableau 1.csv"),
        "communes" : gpd.read_file("fichiersParPole/fts_ra2020_errobi/communes-Tableau 1.csv"),
        "devenir" : gpd.read_file("fichiersParPole/fts_ra2020_errobi/devenir-Tableau 1.csv"),
        "dim_eco" : gpd.read_file("fichiersParPole/fts_ra2020_errobi/dim_eco-Tableau 1.csv"),
        "effectifs_cheptel" : gpd.read_file("fichiersParPole/fts_ra2020_errobi/effectifs_cheptel-Tableau 1.csv"),
        "evolution_n_exploit_sau" : gpd.read_file("fichiersParPole/fts_ra2020_errobi/evolution_n_exploit_sau-Tableau 1.csv"),
        "main_doeuvre" : gpd.read_file("fichiersParPole/fts_ra2020_errobi/main_doeuvre-Tableau 1.csv"),
        "otex_com" : gpd.read_file("fichiersParPole/fts_ra2020_errobi/otex_com-Tableau 1.csv"),
        "otex" : gpd.read_file("fichiersParPole/fts_ra2020_errobi/otex-Tableau 1.csv"),
        "statut" : gpd.read_file("fichiersParPole/fts_ra2020_errobi/statut-Tableau 1.csv"),
        "surfaces" : gpd.read_file("fichiersParPole/fts_ra2020_errobi/surfaces-Tableau 1.csv"),
        "valorisation" : gpd.read_file("fichiersParPole/fts_ra2020_errobi/valorisation-Tableau 1.csv")
        },
    "Garazi Baigorri" : {
        "age" : gpd.read_file("fichiersParPole/fts_ra2020_garazi_baigorri/age-Tableau 1.csv"),
        "chiffres_cles" : gpd.read_file("fichiersParPole/fts_ra2020_garazi_baigorri/chiffres_cles-Tableau 1.csv"),
        "communes" : gpd.read_file("fichiersParPole/fts_ra2020_garazi_baigorri/communes-Tableau 1.csv"),
        "devenir" : gpd.read_file("fichiersParPole/fts_ra2020_garazi_baigorri/devenir-Tableau 1.csv"),
        "dim_eco" : gpd.read_file("fichiersParPole/fts_ra2020_garazi_baigorri/dim_eco-Tableau 1.csv"),
        "effectifs_cheptel" : gpd.read_file("fichiersParPole/fts_ra2020_garazi_baigorri/effectifs_cheptel-Tableau 1.csv"),
        "evolution_n_exploit_sau" : gpd.read_file("fichiersParPole/fts_ra2020_garazi_baigorri/evolution_n_exploit_sau-Tableau 1.csv"),
        "main_doeuvre" : gpd.read_file("fichiersParPole/fts_ra2020_garazi_baigorri/main_doeuvre-Tableau 1.csv"),
        "otex_com" : gpd.read_file("fichiersParPole/fts_ra2020_garazi_baigorri/otex_com-Tableau 1.csv"),
        "otex" : gpd.read_file("fichiersParPole/fts_ra2020_garazi_baigorri/otex-Tableau 1.csv"),
        "statut" : gpd.read_file("fichiersParPole/fts_ra2020_garazi_baigorri/statut-Tableau 1.csv"),
        "surfaces" : gpd.read_file("fichiersParPole/fts_ra2020_garazi_baigorri/surfaces-Tableau 1.csv"),
        "valorisation" : gpd.read_file("fichiersParPole/fts_ra2020_garazi_baigorri/valorisation-Tableau 1.csv")
        },
    "Iholdi Oztibarre" : {
        "age" : gpd.read_file("fichiersParPole/fts_ra2020_iholdi_oztibarre/age-Tableau 1.csv"),
        "chiffres_cles" : gpd.read_file("fichiersParPole/fts_ra2020_iholdi_oztibarre/chiffres_cles-Tableau 1.csv"),
        "communes" : gpd.read_file("fichiersParPole/fts_ra2020_iholdi_oztibarre/communes-Tableau 1.csv"),
        "devenir" : gpd.read_file("fichiersParPole/fts_ra2020_iholdi_oztibarre/devenir-Tableau 1.csv"),
        "dim_eco" : gpd.read_file("fichiersParPole/fts_ra2020_iholdi_oztibarre/dim_eco-Tableau 1.csv"),
        "effectifs_cheptel" : gpd.read_file("fichiersParPole/fts_ra2020_iholdi_oztibarre/effectifs_cheptel-Tableau 1.csv"),
        "evolution_n_exploit_sau" : gpd.read_file("fichiersParPole/fts_ra2020_iholdi_oztibarre/evolution_n_exploit_sau-Tableau 1.csv"),
        "main_doeuvre" : gpd.read_file("fichiersParPole/fts_ra2020_iholdi_oztibarre/main_doeuvre-Tableau 1.csv"),
        "otex_com" : gpd.read_file("fichiersParPole/fts_ra2020_iholdi_oztibarre/otex_com-Tableau 1.csv"),
        "otex" : gpd.read_file("fichiersParPole/fts_ra2020_iholdi_oztibarre/otex-Tableau 1.csv"),
        "statut" : gpd.read_file("fichiersParPole/fts_ra2020_iholdi_oztibarre/statut-Tableau 1.csv"),
        "surfaces" : gpd.read_file("fichiersParPole/fts_ra2020_iholdi_oztibarre/surfaces-Tableau 1.csv"),
        "valorisation" : gpd.read_file("fichiersParPole/fts_ra2020_iholdi_oztibarre/valorisation-Tableau 1.csv")
        },
    "Nive Adour" : {
        "age" : gpd.read_file("fichiersParPole/fts_ra2020_nive_adour/age-Tableau 1.csv"),
        "chiffres_cles" : gpd.read_file("fichiersParPole/fts_ra2020_nive_adour/chiffres_cles-Tableau 1.csv"),
        "communes" : gpd.read_file("fichiersParPole/fts_ra2020_nive_adour/communes-Tableau 1.csv"),
        "devenir" : gpd.read_file("fichiersParPole/fts_ra2020_nive_adour/devenir-Tableau 1.csv"),
        "dim_eco" : gpd.read_file("fichiersParPole/fts_ra2020_nive_adour/dim_eco-Tableau 1.csv"),
        "effectifs_cheptel" : gpd.read_file("fichiersParPole/fts_ra2020_nive_adour/effectifs_cheptel-Tableau 1.csv"),
        "evolution_n_exploit_sau" : gpd.read_file("fichiersParPole/fts_ra2020_nive_adour/evolution_n_exploit_sau-Tableau 1.csv"),
        "main_doeuvre" : gpd.read_file("fichiersParPole/fts_ra2020_nive_adour/main_doeuvre-Tableau 1.csv"),
        "otex_com" : gpd.read_file("fichiersParPole/fts_ra2020_nive_adour/otex_com-Tableau 1.csv"),
        "otex" : gpd.read_file("fichiersParPole/fts_ra2020_nive_adour/otex-Tableau 1.csv"),
        "statut" : gpd.read_file("fichiersParPole/fts_ra2020_nive_adour/statut-Tableau 1.csv"),
        "surfaces" : gpd.read_file("fichiersParPole/fts_ra2020_nive_adour/surfaces-Tableau 1.csv"),
        "valorisation" : gpd.read_file("fichiersParPole/fts_ra2020_nive_adour/valorisation-Tableau 1.csv")
        },
    "Pays de Bidache" : {
        "age" : gpd.read_file("fichiersParPole/fts_ra2020_pays_de_bidache/age-Tableau 1.csv"),
        "chiffres_cles" : gpd.read_file("fichiersParPole/fts_ra2020_pays_de_bidache/chiffres_cles-Tableau 1.csv"),
        "communes" : gpd.read_file("fichiersParPole/fts_ra2020_pays_de_bidache/communes-Tableau 1.csv"),
        "devenir" : gpd.read_file("fichiersParPole/fts_ra2020_pays_de_bidache/devenir-Tableau 1.csv"),
        "dim_eco" : gpd.read_file("fichiersParPole/fts_ra2020_pays_de_bidache/dim_eco-Tableau 1.csv"),
        "effectifs_cheptel" : gpd.read_file("fichiersParPole/fts_ra2020_pays_de_bidache/effectifs_cheptel-Tableau 1.csv"),
        "evolution_n_exploit_sau" : gpd.read_file("fichiersParPole/fts_ra2020_pays_de_bidache/evolution_n_exploit_sau-Tableau 1.csv"),
        "main_doeuvre" : gpd.read_file("fichiersParPole/fts_ra2020_pays_de_bidache/main_doeuvre-Tableau 1.csv"),
        "otex_com" : gpd.read_file("fichiersParPole/fts_ra2020_pays_de_bidache/otex_com-Tableau 1.csv"),
        "otex" : gpd.read_file("fichiersParPole/fts_ra2020_pays_de_bidache/otex-Tableau 1.csv"),
        "statut" : gpd.read_file("fichiersParPole/fts_ra2020_pays_de_bidache/statut-Tableau 1.csv"),
        "surfaces" : gpd.read_file("fichiersParPole/fts_ra2020_pays_de_bidache/surfaces-Tableau 1.csv"),
        "valorisation" : gpd.read_file("fichiersParPole/fts_ra2020_pays_de_bidache/valorisation-Tableau 1.csv")
        },
    "Pays d'Hasparren" : {
        "age" : gpd.read_file("fichiersParPole/fts_ra2020_pays_d_hasparren/age-Tableau 1.csv"),
        "chiffres_cles" : gpd.read_file("fichiersParPole/fts_ra2020_pays_d_hasparren/chiffres_cles-Tableau 1.csv"),
        "communes" : gpd.read_file("fichiersParPole/fts_ra2020_pays_d_hasparren/communes-Tableau 1.csv"),
        "devenir" : gpd.read_file("fichiersParPole/fts_ra2020_pays_d_hasparren/devenir-Tableau 1.csv"),
        "dim_eco" : gpd.read_file("fichiersParPole/fts_ra2020_pays_d_hasparren/dim_eco-Tableau 1.csv"),
        "effectifs_cheptel" : gpd.read_file("fichiersParPole/fts_ra2020_pays_d_hasparren/effectifs_cheptel-Tableau 1.csv"),
        "evolution_n_exploit_sau" : gpd.read_file("fichiersParPole/fts_ra2020_pays_d_hasparren/evolution_n_exploit_sau-Tableau 1.csv"),
        "main_doeuvre" : gpd.read_file("fichiersParPole/fts_ra2020_pays_d_hasparren/main_doeuvre-Tableau 1.csv"),
        "otex_com" : gpd.read_file("fichiersParPole/fts_ra2020_pays_d_hasparren/otex_com-Tableau 1.csv"),
        "otex" : gpd.read_file("fichiersParPole/fts_ra2020_pays_d_hasparren/otex-Tableau 1.csv"),
        "statut" : gpd.read_file("fichiersParPole/fts_ra2020_pays_d_hasparren/statut-Tableau 1.csv"),
        "surfaces" : gpd.read_file("fichiersParPole/fts_ra2020_pays_d_hasparren/surfaces-Tableau 1.csv"),
        "valorisation" : gpd.read_file("fichiersParPole/fts_ra2020_pays_d_hasparren/valorisation-Tableau 1.csv")
        },
    "Soule Xiberoa" : {
        "age" : gpd.read_file("fichiersParPole/fts_ra2020_soule_xiberoa/age-Tableau 1.csv"),
        "chiffres_cles" : gpd.read_file("fichiersParPole/fts_ra2020_soule_xiberoa/chiffres_cles-Tableau 1.csv"),
        "communes" : gpd.read_file("fichiersParPole/fts_ra2020_soule_xiberoa/communes-Tableau 1.csv"),
        "devenir" : gpd.read_file("fichiersParPole/fts_ra2020_soule_xiberoa/devenir-Tableau 1.csv"),
        "dim_eco" : gpd.read_file("fichiersParPole/fts_ra2020_soule_xiberoa/dim_eco-Tableau 1.csv"),
        "effectifs_cheptel" : gpd.read_file("fichiersParPole/fts_ra2020_soule_xiberoa/effectifs_cheptel-Tableau 1.csv"),
        "evolution_n_exploit_sau" : gpd.read_file("fichiersParPole/fts_ra2020_soule_xiberoa/evolution_n_exploit_sau-Tableau 1.csv"),
        "main_doeuvre" : gpd.read_file("fichiersParPole/fts_ra2020_soule_xiberoa/main_doeuvre-Tableau 1.csv"),
        "otex_com" : gpd.read_file("fichiersParPole/fts_ra2020_soule_xiberoa/otex_com-Tableau 1.csv"),
        "otex" : gpd.read_file("fichiersParPole/fts_ra2020_soule_xiberoa/otex-Tableau 1.csv"),
        "statut" : gpd.read_file("fichiersParPole/fts_ra2020_soule_xiberoa/statut-Tableau 1.csv"),
        "surfaces" : gpd.read_file("fichiersParPole/fts_ra2020_soule_xiberoa/surfaces-Tableau 1.csv"),
        "valorisation" : gpd.read_file("fichiersParPole/fts_ra2020_soule_xiberoa/valorisation-Tableau 1.csv")
        },
    "Sud Pays Basque" : {
        "age" : gpd.read_file("fichiersParPole/fts_ra2020_sud_pays_basque/age-Tableau 1.csv"),
        "chiffres_cles" : gpd.read_file("fichiersParPole/fts_ra2020_sud_pays_basque/chiffres_cles-Tableau 1.csv"),
        "communes" : gpd.read_file("fichiersParPole/fts_ra2020_sud_pays_basque/communes-Tableau 1.csv"),
        "devenir" : gpd.read_file("fichiersParPole/fts_ra2020_sud_pays_basque/devenir-Tableau 1.csv"),
        "dim_eco" : gpd.read_file("fichiersParPole/fts_ra2020_sud_pays_basque/dim_eco-Tableau 1.csv"),
        "effectifs_cheptel" : gpd.read_file("fichiersParPole/fts_ra2020_sud_pays_basque/effectifs_cheptel-Tableau 1.csv"),
        "evolution_n_exploit_sau" : gpd.read_file("fichiersParPole/fts_ra2020_sud_pays_basque/evolution_n_exploit_sau-Tableau 1.csv"),
        "main_doeuvre" : gpd.read_file("fichiersParPole/fts_ra2020_sud_pays_basque/main_doeuvre-Tableau 1.csv"),
        "otex_com" : gpd.read_file("fichiersParPole/fts_ra2020_sud_pays_basque/otex_com-Tableau 1.csv"),
        "otex" : gpd.read_file("fichiersParPole/fts_ra2020_sud_pays_basque/otex-Tableau 1.csv"),
        "statut" : gpd.read_file("fichiersParPole/fts_ra2020_sud_pays_basque/statut-Tableau 1.csv"),
        "surfaces" : gpd.read_file("fichiersParPole/fts_ra2020_sud_pays_basque/surfaces-Tableau 1.csv"),
        "valorisation" : gpd.read_file("fichiersParPole/fts_ra2020_sud_pays_basque/valorisation-Tableau 1.csv")
        }
}

# Nettoyage des données par suppression de CA du Pays Basque
geoDonnées = geoDonnées.loc[geoDonnées['echelle'] != 'CA du Pays Basque', :]