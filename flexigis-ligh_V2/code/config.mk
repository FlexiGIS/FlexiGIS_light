#=================================================================================#
#              CONFIGURATION FILE												  #
#=================================================================================#
# 1. URL of the OSM raw data (used for OSM raw data download)
OSM_raw_data_URL:=https://download.geofabrik.de/europe/germany/berlin-latest.osm.pbf
# https://download.geofabrik.de/europe/germany/berlin.poly
# 2. Name of the OSM raw data file (used for data filtering by osmosis)
OSM_raw_data:=../data/01_raw_input_data/berlin-latest.osm.pbf

# 3. Name of the bounding polygon file (used for data filtering by osmosis)
#    Use other polyfiles for other spatial areas
polyfile:=../data/01_raw_input_data/berlin.poly

# 4. Name of the filtered OSM urban data file 
OSM_merged_data:=../data/01_raw_input_data/UrbanInfrastructure.osm.pbf
OSM_convert_data:=../data/01_raw_input_data/UrbanInfrastructure.o5m
OSM_filter_data:=../data/01_raw_input_data/UrbanInfrastructure.osm
shape_file:=../data/01_raw_input_data/UrbanInfrastructure

# 5. Location of the output folders
urban_output:=../data/02_urban_output_data
load_folder:=../data/03_energy_requirements/
visualization_folder:=../data/04_Visualization/
urban_requirements_dir:=../data/03_energy_requirements/

# 6. Weather data (25 km x 25 km) and Feedin calculation parameters
target_file:= ../data/01_raw_input_data/ERA5_data.nc
start_date:=2015-01-01
end_date:= 2015-12-31

region:= 1 #set region to 1 or 0, if you wish to download weather for a region or for single location
# For single coordinate or location (e.g single location in  Berlin)
lon_single_location:=13.1
lat_single_location:=52.3

# For download of weather data for a region (e.g: Berlin region)
# Longitude 'west'-'East' and Latitude 'North'-'South'
lon_region:= 13.1,13.6
lat_region:= 52.3,52.7

turbine_name:= E-101/3050
hub_height:= 135
wind_data:= wind_data.csv

pv_panel:= Advent_Solar_Ventura_210___2008_
inverter_type:= ABB__MICRO_0_25_I_OUTD_US_208__208V_
solar_data:= solar_data.csv