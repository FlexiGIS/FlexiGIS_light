# FlexiGIS-Light version 2+ (esy-osm-shape)

This FlexiGIS-Light version implements esy-osm-shape python package to filter OSM data. It bouycouts the use of database, hence generating a s shapely object of the required street tags for electricity demand simulation.

Before running the make commands in this module, first install [esy-osm-shape package](https://dlr-ve-esy.gitlab.io/esy-osm-shape/) in your python environment by running.

```console
(python_env) foo:~$ pip install esy-osmfilter

```
or if you are using the FlexiGIS-Light package for the first time do
```console
(python_env) foo:~$ pip install -r requirements.txt

```
afterwards cd into the code directory in your linux terminal and run

```console
(python_env) foo:~$ make all
```
The simulated street light load output are saved as csv files and urban geospatial data are .shp file.
