import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gp


"""
Cartographie des pôles pays basque ---------------------------------
"""
filename = "./rga2020_dataviz_challenge.geojson"
file = open(filename)
df = gp.read_file(file)
dfSansCaPaysBasque = df.loc[df["echelle"] != "ca_du_pays_basque",:]
"""
dfSansCaPaysBasque.plot(column="echelle", cmap="YlGn", legend=True,
     legend_kwds={"loc":"center left", 
     "bbox_to_anchor":(1,0.5),
     "fmt":"{:.0f}"})
"""


"""
Représentation chronologique nb exploitations ----------------------
"""
poles = {
    'amikuze': pd.read_table("./fichiersParPole/fts_ra2020_amikuze/evolution_n_exploit_sau-Tableau 1.csv", sep=";"),
    'coteBasqueAdour': pd.read_table("./fichiersParPole/fts_ra2020_cote_basque_adour/evolution_n_exploit_sau-Tableau 1.csv", sep=";"),
    'errobi': pd.read_table("./fichiersParPole/fts_ra2020_errobi/evolution_n_exploit_sau-Tableau 1.csv", sep=";"),
    'garaziBaigorri': pd.read_table("./fichiersParPole/fts_ra2020_garazi_baigorri/evolution_n_exploit_sau-Tableau 1.csv", sep=";"),
    'iholdiOztibarre': pd.read_table("./fichiersParPole/fts_ra2020_iholdi_oztibarre/evolution_n_exploit_sau-Tableau 1.csv", sep=";"),
    'niveAdour': pd.read_table("./fichiersParPole/fts_ra2020_nive_adour/evolution_n_exploit_sau-Tableau 1.csv", sep=";"),
    'paysBidache': pd.read_table("./fichiersParPole/fts_ra2020_pays_de_bidache/evolution_n_exploit_sau-Tableau 1.csv", sep=";"),
    'paysHasparren': pd.read_table("./fichiersParPole/fts_ra2020_pays_d_hasparren/evolution_n_exploit_sau-Tableau 1.csv", sep=";"),
    'souleXiberoa': pd.read_table("./fichiersParPole/fts_ra2020_soule_xiberoa/evolution_n_exploit_sau-Tableau 1.csv", sep=";"),
    'sudPaysBasque': pd.read_table("./fichiersParPole/fts_ra2020_sud_pays_basque/evolution_n_exploit_sau-Tableau 1.csv", sep=";")
}

dfToChrono = pd.DataFrame(
    index=['Amikuze','Cote Basque Adour',
           'Errobi','Garazi Baigorri',
           'Iholdi Oztibarre','Nive Adour',
           'Pays de Bidache','Pays d\'Hasparren',
           'Soule Xiberoa','Sud Pays Basque'],
     columns=[1970,1979,1988,2000,2010,2020]
)

for index,row in poles['amikuze'].iterrows():
          dfToChrono.iloc[0,index] = row[1]
for index,row in poles['coteBasqueAdour'].iterrows():
          dfToChrono.iloc[1,index] = row[1]
for index,row in poles['errobi'].iterrows():
          dfToChrono.iloc[2,index] = row[1]
for index,row in poles['garaziBaigorri'].iterrows():
          dfToChrono.iloc[3,index] = row[1]
for index,row in poles['iholdiOztibarre'].iterrows():
          dfToChrono.iloc[4,index] = row[1]
for index,row in poles['niveAdour'].iterrows():
          dfToChrono.iloc[5,index] = row[1]
for index,row in poles['paysBidache'].iterrows():
          dfToChrono.iloc[6,index] = row[1]
for index,row in poles['paysHasparren'].iterrows():
          dfToChrono.iloc[7,index] = row[1]
for index,row in poles['souleXiberoa'].iterrows():
          dfToChrono.iloc[8,index] = row[1]
for index,row in poles['sudPaysBasque'].iterrows():
          dfToChrono.iloc[9,index] = row[1]

dfToPlot = dfToChrono.transpose()

colors = ['#0000e5','#f8fcbe','#e0f3a8','#bce395',
          '#90d083','#5fba6c','#379e54','#1a7d40',
          '#006435','#004529']

index = 0
for lab,content in dfToPlot.items():
    plt.plot(content, label=lab, color=colors[index])
    index = index + 1
plt.legend(title='Pôles', bbox_to_anchor=(1,1))
plt.show()
