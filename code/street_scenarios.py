"""Generate street light loads timeseries for the aggregated area."""
import pandas as pd
import matplotlib.pyplot as plt
import logging
import os
from pathlib import Path


class simulateStreetLight:
    """Simulate street light Electricity demand."""

    def config(self):
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

    def get_standardLoad(self):
        """Get standard load profile."""
        print('INFO: Normalise Standard Load Profiles')
        self.standardLoad = pd.read_csv(
            os.path.join(self.input_path, 'SLP_hourly.csv'))

        # SL1: All urban lights are operated as
        # - evening (16:15) - midnight (00:00) => 'On'
        # - midnight (00:15) - early morning  (05:15) => 'Off'
        #  - Early morning (05:30 )- morning (09:00) => 'On'
        self.SL1 = self.standardLoad['SB1'] / 1000 

        # All urban roads are illuminated all night
        self.SL2 = self.standardLoad['SB2'] / 1000

        logging.info("Read and normalise Standard Load Profiles.")

    def electricityUsageIndex(self):
        """Calculate electricity Usage Index."""
        print("INFO: Electricity Usage Index kwh/m2 per year")
        self.x_sl = 4 / 1000 #MW/m2 
        self.timestamp = self.standardLoad['Zeitstempel']

    def simulateLoadAllRoad(self):
        """Simulate street lightning demand for different scenarios."""
        print('INFO: Simulate Street Light load')
        # get planet OSM data for highway (line and polygon)
        self.osmLines = pd.read_csv(os.path.join(
            self.input_path2, 'planet_osm_line.csv'))
        self.osmSquares = pd.read_csv(os.path.join(
            self.input_path2, 'planet_osm_polygon.csv'))
        self.osmData = pd.concat([self.osmLines.loc[:, ["highway", "area"]],
                                  self.osmSquares.loc[:, ["highway", "area"]]],
                                 ignore_index=True)
        # for secenario 1 & 2
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
        fname = open(os.path.join(self.output_path,
                                  "streetlight_load.csv"), 'w')
        fname.write('TIME;SB1;SB2;SB2_mainroad;SB1_rest\n')
        for i, row in self.standardLoad.iterrows():
            row = str(self.timestamp[i]) + ';' + \
                str(self.osmArea*self.SL1[i]*self.x_sl) + ';' +\
                str(self.osmArea*self.SL2[i]*self.x_sl) + ';' +\
                str(self.mainRoadsArea*self.SL2[i]*self.x_sl) + ';' +\
                str(self.notMainRoadsArea*self.SL1[i]*self.x_sl) + '\n'
            _streetLoad_.append(row)
        fname.writelines(_streetLoad_)
        fname.close()

    def get_feedInData(self):
        """Get solar data."""
        # demand and supply
        pv = pd.read_csv(os.path.join(
            self.input_path, 'pv_power.csv'), parse_dates=True)
        wind = pd.read_csv(os.path.join(
            self.input_path, 'wind_power.csv'), parse_dates=True)

        wind['pv'] = pv['pv']
        self.feedin = wind

        self.df6 = pd.read_csv(os.path.join(self.output_path, "streetlight_load.csv"),
                               delimiter=";", index_col='TIME', parse_dates=True)
        self.df6 = self.df6.iloc[0:len(wind.index)]  # TODO: fix index
        self.feedin['demand_SB1'] = self.df6['SB1'].values
        self.feedin['demand_SB2'] = self.df6['SB2'].values
        self.df6['SB2/SB1'] = self.df6['SB2_mainroad'] + \
            self. df6['SB1_rest']
        self.feedin['demand_SB2_SB1'] = self.df6['SB2/SB1'].values
        self.feedin.to_csv(os.path.join(
            self.output_path, 'optimization-commodities.csv'))

    # plot scenario
    def plotLoadScenario(self):
        """Calculate total street-light load and plot sample scenario."""
        totalLoad_SB1 = self.df6['SB1'].sum()
        totalLoad_SB2 = self.df6['SB2'].sum()
        totalLoad_SB2_SB1 = self.df6['SB2/SB1'].sum()
        print("INFO: Total Street Light SB1-Load: "+str(totalLoad_SB1)+"kWh")
        print("INFO: Total street light SB2-Load: "+str(totalLoad_SB2)+"kWh")
        print("INFO: Total Main Roads SB2-load: "+str(totalLoad_SB2_SB1)+"kWh")

        # plot load profile
        fig, ax = plt.subplots(1, figsize=(6, 4), facecolor='whitesmoke')
        df6 = self.df6[['SB1', 'SB2', 'SB2/SB1']]
        df6["2014-01-01":"2014-01-03"].plot(ax=ax, legend=True)

        ax.set_facecolor("whitesmoke")
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.1,
                         box.width, box.height * 0.9])

        # Put a legend below current axis
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                  fancybox=True, shadow=True, ncol=5)

        plt.xlabel("Time [Hour]")
        plt.ylabel("Load [kW]")
        plt.title("Street lighting demand profiles")
        plt.savefig(self.output_path_fig +
                    "load_streetlight_planet_osm_line.png",
                    facecolor=fig.get_facecolor(), dpi=300)

        logging.info("Street. quarter hourly ERs simulated.")

    def simulate_StreetLight(self, soda=False, Standardload=True, EUIx=True,
                             sl=True):
        """Trigger all methods for street light simulation."""
        self.config()
        self.get_standardLoad()
        self.electricityUsageIndex()
        self.simulateLoadAllRoad()
        self.get_feedInData()
        self.plotLoadScenario()


if __name__ == "__main__":
    streelight_simulation = simulateStreetLight()
    streelight_simulation.simulate_StreetLight()
