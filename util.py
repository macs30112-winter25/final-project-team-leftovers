import numpy as np
import pandas as pd
import ast

def clean_and_filter(types_list, allowed_types):
    """
    Clean a list of type strings by stripping whitespace, converting to lowercase,
    and filtering out any types not in allowed_types.
    
    Inputs:
      types_list (list): A list of type strings.
      allowed_types (iterable, e.g., list or set): The types we want.

    Returns:
      list: A list of cleaned type strings that are in allowed_types.
    """
    return [t.strip().lower() for t in types_list if t.strip().lower() in allowed_types]

def filter_types_inplace(df, allowed_types, column="Types"):
    """
    Modify the DataFrame in place by converting string representations of lists in the 
    specified 'Types' column into actual lists, cleaning them, and keeping only rows 
    where at least one allowed type remains.
    
    Inputs:
      df (DataFrame): The DataFrame to modify.
      allowed_types (iterable): An iterable (e.g., a set or list) of allowed type strings.
      column (str): The name of the column containing the types (which is Types by default).
    
    Returns:
      None. The DataFrame is modified in place.
    """
    def parse_types(x):
        # If x is a string that looks like a list, try to evaluate it.
        if isinstance(x, str):
            try:
                parsed = ast.literal_eval(x)
                if isinstance(parsed, list):
                    return parsed
                # If it's not a list after eval, fall back to splitting.
                return x.split(",")
            except Exception:
                return x.split(",")
        return x

    # Convert each cell in the column to an actual list.
    df[column] = df[column].apply(parse_types)
    # Clean and filter the list of types for each row.
    df[column] = df[column].apply(lambda x: clean_and_filter(x, allowed_types))
    # Drop rows where the cleaned types list is empty.
    df.drop(df[df[column].apply(lambda x: len(x) == 0)].index, inplace=True)

def haversine_distance_vectorized(lat1, lon1, lat2, lon2):
    """
    Compute the Haversine distance (in kilometers) between a reference point (lat1, lon1)
    and another point (lat2, lon2) using vectorized operations.
    
    Parameters:
      lat1, lon1: coordinates (in decimal degrees)
      lat2, lon2: another coordinates
      
    Returns:
      A np array of distances (in km).
    """
    R = 6371.0  # Earth radius in kilometers
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = np.sin(dlat / 2.0)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def count_amenities_for_house(house_lat, house_lon, place_df, radius_km=1.0):
    """
    Count the number of amenities (e.g., convenience/grocery stores) within a given radius (in km) of a house.
    
    Parameters:
      house_lat (float): Latitude of the house.
      house_lon (float): Longitude of the house.
      place_df (DataFrame): DataFrame for the amenity.
      radius_km (float): Search radius in kilometers (default to 1 km).
      
    Returns:
      int: Number of amenities within the specified radius.
    """
    distances = haversine_distance_vectorized(house_lat, house_lon,
                                               place_df['Latitude'].values,
                                               place_df['Longitude'].values)
    return np.sum(distances <= radius_km)


def crime_summary_for_house(house_lat, house_lon, crime_df, radius_km=1.0):
    """
    For a given house coordinate, compute a summary of crime within the specified radius.
    
    The summary includes:
      - 'violent_crime_count': The number of violent crime
      - 'nonviolent_crime_count': The number of non-violent crime
      - 'most_prevalent_crime': The crime type with the highest proportion.
      - 'crime_proportion': The proportion of incidents that belong to that crime type.
      
    Parameters:
      house_lat (float): Latitude of the house.
      house_lon (float): Longitude of the house.
      crime_df (DataFrame): DataFrame containing crime incidents with columns
                            'Latitude', 'Longitude', and 'Crime Type'.
      radius_km (float): Search radius in kilometers (default to 1 km).
      
    Returns:
      dict: A dictionary with keys 'crime_counts', 'most_prevalent_crime', and 'crime_proportion'.
            If no crime incidents are found within the radius, returns an empty dictionary for counts,
            and None and 0 for the other values.
    """
    # Compute distances from the house to each crime incident.
    distances = haversine_distance_vectorized(house_lat, house_lon,
                                               crime_df['Latitude'].values,
                                               crime_df['Longitude'].values)
    
    violent_crime_types = {
    'ASSAULT', 'BATTERY',
    'CRIMINAL SEXUAL ASSAULT',
    'SEX OFFENSE', 'WEAPONS VIOLATION',
    'ROBBERY', 'HOMICIDE', 'ARSON',
    'KIDNAPPING', 'STALKING',
    'OFFENSE INVOLVING CHILDREN',
    'INTIMIDATION', 'HUMAN TRAFFICKING'
    }
    
    nonviolent_crime_types = {
    'MOTOR VEHICLE THEFT', 'CRIMINAL DAMAGE',
    'BURGLARY', 'DECEPTIVE PRACTICE', 'THEFT',
    'OTHER OFFENSE', 'PUBLIC PEACE VIOLATION',
    'LIQUOR LAW VIOLATION',
    'CONCEALED CARRY LICENSE VIOLATION', 'PUBLIC INDECENCY',
    'OBSCENITY', 'GAMBLING', 'OTHER NARCOTIC VIOLATION',
    'NON-CRIMINAL', 'CRIMINAL TRESPASS'
    }
    
    # Include incidents within the specified radius.
    crime_nearby = crime_df[distances <= radius_km]
    
    # Initialize the summary dictionary.
    summary = {}
    if crime_nearby.empty:
        summary["most_prevalent_crime"] = None
        summary["crime_proportion"] = 0
        summary["violent_crime_count"] = 0
        summary["nonviolent_crime_count"] = 0
        return summary

    # Group by crime type and count the number of incidents per type.
    crime_counts = crime_nearby.groupby("primary_type").size()

    # Compute violent and non-violent totals.
    violent_total = sum(crime_counts.get(ct, 0) for ct in violent_crime_types)
    nonviolent_total = sum(crime_counts.get(ct, 0) for ct in nonviolent_crime_types)
    summary["violent_crime_count"] = violent_total
    summary["nonviolent_crime_count"] = nonviolent_total

    # Calculate total crimes and proportions.
    total_crimes = crime_counts.sum()
    crime_proportions = crime_counts / total_crimes
    
    max_crime_type = crime_proportions.idxmax()
    max_proportion = crime_proportions[max_crime_type]
    summary["most_prevalent_crime"] = max_crime_type
    summary["crime_proportion"] = max_proportion
    
    return summary