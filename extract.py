"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # TODO: Load NEO data from the given CSV file.
    neos = []
    with open(neo_csv_path) as neo_file:
        reader = csv.DictReader(neo_file)
        for neo in reader:
            is_hazardous = neo['pha'] == 'Y'
            neos.append(NearEarthObject(
                designation=neo['pdes'], name=neo['name'],
                diameter=neo['diameter'], hazardous=is_hazardous,
            ))
    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO: Load close approach data from the given JSON file.
    cads = []
    with open(cad_json_path) as cad_file:
        cad_json = json.load(cad_file)
        cad_fields = cad_json['fields']
        cad_data = cad_json['data']
        desired_fields = ['des', 'cd', 'dist', 'v_rel']
        idx = {f: cad_fields.index(f) for f in desired_fields}
        for cad in cad_data:
            cads.append(CloseApproach(
                designation=cad[idx['des']], time=cad[idx['cd']],
                distance=cad[idx['dist']], velocity=cad[idx['v_rel']],
            ))
    return cads
