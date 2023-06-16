import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gp


"""
Cartographie des pôles pays basque ---------------------------------
"""

# Importation du geojson contenant
# les données cartographiques de 
# chaque pôle
filename = "./rga2020_dataviz_challenge.geojson"
file = open(filename)
df = gp.read_file(file)

# Filtrage de ca_du_pays_basque
# qui représente l'ensemble des pôles
dfSansCaPaysBasque = df.loc[df["echelle"] != "ca_du_pays_basque",:]

# Représentation cartographique 
# des pôles 
dfSansCaPaysBasque.plot(column="echelle", cmap="YlGn", legend=True,
     legend_kwds={"loc":"center left", 
     "bbox_to_anchor":(1,.5),
     "fmt":"{:.0f}"})
plt.title('Cartographie des pôles')

"""
Représentation chronologique nb exploitations ----------------------
"""

# Importation des données pour chaque pôle
# et les données sur l'ensemble du pays
# basque, regroupées en un dictionnaire
poles = {
    'Amikuze': pd.read_table("./fichiersParPole/fts_ra2020_amikuze/evolution_n_exploit_sau-Tableau 1.csv", sep=";"),
    'Cote Basque Adour': pd.read_table("./fichiersParPole/fts_ra2020_cote_basque_adour/evolution_n_exploit_sau-Tableau 1.csv", sep=";"),
    'Errobi': pd.read_table("./fichiersParPole/fts_ra2020_errobi/evolution_n_exploit_sau-Tableau 1.csv", sep=";"),
    'Garazi Baigorri': pd.read_table("./fichiersParPole/fts_ra2020_garazi_baigorri/evolution_n_exploit_sau-Tableau 1.csv", sep=";"),
    'Iholdi Oztibarre': pd.read_table("./fichiersParPole/fts_ra2020_iholdi_oztibarre/evolution_n_exploit_sau-Tableau 1.csv", sep=";"),
    'Nive Adour': pd.read_table("./fichiersParPole/fts_ra2020_nive_adour/evolution_n_exploit_sau-Tableau 1.csv", sep=";"),
    'Pays de Bidache': pd.read_table("./fichiersParPole/fts_ra2020_pays_de_bidache/evolution_n_exploit_sau-Tableau 1.csv", sep=";"),
    'Pays d\'Hasparren': pd.read_table("./fichiersParPole/fts_ra2020_pays_d_hasparren/evolution_n_exploit_sau-Tableau 1.csv", sep=";"),
    'Soule Xiberoa': pd.read_table("./fichiersParPole/fts_ra2020_soule_xiberoa/evolution_n_exploit_sau-Tableau 1.csv", sep=";"),
    'Sud Pays Basque': pd.read_table("./fichiersParPole/fts_ra2020_sud_pays_basque/evolution_n_exploit_sau-Tableau 1.csv", sep=";"),
    'Ca du Pays Basque': pd.read_table("./fichiersParPole/fts_ra2020_amikuze/evolution_n_exploit_sau-Tableau 1.csv", sep=";")
}

# Importation des données du 
# Pays Basque
nbExploitPaysBasque = pd.read_table("./fichiersParPole/fts_ra2020_ca_du_pays_basque/evolution_n_exploit_sau-Tableau 1.csv", sep=";")
nbExploitFrance = [1591036,1270085,1088731,763953,603884,496365]

# Initialisation du dataframe
# contenant le nombre d'exploitation
# sur plusieures années par pole
dfToChrono = pd.DataFrame(
    index=['Amikuze','Cote Basque Adour','Errobi',
           'Garazi Baigorri','Iholdi Oztibarre','Nive Adour',
           'Pays de Bidache','Pays d\'Hasparren','Soule Xiberoa',
           'Sud Pays Basque','Ca du Pays Basque'],
    columns=[1970,1979,1988,2000,2010,2020]
)

# Initialisation du dataframe
# contenant le nombre d'exploitation
# sur plusieurs années pour la france
# et le Pays Basque
dfComparaisonFrancePaysBasque = pd.DataFrame(
    index=['Ca du Pays Basque','National'],
    columns=[1970,1979,1988,2000,2010,2020]
)

# Ajout des nombres d'exploitation pour chaque
# année et par pôle
for key in poles:
    for index,row in poles[key].iterrows():
        if key != 'Ca du Pays Basque':
            dfToChrono.loc[key,row[0]] = row[1]

def racineN(x,n):
    return x**(1/float(n))

# Calcul du taux variation
l = []
for i in range(len(dfToChrono)):
    l.append((dfToChrono.iloc[i,5],dfToChrono.iloc[i,0]))
for i in range(len(l)):
    x=float((l[i][0]/l[i][1]))
    l[i]="%.2f"%((racineN(x,5)-1)*100)     

# Ajout des nombres d'exploitation pour chaque
# année et pour la France et le Pays Basque
for index,row in nbExploitPaysBasque.iterrows():
    dfComparaisonFrancePaysBasque.loc['Ca du Pays Basque',row[0]] = row[1]
for i in range(len(nbExploitFrance)):
    dfComparaisonFrancePaysBasque.iloc[1,i] = nbExploitFrance[i]

# Inversion des colonnes et lignes
# pour réaliser le graphique chronologique
dfToPlot = dfToChrono.transpose()
dfToPlot.plot(colormap='YlGn',
              logy=True,
              legend=True)
plt.grid(axis='y', which='both')
plt.legend(bbox_to_anchor=(1,1))
plt.title('Série chronologique évolution nombre d\'exploitation')

# Avec limite logarithmique des ordonnées
dfToPlot.plot(colormap='YlGn',
              logy=True,
              legend=True, ylim=(10,10**4))
plt.grid(axis='y', which='both')
plt.legend(bbox_to_anchor=(1,1))
plt.title('Série chronologique évolution nombre d\'exploitation')

# Création graphique comparaison france 
# et pays basque
dfComparaisonToPlot = dfComparaisonFrancePaysBasque.transpose()
dfComparaisonToPlot.plot(colormap='winter',
              logy=True,
              legend=True)
plt.grid(axis='y', which='both')
plt.rc('axes',axisbelow=True)
plt.legend(bbox_to_anchor=(1,1))
plt.title('Série chronologique évolution nombre d\'exploitation \n au niveau national')


# Ajout du taux variation au dataframe
ls=pd.Series(l)
dfToChrono['variation 1970-2020']=ls.values