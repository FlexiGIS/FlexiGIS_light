"""Read csv files and plot data using geopandas."""
from shapely import wkt
import pandas as pd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
import seaborn as sns

# input and output directories
destination = "../data/04_Visualisation/"
input_destination = "../data/02_urban_output_data/"
line_csv = input_destination+"planet_osm_line.csv"
point_csv = input_destination+"planet_osm_point.csv"
polygon_csv = input_destination+"planet_osm_polygon.csv"

# read csv files
df_line = pd.read_csv(line_csv, index_col=None)
df_point = pd.read_csv(point_csv, index_col=None)
df_polygon = pd.read_csv(polygon_csv, index_col=None)

# Merge all csv files
# _data_all = pd.concat([df_line.loc[:, ["highway", "polygon"]],
#                        df_point.loc[:, ["highway", "polygon"]],
#                        df_polygon.loc[:, ["highway", "polygon"]]])

# Merge line and polygon data
_data_ = pd.concat([df_line.loc[:, ["highway", "polygon"]],
                    df_polygon.loc[:, ["highway", "polygon"]]])


def highway_to_geodata(df):
    """Convert data from dataframe to geodatframe."""
    df["polygon1"] = df["polygon"].apply(wkt.loads)
    df = GeoDataFrame(df, geometry='polygon1')
    df = df.drop(columns=["polygon"])
    return df


def plot_line_polygon():
    """Plot lines and polygons."""
    geodata_highway = highway_to_geodata(_data_)
    fig, ax = plt.subplots(1, figsize=(10, 8))
    geodata_highway.plot(column='highway', categorical=True, legend=True,
                         ax=ax, linewidth=1, cmap='tab20', edgecolor="0.8")

    leg = ax.get_legend()
    leg.set_title("highway")
    leg.set_bbox_to_anchor((0.0, 0.05, 0.01, 0.9))
    plt.title("Highway", fontsize=30)
    plt.axis("off")
    plt.savefig(destination+"roads.png", dpi=300)


def plot_lines():
    """Plot lines."""
    geodata_line = highway_to_geodata(df_line)
    fig, ax = plt.subplots(1, figsize=(10, 8))
    geodata_line.plot(column='highway', categorical=True, legend=True,
                      ax=ax, linewidth=1, cmap='tab20', edgecolor="0.8")

    leg = ax.get_legend()
    leg.set_title("highway")
    leg.set_bbox_to_anchor((0.0, 0.05, 0.01, 0.9))
    plt.title("Highway Lines", fontsize=30)
    plt.axis("off")
    plt.savefig(destination+"lines.png", dpi=300)


def plot_point():
    """Plot points."""
    geodata_point = highway_to_geodata(df_point)
    fig, ax = plt.subplots(1, figsize=(10, 8))
    geodata_point.plot(column='highway', categorical=True, legend=True,
                       ax=ax, linewidth=1, cmap='Accent', edgecolor="0.8")

    leg = ax.get_legend()
    leg.set_title("highway")
    leg.set_bbox_to_anchor((0.0, 0.05, 0.01, 0.9))
    plt.title("Street light infrastructure in Berline", fontsize=30)
    plt.axis("off")
    plt.savefig(destination+"points.png", dpi=300)


def plot_polygon():
    """Plot polygons."""
    geodata_polygon = highway_to_geodata(df_polygon)
    fig, ax = plt.subplots(1, figsize=(10, 8))
    geodata_polygon.plot(column='highway', categorical=True, legend=True,
                         ax=ax, linewidth=1, cmap='Dark2', edgecolor="0.8")

    leg = ax.get_legend()
    leg.set_title("highway")
    leg.set_bbox_to_anchor((0.0, 0.05, 0.01, 0.9))
    plt.title("Road infrastructure in Berlin", fontsize=30)
    plt.axis("off")
    plt.savefig(destination+"polygon.png", dpi=300)


if __name__ == "__main__":
    sns.set_style("dark")
    sns.set_context("notebook", font_scale=0.8, rc={"lines.linewidth": 1.5})
    plot_point()
    plot_line_polygon()
