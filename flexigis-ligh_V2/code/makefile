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
#              Output Variables                                                   #
#=================================================================================#

LINES_SHP:= $(urban_output)/osm_lines/osm_lines.shp
POLYGONS_SHP:= $(urban_output)/osm_shapes/osm_shapes.shp
POINT_SHP:= $(urban_output)/osm_points/osm_points.shp
COMMODITIES:=$(urban_requirements_dir)/optimization-commodities.csv
#=================================================================================#
#              Definition of tasks                                                #
#=================================================================================#
.PHONY: all
.PHONY: download
.PHONY: pbf_data
.PHONY: filter
.PHONY: abstraction
.PHONY: osm_plot
.PHONY: weather_data
.PHONY: feedin_data_format
.PHONY: feedin

all: download pbf_data filter abstraction osm_plot weather_data feedin_data_format feedin

#=================================================================================#
#              DOWNLOAD OSM DATASETS                                              #
#=================================================================================#
# Step1: Download the OSM raw geo urban data.
download:
	@echo "\nSTEP 1 \n:"
	@echo "INFO: Download OSM pbf file"
	wget -nv -O $(OSM_raw_data) $(OSM_raw_data_URL)
	@echo "INFO: OSM DATA DOWNLOAD DONE."
	@echo "===================================="

#=================================================================================#
#              GET BOUNDING REGION USING POLY FILE                                #
#=================================================================================#
pbf_data:
	@echo "\nSTEP 2 \n:"
	@echo "INFO: Filter pbf file using a bounding poly file"
	osmosis \
	--read-pbf file=$(OSM_raw_data) \
	--bounding-polygon file=$(polyfile) \
	--tag-filter accept-ways highway=* \
	--write-pbf file=$(OSM_merged_data)
	@echo "INFO: Filtered pbf file generated"
	@echo "===================================="
#=================================================================================#
#              URBAN DATA FILTER                                     		     #
#=================================================================================#
filter:
	@echo "\nSTEP 3 \n:"
	@echo "Filter osm data and genrate shape file"
	osmconvert $(OSM_merged_data) -o=$(OSM_convert_data)
	osmfilter $(OSM_convert_data) --keep="highway=" -o=$(OSM_filter_data)
	ogr2ogr -skipfailures -f "ESRI Shapefile" $(shape_file) $(OSM_filter_data)
	@echo "INFO: Filtered Urban infrastructure shape files Generated"
	@echo "===================================="
#=================================================================================#
#              URBAN DATA ABSTRACTION                                     	  #
#=================================================================================#
# Step3: Classify highway features
abstraction:
	@echo "\nSTEP 4 \n:"
	@echo "INFO: ABSTRACT URBAN INFRASTRUCTURES FOR HiGHWAY "
	@ if [ -e $(OSM_filter_data) ]; then python osm_filter.py; fi
	@echo "INFO: highway abstraction done"
	@echo "===================================="

#=================================================================================#
#              OSM DATA PLOT		                        					  #
#=================================================================================#
osm_plot:
	@echo "INFO: Plot classified OSM data"
	@ if [ -e $(urban_output) ]; then python osmplot.py ; fi
	@echo "===================================="

#=================================================================================#
#              DOWNLOAD ERA5 WEATHER DATA                                         #
#=================================================================================#
weather_data:
	@echo "\nSTEP 5 \n:"
	@echo "\n *** Getting ERA5 weather data from Climate Data Store (CDS) ***"
	@ echo "weather data region checker: $(region)"
	@if [ "$(region)" -eq 1 ];\
	then python weather_data.py $(lon_region) $(lat_region) $(target_file) $(start_date) $(end_date) $(region); \
	else \
	python weather_data.py $(lon_single_location) $(lat_single_location) $(target_file) $(start_date) $(end_date) $(region); \
	fi
	@echo "INFO: see ../data/01_raw_input_data, for output netcdf"
	@echo "===================================="

#=================================================================================#
#              GENERATE WIND AND SOLAR FEEDIN TIMESERIES                          #
#=================================================================================#
feedin_data_format:
	@echo "\nSTEP 6 \n:"
	@echo "\n Weather data in Feedinlib format"
	@if [ -e $(target_file) ]; then python data_format.py $(lon_single_location) $(lat_single_location) $(target_file); fi
	@echo "INFO: see ../data/01_raw_input_data, for csv files of weather data"
	@echo "===================================="

#=================================================================================#
#              GENERATE WIND AND SOLAR FEEDIN TIMESERIES                          #
#=================================================================================#
feedin:
	@echo "\nSTEP 7 \n:"
	@echo "\n Feedin generation from wind and solar"
	@if [ -e $(target_file) ]; then python feedin.py $(lon_single_location) $(lat_single_location) $(solar_data) $(wind_data) $(turbine_name) $(pv_panel) $(inverter_type) $(hub_height) ; fi
	@echo "INFO: see ../data/01_raw_input_data, for csv files of output power data"
	@echo "===================================="

#=================================================================================#
#              MODELLING URBAN ENERGY REQUIREMENT                                 #
#=================================================================================#

# Step5: Modelling urban energy requirements
streetlight_load:
	@echo "\nSTEP 8 \n:"
	@echo "\n Modelling Streetlight Load and saving utput as csv file to folder '$(load_folder)':"
	@date >> log/streetlight.log
	@if [ -e $(LINES_SHP) ]; then python street_scenarios.py ; fi
	@echo "streetlight energy modelling done." >> log/streetlight.log
	@echo "INFO: Street load simulation complete."
	@echo "===================================="

#=================================================================================#
#              FEEDIN AND REQUIREMENT OPTIMIZATION                                #
#=================================================================================#
optimization:
	@echo "\nSTEP 8 \n:"
	@echo "\n Optimization of Storage and Supply"
	@if [ -e $(COMMODITIES) ]; then python optimize.py ; fi
	@echo "Info: Done!"
	@echo "===================================="
