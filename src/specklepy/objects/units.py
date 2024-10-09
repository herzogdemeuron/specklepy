from enum import Enum
from typing import Union

from specklepy.logging.exceptions import SpeckleException, SpeckleInvalidUnitException

__all__ = [
    "Units",
    "get_encoding_from_units",
    "get_units_from_encoding",
    "get_units_from_string",
]


class Units(Enum):
    mm = "mm"
    cm = "cm"
    m = "m"
    km = "km"
    inches = "in"
    feet = "ft"
    yards = "yd"
    miles = "mi"
    none = "none"
    sqm = "m²"
    cbm = "m³"
    percent = "%"
    watts = "W"
    watts_per_sqm = "W/m²"
    liters_per_sec_sqm = "L/(s·m²)"


UNITS_STRINGS = {
    Units.mm: ["mm", "mil", "millimeters", "millimetres"],
    Units.cm: ["cm", "centimetre", "centimeter", "centimetres", "centimeters"],
    Units.m: ["m", "meter", "meters", "metre", "metres"],
    Units.km: ["km", "kilometer", "kilometre", "kilometers", "kilometres"],
    Units.inches: ["in", "inch", "inches"],
    Units.feet: ["ft", "foot", "feet"],
    Units.yards: ["yd", "yard", "yards"],
    Units.miles: ["mi", "mile", "miles"],
    Units.none: ["none", "null"],
    Units.sqm: ["sqm", "m²", "square meter", "square meters"],
    Units.cbm: ["cbm", "m³", "cubic meter", "cubic meters"],
    Units.percent: ["percent", "%"],
    Units.watts: ["W", "watt", "watts"],
    Units.watts_per_sqm: ["W/m²", "watts per square meter"],
    Units.liters_per_sec_sqm: ["L/(s·m²)", "liters per second per square meter"],
}

UNITS_ENCODINGS = {
    Units.none: 0,
    None: 0,
    Units.mm: 1,
    Units.cm: 2,
    Units.m: 3,
    Units.km: 4,
    Units.inches: 5,
    Units.feet: 6,
    Units.yards: 7,
    Units.miles: 8,
    Units.sqm: 9,
    Units.cbm: 10,
    Units.percent: 11,
    Units.watts: 12,
    Units.watts_per_sqm: 13,
    Units.liters_per_sec_sqm: 14,
}

UNIT_SCALE = {
    Units.none: 1,
    Units.mm: 0.001,
    Units.cm: 0.01,
    Units.m: 1.0,
    Units.km: 1000.0,
    Units.inches: 0.0254,
    Units.feet: 0.3048,
    Units.yards: 0.9144,
    Units.miles: 1609.340,
    Units.sqm: 1.0,  # Already in square meters
    Units.cbm: 1.0,  # Already in cubic meters
    Units.percent: 0.01,  # Convert percentage to decimal
    Units.watts: 1.0,  # Base unit for power
    Units.watts_per_sqm: 1.0,  # Already in W/m²
    Units.liters_per_sec_sqm: 1.0,  # Already in L/(s·m²)
}
"""Unit scaling factor to meters for length-based units and other scale factors."""


def get_units_from_string(unit: str) -> Units:
    if not isinstance(unit, str):
        raise SpeckleInvalidUnitException(unit)
    unit = str.lower(unit)
    for name, alternates in UNITS_STRINGS.items():
        if unit in alternates:
            return name
    raise SpeckleInvalidUnitException(unit)


def get_units_from_encoding(unit: int) -> Units:
    for name, encoding in UNITS_ENCODINGS.items():
        if unit == encoding:
            return name or Units.none

    raise SpeckleException(
        message=(
            f"Could not understand what unit {unit} is referring to."
            f"Please enter a valid unit encoding (eg {UNITS_ENCODINGS})."
        )
    )


def get_encoding_from_units(unit: Union[Units, str, None]):
    maybe_sanitized_unit = unit
    if isinstance(unit, str):
        for unit_enum, aliases in UNITS_STRINGS.items():
            if unit in aliases:
                maybe_sanitized_unit = unit_enum
    try:
        return UNITS_ENCODINGS[maybe_sanitized_unit]
    except KeyError as e:
        raise SpeckleException(
            message=(
                f"No encoding exists for unit {maybe_sanitized_unit}."
                f"Please enter a valid unit to encode (eg {UNITS_ENCODINGS})."
            )
        ) from e


def get_scale_factor_from_string(fromUnits: str, toUnits: str) -> float:
    """Returns a scalar to convert distance values from one unit system to another"""
    return get_scale_factor(
        get_units_from_string(fromUnits), get_units_from_string(toUnits)
    )


def get_scale_factor(fromUnits: Units, toUnits: Units) -> float:
    """Returns a scalar to convert distance values from one unit system to another"""
    return get_scale_factor_to_meters(fromUnits) / get_scale_factor_to_meters(toUnits)


def get_scale_factor_to_meters(fromUnits: Units) -> float:
    """Returns a scalar to convert distance values from one unit system to meters"""
    if fromUnits not in UNIT_SCALE:
        raise ValueError(f"Invalid units provided: {fromUnits}")

    return UNIT_SCALE[fromUnits]
