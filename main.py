import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
import geopandas as gp

# Importation des données pour chaque pôle
# et les données sur l'ensemble du pays
# basque, regroupées en un dictionnaire
evol_nb_exploit = {
    'Amikuze': pd.read_table("./fichiersParPole/fts_ra2020_amikuze/evolution_n_exploit_sau-Tableau 1.csv", sep=";",decimal=","),
    'Côte Basque Adour': pd.read_table("./fichiersParPole/fts_ra2020_cote_basque_adour/evolution_n_exploit_sau-Tableau 1.csv", sep=";",decimal=","),
    'Errobi': pd.read_table("./fichiersParPole/fts_ra2020_errobi/evolution_n_exploit_sau-Tableau 1.csv", sep=";",decimal=","),
    'Garazi Baigorri': pd.read_table("./fichiersParPole/fts_ra2020_garazi_baigorri/evolution_n_exploit_sau-Tableau 1.csv", sep=";",decimal=","),
    'Iholdi Oztibarre': pd.read_table("./fichiersParPole/fts_ra2020_iholdi_oztibarre/evolution_n_exploit_sau-Tableau 1.csv", sep=";",decimal=","),
    'Nive Adour': pd.read_table("./fichiersParPole/fts_ra2020_nive_adour/evolution_n_exploit_sau-Tableau 1.csv", sep=";",decimal=","),
    'Pays de Bidache': pd.read_table("./fichiersParPole/fts_ra2020_pays_de_bidache/evolution_n_exploit_sau-Tableau 1.csv", sep=";",decimal=","),
    'Pays d\'Hasparren': pd.read_table("./fichiersParPole/fts_ra2020_pays_d_hasparren/evolution_n_exploit_sau-Tableau 1.csv", sep=";",decimal=","),
    'Soule Xiberoa': pd.read_table("./fichiersParPole/fts_ra2020_soule_xiberoa/evolution_n_exploit_sau-Tableau 1.csv", sep=";",decimal=","),
    'Sud Pays Basque': pd.read_table("./fichiersParPole/fts_ra2020_sud_pays_basque/evolution_n_exploit_sau-Tableau 1.csv", sep=";",decimal=","),
    'Ca du Pays Basque': pd.read_table("./fichiersParPole/fts_ra2020_ca_du_pays_basque/evolution_n_exploit_sau-Tableau 1.csv", sep=";",decimal=",")
}

# Initialisation du dataframe
# contenant le nombre d'exploitation
# sur plusieures années par pole
df_evol_nb_exploit = pd.DataFrame(
    index=['Amikuze','Côte Basque Adour','Errobi',
           'Garazi Baigorri','Iholdi Oztibarre','Nive Adour',
           'Pays de Bidache','Pays d\'Hasparren','Soule Xiberoa',
           'Sud Pays Basque','Ca du Pays Basque','France'],
    columns=[1970,1979,1988,2000,2010,2020]
)

df_evol_sau = pd.DataFrame(
    index=['Amikuze','Côte Basque Adour','Errobi',
           'Garazi Baigorri','Iholdi Oztibarre','Nive Adour',
           'Pays de Bidache','Pays d\'Hasparren','Soule Xiberoa',
           'Sud Pays Basque','Ca du Pays Basque','France'],
    columns=[1970,1979,1988,2000,2010,2020]
)

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
plt.show()

"""
Construction des dataframes ---------------------------------------------------------------
"""

# Importation des données du 
# Pays Basque
nbExploitPaysBasque = pd.read_table("./fichiersParPole/fts_ra2020_ca_du_pays_basque/evolution_n_exploit_sau-Tableau 1.csv", sep=";")
nbExploitFrance = [1591036,1270085,1088731,763953,603884,496365]

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
for key in evol_nb_exploit:
    for index,row in evol_nb_exploit[key].iterrows():
        df_evol_nb_exploit.loc[key,row[0]] = row[1]
        df_evol_sau.loc[key,row[0]] = row[3]

# Ajout des nombres d'exploitation France
for i in range(len(nbExploitFrance)):
    df_evol_nb_exploit.iloc[11,i] = nbExploitFrance[i]

# Permet de calculer la racine n-ième
def racineN(x,n):
    return x**(1/float(n))

