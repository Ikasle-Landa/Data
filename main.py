import pandas as pd
from graphics import *
import json

def extract_coordinates(json_string):
    try:
        data = json.loads(json_string)
        coordinates = []
        if data["type"] == "MultiPolygon":
            for polygon in data["coordinates"]:
                for ring in polygon:
                    for point in ring:
                        coordinates.append((point[0], point[1]))
        return coordinates
    except (json.JSONDecodeError, KeyError) as e:
        print("Erreur lors de l'extraction des coordonnées :", e)
        return []
    
def scale_coordinates(gps_coordinates, width, height):
    min_lon, min_lat = float("inf"), float("inf")
    max_lon, max_lat = float("-inf"), float("-inf")

    # Trouver les coordonnées minimales et maximales
    for polygon in gps_coordinates:
        for lon, lat in polygon:
            min_lon = min(min_lon, lon)
            min_lat = min(min_lat, lat)
            max_lon = max(max_lon, lon)
            max_lat = max(max_lat, lat)

    # Calculer l'échelle de conversion
    lon_range = max_lon - min_lon
    lat_range = max_lat - min_lat
    lon_scale = width / lon_range
    lat_scale = height / lat_range

    # Appliquer la mise à l'échelle uniforme à toutes les coordonnées
    scaled_coordinates = []
    for polygon in gps_coordinates:
        scaled_polygon = []
        for lon, lat in polygon:
            x = int((lon - min_lon) * lon_scale)
            y = int((lat - min_lat) * lat_scale)
            scaled_polygon.append((x, y))
    scaled_coordinates.append(scaled_polygon)

    return scaled_coordinates

leDataframe = pd.read_csv('DonnéesEnCSVNonTraitées/RGADonnéesDataVizMieux.csv', sep=';', encoding='utf-8', index_col=0) 

laFenêtre = GraphWin("La Fenêtre", 500, 500)

LesFormes = []


for i in leDataframe['Geo Shape']:
    if isinstance(i, str):
        LesFormes.append(extract_coordinates(i))
        
coordonnéesÉcran = scale_coordinates(LesFormes, 500, 500)
for j in range(1, len(coordonnéesÉcran)):
    ligne = Line(Point(coordonnéesÉcran[j-1][0], coordonnéesÉcran[j-1][1]), Point(coordonnéesÉcran[j][0], coordonnéesÉcran[j][1]))
    ligne.setOutline('white')
    ligne.draw(laFenêtre)

laFenêtre.getMouse()
laFenêtre.close()