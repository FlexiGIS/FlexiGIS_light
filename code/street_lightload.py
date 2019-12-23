"""Generate street light loads timeseries for the aggregated area."""
import pandas as pd
import matplotlib.pyplot as plt
import logging
import os
from pathlib import Path

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                    filename="../code/log/street_lightload.log",
                    level=logging.DEBUG)

if Path("../data/03_urban_energy_requirements/").exists():
    logging.info("directory {} already exists.".
                 format("03_urban_energy_requirements"))
    pass
else:
    os.mkdir("../data/03_urban_energy_requirements/")
    logging.info("directory {} succesfully created!.".
                 format("03_urban_energy_requirements"))


def compute_streetlight_load():
    """Generate street light load time series."""
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Configuration
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    soda = 0
    Standardload = 1
    EUIx = 1
    sl = 1

    input_destination1 = "../data/01_raw_input_data/"
    input_destibnation2 = "../data/02_urban_output_data/"
    destination_load = "../data/03_urban_energy_requirements/"
    destination_fig = "../data/04_Visualisation/"
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Read Solar data
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if soda == 1:
        print('solar soda')
        soda = pd.read_csv(input_destination1+'170906_Osternburg-SoDa.csv',
                           encoding="ISO-8859-1", delimiter=',')
        # GHI = soda['Global Horiz']/1000  # convert to kWh/m2
        # wind = soda['Wind speed']
        logging.info("SoDa csv file read.")
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Read Standard Load Profiles
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if Standardload == 1:
        print('Read and normalise Standard Load Profiles')
        # , index_col='Zeitstempel', parse_dates=['Zeitstempel'])
        dfs = pd.read_csv(input_destination1+'SLP-2014.csv', delimiter=';')
        Zeit_stempel = dfs['Zeitstempel']
        SL1 = dfs['SB1'] / 1000  # SL1 = Street Lighting all-night
        # SL2 = dfs['SB2'] / 1000  # SL2 = Street lighting break from 0:00 to
        # 5:00 o'clock
        # dfs['SB1'].plot()
        # dfs['SB2'].plot()
        # grid(True)
        # plt.show()
        logging.info("Read and normalise Standard Load Profiles.")
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Read Electricity Usage Index kwh/m2 per year
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%comput_streetlight_load%%%%%%%%%%%%%%%%%%%%%%
    if EUIx == 1:  # from __future__ import division
        # import datetime
        print('Read electricity Usage Index kwh/m2 per year')
        x_sl = 4/1000  # EUIsl

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Simulate quarter load
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if sl == 1:
        print('Simulate Street. quarter hourly ERs')
        # read csv file of line and polygon
        dfsl1 = pd.read_csv(input_destibnation2+'planet_osm_line.csv')
        dfsl2 = pd.read_csv(input_destibnation2+'planet_osm_polygon.csv')
        dfsl = pd.concat([dfsl1.loc[:, ["highway", "osm_id", "area", "polygon"]
                                    ], dfsl2.loc[:, ["highway", "osm_id",
                                                     "area", "polygon"]]],
                         ignore_index=True)
        area_sl = dfsl['area'].sum()
        # no_building = len(dfsl)
        load_sl = []
        fname = open(destination_load+"streetlight_load.csv", 'w')
        fname.write('TIME;Load[kWh]\n')
        for i, row in dfs.iterrows():
            row = str(Zeit_stempel[i]) + ';' + str(area_sl*SL1[i]*x_sl) + '\n'
            load_sl.append(row)
        fname.writelines(load_sl)
        fname.close()
        df6 = pd.read_csv(destination_load+"streetlight_load.csv",
                          delimiter=";", index_col='TIME', parse_dates=True)
        df6['Load[kWh]'].plot()
        total_street_load = df6['Load[kWh]'].sum()
        print("Total street light load: "+str(total_street_load)+"kWh")
        plt.savefig(destination_fig +
                    "load_streetlight_planet_osm_line.png", dpi=300)

        logging.info("Street. quarter hourly ERs simulated.")


if __name__ == "__main__":
    compute_streetlight_load()
