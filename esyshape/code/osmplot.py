"""Plot shapes using geopandas."""
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd


def plot_line_poly(indir, legend_box, font_size,
                   fig_size, face_color):
    """Plot lines and poly."""
    geodata_lines = gpd.read_file(indir+"osm_lines/osm_lines.shp")
    geodata_polys = gpd.read_file(indir+"osm_poly/osm_poly.shp")
    geodata = pd.concat([geodata_lines[["highway", "geometry"]],
                         geodata_polys[["highway", "geometry"]]])

    fig, ax = plt.subplots(1, figsize=fig_size, facecolor=face_color)
    geodata.plot(column='highway', categorical=True, legend=True,
                 ax=ax, linewidth=1, cmap='tab20', edgecolor="0.8")

    leg = ax.get_legend()
    leg.set_title("highway")
    leg.set_bbox_to_anchor(legend_box)
    plt.title("Road infrastructure in Berlin", fontsize=font_size)
    plt.axis("off")
    # plt.savefig(outdir+"polygon.png", dpi=300)
    plt.show()


def plot_point(indir, legend_box, font_size,
               fig_size, face_color):
    """Plot points."""
    geodata_point = gpd.read_file(indir+"osm_points/osm_points.shp")
    fig, ax = plt.subplots(1, figsize=fig_size, facecolor=face_color)
    geodata_point.plot(column='highway', categorical=True, legend=True,
                       ax=ax, linewidth=1, cmap='Accent', edgecolor="0.8")

    leg = ax.get_legend()
    leg.set_title("highway")
    leg.set_bbox_to_anchor(legend_box)
    plt.title("Street light infrastructure in Berlin", fontsize=font_size)
    plt.axis("off")
    plt.show()

    # plt.savefig(destination+"points.png", facecolor=fig.get_facecolor(),
    #             dpi=300)


if __name__ == "__main__":
    indir = "../data/output_data/"
    outdir = "../data/output_data/"
    font_size = 15
    fig_size = (6, 4)
    legend_box = (0.0, 0.05, 0.01, 0.7)
    face_color = "white"
    print(" == Plot Of Highway Polygons and Lines ==")
    plot_line_poly(indir, legend_box, font_size,
                   fig_size, face_color)
    print(" == Plot Of Highway Points ==")
    plot_point(indir, legend_box, font_size,
               fig_size, face_color)
