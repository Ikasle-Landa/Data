import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.markers as mrk
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



""" 
Graphique en radar --------------------------------------------------------------------------
"""
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
Bubble plot ca_du_pays_basque --------------------------------------------------------
"""

# A utiliser pour le bubble plutot que les données en durs
# datf=dfToChrono.iloc[0:10,:]
# l=pd.Series(datf.index)
# datf['pole'] = l.values
# datf.reset_index(drop=True,inplace=True)


# Nb exploit 2010 - 2020 par taille exploit
# micro2010=list([172,25,262,184,79,71,197,79,212,219,1500,np.nan])
# micro2020=list([160,16,186,179,75,59,188,83,163,154,1263,np.nan])
# petite2010=list([292,16,121,535,194,27,268,92,428,135,2108,np.nan])
# petite2020=list([229,8,97,410,161,19,199,7,308,120,1628,np.nan])
# moyenne2010=list([158,7,33,150,107,12,101,65,103,35,771,np.nan])
# moyenne2020=list([144,3,36,170,112,13,108,52,121,37,796,np.nan])
# grande2010=list([20,np.nan,np.nan,6,6,3,10,20,3,5,76,np.nan])
# grande2020=list([19,np.nan,5,11,8,np.nan,13,19,9,np.nan,90,np.nan])

# # Sau des poles 2010 - 2020 par taille exploit
# sauMicro2010=list([1745.31,178.31,1833.05,2306.02,1232.73,618.42,1955.05,873.79,2374.2,1665.61,,np.nan])
# sauMicro2020=list([2215.84,135.65,1508.2,2205.38,924.2,516.76,2355.55,1308.2,2232.41,1549.36,np.nan])
# sauPetite2010=list([10228.44,77.76,3467.48,14573.88,6372.97,65.123,8774.94,3637.94,14956.01,3475.23,np.nan])
# sauPetite2020=list([8816.89,79.9,2783.3,11751.33,6034.5,556.78,6761.42,3044.76,11903.29,3283.33,np.nan])
# sauMoyenne2010=list([9044.44,139.72,1533.21,6191.65,5434.83,474.28,5015.61,3631.07,61033.83,1306.27,np.nan])
# sauMoyenne2020=list([8989.93,8.59,1694.27,7729.47,6125.36,526.51,5779.08,3522.89,8275.95,1508.84,np.nan])
# sauGrande2010=list([1057.5,np.nan,np.nan,173.69,337.06,91,561.21,1422.3,272.45,410.85,np.nan])
# sauGrande2020=list([1312.8,np.nan,345.52,428.86,357.69,np.nan,759.55,1305.16,691.06,np.nan,np.nan])

# dfToChrono['nb_exploit_micro_2010']=micro2010
# dfToChrono['nb_exploit_petite_2010']=petite2010
# dfToChrono['nb_exploit_moyenne_2010']=moyenne2010
# dfToChrono['nb_exploit_grande_2010']=grande2010

# dfToChrono['nb_exploit_micro_2020']=micro2020
# dfToChrono['nb_exploit_petite_2020']=petite2020
# dfToChrono['nb_exploit_moyenne_2020']=moyenne2020
# dfToChrono['nb_exploit_grande_2020']=grande2020

# dfToChrono['sau_micro_2010']=sauMicro2010
# dfToChrono['sau_petite_2010']=sauPetite2010
# dfToChrono['sau_moyenne_2010']=sauMoyenne2010
# dfToChrono['sau_grande_2010']=sauGrande2010

# dfToChrono['sau_micro_2020']=sauMicro2020
# dfToChrono['sau_petite_2020']=sauPetite2020
# dfToChrono['sau_moyenne_2020']=sauMoyenne2020
# dfToChrono['sau_grande_2020']=sauGrande2020

# for index,row in dfToChrono.iterrows():
#     print(row[9:17])


size=[150,150,150,150]
color=["red","orange","blue","green"]
nb1=[1500,2108,771,76]
nb2=[1263,1628,1796,90]
surf1=[14782.49,66239.88,38904.91,4470.63]
surf2=[14951.55,55015.5,44160.89,5424.04]
text=["micro\nexploitation\n2010","petite\nexploitation\n2010","moyenne\nexploitation\n2010","grande\nexploitation\n2010"]
text2=["micro\nexploitation\n2020","petite\nexploitation\n2020","moyenne\nexploitation\n2020","grande\nexploitation\n2020"]
a=plt.scatter(nb1,surf1,s=size,color=color,alpha=0.5)
b=plt.scatter(nb2,surf2,s=size,color=color)
plt.xlabel("Nombre exploitation")
plt.ylabel("Surface exploitation")
plt.grid(which='both')
for i in range(len(text)):
    if i == 0:
        plt.annotate(text[i],(nb1[i]-150,surf1[i]+4000))
        plt.annotate(text2[i],(nb2[i]-150,surf2[i]-10000))
    elif i == 3:
        plt.annotate(text[i],(nb1[i]-50,surf1[i]+5000))
        plt.annotate(text2[i],(nb2[i]+150,surf2[i]-2800))
    else:
        plt.annotate(text[i],(nb1[i]-150,surf1[i]-10000))
        plt.annotate(text2[i],(nb2[i]-150,surf2[i]-10000))
# plt.legend((a,b),('2010','2020'))
plt.show()

"""
Représentation évolution Otex --------------------------------------------------------
"""
col = []
for key in otexPoles:
    for index,row in otexPoles[key].iterrows():
        if row[0] == 2010:
            col.append(row[2])