# Author: Zhenning Liu
# This file initialize grid search to search and scrapes 
# places data in Chicago using Google Place API

# Resource:
        # 1) https://developers.google.com/maps/documentation/places/web-service/nearby-search
        # 2) https://stackoverflow.com/questions/7370801/how-do-i-measure-elapsed-time-in-python


import requests
import time
import random
import csv
import os
import time
import json

# Replace with actual API Key
API_KEY = ""
BASE_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

# Chicago grid boundaries
LAT_MIN, LAT_MAX = 41.6445, 42.023
LNG_MIN, LNG_MAX = -87.9401, -87.523

# Set boundaries to a smaller scale for demo
#LAT_MIN, LAT_MAX = 41.844, 41.848
#LNG_MIN, LNG_MAX = -87.6405, -87.6403

# Grid step size
LAT_STEP = 0.009  # ~1 km per step 
LNG_STEP = 0.012  # ~1 km per step
RADIUS = 1000  # 1km search radius

def get_places_info(lat, lng, place_type):

    """
    Helper function to get name, address, price_index, ratings, location of places 
    from information requested from Google Place API.
    
    Input:
        lat (int): lattitude of a place
        lng (int): longitude of a place
        place_type (str): place type, e.g., restuarant

    Return: A list of information (including name, address, etc.) of a place
    """

    params = {
        "location": f"{lat},{lng}",
        "radius": RADIUS,
        "type": place_type,
        "key": API_KEY
    }
    
    places = []
    place_objects = []

    while True:
        response = requests.get(BASE_URL, params=params).json()

        for place in response.get("results", []):
            name = place.get("name")
            business_status = place.get("business_status", "Status not available")
            address = place.get("formatted_address") or place.get("vicinity", "Address Not Available") # Use 'formatted_address' for full address
            price_index = place.get("price_level", "Price information not available")
            rating = place.get("rating", "No rating")
            total_ratings = place.get("user_ratings_total", "No ratings")
            types = place.get("types", [])
            lat = place["geometry"]["location"]["lat"]
            lng = place["geometry"]["location"]["lng"]
            places.append((name, business_status, address, price_index, rating, total_ratings, types, lat, lng))
            place_objects.append(place)

        next_page_token = response.get("next_page_token")
        if not next_page_token:
            break
        
        time.sleep(random.uniform(1, 3))
        params["pagetoken"] = next_page_token

    return place_objects, places

def scrape(place_type):

    """
    To scrape places of a specific type and save to a CSV file.
    
    Input:
        place_type: A string of place type (e.g., restaurant)
    
    Returns: None
    """

    # Specify the existing directory to save the CSV files
    output_dir = os.path.join(os.getcwd(), 'google_data')

    # File path for the output CSV
    places_output_file = os.path.join(output_dir, f"{place_type}_data.csv")
    object_output_file = os.path.join(output_dir, f"{place_type}_data.json")

    header = ["Name", "Business Status", "Address", "Price Level", "Rating", "Total Ratings", "Types", "Latitude", "Longitude"]

    all_objects = []
    
    with open(places_output_file, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        # Loop through Chicago in a grid
        lat = LAT_MIN
        while lat <= LAT_MAX:
            # Reset longitude to left most longitude
            lng = LNG_MIN

            # Get all longitudes at a particular lattitude
            while lng <= LNG_MAX:
                print(f"Scraping {place_type} at {lat}, {lng}...")
                place_object, places = get_places_info(lat, lng, place_type)
                writer.writerows(places)
                all_objects.extend(place_object)
                lng += LNG_STEP  # Move right

            lat += LAT_STEP  # Move up

    print(f"Data scraping for {place_type} complete. Data saved to {places_output_file}.")
    
    with open(object_output_file, "w", encoding="utf-8") as f:
        json.dump(all_objects, f, indent=4)
    print(f"JSON data saved to {object_output_file}.")


def main():
    
    """
    Run scrapping
    """

    place_type = input("Please enter a place type to scrape:")
    scrape(place_type)
    
if __name__ == '__main__':

    start_time = time.time()
    main()
    elapsed = time.time() - start_time

    hours, remainder = divmod(elapsed, 3600) # convert seconds to hours and remainder
    minutes, seconds = divmod(remainder, 60) # convert remaining seconds to minutes and remainder
    print("--- {} hours, {} minutes, and {:.2f} seconds ---".format(int(hours), int(minutes), seconds))