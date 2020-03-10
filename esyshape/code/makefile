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
#              Definition of tasks                                                #
#=================================================================================#
.PHONY: all
.PHONY: download
.PHONY: pbf_data
.PHONY: filter
.PHONY: streetlight
.PHONY: osm_plot

#=================================================================================#
#              Environment Variables                                              #
#=================================================================================#
all: download pbf_data filter streetlight osm_plot

#=================================================================================#
#              DOWNLOAD OSM DATASETS                                              #
#=================================================================================#
# Step1: Download the OSM raw geo urban data.
download:
	@echo "\nSTEP 1 \n:"
	@echo "INFO: DOWNLOAD OSM PBF"
	wget -nv -O $(OSM_raw_data) $(OSM_raw_data_URL)
	@echo "INFO: OSM DATA DOWNLOAD DONE."

#=================================================================================#
#              GET BOUNDING REGION USING POLY FILE                                #
#=================================================================================#
pbf_data:
	@echo "\nSTEP 2 \n:"
	@echo "INFO: FILTER PBF FILE WITH BOUNDING POLY FILE"
	osmosis \
	--read-pbf file=$(OSM_raw_data) \
	--bounding-polygon file=$(polyfile) \
	--tag-filter accept-ways highway=* \
	--write-pbf file=$(OSM_merged_data)
	@echo "INFO: URBAN INFRASTRUCTURE PBF FILE GENERATED FROM POLY FILE"

#=================================================================================#
#              URBAN DATA ABSTRACTION                                     		  #
#=================================================================================#
# Step3: Export to esy-OSM filter.
filter:
	@echo "\nSTEP 3 \n:"
	@echo "INFO: FILTER URBAN INFRASTRUCTURE PBF FILE USING: esy-osm-shape"
	@ if [ -e $(OSM_merged_data) ]; then python esy_shape.py; fi
	@echo "INFO: HIGHWAY FILTERING DONE"

#=================================================================================#
#             URBAN ENERGY DEMAND SIMULATION                       				  #
#=================================================================================#
# Step4: Modelling urban energy requirements
streetlight:
	@echo "\n STEP 4: \n Streetlight Load: output as csv file in folder '$(simulation_data)'"
	@if [ -e $(urban_output) ]; then python street_scenarios.py ; fi
	@echo "INFO: STREET LOAD SIMULATION COMPLETE."

#=================================================================================#
#              OSM DATA PLOT		                        					  #
#=================================================================================#
osm_plot:
	@echo "\nSTEP 4  \n:"
	@echo "INFO: PLOT OSM DATA "
	@ if [ -e $(urban_output) ]; then python osmplot.py ; fi
