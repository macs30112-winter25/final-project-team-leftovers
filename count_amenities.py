import os
import pandas as pd
from util import count_amenities_for_house, filter_types_inplace, crime_summary_for_house


current_directory = os.getcwd()

# --- Process Restaurant Data ---
file_path = os.path.join(current_directory, "Google_data", "chicago_restaurants.csv")
df_restaurants = pd.read_csv(file_path, header=None, on_bad_lines='skip')
# restaurant data does not have column name when I write csv
df_restaurants.columns = ["Name", "Business Status", "Address", "City", "Price Level", "Rating", "Total Ratings", "Latitude", "Longitude"]
df_restaurants['Latitude'] = pd.to_numeric(df_restaurants['Latitude'], errors='coerce')
df_restaurants['Longitude'] = pd.to_numeric(df_restaurants['Longitude'], errors='coerce')


# --- Process Convenience/Grocery Store Data ---
store_filepath = os.path.join(current_directory, "Google_data", "convenience_or_grocery_store_data.csv")
store_columns = ["Name", "Business Status", "Address", "Price Level", "Rating", "Total Ratings", "Types", "Latitude", "Longitude"]
df_stores = pd.read_csv(store_filepath, header=None, on_bad_lines='skip')
df_stores.columns = store_columns
df_stores['Latitude'] = pd.to_numeric(df_stores['Latitude'], errors='coerce')
df_stores['Longitude'] = pd.to_numeric(df_stores['Longitude'], errors='coerce')
# Define allowed types for filtering.
allowed_store_types = {"supermarket", "grocery_or_supermarket", "drugstore", "convenience_store"}
# Filter the Types column in place.
filter_types_inplace(df_stores, allowed_store_types, column="Types")
# Remove duplicates
df_stores.drop_duplicates(
    subset=["Name", "Business Status", "Address", "Price Level", "Rating", "Total Ratings", "Latitude", "Longitude"],
    inplace=True
)


# --- Process School Data ---
school_file = os.path.join(current_directory, "Google_data", "school_data.csv")
df_schools = pd.read_csv(school_file, on_bad_lines='skip')
df_schools['Latitude'] = pd.to_numeric(df_schools['Latitude'], errors='coerce')
df_schools['Longitude'] = pd.to_numeric(df_schools['Longitude'], errors='coerce')

df_schools.drop_duplicates(
    subset=["Name", "Business Status", "Address", "Price Level", "Rating", "Total Ratings", "Latitude", "Longitude"],
    inplace=True
)


# --- Process Crime data ---
crime_file = os.path.join(current_directory, "Google_data", "crime.csv")
df_crime = pd.read_csv(crime_file, on_bad_lines='skip')
df_crime['Latitude'] = pd.to_numeric(df_crime['Latitude'], errors='coerce')
df_crime['Longitude'] = pd.to_numeric(df_crime['Longitude'], errors='coerce')


# --- Process Redfin Data ---
houses_file_path = os.path.join(current_directory, "redfin_data", "redfin_cleaned_v2.csv")
df_houses = pd.read_csv(houses_file_path)
df_houses['num_restaurants_within_1km'] = df_houses.apply(
    lambda row: count_amenities_for_house(row['latitude'], row['longitude'], df_restaurants, radius_km=1.0),
    axis=1
)
df_houses['num_stores_within_1km'] = df_houses.apply(
    lambda row: count_amenities_for_house(row['latitude'], row['longitude'], df_stores, radius_km=1.0),
    axis=1
)
df_houses['num_schools_within_1km'] = df_houses.apply(
lambda row: count_amenities_for_house(row['latitude'], row['longitude'], df_schools, radius_km=1.0),
axis=1
)
df_houses['num_crimes_within_1km'] = df_houses.apply(
lambda row: count_amenities_for_house(row['latitude'], row['longitude'], df_crime, radius_km=1.0),
axis=1
)

# count crimes for each house
crime_summary_list = [
    crime_summary_for_house(row['latitude'], row['longitude'], df_crime, radius_km=1.0)
    for _, row in df_houses.iterrows()
]
crime_summary_df = pd.DataFrame(crime_summary_list).fillna(0)
df_houses = df_houses.join(crime_summary_df)

output_csv_path = os.path.join(current_directory, "Google_data", "summary_redfin_v2.csv")
df_houses.to_csv(output_csv_path, index=False)