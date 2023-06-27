import geopandas as gpd
import pandas as pd
from flask import Flask
import numpy as np
from numpy import nan
import contextily as ctx
import geodatasets as gds
import folium
from folium.plugins import StripePattern
import matplotlib.pyplot as plt

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                           Importation                         #
#                               des                             #
#                             données                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

geoDonnees = gpd.read_file("rga2020_dataviz_challenge.geojson")
geoDonneesPole = gpd.read_file("contour_capb_poles_territoriaux.geojson")

# Nettoyage des données par suppression de CA du Pays Basque
geoDonnees = geoDonnees.loc[geoDonnees['echelle'] != 'ca_du_pays_basque', :]
#ax = geoDonnees.plot(column="echelle", cmap="summer", legend=True, legend_kwds={"loc": "center left", "bbox_to_anchor": (1, 0.5), "fmt": "{:.0f}"})
#ctx.add_basemap(ax, crs = geoDonnees.crs)
 
chiffreCle =  pd.read_table("Data/chiffres_cles_des_poles.csv", sep=';',decimal=',')
dfNbExpl = chiffreCle.loc[chiffreCle['nom'] == 'nombre total d\'exploitations',:]
dfNbExpl = dfNbExpl.drop(columns =['type'])

ageParPole = chiffreCle.loc[chiffreCle["type"] == "age_moy", :]

geoDonneesAge = geoDonnees.merge(ageParPole, on='echelle')

mainDf = pd.read_table("Data/devenir_exploitation.csv", sep=";",decimal=",")

mainDf2010 = mainDf.loc[mainDf['annee'] == 2010, :] 
mainDf2020 = mainDf.loc[mainDf['annee'] == 2020, :] 

geoDonneesDevenirExploitation = geoDonnees.merge(mainDf, on="echelle")

geoDonneesMainDf2010 = geoDonneesPole.merge(mainDf2010, on="echelle")
geoDonneesMainDf2020 = geoDonneesPole.merge(mainDf2020, on="echelle")

"""
ax = geoDonneesDevenirExploitation.plot(column="pas de départ du chef ou coexploitant envisagé dans l'immédiat",
                                        cmap="summer", 
                                        legend=True,
                                        legend_kwds={'location':'right','label':'blabla','boundaries':[i for i in range(0,101,10)]})

ax.set_axis_off()
ctx.add_basemap(ax, crs = geoDonneesDevenirExploitation.crs)



ax = geoDonneesAge.plot(column="2010",cmap="summer", legend=True, legend_kwds={"loc": "center left", "bbox_to_anchor": (1, 0.5), "fmt": "{:.0f}"})
ax.set_axis_off()
ctx.add_basemap(ax, crs = geoDonneesAge.crs)

ax = geoDonneesAge.plot(column="2020",cmap="summer", legend=True, legend_kwds={"loc": "center left", "bbox_to_anchor": (1, 0.5), "fmt": "{:.0f}"})
ax.set_axis_off()
ctx.add_basemap(ax, crs = geoDonneesAge.crs)

"""
"""
devenirExploitation = {1:"pas de départ du chef ou coexploitant envisagé dans l'immédiat",
                       2:"disparition des terres au profit d'un usage non agricole",
                       3:"nombre d'exploitations non concernées",
                       4:"reprise par un coexploitant, un membre de la famille ou un tiers",
                       5:"ne sait pas",
                       6:"total d'exploitations concernées",
                       7:"disparition au profit de l'agrandissement d'une ou plusieurs autres exploitations"}


for i in devenirExploitation:
    m = folium.Map(location=[43.3758766,-1.2983944], # center of the folium map
                    tiles="Mapbox Bright",
                    min_zoom=6, max_zoom=15, # zoom range
                    zoom_start=9) # initial zoom


    folium.Choropleth(geo_data=geoDonneesMainDf,
                    data=geoDonneesMainDf,
                    columns=["echelle",devenirExploitation[i]],
                    key_on="feature.properties.echelle",
                    fill_color="YlGn",
                    fill_opacity=0.85,
                    smooth_factor=0,
                    Highlight= True,
                    line_color = "#0000",
                    name = "Données",
                    show=True,
                    overlay=True,).add_to(m)

    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}

    IHM = folium.features.GeoJson(
        data = geoDonneesMainDf,
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=folium.features.GeoJsonTooltip(
            fields=['echelle',devenirExploitation[i]],
            aliases=['echelle',devenirExploitation[i] + ' (en %)'],
            style=("background-color: white; color: #222222; font-family: arial; font-size: 12px; padding: 10px;") 
        )
    )
    m.add_child(IHM)
    m.keep_in_front(IHM)

    # Ajout de de mode de carte 
    folium.TileLayer('cartodbpositron',name="clair",control=True).add_to(m)
    folium.TileLayer("Stamen Terrain",name="relief",control=True).add_to(m)

    # Ajout d'une interface de contrôle
    folium.LayerControl(collapsed=False).add_to(m)


    filename = 'carte' + str(i) + '.html'
    m.save(filename)
"""
dfTemp = pd.read_table('Data/dimensions_exploitation.csv' ,sep=";",decimal=",")

