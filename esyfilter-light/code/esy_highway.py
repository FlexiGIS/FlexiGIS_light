"""Esy-osmfilter for berline."""
import os
import sys
import logging
from pathlib import Path

from esy.osmfilter import run_filter, Node, Way, Relation
from esy.osmfilter import export_geojson

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


def esyFilter(highway_feature, highwayList,
              pbfOSMfile="02-UrbanInfrastructure.osm.pbf",
              outJson="", elementname="osm_geotype",
              outGeojson='', elementAttr='',
              jsontype=''):
    """Download and filter OSM pbf file data using esy-osmfilter."""
    if sys.version_info.major == 2:
        raise RuntimeError('Unsupported python version')
    # see docu for filter structures
    prefilter = {Node: {"highway": highway_feature},
                 Way: {"highway": highway_feature}, Relation: {}}
    blackfilter = [("", ""), ]
    whitefilter = highwayList
    raw_pbf = "../data/input_raw_data/"
    out_dir = "../data/output_data/"
    if Path(out_dir).exists():
        pass
    else:
        os.mkdir(out_dir)
    outJson = out_dir+outJson
    filename = raw_pbf+pbfOSMfile
    # json file for the Data dictionary
    JSON_outputfile = os.path.join(os.getcwd(), outJson)

    PBF_inputfile = os.path.join(os.getcwd(), filename)

    # if not os.path.exists(filename):
    #     filename, headers = urllib.request.urlretrieve(
    #         'https://download.geofabrik.de/europe/germany/'+filename,
    #         filename=filename
    #     )
    #     PBF_inputfile = filename
    # see docu for data- and element-dictionary structures
    [Data, Elements] = run_filter(elementname, PBF_inputfile, JSON_outputfile,
                                  prefilter, whitefilter, blackfilter,
                                  NewPreFilterData=True, CreateElements=True,
                                  LoadElements=True, verbose=True,
                                  multiprocess=True)

    # At this point we could export the elements to a geojson-file
    export_geojson(Elements[elementname][elementAttr], Data,
                   filename=out_dir+outGeojson, jsontype=jsontype)


def esyLinesFilter():
    """Filter highway lines using esy-osmfilter."""
    highway_feature = ['living_street', 'motorway', 'pedestrian',
                       'primary', 'secondary', 'service', 'tertiary',
                       'trunk', 'motorway_link', 'primary_link',
                       'secondary_link', 'tertiary_link',
                       'trunk_link']

    highwayList = [[("highway", "living_street")], [("highway", "motorway")],
                   [("highway", "pedestrian")], [("highway", "primary")],
                   [("highway", "secondary")], [("highway", "service")],
                   [("highway", "tertiary")], [("highway", "trunk")],
                   [("highway", "motorway_link")],
                   [("highway", "primary_link")],
                   [("highway", "secondary_link")],
                   [("highway", "tertiary_link")], [("highway", "trunk_link")]]
    # filter OSM lines
    esyFilter(highway_feature, highwayList,
              pbfOSMfile="02-UrbanInfrastructure.osm.pbf",
              outJson='berlin_line.json', elementname="osm_lines",
              outGeojson='berlin_line.geojson', elementAttr="Way",
              jsontype='Line')


def esyPointsFilter():
    """Filter highway points using esy-osmfilter."""
    highway_feature = ['bus_stop', 'crossing', 'give_way',
                       'motorwyay_junction', 'passing_place',
                       'platform', 'speed_camera', 'stop',
                       'street_lamp', 'traffic_signals']

    highwayList = [[("highway", "bus_stop")], [("highway", "crossing")],
                   [("highway", "give_way")],
                   [("highway", "motorwyay_junction")],
                   [("highway", "passing_place")], [("highway", "platform")],
                   [("highway", "speed_camera")], [("highway", "stop")],
                   [("highway", "street_lamp")],
                   [("highway", "traffic_signals")]]
    # filter OSM points
    esyFilter(highway_feature, highwayList,
              pbfOSMfile="02-UrbanInfrastructure.osm.pbf",
              outJson='berlin_point.json', elementname="osm_points",
              outGeojson='berlin_point.geojson', elementAttr="Node",
              jsontype='Point')


if __name__ == '__main__':
    esyLinesFilter()
    print("esyLinesFilter:        "+"  Done!")
    esyPointsFilter()
    print("esyPointsFilter:       "+"  Done!")
