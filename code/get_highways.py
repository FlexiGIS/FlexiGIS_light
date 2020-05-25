"""Get Highway data from lines, polygons and points table in database.

and returns shape files for each.
"""
import pandas as pd
from db_connect import dbconn_from_args
import logging
import os
from pathlib import Path
from shapely import wkt
from geopandas import GeoDataFrame
import time

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                    filename="../code/log/flexigis_highways.log",
                    level=logging.DEBUG)

# output data destination
destination = "../data/02_urban_output_data/"
if Path(destination).exists():
    logging.info("directory {} already exists.".
                 format("02_urban_output_datas"))
    pass
else:
    os.mkdir(destination)
    logging.info("directory {} succesfully created!.".
                 format("02_urban_output_datas"))


def compute_area(dataset, width):
    """Compute area for each line feature and return a dataframe object.

    dataset: Dataframe object
    width: Dictionary, unique highway category as key and the width in meters
    as value.

    """
    Area = []
    for key, value in width.items():
        area = dataset.loc[key]["length"]*value
        Area.append(area)
    Area = pd.concat(Area)
    dataset["area"] = Area.values
    dataset_new = dataset.reset_index()
    return dataset_new


def data_to_file(dataset, name="name"):
    """Write data to csv/shape file.

    dataset: dataframe object
    name: str object, name of the output shape file (the table name).
    """
    dataset_new = dataset["geometry"].str.split(";", n=1, expand=True)
    dataset["polygon"] = dataset_new[1]
    dataset = dataset.drop(columns=["geometry"])
    dataset = dataset.rename(columns={"polygon": "geometry"})
    dataset["geometry"] = dataset["geometry"].apply(wkt.loads)
    gdf = GeoDataFrame(dataset, geometry="geometry")
    gdf.to_file(driver='ESRI Shapefile', filename=name)
    # dataset.to_csv(name, encoding="utf-8")


class GetLines:
    """Object class that gets data from database and export output to shapefile.

    get_line_from_db: returns querried database table as pandas dataframe.
    get_line_features: gets highway categories(lines), calculate thier area and
    returns dataset as shp file.
    """

    def get_line_from_db(self, cur, conn):
        """Query database and return data as dataframe."""
        # fetch high way column from db (line table)
        self.cur = cur
        self.conn = conn
        self.table = "planet_osm_line"
        self.ways_column = "highway"

        # query database
        # Convert postgres encoded geometric projection to EPSG:3857 format
        # EPSG:3857 is a Spherical Mercator projection coordinate system
        # popularized by web services such as Google and later OpenStreetMap.
        # https://wiki.openstreetmap.org/wiki/EPSG:3857
        sql = "SELECT osm_id, highway, ST_Length(ST_Transform(way, 3857)) as l,\
         ST_ASEWKT(ST_Transform(way, 3857)) as p FROM planet_osm_line"

        self.cur.execute(sql)
        self.rows = self.cur.fetchall()

        # save selected columns as pandas dataframe
        self.df = pd.DataFrame(self.rows, columns=["osm_id", self.ways_column,
                                                   "length", "geometry"])
        self.data = self.df.dropna().sort_values(by="highway")
        logging.info("line properties for highway extracted from database.")
        return self.data

    # get features from dataframe
    def get_line_features(self, dataset):
        """Get OSM Highway features."""
        self.highway_feature = ['living_street', 'motorway', 'pedestrian',
                                'primary', 'secondary', 'service', 'tertiary',
                                'trunk', 'motorway_link', 'primary_link',
                                'secondary_link', 'tertiary_link',
                                'trunk_link']
        self.width = [7.5, 15.50, 7.5, 10.5, 9.5, 7.5, 9.5, 9.5, 6.5, 6.5,
                      6.5, 6.5, 6.5]
        self.dataset = dataset.loc[dataset["highway"].
                                   isin(self.highway_feature)]
        self.new_data_ = self.dataset.set_index(["highway"])
        self._width_ = dict(zip(self.highway_feature, self.width))
        # compute area and save data to csv
        self.new_data_lines = compute_area(self.new_data_, self._width_)
        print(self.new_data_lines.info())
        # print(self.new_data_lines.groupby("highway").sum())
        data_to_file(self.new_data_lines, destination+self.table)
        # return data_to_file(new_data, destination+self.table+".csv")
        logging.info("shape file of line features generated.")


