###################################################################################
#   FlexiGIS                                                                      #
#                                                                                 #
#   Copyright "2020" "DLR VE"                                                     #
#										  #
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

#=================================================================================#
#              Setting the config file                                            #
#=================================================================================#

config:=config.mk
include $(config)
#=================================================================================#
#              Output Files                                                       #
#=================================================================================#

LINES_CSV:= $(urban_output)/planet_osm_line.csv
POLYGONS_CSV:= $(urban_output)/planet_osm_polygon.csv
POINT_CSV:= $(urban_output)/planet_osm_point.csv
COMMODITIES:=$(urban_requirements_dir)/optimization-commodities.csv
#=================================================================================#
#              Definition of tasks                                                #
#=================================================================================#

.PHONY: all
.PHONY: download
.PHONY: filter_data
.PHONY: export_data
.PHONY: abstract_data
.PHONY: streetlight_load
.PHONY: shapefile
.PHONY: drop_database
.PHONY: weather_data
.PHONY:	feedin_data_format
.PHONY: feedin
.PHONY: optimization

#=================================================================================#
#              Environment Variables                                              #
#=================================================================================#

all: drop_database download filter_data export_data abstract_data streetlight_load feedin optimization

#=================================================================================#
#              DOWNLOAD OSM DATASETS                                              #
#=================================================================================#

# Step1: Download the OSM raw geo urban data.
download:
	@echo "\n STEP 1: \nDownload the OSM road infrastructure raw data from \n '$(OSM_raw_data_URL)' \n and saving it to \n '$(OSM_raw_data)':"
	@date >> log/download.log
	wget -nv -O $(OSM_raw_data) $(OSM_raw_data_URL) >> log/download.log 2>&1
	@echo "Done. Download OSM raw data" >> log/download.log
	@echo "--> Done. Download OSM raw data"

filter_data:
	@echo "\n STEP 2: \nFILTERING PBF FILE WITH BOUNDING POLY FILE"
	@date >> log/osmosis.log
	osmosis \
	--read-pbf file=$(OSM_raw_data) \
	--bounding-polygon file=$(polyfile) \
	--tag-filter accept-ways highway=* \
	--write-pbf file=$(OSM_merged_data) >> log/osmosis.log 2>&1;
	@echo "osmosis data filtering done." >> log/osmosis.log
	@date >> log/osmosis.log
	@echo "INFO: URBAN INFRASTRUCTURE PBF FILE GENERATED FROM POLY FILE"
#=================================================================================#
#              URBAN DATA EXPORT TO DATABASE                                      #
#=================================================================================#

# Step3: Export the Filtered OSM data to the Postgres Server.
export_data:
	@echo "\n STEP 3: \nExporting the Filtered OSM data to Postgres Server"
	@date >> log/database.log
	export PGPASSWORD=$(postgres_password); createdb -U $(postgres_user) -h $(postgres_host) $(postgres_database);
	export PGPASSWORD=$(postgres_password); $(osm2pgsql_bin) -r pbf --username=$(postgres_user) --database=$(postgres_database) --host=$(postgres_host) --port=$(postgres_port) -s \
	-C $(osm2pgsql_cache) --hstore --number-processes $(osm2pgsql_num_processes) $(OSM_merged_data);
	#@touch log/database_import.done
	@echo "OSM data export to database done." >> log/database.log
	@date >> log/osm2pgsql.log
	#@date >> log/database.log
	@echo "INFO: GEO-DATA EXPORT TO POSTGRES DATABASE COMPLETE."

#=================================================================================#
#              ABSTRACTION AND DATA PROCESSING (HIGHWAY)                          #
#=================================================================================#

