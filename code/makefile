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
#=================================================================================#
#              Definition of tasks                                                #
#=================================================================================#

.PHONY: all
.PHONY: download
.PHONY: filter_data
.PHONY: export_data
.PHONY: abstract_data
.PHONY: streetlight_load
.PHONY: drop_database

#=================================================================================#
#              Environment Variables                                              #
#=================================================================================#

all: drop_database download filter_data export_data abstract_data streetlight_load drop_database

#=================================================================================#
#              DOWNLOAD OSM DATASETS                                              #
#=================================================================================#

# Step1: Download the OSM raw geo urban data.
download:
	@echo "\n### Step1 ### \nDownload the OSM road infrastructure raw data from \n   '$(OSM_raw_data_URL)' \n and saving it to \n   '$(OSM_raw_data)':"
	@date >> log/download.log
	wget -nv -O $(OSM_raw_data) $(OSM_raw_data_URL) >> log/download.log 2>&1
	@echo "Done. Download OSM raw data" >> log/download.log
	#@date >> log/download.log
	@echo "--> Done. Download OSM raw data"

filter_data:
	@echo "\n### Filtering the OSM road infrastructure raw data for highways:"
	@date >> log/osmosis.log
	osmosis \
	--read-pbf file=$(OSM_raw_data) \
	--tag-filter accept-ways building=* --used-node \
	--bounding-polygon file=$(polyfile) \
	--buffer outPipe.0=building \
	--read-pbf file=$(OSM_raw_data) \
	--tag-filter accept-ways highway=* --used-node \
	--bounding-polygon file=$(polyfile) \
	--buffer outPipe.0=highway \
	--read-pbf file=$(OSM_raw_data) \
	--tag-filter accept-ways landuse=* --used-node \
	--bounding-polygon file=$(polyfile) \
	--buffer outPipe.0=landuse_1 \
	--read-pbf file=$(OSM_raw_data) \
	--tag-filter accept-relations landuse=* --used-node \
	--bounding-polygon file=$(polyfile) \
	--buffer outPipe.0=landuse_2 \
	--merge inPipe.0=landuse_1 inPipe.1=landuse_2 \
	--buffer outPipe.0=landuse_all \
	--merge inPipe.0=landuse_all inPipe.1=building \
	--buffer outPipe.0=landuse_building \
	--merge inPipe.0=landuse_building inPipe.1=highway \
	--write-pbf file=$(OSM_merged_data) >> log/osmosis.log 2>&1;
	#@touch log/filter.done
	@echo "osmosis data filtering done." >> log/osmosis.log
	@date >> log/osmosis.log
	@echo "--> Done. OSM filtered urban energy infrastructure"
#=================================================================================#
#              URBAN DATA EXPORT TO DATABASE                                      #
#=================================================================================#

# Step3: Export the Filtered OSM data to the Postgres Server.
export_data:
	@echo "\n### Step3 ### \nExporting the Filtered OSM data to Postgres Server:"
	@date >> log/database.log
	export PGPASSWORD=$(postgres_password); createdb -U $(postgres_user) -h $(postgres_host) $(postgres_database);
	export PGPASSWORD=$(postgres_password); $(osm2pgsql_bin) -r pbf --username=$(postgres_user) --database=$(postgres_database) --host=$(postgres_host) --port=$(postgres_port) -s \
	-C $(osm2pgsql_cache) --hstore --number-processes $(osm2pgsql_num_processes) $(OSM_merged_data);
	#@touch log/database_import.done
	@echo "OSM data export to database done." >> log/database.log
	@date >> log/osm2pgsql.log
	#@date >> log/database.log
	@echo "--> Done. FlexiGIS OSM data Export."

#=================================================================================#
#              ABSTRACTION AND DATA PROCESSING (HIGHWAY)                          #
#=================================================================================#

# Step4: Execute the abstraction script get_highways.py on the database created in Step3
abstract_data:
	@echo "\n### Step4 ### \nRunning the extraction script get_highways.py on the database '$(postgres_database)':"
	# log/abstraction.done: log/database_import.done
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
	@echo "--> Done. FlexiGIS Highways Data Abstraction."

#=================================================================================#
#              MODELLING URBAN ENERGY REQUIREMENT                                 #
#=================================================================================#

# Step5: Modelling urban energy requirements
streetlight_load:
	@echo "\n### Step5 ### \nModelling streetlight load and saving output as csv file to folder '$(load_folder)':"
	@date >> log/streetlight.log
	@if [ -e $(LINES_CSV) ]; then python street_lightload.py ; fi
	@echo "streetlight energy modelling done." >> log/streetlight.log
	@echo "--> Done. Saving load data as CSV files and Load profile plot as png"
#=================================================================================#
#              DROPPING                                                           #
#=================================================================================#

# If you wish to drop your database

drop_database:
	$(eval answer := $(shell read -r -p "Do you really want to delete the FlexiGIS database '$(postgres_database)'? Type 'yes' if you are sure you wish to continue: " ANSWER; echo $$ANSWER))
	@if [ "$(answer)" = "yes" ]; then if(dropdb --username=$(postgres_user) --port=$(postgres_port) --host=$(postgres_host) $(postgres_database)); then echo "The FlexiGIS database '$(postgres_database)' has been dropped."; fi else echo "\nDid not drop the FlexiGIS database '$(postgres_database)'."; fi

