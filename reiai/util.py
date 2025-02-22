import pandas as pd
import math


def check_none(values: dict):
    """
    Check if any value in the dictionary is None.
    Throws an error if any value is None.
    :param values: dictionary of values
    """
    for key, value in values.items():
        if value is None:
            raise ValueError(f"{key} cannot be None")




def split_address(address: str) -> list[str]:
    """
    Split address into parts. It splits by comma and assumes
    that the third part is state and zipcode.
    :param address: address string
    :return: list of address parts
    """
    split = address.strip().split(",")
    if len(split) < 3:
        return split
    address_list = split[:2]
    address_list = split[2].split()
    if len(split) > 3:
        address_list.extend(split[3:])
    return address_list


def get_unique_vals(df: pd.DataFrame, max_vals: int = 10) -> dict:
    """
    Get unique values for each column in the dataframe.
    :param df: dataframe
    :param max_vals: maximum number of unique values to return
    :return: dictionary of unique values
    """
    unique_vals = {}
    for col in df.columns:
        vals = df[col].unique()
        if len(vals) > max_vals:
            vals = vals[:max_vals]
        unique_vals[col] = vals
    return unique_vals



def get_polygon(center_lat: float, center_lon: float, radius: float, 
                n_gon = 8) -> list:
    """
    Get polygon coordinates given center and radius in miles.
    :param center_lat: center latitude
    :param center_lon: center longitude
    :param radius: radius in miles
    :param n_gon: number of sides in polygon
    :return: list of polygon coordinates
    """
    check_none({
        "center_lat": center_lat,
        "center_lon": center_lon,
        "radius": radius,
    })
    if n_gon < 3:
        raise ValueError("n_gon must be at least 3")
    coords = []
    # note that radius is in miles
    for i in range(n_gon):
        angle = 2 * math.pi * i / n_gon
        lat = center_lat + radius * math.cos(angle) / 69
        lon = center_lon + radius * math.sin(angle) / 69
        coords.append((lat, lon))
    return coords