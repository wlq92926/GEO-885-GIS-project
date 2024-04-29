import geopandas as gpd
import folium
from folium.plugins import FastMarkerCluster
import shapely
import datetime
import scipy.stats as stats
import matplotlib.pyplot as plt

class MapAccident:
    def __init__(self, buffer_T, beforeimply, afterimply):
        self.buffer_T = buffer_T
        self.beforeimply = beforeimply
        self.afterimply = afterimply

    def display_map(self):
        c_long = 47.377637
        c_lat = 8.540391
        zoom = 12
        m = folium.Map([c_long, c_lat], zoom_start = zoom)

        traffic_layer = folium.GeoJson(data = self.buffer_T,
                                       popup = folium.GeoJsonPopup(fields=["implemented_YYYYMM"]))
        traffic_layer.add_to(m)

        before_layer = folium.GeoJson(data = self.beforeimply,
                                      marker = folium.CircleMarker(radius = 3, fill_color = "red",
                                                                   fill_opacity = 0.8, color = "black", weight = 0.3),
                                      popup = folium.GeoJsonPopup(fields = ["accident_date", "AccidentType_en"]))
        before_layer.add_to(m)

        after_layer = folium.GeoJson(data = self.afterimply,
                                     marker = folium.CircleMarker(radius = 3, fill_color = "orange",
                                                                  fill_opacity = 0.8, color = "black", weight = 0.3),
                                     popup = folium.GeoJsonPopup(fields = ["accident_date", "AccidentType_en"]))
        after_layer.add_to(m)
        display(m)