###################################################################################
#   FlexiGIS_road_infrastructure                                                  #
#                                                                                 #
#   Copyright "2020" "DLR VE"                                                     #
#										  										  #
#   Licensed under the BSD-3-Clause, "New BSD License" or "Modified BSD License"  #
#                                                                                 #
#   Redistribution and use in source and binary forms, with or without            #
#   modification, are permitted provided that the following conditions are met:   #
#                                                                                 #
#   1. Redistributions of source code must retain the above copyright notice,     #
#      this list of conditions and the following disclaimer.                      #
#                                                                                 #
#   2. Redistributions in binary form must reproduce the above copyright notice,  #
#      this list of conditions and the following disclaimer in the documentation  #
#      and/or other materials provided with the distribution.                     #
#                                                                                 #
#   3. Neither the name of the copyright holder nor the names of its contributors #
#      may be used to endorse or promote products derived from this software      #
#      without specific prior written permission.                                 #
#                                                                                 #
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"   #
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE     #
#   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE#
#   DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE  #
#   FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL    #
#   DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR    #
#   SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER    #
#   CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, #
#   OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE #
#   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.          #
#                                                                                 #
#        https://opensource.org/licenses/BSD-3-Clause                             #
###################################################################################

# Change the following default values according to your respective system environment

# 1. URL of the OSM raw data (used for OSM raw data download)
OSM_raw_data_URL:=https://download.geofabrik.de/europe/germany/berlin-latest.osm.pbf
# https://download.geofabrik.de/europe/germany/berlin.poly
# 2. Name of the OSM raw data file (used for data filtering by osmosis)
OSM_raw_data:=../data/01_raw_input_data/berlin-latest.osm.pbf

# 3. Name of the bounding polygon file (used for data filtering by osmosis)
#    Use other polyfiles for other spatial areas
polyfile:=../data/01_raw_input_data/berlin.poly

# 4. Specify the location of the osmosis binary file and its (alternative)
#    temporary folder if more disk space is needed when filtering OSM raw data
#    For Mac OS systems it might be /usr/local/bin/osmosis
osmosis_bin:=../data/01_raw_input_data/osmosis/

# 5. Name of the filtered OSM urban data file (used for data export by osm2pgsql)
OSM_merged_data:=../data/01_raw_input_data/02-UrbanInfrastructure.osm.pbf

# 6. Name of the stylefile (used for data export by osm2pgsql)
stylefile:=../data/01_raw_input_data/urban.style

# 7. Specify the location of osm2pgsql binary file, the available cache (MB) and
#    number of processors used by osm2pgsql for data export to the database
#    For Mac OS systems it might be /usr/bin/osm2pgsql
osm2pgsql_bin:=/usr/bin/osm2pgsql
osm2pgsql_cache:=6000
osm2pgsql_num_processes:=1

# 8. PostgreSQL connection parameters:
#    The database will be created and hold the filtered OSM urban data
postgres_cluster:=9.1/main
postgres_database:=esy_Berlin_FlexiGIS_test_2020
postgres_user:=xxxx
postgres_port:=xxxxx
postgres_host:=xxxxx
postgres_password:=xxxxxx

# 9. Location of the output folders
urban_output:=../data/02_urban_output_data/
load_folder:=../data/03_urban_energy_requirements/
visualization_folder:=../data/04_Visualization/
urban_requirements_dir:=../data/03_urban_energy_requirements/

# 10. Weather data (25 km x 25 km) and Feedin calculation parameters
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
