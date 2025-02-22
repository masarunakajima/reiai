"""
Module Name: google_api
Description: Google API for processing real estate related texts

Author: Masaru Nakajima

Copyright (c) 2024 Masaru Nakajima

"""


import os
import json
import requests

import googlemaps


def check_geocode():
    """
    Check the geocode function
    """
    api_key = os.getenv("GOOGLE_MAP_API_KEY")
    gmaps = googlemaps.Client(key=api_key)
    geocode_result = gmaps.geocode("1600 Amphitheatre Parkway, Mountain View, CA")
    return geocode_result


def parse_geocode_output(geocode_result):
    """
    Parse geocode output.
    :param geocode_result: Geocode result
    :return: Dictionary containing address information
    """

    if len(geocode_result) == 0:
        return {}
    geocode_result = geocode_result[0]

    address_components = geocode_result["address_components"]
    output = {}
    for component in address_components:
        types = component["types"]
        if "street_number" in types:
            output["street_number"] = component["long_name"]
        elif "route" in types:
            output["route"] = component["long_name"]
        elif "locality" in types:
            output["city"] = component["long_name"]
        elif "administrative_area_level_2" in types:
            output["county"] = component["long_name"]
        elif "administrative_area_level_1" in types:
            output["state"] = component["short_name"]
        elif "country" in types:
            output["country"] = component["long_name"]
        elif "postal_code" in types:
            output["postal_code"] = component["long_name"]
        elif "subpremise" in types:
            output["subpremise"] = component["long_name"]

    for component in geocode_result["geometry"]:
        if component == "location":
            latlon = geocode_result["geometry"][component]
            output["latitude"] = latlon["lat"]
            output["longitude"] = latlon["lng"]

    full_address = geocode_result["formatted_address"]
    output["full_address"] = full_address
    output["address"] = full_address.split(",")[0]
    return output


def geocode(address_string, api_key):
    """
    Given a list of address strings, return the geocoded addresses.
    :param address_string: Address string 
    :param api_key: Google API key
    :return: List of geocoded addresses
    """

    if address_string.strip() == "":
        return {}
    
    gmaps = googlemaps.Client(key=api_key)
    geocode_result = gmaps.geocode(address_string)

    return parse_geocode_output(geocode_result)