mainDf = mainDf.merge(dfTemp,how='right',right_on="echelle",left_on="echelle")

mainDf.replace(-999,nan, inplace=True)



#echelles = mainDf["echelle"].drop_duplicates()


"""
dimension2010 = mainDf2010.pivot(index="dim", columns="echelle",values="n_exploit")


echelle = None
for i in dimension2010 :
    if i != echelle and i != "dim":
        total = dimension2010[i].sum()
        echelle = i
    for j in range(len(dimension2010[i])):
        dimension2010[i][j] = (dimension2010[i][j] / total) * 100

dimension2010 = dimension2010.reindex(columns=['Nive Adour','Errobi','Sud Pays Basque','Cote Basque Adour',"Pays d'Hasparren",'Pays de Bidache','Soule Xiberoa','Amikuze','Iholdi Otzibarre','Garazi Baigorri'])
dimension2010 = dimension2010.T
dimension2010 = dimension2010.reindex(columns=['microexploitations','petites','moyennes','grandes'])
dimension2010.plot(kind="bar", stacked=True, legend='reverse')
plt.legend(bbox_to_anchor=(1.05,0.5), loc='upper left') # titre : Répartition de la taille des exploitations par pôles en 2010
plt.show()

dimension2020 = mainDf2020.pivot(index="dim", columns="echelle",values="n_exploit")


echelle = None
for i in dimension2020 :
    if i != echelle and i != "dim":
        total = dimension2020[i].sum()
        echelle = i
    for j in range(len(dimension2020[i])):
        dimension2020[i][j] = (dimension2020[i][j] / total) * 100

dimension2020 = dimension2020.reindex(columns=['Nive Adour','Cote Basque Adour','Errobi','Sud Pays Basque',"Pays d'Hasparren",'Pays de Bidache','Amikuze','Soule Xiberoa','Garazi Baigorri','Iholdi Otzibarre'])
dimension2020 = dimension2020.T
dimension2020 = dimension2020.reindex(columns=['microexploitations','petites','moyennes','grandes'])
dimension2020.plot(kind="bar", stacked=True, legend='reverse')
plt.legend(bbox_to_anchor=(1.05,0.6), loc='upper left') # titre : Répartition de la taille des exploitations par pôles en 2020
plt.show()


dimension2010 = mainDf2010.pivot(index="dim", columns="echelle",values="sau_ha")

dimension2020 = mainDf2020.pivot(index="dim", columns="echelle",values="sau_ha")


echelle = None
for i in dimension2020 :
    if i != echelle and i != "dim":
        echelle = i
    for j in range(len(dimension2020[i])):
        val2010 = dimension2010[i][j]
        dimension2020[i][j] = (dimension2020[i][j] - val2010) / val2010 
"""
"""
dimension2020 = dimension2020.T.reindex(columns=['microexploitations','petites','moyennes','grandes'])
dimension2020.plot(kind="bar",title="Taux de variation des SAU entre 2010 & 2020", legend='reverse')
plt.legend(bbox_to_anchor=(1.05,0.6), loc='upper left')
plt.show()


dfCaPB = pd.read_table('Data/dimension_ca_du_pays_basque.csv',sep=";",decimal=",")

dfCaPB2010 = dfCaPB.loc[dfCaPB['annee'] == 2010,:]
dfCaPB2020 = dfCaPB.loc[dfCaPB['annee'] == 2020,:]

dfNbExpl2010 = dfCaPB2010.pivot(index="dim", columns="echelle",values="n_exploit")

total = dfNbExpl2010['ca_du_pays_basque'].sum()

for i in range(len(dfNbExpl2010['ca_du_pays_basque'])):
    dfNbExpl2010['ca_du_pays_basque'][i] = (dfNbExpl2010['ca_du_pays_basque'][i] / total) * 100

dfNbExpl2010 = dfNbExpl2010.T
dfNbExpl2010 = dfNbExpl2010.reindex(columns=['microexploitations','petites','moyennes','grandes'])
dfNbExpl2010.plot(kind="bar", stacked=True, legend='reverse')
plt.legend(title="Pôles",bbox_to_anchor=(1.05,0.6), loc='upper left') # titre : Répartition de la taille des exploitations en 2010
plt.title("Répartition du nombre d'exploitations par rapport à leur taille en 2010")
plt.show()

dfNbExpl2020 = dfCaPB2020.pivot(index="dim", columns="echelle",values="n_exploit")

total = dfNbExpl2020['ca_du_pays_basque'].sum()

for i in range(len(dfNbExpl2020['ca_du_pays_basque'])):
    dfNbExpl2020['ca_du_pays_basque'][i] = (dfNbExpl2020['ca_du_pays_basque'][i] / total) * 100

dfNbExpl2020 = dfNbExpl2020.T
dfNbExpl2020 = dfNbExpl2020.reindex(columns=['microexploitations','petites','moyennes','grandes'])
dfNbExpl2020.plot(kind="bar", stacked=True, legend='reverse')
plt.legend(title="Pôles",bbox_to_anchor=(1.05,0.6), loc='upper left') # titre : Répartition de la taille des exploitations en 2020
plt.title("Répartition du nombre d'exploitations par rapport à leur taille en 2020")
plt.show()



dfNbExpl2010 = dfCaPB2010.pivot(index="dim", columns="echelle",values="sau_ha")

dfNbExpl2020 = dfCaPB2020.pivot(index="dim", columns="echelle",values="sau_ha")



for i in range(len(dfNbExpl2020['ca_du_pays_basque'])):
    val2010 = dfNbExpl2010['ca_du_pays_basque'][i]
    dfNbExpl2020['ca_du_pays_basque'][i] = (dfNbExpl2020['ca_du_pays_basque'][i] - val2010) / val2010 

dfNbExpl2020 = dfNbExpl2020.T.reindex(columns=['microexploitations','petites','moyennes','grandes'])
dfNbExpl2020.plot(kind="bar",title="Taux de variation des SAU entre 2010 & 2020", legend='reverse')
plt.legend(title="Pôles",bbox_to_anchor=(1.05,0.6), loc='upper left')
plt.savefig('Graphique.svg',bbox_inches='tight',format='svg')
plt.show()

"""