# Calcul du taux variation décennale, taux global,
# taux entre 2010 - 2020 nb_exploit et sau_moy
tauxDecennaleNbExploit = []
tauxNbExploit = []
tauxNbExploit2010et2020 = []
tauxDecennaleSauMoy = []
tauxSauMoy = []
tauxSauMoy2010et2020 = []
# Ajout des valeurs respectives
for i in range(len(df_evol_nb_exploit)):
    tauxDecennaleNbExploit.append((df_evol_nb_exploit.iloc[i,5],df_evol_nb_exploit.iloc[i,0]))
    tauxNbExploit.append((df_evol_nb_exploit.iloc[i,5],df_evol_nb_exploit.iloc[i,0]))
    tauxNbExploit2010et2020.append((df_evol_nb_exploit.iloc[i,5],df_evol_nb_exploit.iloc[i,4]))
    tauxDecennaleSauMoy.append((df_evol_sau.iloc[i,5],df_evol_sau.iloc[i,0]))
    tauxSauMoy.append((df_evol_sau.iloc[i,5],df_evol_sau.iloc[i,0]))
    tauxSauMoy2010et2020.append((df_evol_sau.iloc[i,5],df_evol_sau.iloc[i,4]))
# calcul des taux
for i in range(len(tauxDecennaleNbExploit)):
    x=float(tauxDecennaleNbExploit[i][0]/tauxDecennaleNbExploit[i][1])
    tauxDecennaleNbExploit[i]=round(((racineN(x,5)-1)*100),2) 
    tauxNbExploit[i]=round(float((tauxNbExploit[i][0]-tauxNbExploit[i][1])/tauxNbExploit[i][1]),2)
    tauxNbExploit2010et2020[i]=round(float((tauxNbExploit2010et2020[i][0]-tauxNbExploit2010et2020[i][1])/tauxNbExploit2010et2020[i][1]),2)
    x=float(tauxDecennaleSauMoy[i][0]/tauxDecennaleSauMoy[i][1])
    tauxDecennaleSauMoy[i]=round(((racineN(x,5)-1)*100),2) 
    tauxSauMoy[i]=round(float((tauxSauMoy[i][0]-tauxSauMoy[i][1])/tauxSauMoy[i][1]),2)
    tauxSauMoy2010et2020[i]= round(float((tauxSauMoy2010et2020[i][0]-tauxSauMoy2010et2020[i][1])/tauxSauMoy2010et2020[i][1]),2)

# Ajout des taux variations a df_evol_nb_exploit
ls=pd.Series(tauxDecennaleNbExploit)
df_evol_nb_exploit['taux_decennal']=ls.values
ls=pd.Series(tauxNbExploit)
df_evol_nb_exploit['taux_1970-2020']=ls.values
ls=pd.Series(tauxNbExploit2010et2020)
df_evol_nb_exploit['taux_2010-2020']=ls.values
# Ajout des taux variations a df_evol_sau
ls=pd.Series(tauxDecennaleSauMoy)
df_evol_sau['taux_decennal']=ls.values
ls=pd.Series(tauxSauMoy)
df_evol_sau['taux_1970-2020']=ls.values
ls=pd.Series(tauxSauMoy2010et2020)
df_evol_sau['taux_2010-2020']=ls.values

# Ajout des nombres d'exploitation pour chaque
# année, pour la France et le Pays Basque
for index,row in nbExploitPaysBasque.iterrows():
    dfComparaisonFrancePaysBasque.loc['Ca du Pays Basque',row[0]] = row[1]
for i in range(len(nbExploitFrance)):
    dfComparaisonFrancePaysBasque.iloc[1,i] = nbExploitFrance[i]


"""
Représentation évolution taux décennal nombre exploitations et sau --------------------------
"""

# Récupération des noms des poles
label=list(df_evol_sau.index)
# Suppression de la France
s = label.pop(11)
la = label.pop(10)
# Récupération des valeurs taux décennal nb exploit
txDecNbExploit=list(df_evol_nb_exploit['taux_decennal'].values)
# Suppression de la France
s = txDecNbExploit.pop(11)
lb = txDecNbExploit.pop(10)
# Récupération des valeurs taux décennal sau
txDecSauMoy=list(df_evol_sau['taux_decennal'].values)
# Suppression de la France
s = txDecSauMoy.pop(11)
lc = txDecSauMoy.pop(10)
plt.barh(label,width=txDecNbExploit,color='#ff2c2c')
for i in range(len(txDecNbExploit)):
    plt.text(txDecNbExploit[i]/2,i-0.15,str(txDecNbExploit[i])+' %',ha='center',color='white')
