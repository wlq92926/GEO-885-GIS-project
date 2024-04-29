import requests
import pandas as pd
import json
import geopandas as gpd
import folium


class TrafficAxis:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_data(self):
        data = gpd.read_file(self.file_path + "vas.vas_tempo_ist_event.json")
        data = data.to_crs(epsg = 3857)
        return data

    def formatting_time(self, data):
        # formatting time attribute to year, month, and year with month
        data["implemented_year"] = data["umgesetzt_datum"].str[:4]
        data["implemented_month"] = data["umgesetzt_datum"].str[4:6]
        data["implemented_YYYYMM"] = data["umgesetzt_datum"].str[:6]
        # filter axis that are not null
        # filter axis that implemented a speed limit after year 2011 (according to the accident data)
        traffic_axis = data[data["umgesetzt_datum"].notnull()]
        traffic_axis = traffic_axis[traffic_axis["implemented_year"].astype(int) >= 2011]
        return traffic_axis

    def speed_zone(self, traffic_axis, speed_limit):
        traffic_axis_T = traffic_axis[traffic_axis["temporegime_technical"] == speed_limit]
        return traffic_axis_T


class Accident:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_data(self):
        data = gpd.read_file(self.file_path + "roadtrafficaccidentlocations.json")
        data = data.to_crs(epsg = 3857)
        return data

    def organize(self, data):
        # drop the non-useful columns in the accident data
        columns_to_drop = ['AccidentType_de', 'AccidentType_fr', 'AccidentType_it', 'AccidentSeverityCategory_de',
                           'AccidentSeverityCategory_fr', 'AccidentSeverityCategory_it', 'RoadType_de', 'RoadType_fr',
                           'RoadType_it', 'AccidentMonth_de', 'AccidentMonth_fr', 'AccidentMonth_it',
                           'AccidentWeekDay_de', 'AccidentWeekDay_fr', 'AccidentWeekDay_it']
        data = data.drop(columns = columns_to_drop, axis = 1)
        return data
