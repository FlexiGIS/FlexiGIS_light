"""Convert categorised csv file to shape file."""
import pandas as pd
from geopandas import GeoDataFrame
from shapely import wkt
import glob
import os
from pathlib import Path


def csv_to_shapefile():
    """Convert csv files of categorised OSM data to shape file."""
    shape_file_dest = "../data/02_urban_output_data/shape_files/"
    folder = "../data/02_urban_output_data/"

    # csv files
    csv_files = glob.glob(folder + "*.csv")
    for csv_file in csv_files:
        base_name = os.path.basename(csv_file)
        base_name = os.path.splitext(base_name)[0]
        print("Creating shape file for"+" "+str(base_name))
        df = pd.read_csv(csv_file, index_col=False)

        if "Unnamed: 0" in df:
            df = df.drop(columns=["Unnamed: 0"])

        df["geometry_shp"] = df["geometry"].apply(wkt.loads)
        gdf = GeoDataFrame(df, geometry="geometry_shp")
        gdf = gdf.drop(columns=["geometry"])
        gdf.rename(columns={"geometry_shp": "geometry"})
        # gdf.crs = {'init': 'epsg:4326'}
        # gdf = gdf.to_crs({'init': 'epsg:3857'})
        gdf.to_file(driver='ESRI Shapefile',
                    filename=shape_file_dest+base_name)

    print("INFO: Shape Files For OSM Categories Generated. See " + " " +
          shape_file_dest+" "+"for output files")


def shapeFile_dir():
    """Create shapefile directory."""
    folder = "../data/02_urban_output_data/"
    shape_file_dest = os.path.join(folder, "shape_files/")

    if Path(shape_file_dest).exists():
        pass
    else:
        os.mkdir(shape_file_dest)


if __name__ == "__main__":
    shapeFile_dir()
    csv_to_shapefile()