plt.barh(la,width=lb,color='#c30010')
plt.text(lb/2,10-0.15,str(lb)+' %',ha='center',color='white')
plt.barh(label,width=txDecSauMoy,color='#46923c')
for i in range(len(txDecSauMoy)):
    plt.text(txDecSauMoy[i]/2,i-0.15,str(txDecSauMoy[i])+'% ',ha='center',color='white')
plt.barh(la,width=lc,color='#276221')
plt.text(lc/2,10-0.15,str(lc)+'% ',ha='center',color='white')
plt.xlabel('      taux décennal                                    taux décennal \nnombre d\'exploitations                             sau moyen')
#plt.savefig('./assets/evol_tx_dec.svg',format='svg',bbox_inches='tight')
plt.show()

# df_evol_nb_exploit.to_csv("./assets/evol.csv",decimal=",",sep=";")
# df_evol_sau.to_csv("./assets/evol_sau.csv",decimal=",",sep=";")


"""
Représentation chronologique nb exploitations ----------------------
"""

# Inversion des colonnes et lignes
# pour réaliser le graphique chronologique
dfToPlot = df_evol_nb_exploit.iloc[0:9,0:6].transpose()
dfToPlot.plot(colormap='YlGn',
              logy=True,
              legend=True)
plt.grid(axis='y', which='both')
plt.legend(bbox_to_anchor=(1,1))

plt.title('Série chronologique de l\'évolution \n du nombre d\'exploitations')
#plt.savefig('./assets/Serie_chrono_evol.svg',format='svg',bbox_inches='tight')
plt.show()

# Création graphique comparaison france 
# et pays basque
dfComparaisonToPlot = dfComparaisonFrancePaysBasque.transpose()
dfComparaisonToPlot.plot(colormap='winter',
              logy=True,
              legend=True)
plt.grid(axis='y', which='both')
plt.rc('axes',axisbelow=True)
plt.legend(bbox_to_anchor=(1,1))
plt.title('Série chronologique de l\'évolution \ndu nombre d\'exploitations au niveau national')
#plt.savefig('./assets/Serie_chrono_evol_national.svg',format='svg',bbox_inches='tight')
plt.show()


"""
Bubble plot ca_du_pays_basque --------------------------------------------------------
"""
size=[150,150,150,150]
color=["red","orange","blue","green"]

# Nb exploit 2010 - 2020 par taille exploit
micro2010=list([172,25,262,184,79,71,197,79,212,219,1500,np.nan])
micro2020=list([160,16,186,179,75,59,188,83,163,154,1263,np.nan])
petite2010=list([292,16,121,535,194,27,268,92,428,135,2108,np.nan])
petite2020=list([229,8,97,410,161,19,199,7,308,120,1628,np.nan])
moyenne2010=list([158,7,33,150,107,12,101,65,103,35,771,np.nan])
moyenne2020=list([144,3,36,170,112,13,108,52,121,37,796,np.nan])
grande2010=list([20,np.nan,np.nan,6,6,3,10,20,3,5,76,np.nan])
grande2020=list([19,np.nan,5,11,8,np.nan,13,19,9,np.nan,90,np.nan])

# # Sau des poles 2010 - 2020 par taille exploit
sauMicro2010=list([1745.31,178.31,1833.05,2306.02,1232.73,618.42,
                   1955.05,873.79,2374.2,1665.61,14782.49,np.nan])
sauMicro2020=list([2215.84,135.65,1508.2,2205.38,924.2,516.76,
                   2355.55,1308.2,2232.41,1549.36,14951.55,np.nan])
sauPetite2010=list([10228.44,77.76,3467.48,14573.88,6372.97,65.123,
                    8774.94,3637.94,14956.01,3475.23,66239.88,np.nan])
