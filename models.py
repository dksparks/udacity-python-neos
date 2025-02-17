"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a
unique primary designation, an optional unique name, an optional
diameter, and a flag for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an
NEO. Each has an approach datetime, a nominal approach distance, and a
relative approach velocity.

A `NearEarthObject` maintains a collection of its close approaches, and
a `CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted
from the data files from NASA, so these objects should be able to handle
all of the quirks of the data set, such as missing names and unknown
diameters.
"""
from helpers import cd_to_datetime, datetime_to_str
from math import isnan


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the
    object, such as its primary designation (required, unique), IAU name
    (optional), diameter in kilometers (optional - sometimes unknown),
    and whether it's marked as potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close
    approaches - initialized to an empty collection, but eventually
    populated in the `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info:
            A dictionary of excess keyword arguments supplied to the
            constructor.
        """
        # The designation and hazardous attributes are required.
        self.designation = str(info['designation'])
        self.hazardous = bool(info['hazardous'])

        # The name attribute could be missing or the empty string.
        raw_name = info.get('name')
        self.name = str(raw_name) if raw_name else None

        # Set diameter to nan only if it is missing or empty string.
        # In particular, if it is set as zero, leave it as is.
        raw_diameter = info.get('diameter')
        if raw_diameter == '' or raw_diameter is None:
            self.diameter = float('nan')
        else:
            self.diameter = float(raw_diameter)

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name is None:
            return self.designation
        else:
            return f'{self.designation} ({self.name})'

    def __str__(self):
        """Return `str(self)`."""
        if isnan(self.diameter):
            diam_str = f'an unknown diameter'
        else:
            diam_str = f'a diameter of {self.diameter:.3f} km'
        hazard_str = 'is' if self.hazardous else 'is not'
        hazard_str += ' potentially hazardous'
        return f'NEO {self.fullname} has {diam_str} and {hazard_str}.'

    def __repr__(self):
        """Return `repr(self)`."""
        return f'NearEarthObject(designation={self.designation!r}, ' \
                f'name={self.name!r}, diameter={self.diameter:.3f}, ' \
                f'hazardous={self.hazardous!r})'

    def serialize(self):
        """Return a dictionary describing the NEO."""
        return {
            'designation': self.designation,
            'name': self.name if self.name else '',
            'diameter_km': self.diameter,
            'potentially_hazardous': self.hazardous,
        }


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close
    approach to Earth, such as the date and time (in UTC) of closest
    approach, the nominal approach distance in astronomical units, and
    the relative approach velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its
    `NearEarthObject` - initially, this information (the NEO's primary
    designation) is saved in a private attribute, but the referenced NEO
    is eventually replaced in the `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info:
            A dictionary of excess keyword arguments supplied to the
            constructor.
        """
        self._designation = str(info['designation'])
        self.time = cd_to_datetime(info['time'])
        self.distance = float(info['distance'])
        self.velocity = float(info['velocity'])

        # Create an attribute for the referenced NEO, initially None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of the approach time.

        The value in `self.time` should be a Python `datetime` object.
        While a `datetime` object has a string representation, the
        default representation includes seconds - significant figures
        that don't exist in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable
        representations and in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        # Use a meaningful description even if the approach has not yet
        # been connected to its NEO object.
        if self.neo is None:
            neo_string = f'the object {self._designation}'
        else:
            neo_string = self.neo.fullname
        return f'At {self.time_str}, {neo_string} approaches Earth ' \
                f'at a distance of {self.distance:.2f} au ' \
                f'with a velocity of {self.velocity:.2f} km/s.'

    def __repr__(self):
        """Return `repr(self)`."""
        return f'CloseApproach(time={self.time_str!r}, ' \
                f'distance={self.distance:.2f}, ' \
                f'velocity={self.velocity:.2f}, neo={self.neo!r})'

    def serialize(self):
        """Return a dictionary describing the approach."""
        return {
            'datetime_utc': self.time_str,
            'distance_au': self.distance,
            'velocity_km_s': self.velocity,
        }
