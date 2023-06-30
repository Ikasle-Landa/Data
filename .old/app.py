from flask import Flask, render_template_string
import geopandas as gpd
import pandas as pd
from numpy import nan
import contextily as ctx
import geodatasets as gds
import folium
from folium.plugins import StripePattern
from xyzservices import TileProvider
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
# ax = geoDonnees.plot(column="echelle", cmap="summer", legend=True, legend_kwds={"loc": "center left", "bbox_to_anchor": (1, 0.5), "fmt": "{:.0f}"})
# ctx.add_basemap(ax, crs = geoDonnees.crs)

chiffresCles =  pd.read_table("Data/chiffres_cles_des_poles.csv", sep=';')

ageParPole = chiffresCles.loc[chiffresCles["type"] == "age_moy", :]

geoDonneesAge = geoDonnees.merge(ageParPole, on='echelle')

mainDf = pd.read_table("Data/devenir_exploitation.csv", sep=";",decimal=",")

geoDonneesDevenirExploitation = geoDonnees.merge(mainDf, on="echelle")

geoDonneesMainDf = geoDonneesPole.merge(mainDf, on="echelle")


# devenirExploitation = {1:"pas de départ du chef ou coexploitant envisagé dans l'immédiat",
#                        2:"disparition des terres au profit d'un usage non agricole",
#                        3:"nombre d'exploitations non concernées",
#                        4:"reprise par un coexploitant, un membre de la famille ou un tiers",
#                        5:"ne sait pas",
#                        6:"total d'exploitations concernées",
#                        7:"disparition au profit de l'agrandissement d'une ou plusieurs autres exploitations"}




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                            Génération                         #
#                            de la page                         #
#                               web                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def Accueil():
    dfVariation = pd.read_table('Data/variation1970-2020.csv', sep=';')
    l = list(dfVariation.columns)
    l[0] = 'echelle'
    dfVariation.columns = l

    gdfVariation = geoDonneesPole.merge(dfVariation, on='echelle')
    #variation_decennale
    
    tiles = TileProvider(
        url='https://server.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}',
        attribution='Tiles &copy; Esri &mdash; Source: Esri',
        name='Esri World Shaded Relief',
    )
    m = folium.Map(location=[43.3758766,-1.2983944], # center of the folium map
                tiles=tiles,
                min_zoom=10, max_zoom=10, # zoom range = donc pas de zoom possible
                zoom_start=10,
                max_bounds=True, # limites de la carte
                # min_lon=42.9946180429134, max_lon=43.621640458022526, 
                # min_lat=-1.9649778623793732, max_lat=-1.1722117212575165,
                zoom_control=False)


    folium.Choropleth(geo_data=gdfVariation,
                data=gdfVariation,
                columns=["echelle",'taux_1970-2020'],
                key_on="feature.properties.echelle",
                fill_color='Reds_r',
                legend_name="Taux de variation du nombre d'exploitation entre 1970 & 2020",
                fill_opacity=0.95,
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
        data = gdfVariation,
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=folium.features.GeoJsonTooltip(
            fields=['echelle','taux_1970-2020'],
            aliases=['echelle','Taux de variation :'],
            style=("background-color: white; color: #222222; font-family: arial; font-size: 12px; padding: 10px;") 
        )
    )
    m.add_child(IHM)
    m.keep_in_front(IHM)

    # # Ajout de de mode de carte 
    # folium.TileLayer('OpenStreetMap',name="OpenStreetMap",control=True).add_to(m)
    # folium.TileLayer("Stamen Terrain",name="relief",control=True).add_to(m)

    # # Ajout d'une interface de contrôle
    # folium.LayerControl(collapsed=False).add_to(m)

    m.get_root().render()
    header = m.get_root().header.render()
    body_html = m.get_root().html.render()
    script = m.get_root().script.render()    
    
    return header, body_html, script
    
# @app.route("/carte<int:numero>")
# def carte(numero : int):
#     devenirExploitation = {1:"pas de départ du chef ou coexploitant envisagé dans l'immédiat",
#                        2:"disparition des terres au profit d'un usage non agricole",
#                        3:"nombre d'exploitations non concernées",
#                        4:"reprise par un coexploitant, un membre de la famille ou un tiers",
#                        5:"ne sait pas",
#                        6:"total d'exploitations concernées",
#                        7:"disparition au profit de l'agrandissement d'une ou plusieurs autres exploitations"}
    
#     m = folium.Map(location=[43.3758766,-1.2983944], # center of the folium map
#                     tiles="OpenStreetMap",
#                     min_zoom=6, max_zoom=15, # zoom range
#                     zoom_start=9) # initial zoom


#     folium.Choropleth(geo_data=geoDonneesMainDf,
#                     data=geoDonneesMainDf,
#                     columns=["echelle",devenirExploitation[numero]],
#                     key_on="feature.properties.echelle",
#                     fill_color="YlGn",
#                     fill_opacity=0.85,
#                     smooth_factor=0,
#                     Highlight= True,
#                     line_color = "#0000",
#                     name = "Données",
#                     show=True,
#                     overlay=True,).add_to(m)

#     style_function = lambda x: {'fillColor': '#ffffff', 
#                                 'color':'#000000', 
#                                 'fillOpacity': 0.1, 
#                                 'weight': 0.1}
#     highlight_function = lambda x: {'fillColor': '#000000', 
#                                     'color':'#000000', 
#                                     'fillOpacity': 0.50, 
#                                     'weight': 0.1}

#     IHM = folium.features.GeoJson(
#         data = geoDonneesMainDf,
#         style_function=style_function, 
#         control=False,
#         highlight_function=highlight_function, 
#         tooltip=folium.features.GeoJsonTooltip(
#             fields=['echelle',devenirExploitation[numero]],
#             aliases=['echelle',devenirExploitation[numero] + ' (en %)'],
#             style=("background-color: white; color: #222222; font-family: arial; font-size: 12px; padding: 10px;") 
#         )
#     )
#     m.add_child(IHM)
#     m.keep_in_front(IHM)

#     # Ajout de de mode de carte 
#     folium.TileLayer('cartodbdark_matter',name="dark mode",control=True).add_to(m)
#     folium.TileLayer("Stamen Terrain",name="relief",control=True).add_to(m)

#     # Ajout d'une interface de contrôle
#     folium.LayerControl(collapsed=False).add_to(m)
    
#     m.get_root().render()
#     header = m.get_root().header.render()
#     body_html = m.get_root().html.render()
#     script = m.get_root().script.render()
    
    
    
#     return render_template_string(
#         open("carte.html").read(),
#         header=header,
#         titre=devenirExploitation[numero],
#         body_html=body_html,
#         script=script,
#     )
    

if __name__ == "__main__":
    accueil = Accueil()
    with open("header", "w") as f:
        f.write(accueil[0])
    with open("body", "w") as f:
        f.write(accueil[1])
    with open("script", "w") as f:
        f.write(accueil[2])
    
    
# Codes couleurs
# Couleur 1 : #29521a
# Couleur 2 : #007e20
# Couleur 3 : #1caa56
# Couleur 4 : #a3d8ab
# Couleur 5 : #d8fcd9