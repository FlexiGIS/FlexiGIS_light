
#=================================================================================#
#              CONFIGURATION FILE												  #
#=================================================================================#
# 1. URL of the OSM raw data (used for OSM raw data download)
OSM_raw_data_URL:=https://download.geofabrik.de/europe/germany/berlin-latest.osm.pbf
# https://download.geofabrik.de/europe/germany/berlin.poly
# 2. Name of the OSM raw data file (used for data filtering by osmosis)
OSM_raw_data:=../data/input_raw_data/berlin-latest.osm.pbf

# 3. Name of the bounding polygon file (used for data filtering by osmosis)
#    Use other polyfiles for other spatial areas
polyfile:=../data/input_raw_data/berlin.poly

# 4. Name of the filtered OSM urban data file (used for data export by osm2pgsql)
OSM_merged_data:=../data/input_raw_data/02-UrbanInfrastructure.osm.pbf

# 6. Location of the output folders
urban_output:=../data/output_data/osm_lines/osm_lines.shp
simulation_data:=../data/simulation_data/