# Step4: Execute the abstraction script get_highways.py on the database created in Step3
abstract_data:
	@echo "\n STEP 4: \n Running the abstraction script on '$(postgres_database)':"
	@date >> log/abstract.log
	@if [ $(postgres_password) =  ]; \
	then \
	python get_highways.py -U $(postgres_user) -P $(postgres_port) -H $(postgres_host) -D $(postgres_database) ;\
	else \
	python get_highways.py -U $(postgres_user) -P $(postgres_port) -H $(postgres_host) -D $(postgres_database) -X $(postgres_password) ; \
	fi
	@echo "highway data abstraction done." >> log/abstract.log
	@if [ -e $(POLYGONS_CSV) ]; then python plot_highway.py ; fi
	@echo "highway plots generated." >> log/abstract.log
	@echo "INFO: HIGHWAY GEO_DATA ABSTRACTION COMPLETE."

#=================================================================================#
#             CREATE SHAPEFILE FROM  GEOREFERENCED CSV FILE                       #
#=================================================================================#
# if you wish to generate shape files for interactive visualisation on QGIS
shapefile:
	@echo "\n STEP 6: \n Convert Georeferenced csv files to shape files ###"
	@if [ -e $(LINES_CSV) ]; then python create_shapefile.py; fi
	@echo "INFO: HIGHWAYS SHAPE FILE CREATED."


#=================================================================================#
#              MODELLING URBAN ENERGY REQUIREMENT                                 #
#=================================================================================#

# Step5: Modelling urban energy requirements
streetlight_load:
	@echo "\n STEP 5: \n Modelling Streetlight Load and saving utput as csv file to folder '$(load_folder)':"
	@date >> log/streetlight.log
	@if [ -e $(LINES_CSV) ]; then python street_scenarios.py ; fi
	@echo "streetlight energy modelling done." >> log/streetlight.log
	@echo "INFO: STREET LOAD SIMULATION COMPLETE."


#=================================================================================#
#              DOWNLOAD ERA5 WEATHER DATA                                         #
#=================================================================================#
weather_data:
	@echo "\n *** Getting ERA5 weather data from Climate Data Store (CDS) ***"
	@if [ "$(region)" = "True" ];\
	then python weather_data.py $(lon_region) $(lat_region) $(target_file) $(start_date) $(end_date) $(region); \
	else \
	python weather_data.py $(lon_single_location) $(lat_single_location) $(target_file) $(start_date) $(end_date) $(region);\
	fi
	@echo "INFO: see ../data/01_raw_input_data, for output netcdf"


#=================================================================================#
#              GENERATE WIND AND SOLAR FEEDIN TIMESERIES                          #
#=================================================================================#
feedin_data_format:
	@echo "\n Weather data in Feedinlib format"
	@if [ -e $(target_file) ]; then python data_format.py $(lon_single_location) $(lat_single_location) $(target_file); fi
	@echo "INFO: see ../data/01_raw_input_data, for csv files of weather data"

#=================================================================================#
#              GENERATE WIND AND SOLAR FEEDIN TIMESERIES                          #
#=================================================================================#
feedin:
	@echo "\n Feedin generation from wind and solar"
	@if [ -e $(target_file) ]; then python feedin.py $(lon_single_location) $(lat_single_location) $(solar_data) $(wind_data) $(turbine_name) $(pv_panel) $(inverter_type) $(hub_height) ; fi
	@echo "INFO: see ../data/01_raw_input_data, for csv files of output power data"


optimization:
	@echo "\n Optimization of Storage and Supply"
	@if [ -e $(COMMODITIES) ]; then python optimize.py ; fi
	@echo "Info: Done!"


#=================================================================================#
#              DROPPING                                                           #
#=================================================================================#
# If you wish to drop your database
drop_database:
	$(eval answer := $(shell read -r -p "Do you really want to delete the FlexiGIS database '$(postgres_database)'? Type 'yes' or 'y' if you are sure you wish to continue: " ANSWER; echo $$ANSWER))
	@if [ "$(answer)" = "yes" ] || [ "$(answer)" = "y" ]; then if(dropdb --username=$(postgres_user) --port=$(postgres_port) --host=$(postgres_host) $(postgres_database)); then echo "The FlexiGIS database '$(postgres_database)' has been dropped."; fi else echo "\nDid not drop the FlexiGIS database '$(postgres_database)'."; fi