sauPetite2020=list([8816.89,79.9,2783.3,11751.33,6034.5,556.78,
                    6761.42,3044.76,11903.29,3283.33,55015.5,np.nan])
sauMoyenne2010=list([9044.44,139.72,1533.21,6191.65,5434.83,474.28,
                     5015.61,3631.07,6133.83,1306.27,38904.91,np.nan])
sauMoyenne2020=list([8989.93,8.59,1694.27,7729.47,6125.36,526.51,
                     5779.08,3522.89,8275.95,1508.84,44160.89,np.nan])
sauGrande2010=list([1057.5,np.nan,np.nan,173.69,337.06,91,561.21,
                    1422.3,272.45,410.85,4470.63,np.nan])
sauGrande2020=list([1312.8,np.nan,345.52,428.86,357.69,np.nan,759.55,
                    1305.16,691.06,np.nan,5424.04,np.nan])

df_evol_nb_exploit['nb_exploit_micro_2010']=micro2010
df_evol_nb_exploit['nb_exploit_petite_2010']=petite2010
df_evol_nb_exploit['nb_exploit_moyenne_2010']=moyenne2010
df_evol_nb_exploit['nb_exploit_grande_2010']=grande2010

df_evol_nb_exploit['nb_exploit_micro_2020']=micro2020
df_evol_nb_exploit['nb_exploit_petite_2020']=petite2020
df_evol_nb_exploit['nb_exploit_moyenne_2020']=moyenne2020
df_evol_nb_exploit['nb_exploit_grande_2020']=grande2020

df_evol_nb_exploit['sau_micro_2010']=sauMicro2010
df_evol_nb_exploit['sau_petite_2010']=sauPetite2010
df_evol_nb_exploit['sau_moyenne_2010']=sauMoyenne2010
df_evol_nb_exploit['sau_grande_2010']=sauGrande2010

df_evol_nb_exploit['sau_micro_2020']=sauMicro2020
df_evol_nb_exploit['sau_petite_2020']=sauPetite2020
df_evol_nb_exploit['sau_moyenne_2020']=sauMoyenne2020
df_evol_nb_exploit['sau_grande_2020']=sauGrande2020

text=["micro\nexploitation\n","petite\nexploitation\n",
      "moyenne\nexploitation\n","grande\nexploitation\n"]

legend_elm=[Line2D([0],[0],markerfacecolor=color[0],marker='o',markersize=5,
                   color='w',alpha=0.5,label='Micro-exploitations 2010'),
            Line2D([0],[0],markerfacecolor=color[0],marker='o',markersize=5,
                   color='w',label='Micro-exploitations 2020'),
            Line2D([0],[0],markerfacecolor=color[1],marker='o',markersize=5,
                   color='w',alpha=0.5,label='Petites exploitations 2010'),
            Line2D([0],[0],markerfacecolor=color[1],marker='o',markersize=5,
                   color='w',label='Petites exploitations 2020'),
            Line2D([0],[0],markerfacecolor=color[2],marker='o',markersize=5,
                   color='w',alpha=0.5,label='Moyennes exploitations 2010'),
            Line2D([0],[0],markerfacecolor=color[2],marker='o',markersize=5,
                   color='w',label='Moyennes exploitations 2020'),
            Line2D([0],[0],markerfacecolor=color[3],marker='o',markersize=5,
                   color='w',alpha=0.5,label='Grandes exploitations 2010'),
            Line2D([0],[0],markerfacecolor=color[3],marker='o',markersize=5,
                   color='w',label='Grandes exploitations 2020')]

for index,row in df_evol_nb_exploit.iterrows():
    if index != 'France':
        a = plt.scatter(row[9:13],row[17:21],s=size,color=color)
        b = plt.scatter(row[13:17],row[21:],s=size,color=color,alpha=0.5)
        x1 = row[9:13]
        x2 = row[13:17]
        y1 = row[17:21]
        y2 = row[21:]
        plt.xlabel("Nombre exploitations 2010 - 2020")
        plt.ylabel("Sau totale 2010 - 2020")
        plt.grid(which='both')
        plt.title(str(index))
        plt.legend(handles=legend_elm,bbox_to_anchor=(1,1),loc="upper left")
        #plt.savefig(f'./assets/{index}.svg',format='svg',bbox_inches='tight')
        plt.show()

