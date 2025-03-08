import os
import pandas as pd
from util import (
    count_nearby,
    crime_summary,
    compute_restaurant_stats,
    impute_house_price_per_sq_ft
)

def load_and_clean_csv(filepath, header='infer', columns=None, drop_duplicates_cols=None):
    """
    Reads a CSV file, assigning column names if header is missing.
    
    Inputs:
      filepath: path to CSV file.
      header: default if file has a header, or None if not.
      columns: list of column names to assign if header is None 
                mainly for restaurant csv which has no columns.
      drop_duplicates_cols: list of columns to use for dropping duplicates.
    
    Returns:
      Cleaned DataFrame.
    """
    if header is None and columns is not None:
        # File has no header; assign provided column names.
        df = pd.read_csv(filepath, header=None, names=columns, on_bad_lines='skip')
    else:
        # File already has headers; read normally.
        df = pd.read_csv(filepath, header=header, on_bad_lines='skip')
    
    numeric_cols = ["Longitude", "Latitude", "Price Level", "Rating"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    # Drop duplicates
    if drop_duplicates_cols:
        df = df.drop_duplicates(subset=drop_duplicates_cols)
    
    return df

def process_data():
    """
    To process the data, calculate essential data and aggregate data 
    to a master data frame
    """
    # Get the current working directory
    current_directory = os.getcwd()
    
    # Define data directories
    google_data_dir = os.path.join(current_directory, "Google_data")
    redfin_data_dir = os.path.join(current_directory, "redfin_data")

    # --- Load Input CSVs Scraped from get_places.py ---
    # Restaurants
    restaurants_file = os.path.join(google_data_dir, "chicago_restaurants.csv")
    df_restaurants = load_and_clean_csv(
        restaurants_file, header=None,
        columns=["Name", "Business Status", "Address", "City", "Price Level", "Rating", "Total Ratings", "Latitude", "Longitude"],
        drop_duplicates_cols=["Name", "Business Status", "Address", "Price Level", "Rating", "Total Ratings", "Latitude", "Longitude"]
    )
    
    # Convenience / Grocery Stores
    stores_file = os.path.join(google_data_dir, "convenience_store_data.csv")
    df_stores = pd.read_csv(stores_file, on_bad_lines='skip')
    print(df_stores.columns)
    df_stores = load_and_clean_csv(
        stores_file,
        drop_duplicates_cols=["Name", "Business Status", "Address", "Price Level", "Rating", "Total Ratings", "Latitude", "Longitude"]
    )
    
    # Schools
    schools_file = os.path.join(google_data_dir, "school_data.csv")
    df_schools = load_and_clean_csv(
        schools_file,
        drop_duplicates_cols=["Name", "Business Status", "Address", "Price Level", "Rating", "Total Ratings", "Latitude", "Longitude"]
    )
    
    # Hospitals
    hospital_file = os.path.join(google_data_dir, "hospital_data.csv")
    df_hospital = load_and_clean_csv(
        hospital_file,
        drop_duplicates_cols=["Name", "Business Status", "Address", "Price Level", "Rating", "Total Ratings", "Latitude", "Longitude"]
    )
    
    # Crime Data
    crime_file = os.path.join(google_data_dir, "crime.csv")
    df_crime = load_and_clean_csv(crime_file)
    
    # --- Load Housing Data from Redfin) ---
    redfin_file = os.path.join(redfin_data_dir, "redfin_cleaned_v2.csv")
    df_houses = pd.read_csv(redfin_file)

    # --- Compute Nearby Features for Each House ---
    df_houses['price_per_sq_ft'] = df_houses.apply(
        lambda row: impute_house_price_per_sq_ft(row, df_houses, radius_km=1.0),
        axis=1
    )
    df_houses['num_restaurants'] = df_houses.apply(
        lambda row: count_nearby(row['latitude'], row['longitude'], df_restaurants, radius_km=1),
        axis=1
    )
    df_houses['avg_restaurant_price_level'] = df_houses.apply(
        lambda row: compute_restaurant_stats(row['latitude'], row['longitude'], df_restaurants, 'Price Level', radius_km=1),
        axis=1
    )
    df_houses['avg_restaurant_rating'] = df_houses.apply(
        lambda row: compute_restaurant_stats(row['latitude'], row['longitude'], df_restaurants, 'Rating', radius_km=1),
        axis=1
    )
    df_houses['num_stores'] = df_houses.apply(
        lambda row: count_nearby(row['latitude'], row['longitude'], df_stores, radius_km=1),
        axis=1
    )
    df_houses['num_schools'] = df_houses.apply(
        lambda row: count_nearby(row['latitude'], row['longitude'], df_schools, radius_km=1),
        axis=1
    )
    df_houses['num_hospitals'] = df_houses.apply(
        lambda row: count_nearby(row['latitude'], row['longitude'], df_hospital, radius_km=1),
        axis=1
    )
    df_houses['num_crimes'] = df_houses.apply(
        lambda row: count_nearby(row['latitude'], row['longitude'], df_crime, radius_km=1.0),
        axis=1
    )
    
    # Compute a crime summary (e.g., counts and most prevalent crime) for each house
    crime_summary_list = [
        crime_summary(row['latitude'], row['longitude'], df_crime, radius_km=1.0)
        for _, row in df_houses.iterrows()
    ]
    crime_summary_df = pd.DataFrame(crime_summary_list).fillna(0)
    df_master = df_houses.join(crime_summary_df)

    return df_master

def save_output(df_master):
    current_directory = os.getcwd()
    output_csv_path = os.path.join(current_directory, "Google_data", "summary_redfin.csv")
    df_master.to_csv(output_csv_path, index=False)
    print(f"Master DataFrame saved to {output_csv_path}")

def main():
    master_df = process_data()
    save_output(master_df)

if __name__ == '__main__':
    main()
