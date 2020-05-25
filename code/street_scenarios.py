"""Generate street light loads timeseries for the aggregated area."""
import pandas as pd
import matplotlib.pyplot as plt
import logging
import os
from pathlib import Path
import geopandas as gpd
import time


class simulateStreetLight:
    """Simulate street light Electricity demand."""

    def configuration(self):
        """Generate street light load time series."""
        self.input_path = "../data/01_raw_input_data/"
        self.input_path2 = "../data/02_urban_output_data/"
        self.output_path = "../data/03_urban_energy_requirements/"
        self.output_path_fig = "../data/04_Visualisation/"

        logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                            filename="../code/log/street_lightload.log",
                            level=logging.DEBUG)

        if Path(self.output_path).exists():
            logging.info("directory {} already exists.".
                         format("03_urban_energy_requirements"))
            pass
        else:
            os.mkdir(self.output_path)
            logging.info("directory {} succesfully created!.".
                         format("03_urban_energy_requirements"))

# soda=True
    def get_solarData(self):
        """Read solar data."""
        print("SOLAR DATA")
        self.soda = pd.read_csv(self.input_path +
                                '170906_Osternburg-SoDa.csv',
                                encoding="ISO-8859-1", delimiter=',')
        logging.info('read Soda csv file.')
        return self.soda

# Standardload=True

    def get_standardLoad(self):
        """Read standard load profile."""
        print('INFO: Normalise Standard Load Profiles')
        self.standardLoad = pd.read_csv(self.input_path+'SLP-2014.csv',
                                        delimiter=';')

        # SL1: All urban lights are operated as
        # - evening (16:15) - midnight (00:00) => 'On'
        # - midnight (00:15) - early morning  (05:15) => 'Off'
        #  - Early morning (05:30 )- morning (09:00) => 'On'
        self.SL1 = self.standardLoad['SB1'] / 1000

        # All urban roads are illuminated all night
        self.SL2 = self.standardLoad['SB2'] / 1000

        logging.info("Read and normalise Standard Load Profiles.")

# if EUIx=True
    def electricityUsageIndex(self):
        """Calculate electricity Usage Index."""
        print("INFO: Electricity Usage Index kwh/m2 per year")
        self.x_sl = 4 / 1000
        self.timestamp = self.standardLoad['Zeitstempel']

# if sl = True
    def simulateLoadAllRoad(self):
        """Simulate quarter load."""
        print('INFO: Simulate Street Light For Every 15mins')
        # get planet OSM data for highway (line and polygon)
        self.osmLines = gpd.read_file(
            self.input_path2+'planet_osm_line/planet_osm_line.shp')
        self.osmSquares = gpd.read_file(self.input_path2 +
                                        'planet_osm_polygon/planet_osm_polygon.shp')
        self.osmData = pd.concat([self.osmLines.loc[:, ["highway", "area"]],
                                  self.osmSquares.loc[:, ["highway", "area"]]],
                                 ignore_index=True)
        # for sxcenario 1 & 2
        self.osmArea = self.osmData["area"].sum()
        # scenario 3 => main roads only for all night
        mainRoads = ['living_street', 'motorway', 'pedestrian', 'primary',
                     'secondary', 'service', 'tertiary', 'trunk']
        self.mainRoadsArea = self.osmLines[self.osmLines["highway"].
                                           isin(mainRoads)]["area"].sum()
        # scenario 4 => minus the selected main roads
        # operated using SL1 (on and off)
        self.notMainRoadsArea = self.osmData[~self.osmData["highway"].
                                             isin(mainRoads)]["area"].sum()

# write calculated street-light load of different scenarios to csv
        _streetLoad_ = []
        fname = open(self.output_path+"streetlight_load.csv", 'w')
        fname.write('TIME;SB1[kWh];SB2[kWh];SB2_mainroad[kWh];SB1_rest[kWh]\n')
        for i, row in self.standardLoad.iterrows():
            row = str(self.timestamp[i]) + ';' + \
                str(self.osmArea*self.SL1[i]*self.x_sl) + ';' +\
                str(self.osmArea*self.SL2[i]*self.x_sl) + ';' +\
                str(self.mainRoadsArea*self.SL2[i]*self.x_sl) + ';' +\
                str(self.notMainRoadsArea*self.SL1[i]*self.x_sl) + '\n'
            _streetLoad_.append(row)
        fname.writelines(_streetLoad_)
        fname.close()

# plot scenario SB1
    def plotLoadScenario(self):
        """Calculate total street-light load and plot sample scenario."""
        df6 = pd.read_csv(self.output_path+"streetlight_load.csv",
                          delimiter=";", index_col='TIME', parse_dates=True)
        totalLoad_SB1 = df6['SB1[kWh]'].sum()
        totalLoad_SB2 = df6['SB2[kWh]'].sum()
        totalMainRoadLoad = df6['SB2_mainroad[kWh]'].sum()
        totalRestLoad_SB2 = df6['SB1_rest[kWh]'].sum()
        print("INFO: Total Street Light SB1-Load: "+str(totalLoad_SB1)+"kWh")
        print("INFO: Total street light SB2-Load: "+str(totalLoad_SB2)+"kWh")
        print("INFO: Total Main Roads SB2-load: "+str(totalMainRoadLoad)+"kWh")
        print("INFO: Total Load Excluding Main-roads SB1: " +
              str(totalRestLoad_SB2) + "kWh")

        # plot load profile
        fig, ax = plt.subplots(1, figsize=(8, 4), facecolor='whitesmoke')
        df6 = df6[["SB1[kWh]"]]
        df6["2014-01-01":"2014-01-15"].\
            plot(ax=ax, legend=False, color="royalblue",
                 title="Street-lighting load time-series")

        ax.set_facecolor("whitesmoke")
        plt.xlabel("Time [15 min.]")
        plt.ylabel("Load [kWh]")
        plt.savefig(self.output_path_fig +
                    "load_streetlight_planet_osm_line.png",
                    facecolor=fig.get_facecolor(), dpi=300)

        logging.info("Street. quarter hourly ERs simulated.")

    def simulate_Street_Light(self, soda=False, Standardload=True, EUIx=True,
                              sl=True):
        """Trigger methods for street light simulation."""
        self.configuration()
        if soda:
            self.get_solarData()

        if Standardload:
            self.get_standardLoad()

        if EUIx:
            self.electricityUsageIndex()

        if sl:
            self.simulateLoadAllRoad()
            self.plotLoadScenario()


if __name__ == "__main__":
    t1 = time.time()
    streelight_simulation = simulateStreetLight()
    streelight_simulation.simulate_Street_Light()
    t2 = time.time()
    total_time = round(t2-t1)
    print("INFO: Total simulation time = %ss" % (total_time))