class GetPolygons:
    """Gets highway polygons from database and export output to shape.

    get_polygons_from_db: returns querried database table as pandas dataframe.
    get_polygons_features: returns shape file of highway categories(polygons).
    """

    def get_polygons_from_db(self, cur, conn):
        """Query database and return data as dataframe."""
        # fetch high way column from db (line table)
        self.cur = cur
        self.conn = conn
        self.table = "planet_osm_polygon"
        self.ways_column = "highway"

        sql = "SELECT osm_id, highway, ST_Area(ST_Transform(way, 3857)) a,\
         ST_ASEWKT(ST_Transform(way, 3857))as p FROM planet_osm_polygon"

        self.cur.execute(sql)
        self.rows = self.cur.fetchall()

        # save selected columns as pandas dataframe
        self.df = pd.DataFrame(self.rows, columns=[
            "osm_id", self.ways_column,
            "area", "geometry"])
        self.data = self.df.dropna().sort_values(by="highway")
        return self.data
        logging.info("polygon properties for highway extracted from database.")
    # get features from dataframe

    def get_polygons_features(self, dataset):
        """Get OSM Highway features."""
        self.highway_feature = ['crossing', 'footway', 'living_street',
                                'pedestrian', 'platform', 'residential',
                                'service', 'traffic_island']
        self.dataset = dataset.loc[dataset["highway"].
                                   isin(self.highway_feature)]
        self.new_data_polygons = self.dataset.set_index(["highway"])
        print(self.new_data_polygons.info())
        data_to_file(self.new_data_polygons, destination+self.table)
        logging.info("shape file for polygons generated.")


class GetPoints:
    """Gets highway points(Nodes) from database and export output to shape file.

    get_point_from_db: returns querried database table as pandas dataframe.
    get_point_features: returns shape file of highway categories(points)
    """

    def get_point_from_db(self, cur, conn):
        """Extract database table."""
        # fetch high way column from db (line table)
        self.cur = cur
        self.conn = conn
        self.table = "planet_osm_point"
        self.ways_column = "highway"

        # query database
        sql = "SELECT osm_id, highway,ST_ASEWKT(ST_Transform(way, 3857))as p,\
         ST_X(ST_Transform (way, 3857)) as Longitude,\
          ST_Y(ST_Transform(way, 3857)) as Latitude FROM planet_osm_point"

        self.cur.execute(sql)
        self.rows = self.cur.fetchall()

        # save selected columns as pandas dataframe
        self.df = pd.DataFrame(self.rows, columns=[
            "osm_id", self.ways_column, "geometry", "Longitude", "Latitude"])
        self.data = self.df.dropna().sort_values(by="highway")
        return self.data
        logging.info("Node properties for highway extracted from database.")
    # get features from dataframe

    def get_point_features(self, dataset):
        """Get OSM Highway features."""
        self.highway_feature = ['bus_stop', 'crossing', 'give_way',
                                'motorwyay_junction', 'passing_place',
                                'platform', 'speed_camera', 'stop',
                                'street_lamp', 'traffic_signals']
        self.dataset = dataset.loc[dataset["highway"].
                                   isin(self.highway_feature)]
        self.new_data_points = self.dataset.set_index(["highway"])
        print(self.new_data_points.info())
        data_to_file(self.new_data_points, destination+self.table)
        logging.info("shape file for points generated.")


if __name__ == "__main__":
    conn = dbconn_from_args()
    cur = conn.cursor()
    t1 = time.time()
    # get higways from lines
    print("  === HIGHWAY LINES ====")
    lines = GetLines()
    data_line = lines.get_line_from_db(cur, conn)
    lines.get_line_features(data_line)

    # get highway polygons
    print("  === HIGHWAY SHAPES ====")
    squares = GetPolygons()
    data_square = squares.get_polygons_from_db(cur, conn)
    squares.get_polygons_features(data_square)

    # get highway points
    print("  === HIGHWAY POINTS ====")
    points = GetPoints()
    data_point = points.get_point_from_db(cur, conn)
    points.get_point_features(data_point)
    t2 = time.time()
    total_time = round(t2-t1)
    print("INFO: Elapsed time = %ss" % (total_time))
