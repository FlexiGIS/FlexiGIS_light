
"""Generate OSM data using esy-osm-shape."""
import shapely.geometry as shg
import esy.osm.pbf
import esy.osm.shape as esys
from json import dumps
from shapely.geometry import mapping, shape
import pandas as pd
import json
from shapely import wkt
import geopandas


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


def esyShape(osm_File_Name="02-UrbanInfrastructure.osm.pbf"):
    """Get highway shapely object from esy_osm_shape."""
    print("Getting Highway Shapely Object From esy-osm-shape")
    datapath = "../data/input_raw_data/"
    data = datapath+osm_File_Name
    shape_ = esys.Shape(data)
    highway = [
        obj
        for obj in shape_(
            lambda e: e.tags.get('highway') is not None and
            (type(e) is not esy.osm.pbf.Relation or 'multipolygon' in e.tags))
        if obj is not None
    ]
    return highway


def esyPoints(highway, outdir="../data/output_data/"):
    """Get osm points from highway tags."""
    print("Getting Points From Highway Shapely Object")
    highway_point = [s for s in highway if type(s) is shg.Point]
    _points_ = {'bus_stop', 'crossing', 'give_way',
                'motorwyay_junction', 'passing_place',
                'platform', 'speed_camera', 'stop',
                'street_lamp', 'traffic_signals'}

    # get OSM id of points
    id_point = [i.id
                for i in highway_point
                if i.tags["highway"] in _points_
                ]
    # get OSM tags of interest
    tags_point = [
        i.tags["highway"]
        for i in highway_point
        if i.tags["highway"] in _points_
    ]
    # get OSM geometry for points
    geometry_point = [
        dumps(mapping(i))
        for i in highway_point
        if i.tags["highway"] in _points_
    ]
    # convert geometry to valid geometry for geopandas
    coord_point = [
        str(shape(json.loads(j)))
        for j in geometry_point
    ]
    # create a dataframe of selected tags
    df_point = pd.DataFrame(
        {'OSM-id': id_point,
         'highway': tags_point,
         'geometry': coord_point
         })
    # convert dataframe to geodataframe and save output to shape file
    df_point["geometry"] = df_point["geometry"].apply(wkt.loads)
    geodata_points = geopandas.GeoDataFrame(df_point, geometry="geometry")
    geodata_points.crs = {'init': 'epsg:4326'}
    geodata_points = geodata_points.to_crs({'init': 'epsg:3857'})
    # geodata_points.to_file(outdir+"osm_points.geojson", driver='GeoJSON')
    geodata_points.to_file(driver='ESRI Shapefile',
                           filename=outdir+"osm_points")
    print(geodata_points.info())
    # return geodata_points


def esyLines(highway, outdir="../data/output_data/"):
    """Get osm points from highway tags."""
    print("Getting Lines From Highway Shapely Object")
    highway_line = [s for s in highway if type(s) is shg.LineString]
    # lines
    _lines_ = ['living_street', 'motorway', 'pedestrian',
               'primary', 'secondary', 'service', 'tertiary',
               'trunk', 'motorway_link', 'primary_link',
               'secondary_link', 'tertiary_link', 'trunk_link']
    highway_width = [7.5, 15.50, 7.5, 10.5, 9.5, 7.5, 9.5, 9.5, 6.5, 6.5,
                     6.5, 6.5, 6.5]
    street_widthmap = dict(zip(_lines_, highway_width))
    id_line = [i.id
               for i in highway_line
               if i.tags["highway"] in _lines_
               ]

    tags_line = [
        i.tags["highway"]
        for i in highway_line
        if i.tags["highway"] in _lines_
    ]

    geometry_line = [
        dumps(mapping(i))
        for i in highway_line
        if i.tags["highway"] in _lines_
    ]

    coord_line = [
        str(shape(json.loads(j)))
        for j in geometry_line
    ]

    df_lines = pd.DataFrame(
        {'OSM-id': id_line,
         'highway': tags_line,
         'geometry': coord_line
         })
    df_lines["geometry"] = df_lines["geometry"].apply(wkt.loads)
    geodata_lines = geopandas.GeoDataFrame(df_lines, geometry="geometry")
    geodata_lines.crs = {'init': 'epsg:4326'}
    geodata_lines = geodata_lines.to_crs({'init': 'epsg:3857'})
    # compute highway tags length
    geodata_lines["length"] = geodata_lines.geometry.length
    geodata_lines = geodata_lines.sort_values("highway")
    # compute highway tags area based on their width
    geodata_lines = compute_area(geodata_lines, street_widthmap)
    # geodata_lines.to_file(outdir+"osm_lines.geojson", driver='GeoJSON')
    geodata_lines.to_file(driver='ESRI Shapefile',
                          filename=outdir+"osm_lines")
    print(geodata_lines.info())


def esyPolygons(highway, outdir="../data/output_data/"):
    """Get osm polygons from highway tags."""
    print("Getting Polygons From Highway Shapely Object")
    highway_polygon = [s for s in highway if type(s) is shg.Polygon]
    # highway_multipoly = [s for s in highway if type(s) is shg.MultiPolygon]
    # polygons
    _polys_ = {'crossing', 'footway', 'living_street',
               'pedestrian', 'platform', 'residential',
               'service', 'traffic_island'}
    id_poly = [i.id
               for i in highway_polygon
               if i.tags["highway"] in _polys_
               ]

    tags_poly = [
        i.tags["highway"]
        for i in highway_polygon
        if i.tags["highway"] in _polys_
    ]

    geometry_poly = [
        dumps(mapping(i))
        for i in highway_polygon
        if i.tags["highway"] in _polys_
    ]

    coord_poly = [
        str(shape(json.loads(j)))
        for j in geometry_poly
    ]

    df_poly = pd.DataFrame(
        {'OSM-id': id_poly,
         'highway': tags_poly,
         'geometry': coord_poly
         })

    df_poly["geometry"] = df_poly["geometry"].apply(wkt.loads)
    geodata_polys = geopandas.GeoDataFrame(df_poly, geometry="geometry")
    geodata_polys.crs = {'init': 'epsg:4326'}
    geodata_polys = geodata_polys.to_crs({'init': 'epsg:3857'})
    geodata_polys["area"] = geodata_polys.geometry.area
    # geodata_polys.to_file(outdir+"osm_poly.geojson", driver='GeoJSON')
    geodata_polys.to_file(driver='ESRI Shapefile',
                          filename=outdir+"osm_poly")

    print(geodata_polys.info())


if __name__ == "__main__":
    highway = esyShape(osm_File_Name="02-UrbanInfrastructure.osm.pbf")

    print("============================")
    print(" --- Highway Points --- ")
    print("============================")

    esyPoints(highway)

    print("============================")
    print(" --- Highway Lines --- ")
    print("============================")

    esyLines(highway)

    print("============================")
    print(" --- Highway Polygons --- ")
    print("============================")

    esyPolygons(highway)
