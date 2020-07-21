'''This script is use to derive optimal RE feedin capacity and also the optimal
storage required for an energy system. The optimisation is carried out using
the oemof solph package. The below codes are taken from the `oemof-example`_ codes
github repository. The optimization settings are described below by the following parameters:

- optimize wind, pv and storage

See link here: `oemof-example`_
'''
import pandas as pd
import os
import pprint as pp
import matplotlib.pyplot as plt
import pickle
import logging
from oemof.tools import economics
import oemof.solph as solph
from oemof.outputlib import processing, views
import oemof.outputlib as outputlib
import oemof_visio as oev
from utils import shape_legend


# logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
#                     filename="../code/log/optimize.log",
#                     level=logging.DEBUG)


# load demand and supply data
def get_commodities(data_path,
                    filename='optimization-commodities.csv'):
    """Import simulated urban electricty demand and feedin data.

    :pandas dataframe:  data: with hourly resolution as index
    """
    data = pd.read_csv(os.path.join(data_path, filename),
                       index_col='time', parse_dates=True)
    return data


# Create oemof energy system
def oemof_power_system(data, dir_path):
    """Creates an oemof energy system model and optimizes the investment of
    flexibilty technology.

    :dataframe: data: demand, normalized pv and windpower timeseries
    :string: dir_path_2: directory path, to temporary dump optimization results
    """
    # create an energy system using setting defualt economic parameters
    number_timesteps = len(data.index)
    period = data.index.year[10]
    date_time_index = pd.date_range('1/1/'+str(period),
                                    periods=number_timesteps,
                                    freq='H')
    energysystem = solph.EnergySystem(timeindex=date_time_index)
    # # create natural gas bus
    # bgas = solph.Bus(label="natural_gas")

    # create electricity bus
    bel = solph.Bus(label="electricity")
    energysystem.add(bel)
    # create excess component for the electricity bus to allow overproduction
    energysystem.add(solph.Sink(label='excess_bel',
                                inputs={bel: solph.Flow()}))
    # gas_resource = solph.Source(label='rgas', outputs={bgas: solph.Flow(
    #     nominal_value=29825293, summed_max=1)})

    # create fixed source object representing wind power plants
    energysystem.add(solph.Source(label='wind', outputs={bel: solph.Flow(
        actual_value=data['wind'], nominal_value=1000000, fixed=True)}))

    # create fixed source object representing pv power plants
    energysystem.add(solph.Source(label='pv', outputs={bel: solph.Flow(
        actual_value=data['pv'], nominal_value=582000, fixed=True)}))

    # create simple sink object representing the electrical demand
    energysystem.add(solph.Sink(label='demand', inputs={bel: solph.Flow(
        actual_value=data['demand_SB2'], fixed=True, nominal_value=1)}))

    # create simple transformer object representing a gas power plant
    # pp_gas = solph.Transformer(
    #     label="pp_gas",
    #     inputs={bgas: solph.Flow()},
    #     outputs={bel: solph.Flow(nominal_value=10e10, variable_costs=0)},
    #     conversion_factors={bel: 0.58})

    # create storage object representing a battery
    storage = solph.components.GenericStorage(
        nominal_storage_capacity=10077997,
        label='storage',
        inputs={bel: solph.Flow(nominal_value=10077997/6)},
        outputs={bel: solph.Flow(
            nominal_value=10077997/6, variable_costs=0.001)},
        loss_rate=0.00, initial_storage_level=None,
        inflow_conversion_factor=1, outflow_conversion_factor=0.8,
    )

    energysystem.add(storage)
    return energysystem


# Optimise the energy system
def optimize(energysystem, data_path, fname='om_data'):
    """linear optimization of the energy system."""
    om = solph.Model(energysystem)
    om.solve(solver='cbc', solve_kwargs={'tee': False})
    # Dump results in disc for future analysis
    energysystem.results['main'] = outputlib.processing.results(om)
    energysystem.results['meta'] = outputlib.processing.meta_results(om)
    energysystem.dump(dpath=data_path, filename=fname)
    energysystem_data = energysystem
    return energysystem_data


def check_results_dataframe(energysystem_data):
    """Explore optimized supply, storage and investments.
    Also calculates renewable share in the system.

    :dict: results
    :dataframe: elect_bus
    """
    # Restore dumped result for - later Processing *
    # energysystem = solph.EnergySystem()
    # energysystem.restore(
    #     dpath='../data/03_urban_energy_requirements/', filename='om_data')
    results = energysystem_data.results['main']
    electricity_bus = views.node(results, 'electricity')
    custom_storage = views.node(results, 'storage')
    elect_bus = electricity_bus['sequences']
    print('** electricity sequence head(5) **')
    print(elect_bus.head(5))
    storage_ = custom_storage['sequences']
    print('** storage sequence head(5) **')
    print(storage_.head(5))


def plot(energysystem_data, year):
    """This code is copied from the oemof plotting examples.

    It allows for the customization of the plot using oemof/oev plotting object.
    See link here: `oemof-plotting_examples`_
    https://github.com/oemof/oemof-examples/tree/master/oemof_examples/oemof.solph/v0.3.x/plotting_examples
    """
    results = energysystem_data.results['main']
    cdict = {
        (('electricity', 'demand'), 'flow'): '#ce4aff',
        (('electricity', 'excess_bel'), 'flow'): '#555555',
        (('electricity', 'storage'), 'flow'): '#42c77a',
        (('pv', 'electricity'), 'flow'): '#ffde32',
        (('storage', 'electricity'), 'flow'): '#42c77a',
        (('wind', 'electricity'), 'flow'): '#5b5bae'}
    inorder = [(('pv', 'electricity'), 'flow'),
               (('wind', 'electricity'), 'flow'),
               (('storage', 'electricity'), 'flow')]

    fig = plt.figure(figsize=(14, 8))
    electricity_seq = views.node(results, 'electricity')['sequences']
    plot_slice = oev.plot.slice_df(electricity_seq[str(year)+'-03-01':str(year)+'-03-20'],
                                   date_from=pd.datetime(year, 1, 1))
    my_plot = oev.plot.io_plot('electricity', plot_slice, cdict=cdict,
                               inorder=inorder, ax=fig.add_subplot(1, 1, 1),
                               smooth=True)
    ax = shape_legend('electricity', **my_plot)
    ax = oev.plot.set_datetime_ticks(ax, plot_slice.index, tick_distance=48,
                                     date_format='%d-%m-%H', offset=12)

    ax.set_ylabel('Power in MW')
    ax.set_xlabel(str(year))
    ax.set_title("Electricity bus")
    plt.savefig('../data/04_Visualisation/om.png', dpi=300)
    logging.info("Generate plot of optimized variables.")
    plt.show()


if __name__ == '__main__':
    data_path_1 = '../data/03_urban_energy_requirements/'
    dir_path_2 = '../data/01_raw_input_data/'
    data = get_commodities(
        data_path_1, filename='optimization-commodities.csv')
    year = data.index.year[10]
    energysystem = oemof_power_system(data, dir_path_2)
    energysystem_data = optimize(energysystem, data_path_1)
    check_results_dataframe(energysystem_data)
    plot(energysystem_data, year)
