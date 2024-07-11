"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`,
each of which accept an `results` stream of close approaches and a path
to which to write the data.

These functions are invoked by the main module with the output of the
`limit` function and the filename supplied by the user at the command
line. The file's extension determines which of these functions is used.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each
    output row corresponds to the information in a single close approach
    from the `results` stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename:
        A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous',
    )
    with open(filename, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()
        for ca in results:

            # Note: The reviewer of my first submission suggested that
            # there was a problem with the .serialize() methods, but in
            # fact the issue seems merely to be the fact that I used the
            # dictionary union operator '|' in the line below.
            # This operator only became available in Python 3.9, which
            # is why it works fine on my machine (running Python 3.12.3)
            # but results in a TypeError for the reviewer.
            #
            # writer.writerow(ca.serialize() | ca.neo.serialize())
            #
            # The revised code, which should run properly on the
            # reviewer's older version of Python, is below.

            approach_dict = ca.serialize()
            neo_dict = ca.neo.serialize()
            for key, value in neo_dict.items():
                approach_dict[key] = value
            writer.writerow(approach_dict)
            

def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the
    output is a list containing dictionaries, each mapping
    `CloseApproach` attributes to their values and the 'neo' key mapping
    to a dictionary of the associated NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename:
        A Path-like object pointing to where the data should be saved.
    """
    with open(filename, 'w') as json_file:
        output = []
        for ca in results:
            data = ca.serialize()
            data['neo'] = ca.neo.serialize()
            output.append(data)
        json.dump(output, json_file, indent=2)
