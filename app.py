from flask import Flask, render_template_string
import geopandas as gpd
import pandas as pd
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


devenirExploitation = {1:"pas de départ du chef ou coexploitant envisagé dans l'immédiat",
                       2:"disparition des terres au profit d'un usage non agricole",
                       3:"nombre d'exploitations non concernées",
                       4:"reprise par un coexploitant, un membre de la famille ou un tiers",
                       5:"ne sait pas",
                       6:"total d'exploitations concernées",
                       7:"disparition au profit de l'agrandissement d'une ou plusieurs autres exploitations"}


app = Flask(__name__)

@app.route("/")
def Accueil():
    m = folium.Map(location=[43.3758766,-1.2983944], # center of the folium map
                tiles="cartodbdark_matter",
                min_zoom=10, max_zoom=10, # zoom range
                zoom_start=10,
                min_lon=43.3758766, max_lon=-1.2983944,
                min_lat=43.3758766, max_lat=1.2983944) # initial zoom


    folium.Choropleth(geo_data=geoDonneesMainDf,
                    # data=geoDonneesMainDf,
                    # columns=["echelle", "pas de départ du chef ou coexploitant envisagé dans l'immédiat"],
                    key_on="feature.properties.echelle",
                    nan_fill_color="white",
                    fill_color="#f1f1f1",
                    fill_opacity=0.67,
                    smooth_factor=0,
                    Highlight= True,
                    line_color = "#0000",
                    name = "Pôles",
                    show=True,
                    overlay=True,).add_to(m)

    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#ffffff', 
                                    'color':'#000000', 
                                    'fillOpacity': 1, 
                                    'weight': 0.1}

    IHM = folium.features.GeoJson(
        data = geoDonneesMainDf,
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=folium.features.GeoJsonTooltip(
            fields=['echelle'],
            aliases=['Pôle :'],
            style=("background-color: white; color: #222222; font-family: arial; font-size: 12px; padding: 10px;") 
        )
    )
    m.add_child(IHM)
    m.keep_in_front(IHM)

    # Ajout de de mode de carte 
    folium.TileLayer('OpenStreetMap',name="OpenStreetMap",control=True).add_to(m)
    folium.TileLayer("Stamen Terrain",name="relief",control=True).add_to(m)

    # Ajout d'une interface de contrôle
    folium.LayerControl(collapsed=False).add_to(m)

    m.get_root().render()
    header = m.get_root().header.render()
    body_html = m.get_root().html.render()
    script = m.get_root().script.render()
    
    
    
    return render_template_string(
        open("index.html").read(),
        header=header,
        body_html=body_html,
        script=script,
    )

if __name__ == "__main__":
    app.run(debug=True)