import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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
    'Ca du Pays Basque': pd.read_table("./fichiersParPole/fts_ra2020_ca_du_pays_basque/evolution_n_exploit_sau-Tableau 1.csv", sep=";")
}

otexPoles = {
    'Amikuze': pd.read_table("./fichiersParPole/fts_ra2020_amikuze/otex-Tableau 1.csv", sep=";"),
    'Cote Basque Adour': pd.read_table("./fichiersParPole/fts_ra2020_cote_basque_adour/otex-Tableau 1.csv", sep=";"),
    'Errobi': pd.read_table("./fichiersParPole/fts_ra2020_errobi/otex-Tableau 1.csv", sep=";"),
    'Garazi Baigorri': pd.read_table("./fichiersParPole/fts_ra2020_garazi_baigorri/otex-Tableau 1.csv", sep=";"),
    'Iholdi Oztibarre': pd.read_table("./fichiersParPole/fts_ra2020_iholdi_oztibarre/otex-Tableau 1.csv", sep=";"),
    'Nive Adour': pd.read_table("./fichiersParPole/fts_ra2020_nive_adour/otex-Tableau 1.csv", sep=";"),
    'Pays de Bidache': pd.read_table("./fichiersParPole/fts_ra2020_pays_de_bidache/otex-Tableau 1.csv", sep=";"),
    'Pays d\'Hasparren': pd.read_table("./fichiersParPole/fts_ra2020_pays_d_hasparren/otex-Tableau 1.csv", sep=";"),
    'Soule Xiberoa': pd.read_table("./fichiersParPole/fts_ra2020_soule_xiberoa/otex-Tableau 1.csv", sep=";"),
    'Sud Pays Basque': pd.read_table("./fichiersParPole/fts_ra2020_sud_pays_basque/otex-Tableau 1.csv", sep=";"),
    'Ca du Pays Basque': pd.read_table("./fichiersParPole/fts_ra2020_ca_du_pays_basque/otex-Tableau 1.csv", sep=";")
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
           'Sud Pays Basque','Ca du Pays Basque','France'],
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
        dfToChrono.loc[key,row[0]] = row[1]

for i in range(len(nbExploitFrance)):
    dfToChrono.iloc[11,i] = nbExploitFrance[i]

def racineN(x,n):
    return x**(1/float(n))

# Calcul du taux variation
varSur50ans = []
varSur1an = []
varEntre2010et2020 = []
for i in range(len(dfToChrono)):
    varSur50ans.append((dfToChrono.iloc[i,5],dfToChrono.iloc[i,0]))
    varEntre2010et2020.append((dfToChrono.iloc[i,5],dfToChrono.iloc[i,4]))
for i in range(len(varSur50ans)):
    x=float(varSur50ans[i][0]/varSur50ans[i][1])
    e=float((varSur50ans[i][0]-varSur50ans[i][1])/varSur50ans[i][1])
    d=float((varEntre2010et2020[i][0]-varEntre2010et2020[i][1])/varEntre2010et2020[i][1])
    varSur50ans[i]="%.2f"%((racineN(x,50)-1)*100) 
    varSur1an.append("%.2f"%e)
    varEntre2010et2020[i]="%.2f"%d    

# Ajout des nombres d'exploitation pour chaque
# année et pour la France et le Pays Basque
for index,row in nbExploitPaysBasque.iterrows():
    dfComparaisonFrancePaysBasque.loc['Ca du Pays Basque',row[0]] = row[1]
for i in range(len(nbExploitFrance)):
    dfComparaisonFrancePaysBasque.iloc[1,i] = nbExploitFrance[i]

# Inversion des colonnes et lignes
# pour réaliser le graphique chronologique
dfToPlot = dfToChrono.iloc[0:9,:].transpose()
dfToPlot.plot(colormap='YlGn',
              logy=True,
              legend=True)
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
ls=pd.Series(varSur50ans)
dfToChrono['variation_1970-2020']=ls.values
ls=pd.Series(varSur1an)
dfToChrono['variation_sur_1_an']=ls.values
ls=pd.Series(varEntre2010et2020)
dfToChrono['variation_entre_2010_2020']=ls.values



# plt.style.use('ggplot')
# taux1an = []
# ensemblePole = []
# for index,row in dfToChrono.iterrows():
#     if index != 'Ca du Pays Basque' and index != 'France':
#         taux1an.append(float(row['variation_sur_1_an']))
#         ensemblePole.append(index)


categories=['taux evolution nb exploit','taux evolution superficie',
            'pourcentage 1','pourcentage 2','pourcentage 3']
pole1 = [2,5,2,4,8,2]
label_loc=np.linspace(start=0,stop=2*np.pi,num=len(pole1))

rad=np.arange(12.)*np.pi/6
r=np.degrees(rad)
plt.figure(figsize=(8,8))
plt.subplot(polar=True)
plt.plot(label_loc,pole1,label=dfToChrono.index[0])
plt.title('toto')
lines, labels = plt.thetagrids(range(0,360,72),labels=categories)
plt.legend()
plt.show()





"""
Bubble plots --------------------------------------------------------
"""

datf=dfToChrono.iloc[0:10,:]
l=pd.Series(datf.index)
datf['pole'] = l.values
datf.reset_index(drop=True,inplace=True)

ls=list(datf[1970])
pole=list(datf['pole'])
ann=list(datf[2010])
color=["lightblue","lightgray","yellow","orange","red",
       "green","purple","pink","blue","brown"]
colTest=np.arange(10)

plt.scatter(pole,ann,s=ls,c=colTest,cmap="YlGn")
plt.ylabel("Nombre exploitation en 2010")
plt.grid(which='both')
plt.colorbar()
plt.xticks(rotation=45,ha="right")
plt.show()


"""
Bubble plot ca_du_pays_basque -------------------------------------
"""

datf=dfToChrono.iloc[0:10,:]
l=pd.Series(datf.index)
datf['pole'] = l.values
datf.reset_index(drop=True,inplace=True)

ls=[200,500,800,1100,200,500,800,1100]
pole=[1500,2108,771,76,1263,1628,1796,90]
ann=[14782.49,66239.88,38904.91,4470.63,14951.55,55015.5,44160.89,5424.04]
color=["#2CA9FF","#2CA9FF","#2CA9FF","#2CA9FF",
       "#FF4252","#FF4252","#FF4252","#FF4252"]
colTest=np.arange(10)

plt.scatter(pole,ann,s=ls,c=color)
plt.xlabel("Nombre exploitation")
plt.ylabel("Surface exploitation")
plt.grid(which='both')
plt.show()












# dataFrm=dfToChrono.iloc[0:10,:]
# total=sum(dataFrm[2010])
# proportions=[(float(val)/total) for val in dataFrm[2010]]
# width=40
# height=10
# total=width*height
# tilesPer=[round(prop*total) for prop in proportions]



# l=list(dataFrm.index)
# de=list(dataFrm[2010])
# sz=dataFrm[2010].max()
# b_normal=dataFrm[2010]/dataFrm[2010].max()

# for index,row in dataFrm.iterrows():
#     for i in range(len(row)):
#         row[i] = float(row[i])


# ds=list(b_normal)

# plt.figure(figsize=(12,8))
# plt.scatter(l,de,
#             color='darkblue',alpha=0.5,s=b_normal*2000)







"""
Représentation évolution Otex --------------------------------------------------------
"""
col = []
for key in otexPoles:
    for index,row in otexPoles[key].iterrows():
        if row[0] == 2010:
            col.append(row[2])