"""Plot shapes using geopandas."""
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import seaborn as sns


def plot_line_poly(indir, legend_box, font_size,
                   fig_size, face_color):
    """Plot lines and poly."""
    geodata_lines = gpd.read_file(indir+"osm_lines/osm_lines.shp")
    geodata_polys = gpd.read_file(indir+"osm_shapes/osm_shapes.shp")
    geodata = pd.concat([geodata_lines[["highway", "geometry"]],
                         geodata_polys[["highway", "geometry"]]])

    fig, ax = plt.subplots(1, figsize=fig_size, facecolor=face_color)
    geodata.plot(column='highway', categorical=True, legend=True,
                 ax=ax, linewidth=0.8, cmap='tab20', edgecolor="0.8")

    leg = ax.get_legend()
    leg.set_title("highway")
    leg.set_bbox_to_anchor(legend_box)
    plt.title("Road infrastructure in Berlin", fontsize=font_size)
    plt.axis("off")
    plt.savefig(indir+"polygon.png", dpi=300)


def plot_point(indir, legend_box, font_size,
               fig_size, face_color):
    """Plot points."""
    geodata_point = gpd.read_file(indir+"osm_points/osm_points.shp")
    fig, ax = plt.subplots(1, figsize=fig_size, facecolor=face_color)
    geodata_point.plot(column='highway', categorical=True, legend=True,
                       ax=ax, linewidth=0.8, cmap='Accent', edgecolor="0.8")

    leg = ax.get_legend()
    leg.set_title("highway")
    leg.set_bbox_to_anchor(legend_box)
    plt.title("Street light infrastructure in Berlin", fontsize=font_size)
    plt.axis("off")
    plt.savefig(indir+"points.png", facecolor=fig.get_facecolor(),
                dpi=300)


if __name__ == "__main__":
    dir_path = "../data/02_urban_output_data/"
    sns.set_style("dark")
    sns.set_context("notebook", font_scale=0.5, rc={"lines.linewidth": 1})
    font_size = 12
    fig_size = (8, 5)
    legend_box = (0.0, 0.02, 0.02, 0.7)
    face_color = "white"
    print(" == Plot Of Highway Polygons and Lines ==")
    plot_line_poly(dir_path, legend_box, font_size,
                   fig_size, face_color)
    print(" == Plot Of Highway Points ==")
    plot_point(dir_path, legend_box, font_size,
               fig_size, face_color)
