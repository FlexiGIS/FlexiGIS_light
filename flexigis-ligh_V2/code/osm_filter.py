import geopandas as gpd
import pandas as pd
import numpy as np
import os
from pathlib import Path


def make_directory():
    destination = "../data/02_urban_output_data/"
    if Path(destination).exists():
        pass
    else:
        os.mkdir(destination)


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


# Filter highway lines
def filter_highway_lines(shp_file_lines, desitination_folder):
    highway_lines = gpd.read_file(shp_file_lines)
    highway_lines = highway_lines.to_crs({'init': 'epsg:3857'})
    # needed highway features
    highway_feature_lines = {'living_street', 'motorway', 'pedestrian',
                             'primary', 'secondary', 'service', 'tertiary',
                             'trunk', 'motorway_link', 'primary_link',
                             'secondary_link', 'tertiary_link',
                             'trunk_link'}

    width = [7.5, 15.50, 7.5, 10.5, 9.5, 7.5, 9.5, 9.5, 6.5, 6.5,
             6.5, 6.5, 6.5]
    highway_width = dict(zip(highway_feature_lines, width))

    highway_lines = highway_lines.loc[highway_lines["highway"].isin(
        highway_feature_lines)]
    highway_lines = highway_lines[["osm_id", "highway", "geometry"]]

    # compute line length and area
    highway_lines["length"] = highway_lines.geometry.length
    highway_lines = compute_area(highway_lines, highway_width)
    highway_lines = highway_lines.sort_values("highway")
    highway_lines.to_file(driver='ESRI Shapefile',
                          filename=desitination_folder+"osm_lines")
    print(highway_lines.head(20))

# Filter highway points


def filter_highway_points(shape_file_points, desitination_folder):

    highway_points = gpd.read_file(shape_file_points)
    highway_points = highway_points.to_crs({'init': 'epsg:3857'})
    highway_feature_points = {'bus_stop', 'crossing', 'stop;crossing',
                              'give_way', 'give_way;traffic_signals',
                              'motorway_junction', 'passing_place',
                              'platform', 'speed_camera', 'stop',
                              'street_lamp', 'traffic_signals',
                              'give_way;traffic_signals', 'traffic_sign',
                              'rest_area', 'speed_display', 'mini_roundabout',
                              'emergency_access_point'
                              }
    highway_points = highway_points.loc[highway_points["highway"].isin(
        highway_feature_points)]
    highway_points = highway_points[["osm_id", "highway", "geometry"]]
    highway_points = highway_points.sort_values("highway")
    highway_points.to_file(driver='ESRI Shapefile',
                           filename=desitination_folder+"osm_points")


# Filter highway shapes (polygons)
def filter_highway_shapes(shape_file_polygon, desitination_folder):
    highway_shapes = gpd.read_file(shape_file_polygon)
    highway_shapes = highway_shapes.to_crs({'init': 'epsg:3857'})

    # convert None entries to nan string
    #highway_shapes = highway_shapes.fillna(value=np.nan)
    highway_shapes = highway_shapes.loc[:, [
        "osm_way_id", "other_tags", "geometry"]]
    highway_shapes = highway_shapes[highway_shapes["other_tags"].notna()]
    highway_feature = {'crossing', 'footway', 'living_street',
                       'pedestrian', 'platform', 'residential',
                       'service', 'traffic_island'}

    # create a clean highway tag column
    tag_val = []
    tag = "highway"
    for i in highway_shapes.other_tags.values:
        if tag in i:
            tag_true = 1
            tag_val.append(tag_true)
        else:
            tag_false = 0
            tag_val.append(tag_false)

    highway_shapes["bool"] = tag_val
    highway_shapes = highway_shapes[highway_shapes["bool"] == 1]

    filter_tag = []
    for n in highway_shapes["other_tags"].values:
        ll = n.split(",")
        for lll in ll:
            if lll.startswith('"highway"'):
                filter_tag.append(lll)

    feature_list = []
    for i in filter_tag:
        m = i.split('"')
        feature_list.append(m[3])

    highway_shapes["highway"] = feature_list
    highway_shapes_df = highway_shapes.loc[highway_shapes["highway"].isin(
        highway_feature)]
    highway_shapes_df = highway_shapes_df[[
        "highway", "osm_way_id", "geometry"]]
    highway_shapes_df = highway_shapes_df.sort_values("highway")
    highway_shapes_df['area'] = highway_shapes_df.geometry.area
    highway_shapes_df.to_file(driver='ESRI Shapefile',
                              filename=desitination_folder+"osm_shapes")
    print(highway_shapes_df.head(20))


if __name__ == "__main__":
    input_path = "../data/01_raw_input_data/"
    desitination_folder = "../data/02_urban_output_data/"

    shp_lines = 'UrbanInfrastructure/lines.shp'
    shp_points = 'UrbanInfrastructure/points.shp'
    shp_shapes = 'UrbanInfrastructure/multipolygons.shp'
    # create output directory
    _ = make_directory()

    print("  === HIGHWAY LINES ====")
    shp_file_lines = os.path.join(input_path, shp_lines)
    filter_highway_lines(shp_file_lines, desitination_folder)

    print("============================")
    print("  === HIGHWAY POINTS ====")
    shp_file_points = os.path.join(input_path, shp_points)
    filter_highway_points(shp_file_points, desitination_folder)

    print("============================")
    print("  === HIGHWAY SHAPES ====")
    shp_file_shapes = os.path.join(input_path, shp_shapes)
    filter_highway_shapes(shp_file_shapes, desitination_folder)