"""
#Radar
dimension2020 = dimension2020.T
regroupementPole = {1:["Iholdi Otzibarre","Soule Xiberoa","Garazi Baigorri"],2:["Pays de Bidache","Amikuze","Pays d'Hasparren"],3:["Sud Pays Basque","Errobi","Cote Basque Adour","Nive Adour"]}
couleur = ["green","red","blue","orange"]
for x in regroupementPole:
    echelle = regroupementPole[x]
    ind = 0
    angles = np.linspace(0, 2 * np.pi, 4, endpoint=False).tolist()
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    for i in echelle:
        categories=['microexploitations','petites','moyennes','grandes']
        pole = list([dimension2020[j][i] for j in categories])
        label_loc=np.linspace(start=0,stop=2*np.pi,num=len(pole))
       
        pole += pole[:1]
        ax.plot(angles, pole, color=couleur[ind], linewidth=1, label=regroupementPole[x][ind])
        ax.fill(angles, pole, color=couleur[ind], alpha=0.5)
        ind += 1
        

    plt.title("Taux de variation des SAU entre 2010 & 2020")
    lines, labels = plt.thetagrids(range(0,360,90),labels=categories)
    plt.legend(title="Pôles",loc='upper right', bbox_to_anchor=(1.25, 1))
    fig.savefig('./Graphiques/Radar_SAU_2010_2020'+str(x)+'.svg',bbox_inches='tight',format='svg')
    plt.show()

"""
m = folium.Map(location=[43.3758766,-1.2983944], # center of the folium map
                tiles="OpenStreetMap",
                min_zoom=6, max_zoom=15, # zoom range
                zoom_start=9) # initial zoom


folium.Choropleth(geo_data=geoDonneesMainDf,
                data=geoDonneesMainDf,
                columns=["echelle",'n_exploit'],
                key_on="feature.properties.echelle",
                fill_color="YlGn",
                fill_opacity=0.85,
                smooth_factor=0,
                Highlight= True,
                line_color = "#0000",
                name = "Données",
                show=True,
                overlay=True,).add_to(m)

style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}

IHM = folium.features.GeoJson(
    data = geoDonneesMainDf,
    style_function=style_function, 
    control=False,
    highlight_function=highlight_function, 
    tooltip=folium.features.GeoJsonTooltip(
        fields=['echelle','n_exploit'],
        aliases=['echelle','Nombre d\'exploitations :'],
        style=("background-color: white; color: #222222; font-family: arial; font-size: 12px; padding: 10px;") 
    )
)
m.add_child(IHM)
m.keep_in_front(IHM)

# Ajout de de mode de carte 
folium.TileLayer('cartodbpositron',name="clair",control=True).add_to(m)
folium.TileLayer("Stamen Terrain",name="relief",control=True).add_to(m)

# Ajout d'une interface de contrôle
folium.LayerControl(collapsed=False).add_to(m)


m