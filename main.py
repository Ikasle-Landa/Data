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
df.plot(column="echelle", cmap="YlGn", legend=True,
     legend_kwds={"loc":"center left", 
     "bbox_to_anchor":(1,0.5),
     "fmt":"{:.0f}"})
"""


"""
Représentation chronologique nb exploitations ----------------------
"""
amikuze = pd.read_table("./fichiersParPole/fts_ra2020_amikuze/evolution_n_exploit_sau-Tableau 1.csv", sep=";")
chronoAmikuze = pd.crosstab(amikuze["annee"],amikuze["n_exploit"])
# chronoAmikuze.plot()