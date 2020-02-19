"""Geojson/json to GeoDataFrame/Dataframe."""
import json
from pandas.io.json import json_normalize
from geopandas import GeoDataFrame
import geopandas
import pandas as pd
# from matplotlib import pyplot as plt


def compute_area(dataset, width):
    """Compute area for each line feature and return a dataframe object.

    dataset: Dataframe object
    width: Dictionary, unique highway category as key and the width in meters
    as value.

    """
    Area = []
    dataset = dataset.set_index(["highway"])
    for key, value in width.items():
        area = dataset.loc[key]["length"]*value
        Area.append(area)
    Area = pd.concat(Area)
    dataset["area"] = Area.values
    dataset_new = dataset.reset_index()
    return dataset_new


def geoJsonToGeoDataframe(jsonFile):
    """Geojson to GeoDataFrame."""
    print("INFO: READING GEOJSON FILE")
    data_geometry = geopandas.read_file(jsonFile)
    with open(jsonFile, "r") as read_file:
        data = json.load(read_file)
    highwayData = json_normalize(data["features"])
    highwayData = highwayData[["OSM-id", "properties.highway"]]
    highwayData_rename = highwayData.\
        rename(columns={"properties.highway": "highway"})
    highwayData_rename["geometry"] = data_geometry.geometry
    geodata = GeoDataFrame(highwayData_rename, geometry='geometry')

    print("INFO: CRS 3857 CONVERSION")
    # change the crs/projection of the geometry to 3857
    geodata.crs = {'init': 'epsg:4326'}
    geodata = geodata.to_crs({'init': 'epsg:3857'})
    return geodata


def esyLines(jsonFile="berlin_line.geojson"):
    """OSM lines using esy-osmfilter."""
    highway_feature = ['living_street', 'motorway', 'pedestrian',
                       'primary', 'secondary', 'service', 'tertiary',
                       'trunk', 'motorway_link', 'primary_link',
                       'secondary_link', 'tertiary_link',
                       'trunk_link']
    highway_width = [7.5, 15.50, 7.5, 10.5, 9.5, 7.5, 9.5, 9.5, 6.5, 6.5,
                     6.5, 6.5, 6.5]
    width = dict(zip(highway_feature, highway_width))
    out_dir = "../data/output_data/"
    jsonFile = out_dir+jsonFile
    # get filtered geojson file, and transform to geodataframe
    geodata = geoJsonToGeoDataframe(jsonFile)
    # calculate length of the geometry
    print("INFO: CALCULATING HIGHWAY LENGTH")
    geodata["length"] = geodata.geometry.length
    esy_osmData = geodata.sort_values("highway")

    # calculate area using the width of the highway categories
    print("INFO: CALCULATING HIGHWAY AREA")
    esy_osmData = compute_area(esy_osmData, width)
    esy_osmData = esy_osmData[["OSM-id", "highway", "length",
                               "area", "geometry"]]
    print("INFO: WRITE TO CSV & SHAPE FILE")
    esy_osmData.to_file(driver='ESRI Shapefile',
                        filename=out_dir+"planet_osm_line")
    esy_osmData.to_csv(out_dir+"planet_osm_line/planet_osm_line.csv",
                       encoding="utf-8")

    # print(esy_osmData[["highway", "area"]].groupby("highway").sum())
    # print(geodata[["highway", "length"]].groupby("highway").sum())
    # geodata.plot(column='highway')
    # plt.show()


def esyPoints(jsonFile="berlin_point.geojson"):
    """Get points using esy-osmfilter."""
    # get filtered geojson file, and transform to geodataframe
    out_dir = "../data/output_data/"
    jsonFile = out_dir+jsonFile
    geodata = geoJsonToGeoDataframe(jsonFile)
    esy_osmData = geodata.sort_values("highway")
    print("INFO: WRITE TO CSV & SHAPE FILE")
    esy_osmData.to_file(driver='ESRI Shapefile',
                        filename=out_dir+"planet_osm_point")
    esy_osmData.to_csv(out_dir+"planet_osm_point/planet_osm_point.csv",
                       encoding="utf-8")


if __name__ == "__main__":
    print("RUNING: ======== HIGHWAY-ABSTRACTION ========")
    esyLines()
    print("HIGHWAY-ABSTRACTION: LINES ===== DONE")
    esyPoints()
    print("HIGHWAY-ABSTRACTION: POINTS ===== DONE")
