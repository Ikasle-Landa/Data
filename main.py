import geopandas as gpd

LeDataFrame = gpd.read_file("rga2020_dataviz_challenge.geojson")

LeDataFrame.plot(column='echelle', legend=True)