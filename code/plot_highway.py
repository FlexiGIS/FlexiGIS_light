"""Read csv files and plot data using geopandas."""
# from shapely import wkt
import pandas as pd
# from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd


# def highway_to_geodata(df):
#     """Convert data from dataframe to geodatframe."""
#     df["polygon"] = df["geometry"].apply(wkt.loads)
#     df = GeoDataFrame(df, geometry='polygon')
#     df = df.drop(columns=["geometry"])
#     return df


def plot_line_polygon(_data_, destination, legend_box, font_size,
                      fig_size, face_color):
    """Plot lines and polygons."""
    geodata_highway = _data_
    fig, ax = plt.subplots(1, figsize=fig_size, facecolor=face_color)
    geodata_highway.plot(column='highway', categorical=True, legend=True,
                         ax=ax, linewidth=1, cmap='tab20', edgecolor="0.8")

    # ax.set_facecolor("whitesmoke")
    leg = ax.get_legend()
    leg.set_title("highway")
    leg.set_bbox_to_anchor(legend_box)
    plt.title("Road infrastructure in Berlin", fontsize=font_size)
    plt.axis("off")
    plt.savefig(destination+"roads.png", facecolor=fig.get_facecolor(),
                dpi=300)


def plot_lines(df_line, destination, legend_box, font_size,
               fig_size, face_color):
    """Plot lines."""
    geodata_line = df_line
    fig, ax = plt.subplots(1, figsize=fig_size, facecolor=face_color)
    geodata_line.plot(column='highway', categorical=True, legend=True,
                      ax=ax, linewidth=1, cmap='tab20', edgecolor="0.8")

    # ax.set_facecolor("whitesmoke")
    leg = ax.get_legend()
    leg.set_title("highway")
    leg.set_bbox_to_anchor(legend_box)
    plt.title("Road infrastructure in Berlin", fontsize=font_size)
    plt.axis("off")
    plt.savefig(destination+"lines.png", facecolor=fig.get_facecolor(),
                dpi=300)


def plot_point(df_point, destination, legend_box, font_size,
               fig_size, face_color):
    """Plot points."""
    geodata_point = df_point
    fig, ax = plt.subplots(1, figsize=fig_size, facecolor=face_color)
    geodata_point.plot(column='highway', categorical=True, legend=True,
                       ax=ax, linewidth=1, cmap='Accent', edgecolor="0.8")

    # ax.set_facecolor("whitesmoke")
    leg = ax.get_legend()
    leg.set_title("highway")
    leg.set_bbox_to_anchor(legend_box)
    plt.title("Street light infrastructure in Berlin", fontsize=font_size)
    plt.axis("off")
    plt.savefig(destination+"points.png", facecolor=fig.get_facecolor(),
                dpi=300)


def plot_polygon(df_polygon, destination, legend_box, font_size,

                 fig_size, face_color):
    """Plot polygons."""
    geodata_polygon = df_polygon
    fig, ax = plt.subplots(1, figsize=fig_size, facecolor=face_color)
    geodata_polygon.plot(column='highway', categorical=True, legend=True,
                         ax=ax, linewidth=1, cmap='Dark2', edgecolor="0.8")

    # ax.set_facecolor("whitesmoke")
    leg = ax.get_legend()
    leg.set_title("highway")
    leg.set_bbox_to_anchor(legend_box)
    plt.title("Road infrastructure in Berlin", fontsize=font_size)
    plt.axis("off")
    plt.savefig(destination+"polygon.png", facecolor=fig.get_facecolor(),
                dpi=300)


if __name__ == "__main__":
    # input and output directories
    destination = "../data/04_Visualisation/"
    input_destination = "../data/02_urban_output_data/"
    line_csv = input_destination+"planet_osm_line/planet_osm_line.shp"
    point_csv = input_destination+"planet_osm_point/planet_osm_point.shp"
    polygon_csv = input_destination+"planet_osm_polygon/planet_osm_polygon.shp"

    # read shp files
    df_line = gpd.read_file(line_csv)
    df_point = gpd.read_file(point_csv)
    df_polygon = gpd.read_file(polygon_csv)
    _data_ = pd.concat([df_line.loc[:, ["highway", "geometry"]],
                        df_polygon.loc[:, ["highway", "geometry"]]])

    sns.set_style("dark")
    sns.set_context("notebook", font_scale=0.8, rc={"lines.linewidth": 1.5})
    legend_box = (0.0, 0.05, 0.01, 0.7)
    font_size = 15
    fig_size = (8, 5)
    face_color = "whitesmoke"

    plot_point(df_point, destination, legend_box, font_size,
               fig_size, face_color)
    plot_line_polygon(_data_, destination, legend_box, font_size,
                      fig_size, face_color)
