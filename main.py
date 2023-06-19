import geopandas as gpd
import pandas as pd
from flask import Flask
from numpy import nan
import contextily as ctx
import geodatasets as gds
import folium
from folium.plugins import StripePattern

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                           Importation                         #
#                               des                             #
#                             données                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

geoDonnees = gpd.read_file("rga2020_dataviz_challenge.geojson")
geoDonneesPole = gpd.read_file("contour_capb_poles_territoriaux.geojson")

# Nettoyage des données par suppression de CA du Pays Basque
geoDonnees = geoDonnees.loc[geoDonnees['echelle'] != 'ca_du_pays_basque', :]
# ax = geoDonnees.plot(column="echelle", cmap="summer", legend=True, legend_kwds={"loc": "center left", "bbox_to_anchor": (1, 0.5), "fmt": "{:.0f}"})
# ctx.add_basemap(ax, crs = geoDonnees.crs)

chiffresCles =  pd.read_table("Data/chiffres_cles_des_poles.csv", sep=';')

ageParPole = chiffresCles.loc[chiffresCles["type"] == "age_moy", :]

geoDonneesAge = geoDonnees.merge(ageParPole, on='echelle')

mainDf = pd.read_table("Data/devenir_exploitation.csv", sep=";",decimal=",")

geoDonneesDevenirExploitation = geoDonnees.merge(mainDf, on="echelle")

geoDonneesMainDf = geoDonneesPole.merge(mainDf, on="echelle")

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



devenirExploitation = {1:"pas de départ du chef ou coexploitant envisagé dans l'immédiat",
                       2:"disparition des terres au profit d'un usage non agricole",
                       3:"nombre d'exploitations non concernées",
                       4:"reprise par un coexploitant, un membre de la famille ou un tiers",
                       5:"ne sait pas",
                       6:"total d'exploitations concernées",
                       7:"disparition au profit de l'agrandissement d'une ou plusieurs autres exploitations"}


for i in devenirExploitation:
    m = folium.Map(location=[43.3758766,-1.2983944], # center of the folium map
                    tiles="OpenStreetMap",
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
    folium.TileLayer('cartodbdark_matter',name="dark mode",control=True).add_to(m)
    folium.TileLayer("Stamen Terrain",name="relief",control=True).add_to(m)

    # Ajout d'une interface de contrôle
    folium.LayerControl(collapsed=False).add_to(m)


    filename = 'carte' + str(i) + '.html'
    m.save(filename)
"""

dfTemp = pd.read_table('Data/dimensions_exploitation.csv' ,sep=";",decimal=",")

mainDf = mainDf.merge(dfTemp,how='right',right_on="echelle",left_on="echelle")

mainDf.replace(-999,nan, inplace=True)

echelles = mainDf["echelle"].drop_duplicates()

mainDf2010 = mainDf.loc[mainDf['annee'] == 2010, :] 
mainDf2020 = mainDf.loc[mainDf['annee'] == 2020, :] 

dimension2010 = mainDf2010.pivot(index="dim", columns="echelle",values="n_exploit")


echelle = None
for i in dimension2010 :
    if i != echelle and i != "dim":
        total = dimension2010[i].sum()
        echelle = i
    for j in range(len(dimension2010[i])):
        dimension2010[i][j] = (dimension2010[i][j] / total) * 100

dimension2010.T.plot(kind="bar", stacked=True, legend='reverse')
